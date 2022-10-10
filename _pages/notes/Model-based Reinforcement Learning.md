---
title: Model-based Reinforcement Learning
permalink: /notes/Model-based Reinforcement Learning
alias: [model-based]
---

Basic methods:
- **I2A**: [Imagination-Augmented Agents](https://arxiv.org/pdf/1707.06203.pdf)
	- Many model-based RL methods are not robust because they treat the model as infallible and use it for classical planning. I2A uses a more implicit approach in which a rollout encoder [RNN](RNN) produces an embedding for each rollout, which are then stacked into a single __imagination code__. The imagination code serves the input to a model-based policy model $\pi$. Furthermore, $\pi$ is not used directly, but used to define an additional cross-entropy loss for a model-free (A3C) policy $\hat{\pi}$ which is actually used for behaviour.
	- One model rollout is done for each action, with $\hat{\pi}$ followed thereafter. It is also found to be more efficient to pre-train the model.
- **MBMF**: Model-Based RL with Model-Free Fine-Tuning
- [World Models](World%20Models)
	- Learn a latent representation of image observations using a VAE, then train an [RNN](RNN) to output a probability distribution (Gaussian mixture) over the next latent vector. For a simple linear controller with only a few hundred parameters, an evolutionary algorithm can be used to optimise entirely within the "imaginary" world of model rollouts.
- **MVE**: Model-based Value Expansion
	- Model and true reward function for short-term up to a planning horizon $H$, Q learning for long-term. Improve accuracy compared with using each alone
	- DDPG on Half Cheetah. $H$ intuitive hyperparameter to tune.
