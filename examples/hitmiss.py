# Adaptation of Example 11.6 from
#
# F. S. Hillier and G. J. Lieberman (1990). Introduction to operations
# research. McGraw-Hill.
#
# The Hit-and-Miss Manufacturing Company has received an order to supply one
# item of a particular type. However, manufacturing this item is difficult, and
# the customer has specified such stringent quality requirements that the
# company may have to produce more than one item to obtain an item that is
# acceptable.
#
# The company estimates that each item of this type will be acceptable with
# probability $1/2$ and defective with probability $1/2$. Each item costs \$100
# to produce, and excess items are worthless. In addition, a setup cost of
# \$300 must be incurred whenever the production process is setup for this
# item. The company has time to make no more than 3 production runs, and at
# most 5 items can be produced in each run. If an acceptable item has not been
# obtained by the end of the third production run, the manufacturer is in
# breach of contract and must pay a penalty of \$1600.

# The objective is to determine how many items to produce in each production run
# in order to minimize the total expected cost.

from stochasticdp import StochasticDP

number_of_stages = 4
states = [0, 1]
decisions = [0, 1, 2, 3, 4, 5]

dp = StochasticDP(number_of_stages, states, decisions, minimize=True)

for t in range(number_of_stages - 1):
    # From state 0
    for x in decisions:
        dp.add_transition(stage=t, from_state=0, decision=x, to_state=0,
                          probability=1, contribution=300 * (x > 0) + 100 * x)
        dp.add_transition(stage=t, from_state=0, decision=x, to_state=1,
                          probability=0, contribution=300 * (x > 0) + 100 * x)

    # From state 1
    for x in decisions:
        dp.add_transition(stage=t, from_state=1, decision=x, to_state=0,
                          probability=1 - (1/2) ** x,
                          contribution=300 * (x > 0) + 100 * x)
        dp.add_transition(stage=t, from_state=1, decision=x, to_state=1,
                          probability=(1/2) ** x,
                          contribution=300 * (x > 0) + 100 * x)

dp.add_boundary(state=0, value=0)
dp.add_boundary(state=1, value=1600)

value, policy = dp.solve()

print(value)
print(policy)
