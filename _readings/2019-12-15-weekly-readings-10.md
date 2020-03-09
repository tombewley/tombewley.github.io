---
title: 'Weekly Readings #10'
date: 2019-12-14
permalink: /posts/2019/12/weekly-readings-10/
tags:
  - weekly-readings
---

State representation learning in Atari; AI shortcuts and ethical debt; cloning swarms.

## 📝 Papers

### Anand, Ankesh, Evan Racah, Sherjil Ozair, Yoshua Bengio, Marc-Alexandre Côté, and R. Devon Hjelm. “Unsupervised State Representation Learning in Atari.” *ArXiv:1906.08226 [Cs, Stat]*, November 3, 2019.

Introduce Atari 2600 games as a useful benchmark for state representation learning, and a method for SRL called *Spatiotemporal DeepInfomax* (ST-DIM) that works by "maximising mutual information across spatially and temporally distinct features of a CNN encoder of the observations".

Given a dataset of observations $\mathcal{O}=o_1,…,o_N$, the SRL problem is cast as a maximisation of a lower-bound estimate of the mutual information (using `infoNCE`) between consecutive observations $o_t,\ o_{t+1}$. The actual value to be maximised is the sum of two mutual information estimates:

- **Global-local**: the summed mutual information estimate between each spatially-local feature activation of a convolutional layer of the CNN encoder at time $t+1$, and the final output vector of the encoder (after dense layers) at time $t$.
- **Local-local** the summed mutual information estimate between each spatially-local feature activation of a convolutional layer of the CNN encoder at time $t+1$, and the corresponding activation at time $t$.

After learning is complete, the output vector of the encoder is used as the state representation. The usefulness of this representation is evaluated by assessing how well it can predict the values of so-called *generative variables* describing the ground-truth game state (e.g. the $x$, $y$ coordinates of the player and enemies). 

For each identified generative variable for a given game, a supervised learning problem is set up where the goal is to learn a *linear* mapping from the state representation to the ground truth value of that variable. The average error of these linear mappings is used as a measure of state representation quality.

In tests on a variety of Atari 2600 games, ST-DIM generally outperforms baseline methods including a randomly-initialised CNN encoder and a variational encoder on raw observations. However, performance is significantly below end-to-end learning of both the encoder and linear mapping by backpropagating gradients through the whole system, suggesting further improvements are possible.

### Cristianini, Nello. “Shortcuts to Artiﬁcial Intelligence,” 2019.

Argues that three crucial instances of historic shortcut-taking explain the current paradigm of AI, and are also responsible for the current 'ethical debt' of the field.

The AI field started with the dream of building a reasoning computer, informed by fundamental discoveries about the principles underlying intelligence. But as in any paradigm shift, the *definition of success* has since changed. In recent decades, we have managed to avoid building complex world models and explicit knowledge representations, by collecting vast bodies of data and using statistical optimisation algorithms to emulate very specific skills. 

This approach has a low immediate cost (in terms of effort) and gets us some part of the way to a 'free lunch'. However, we are quickly learning that it has numerous negative social consequences, specifically due to bias and manipulability, as well as a lack of privacy, accountability and transparency.

The three shortcuts identified are:

- **Replacing causation with correlation**: the perceived need for an underlying theory of phenomena and behaviour has reduced.
- **Using data 'from the wild'** instead of from carefully-designed experiments, and ignoring factors concerning its wider context.
- **Settling for proxies and implicit feedback** instead of measuring important signals directly. This involves strong assumptions about the representativeness of the proxy signals.

These shortcuts have unquestionably enabled rapid, low-cost advancements in areas such as image classification and natural language processing. But now is the time to consider an alternative paradigm, featuring:

- Greater prevalence of causal and interpretable models, which may have reduced optimisation performance.
- More explicit, semantically-constrained knowledge representations. 
- More careful consideration of the data 'supply chain' and the means of performance evaluation.

### Zhou, Siyu, Mariano J. Phielipp, Jorge A. Sefair, Sara I. Walker, and Heni Ben Amor. “Clone Swarms: Learning to Predict and Control Multi-Robot Systems by Imitation.” *ArXiv:1912.02811 [Cs]*, December 5, 2019.

A method is described for cloning the behaviour of swarms (small flocks of boids that avoid each other and static obstacles while moving towards a common goal location in a 2D environment). The cloned policy can be used for both prediction and control. The proposed model, called *SwarmNet*, works as follows:

- The target swarm policy is observed and a history of positions and velocities are collected. A single input instance to the model consists of a $T\times N\times D$ tensor, where $T$ is a number of consecutive timesteps, $N$ is the size of the swam and $D$ is the dimensionality of the state representation for each agent ($4$ for position and velocity in a 2D environment). This is concatenated along the $D$ axis with a set of 'context' variables, such as the locations of obstacles [this isn't explained in detail].
- Temporal dynamics are computed by passing the data through a series of $L$ 1D convolutions along the time axis, thereby condensing this dimension to $T_s=T-L(K-1)$ where $K$ is the kernel size. $C$ convolution filters are used, so the result is a tensor of dimensionality $T_s\times N\times C$.
- The condensed tensor is split along the agent axis, and the resultant $T_s\times C$ matrices are used to initialise the $N$ node states of a fully-connected graph. One step of *graph convolution* is used to modify these node states based on edge connections.
- After graph convolution, the tensor is reassembled and fed into a final feedforward network which maps it into one with shape $T_s\times N\times D$. This can be interpreted as state predictions for the next $T_s$ timesteps, given the previous $T$ ones.

The model is trained to minimise the mean squared prediction error compared with the ground-truth positions and velocities in the following timesteps. A curriculum learning approach is taken, whereby initially just the single next timestep is used for scoring, but the number of assessed prediction steps is gradually increased (up to $10$) as training proceeds.  

Noisy and nondeterministic environments can be handled by incorporating dropout into the training process. Using dropout (with the same probabilities) during prediction then enables the generation of stochastic trajectories with approximately the same statistics as samples from the training distribution.

## 🗝️  Key Insights

- Measurement of both spatial and temporal smoothness (e.g. via mutual information maximisation) appears to be an effective way of constraining state representations to contain information about the important generative variables. Measuring SRL performance in these terms is an intuitive and highly meaningful approach.
- Well-founded criticisms of the current paradigm in artificial intelligence are coming thick and fast these days. Cristianini's focus on the 'shortcuts' of settling for correlation over causation, 'wild' data over controlled experiment, and proxies over direct measurement is a great way to frame this discussion.

- A graph neural network is a natural way of encoding agent states and interactions in a MAS, particularly in a swarm where the degree of rigid structure is low and interactions are ad-hoc. 