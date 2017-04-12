# stochasticdp

A simple implementation of backwards induction for solving finite-horizon, finite-space stochastic dynamic programs.

## Installation

`stochasticdp` is available on PyPI:

```bash
pip install stochasticdp
```

## Usage

To initialize a stochastic dynamic program:

```python
dp = StochasticDP(number_of_stages, states, decisions, minimize)
```

where

* `number_of_stages` is an integer
* `states` is a list
* `decisions` is a list
* `minimize` is a boolean

This results in a stochastic dynamic program with stages numbered `0, ..., number_of_stages - 1`, and initializes the following dictionaries:

* `dp.transition`, where `dp.transition[m, n, t, x]` is the probability of moving from state `n` to state `m` in stage `t` under decision `x`
* `dp.contribution`, where `dp.contribution[m, n, t, x]` is the immediate contribution of resulting from moving from state `n` to state `m` in stage `t` under decision `x`
* `dp.boundary`, where `dp.boundary[n]` is the boundary condition for the value-to-go function at state `n`

To solve the stochastic dynamic program:

```python
value, policy = dp.solve()
```

where

* `value` is a dictionary: `value[t, n]` is the value-to-go function at stage `t` and state `n`
* `policy` is a dictionary: `policy[t, n]` is the optimizer of `value[t, n]`
