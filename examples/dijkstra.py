# Adaptation of Exercise 9-26 from
#
# R. Rardin (1998). Optimization in operations research. Prentice Hall.
#
# The Dijkstra Brewing Company is planning production of its new limited run
# beer, Primal Pilsner. The company must supply 1 batch next month, then 2 and
# 4 in successive months. Each month in which the company produces the beer
# requires a factory setup cost of \$5,000. Each batch of beer costs \$2,000 to
# produce. Batches can be held in inventory at a cost of \$1,000 per batch per
# month. Capacity limitations allow a maximum of 3 batches to be produced
# during each month. In addition, the size of the company's warehouse restricts
# the ending inventory for each month to at most 3 batches. The company has no
# initial inventory.
#
# The company wants to find a production plan that will meet all demands on time
# and minimizes its total production and holding costs over the next 3 months.
# Formulate this problem as a dynamic program.

from stochasticdp import StochasticDP

d = [1, 2, 4]

number_of_stages = 4
states = [0, 1, 2, 3]
decisions = [0, 1, 2, 3]

dp = StochasticDP(number_of_stages, states, decisions, minimize=True)

for t in range(number_of_stages - 1):
    for n in states:
        for x in decisions:
            if n + x - d[t] <= 3 and n + x - d[t] >= 0:
                c = 5 * (x > 0) + 2 * x + 1 * (n + x - d[t])
                dp.add_transition(stage=t,
                                  from_state=n,
                                  decision=x,
                                  to_state=n + x - d[t],
                                  probability=1,
                                  contribution=c)

for n in states:
    dp.add_boundary(state=n, value=0)

value, policy = dp.solve()

print(value)
print(policy)
