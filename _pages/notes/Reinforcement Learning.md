---
title: "Reinforcement Learning"
permalink: /notes/Reinforcement%20Learning
---

S = discrete set of environmental states

A = discrete set of agent actions

r = scalar set of reinforcement signals

I = input function (how the agent views the state of the world)

pi = mapping from state to action

Assume the world is stochastic (same S, same A might cause different outcomes) *but* stationary (outcomes have fixed probabilities for given S, A pair).

I might be a partial or full observation of the world. For computer games, we typically have full information - that’s why they’re a good environment to test reinforcement learning. In fully-observed systems, I = S.

In a stochastic world, need to balance exploration and exploitation (just like BO).

What’s the optimal behaviour over time? High reward quickly, or evenly spread out?

- We could specify a finite time horizon over which we care about, and predict the sum expected reward across that horizon.

- We could try to predict the expected average per-timestep reward from now until infinite horizon.

- In practice, the most common approach is called discounted reward - sum for an infinite time, discounting each timestep by the power of its distance from the present state.

In an ideal world, we could compute $p(s(t) \vert s(t-1), a(t))$ and $p(r(t)\vert s(t-1), s(t))$ and *analytically* find the best strategy but this is not practically possible in most cases, so we have to learn mappings from data through some kind of search.

The multi-armed bandit problem is a thought experiment used to understand this problem, where the space of A is small (i.e. which of the k arms to pull) but the space of S is large and unseen.

Reinforcement learning is highly sensitive to small perturbations in the setup of the environment (e.g. a different world shape in pacman) as it is essentially a model-free decision machine. Several proposals have been put forward to improve this. One recent examples is Schema Networks.

Utilitarian reward functions are obviously over-simplistic as humans are often not fully utilitarian and we disagree about utility. We must model the optimal choice of reward function as a variable with uncertainty, and make decisions accordingly (Bayes theorem!)