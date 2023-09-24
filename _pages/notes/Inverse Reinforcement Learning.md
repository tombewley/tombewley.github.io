---
title: Inverse Reinforcement Learning
permalink: /notes/Inverse Reinforcement Learning
---
A variant of [Imitation Learning](Imitation%20Learning), which also goes by the name of **Inverse Optimal Control**.

Even if we don't care about learning the reward function itself, and only care about the final policy, IRL often performs better than other IL methods on challenging problems. To quote a line from [Algorithms for Inverse Reinforcement Learning](Algorithms%20for%20Inverse%20Reinforcement%20Learning), this may be because *"the reward function, rather than the policy is the most succinct, robust, and transferable definition of the task"*.

It can also be thought of as a form of [Preference-based RL](Preference-based%20RL), in which the demonstrated trajectories are assumed to be preferred to unseen ones, defining *implicit preferences*.