from math import inf, isclose


class FrozenDict(dict):
    __frozen = False

    def freeze(self):
        self.__frozen = True

    def __setitem__(self, key, value):
        if self.__frozen and key not in self:
            raise KeyError('Invalid state, stage, or decision')
        super().__setitem__(key, value)


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

        # Initialize transition probabilities to 0
        self.transition = FrozenDict()
        for t in range(self.number_of_stages - 1):
            for n in self.states:
                for nn in self.states:
                    for x in self.decisions:
                        self.transition[nn, n, t, x] = 0
        self.transition.freeze()

        # Initialize contributions to 0
        self.contribution = FrozenDict()
        for t in range(self.number_of_stages - 1):
            for n in self.states:
                for nn in self.states:
                    for x in self.decisions:
                        self.contribution[nn, n, t, x] = 0
        self.contribution.freeze()

        # Initialize boundary conditions to 0
        self.boundary = FrozenDict()
        for n in self.states:
            self.boundary[n] = 0
        self.boundary.freeze()

    def validate(self):
        # Transition probabilities for each n, t, x must sum to 1 or 0
        for n in self.states:
            for t in range(self.number_of_stages - 1):
                for x in self.decisions:
                    prob_sum = sum(self.transition[nn, n, t, x]
                                   for nn in self.states)
                    if not (isclose(prob_sum, 1) or
                            isclose(prob_sum, 0, abs_tol=1e-09)):
                        raise ValueError(
                            "Dynamic program is not well-defined. "
                            "Check the transition probabilities."
                        )

    def solve(self):
        # Validate the DP
        self.validate()

        # Value function
        # value[n, t]
        value = {}

        # Policy
        # policy[n, t]
        policy = {}

        # Boundary conditions
        for n in self.states:
            value[self.number_of_stages - 1, n] = self.boundary[n]

        # Solve backwards
        for t in range(self.number_of_stages - 2, -1, -1):
            for n in self.states:
                value[t, n] = self._sign * inf
                policy[t, n] = None
                for x in self.decisions:
                    if isclose(sum(self.transition[nn, n, t, x]
                                   for nn in self.states), 1):
                        temp_value = sum(self.transition[nn, n, t, x] *
                                         (self.contribution[nn, n, t, x] +
                                          value[t + 1, nn])
                                         for nn in self.states
                                         if self.transition[nn, n, t, x] > 0)
                        if self._sign * temp_value < self._sign * value[t, n]:
                            value[t, n] = temp_value
                            policy[t, n] = x

        return value, policy
