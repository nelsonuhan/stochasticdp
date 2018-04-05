from math import inf, isclose


class TransitionData(dict):
    def __init__(self, number_of_stages, states, decisions):
        self.number_of_stages = number_of_stages
        self.states = set(states)
        self.decisions = set(decisions)

    def __setitem__(self, key, value):
        try:
            m, n, t, x = key
        except ValueError:
            raise ValueError('State, stage, or decision missing')

        if ((m not in self.states) or
                (n not in self.states) or
                (t >= self.number_of_stages) or
                (x not in self.decisions)):
            raise KeyError('Invalid state, stage, or decision')
        super().__setitem__(key, value)

    def __getitem__(self, key):
        try:
            m, n, t, x = key
        except ValueError:
            raise ValueError('Not enough indices')

        if ((m not in self.states) or
                (n not in self.states) or
                (t >= self.number_of_stages) or
                (x not in self.decisions)):
            raise KeyError('Invalid state, stage, or decision')

        if key not in self:
            return None
        else:
            return super().__getitem__(key)

    def __repr__(self):
        entries = []
        for (m, n, t, x), v in self.items():
            entries.append(
                " (stage: {0}, from_state: {1},".format(t, m) +
                " decision: {0}, to_state: {1}): {2}".format(x, n, v)
            )
        string = '{' + '\n'.join(entries).strip() + '}'
        return string


class StateData(dict):
    def __init__(self, states):
        self.states = set(states)

    def __setitem__(self, key, value):
        if key not in self.states:
            raise KeyError('Invalid state')
        super().__setitem__(key, value)

    def __getitem__(self, key):
        if key not in self.states:
            raise KeyError('Invalid state')

        if key not in self:
            return None
        else:
            return super().__getitem__(key)


class ValueToGoData(dict):
    def __init__(self, number_of_stages, states):
        self.number_of_stages = number_of_stages
        self.states = set(states)

    def __setitem__(self, key, value):
        try:
            t, n = key
        except ValueError:
            raise ValueError('Stage or state missing')

        if ((n not in self.states) or
                (t >= self.number_of_stages)):
            raise KeyError('Invalid stage or state')
        super().__setitem__(key, value)

    def __getitem__(self, key):
        try:
            t, n = key
        except ValueError:
            raise ValueError('Not enough indices')

        if ((n not in self.states) or
                (t >= self.number_of_stages)):
            raise KeyError('Invalid stage or state')

        if key not in self:
            return None
        else:
            return super().__getitem__(key)

    def __repr__(self):
        entries = []
        for (t, n), v in self.items():
            entries.append(" (stage: {0}, state: {1}): {2}".format(t, n, v))
        string = '{' + '\n'.join(entries).strip() + '}'
        return string


class StochasticDP(object):
    def __init__(self, number_of_stages, states, decisions, minimize=True):
        # Initialize basic input data
        self.number_of_stages = number_of_stages
        self.states = states
        self.decisions = decisions
        self.minimize = minimize

        # Set comparison direction based on minimize/maximize
        if self.minimize:
            self._sign = 1
        else:
            self._sign = -1

        # Initialize transition probabilities
        self.probability = TransitionData(self.number_of_stages,
                                          self.states,
                                          self.decisions)

        # Initialize contributions
        self.contribution = TransitionData(self.number_of_stages,
                                           self.states,
                                           self.decisions)

        # Initialize boundary conditions
        self.boundary = StateData(self.states)

    def add_transition(self, stage, from_state, decision, to_state,
                       probability, contribution):
        self.probability[to_state, from_state, stage, decision] = probability
        self.contribution[to_state, from_state, stage, decision] = contribution

    def add_boundary(self, state, value):
        self.boundary[state] = value

    def solve(self):
        # Validate the transition probabilities
        #    Transition probabilities for each n, t, x must sum to 1 or 0
        # Create dictionary of allowable decisions
        allowable_decisions = {}
        for t in range(self.number_of_stages - 1):
            for n in self.states:
                for x in self.decisions:
                    sum_probability = sum(
                        self.probability[nn, n, t, x]
                        for nn in self.states
                        if self.probability[nn, n, t, x]
                    )
                    if isclose(sum_probability, 1):
                        try:
                            allowable_decisions[t, n].append(x)
                        except KeyError:
                            allowable_decisions[t, n] = [x]
                    elif isclose(sum_probability, 0, abs_tol=1e-09):
                        pass
                    else:
                        raise ValueError(
                            "Dynamic program is not well-defined. "
                            "Check the transition probabilities "
                            "from state {0} at stage {1} under decision {2}"
                            .format(n, t, x)
                        )

        # Value function
        # value[t, n]
        value = ValueToGoData(self.number_of_stages, self.states)

        # Policy
        # policy[t, n]
        policy = ValueToGoData(self.number_of_stages, self.states)

        # Boundary conditions
        for n in self.states:
            value[self.number_of_stages - 1, n] = self.boundary[n]

        # Solve backwards
        for t in range(self.number_of_stages - 2, -1, -1):
            for n in self.states:
                value_decision = {}
                for x in allowable_decisions[t, n]:
                    value_decision[x] = sum(
                        self.probability[nn, n, t, x] *
                        (self.contribution[nn, n, t, x] +
                         value[t + 1, nn])
                        for nn in self.states
                        if self.probability[nn, n, t, x]
                    )

                if self.minimize:
                    value[t, n] = min(value_decision.values())
                else:
                    value[t, n] = max(value_decision.values())

                policy[t, n] = set(
                    x for x in allowable_decisions[t, n]
                    if isclose(value_decision[x], value[t, n])
                )

        return value, policy
