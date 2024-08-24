---
---
title: "Learning Interpretable Models of Aircraft Handling Behaviour by Reinforcement Learning from Human Feedback"
pubtype: "conference"
collection: publications
permalink: /publication/reward_trees
excerpt: 'We show that reward learning with tree models can be competitive with neural networks in an aircraft handling domain, and demonstrate some of its interpretability benefits.'
date: 2023-05-26
venue: 'AIAA SciTech Forum'
paperurl: 'https://arxiv.org/abs/2305.16924'
citation: 'Bewley, Tom, Jonathan Lawry, and Arthur Richards. &quot;Learning Interpretable Models of Aircraft Handling Behaviour by Reinforcement Learning from Human Feedback&quot; <i>AIAA SciTech Forum</i>. 2023.'
---
We propose a method to capture the handling abilities of fast jet pilots in a software model via reinforcement learning (RL) from human preference feedback. We use pairwise preferences over simulated flight trajectories to learn an interpretable rule-based model called a reward tree, which enables the automated scoring of trajectories alongside an explanatory rationale. We train an RL agent to execute high-quality handling behaviour by using the reward tree as the objective, and thereby generate data for iterative preference collection and further refinement of both tree and agent. Experiments with synthetic preferences show reward trees to be competitive with uninterpretable neural network reward models on quantitative and qualitative evaluations.
