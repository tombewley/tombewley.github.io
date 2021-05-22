---
title: "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning"
permalink: /notes/A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning.md
author_profile: true
---

[[2011]] [[AISTATS]] #Content/Paper by [[Stéphane Ross]], Geoffrey J Gordon, and [[J Andrew Bagnell]]. 

In [[Imitation Learning]] (among other sequential prediction problems), future observations depend on previous actions, which violates the common i.i.d. assumption made in statistical learning. Ignoring this issue compromises learning: mistakes lead the [[Imitator]] to parts of the state space never encountered by the [[Target]] policy, leading to a compounding of errors. Here an [[Online Learning]] algorithm called `DAgger` is proposed to find a strong policy under these conditions.
Denote $d^t_\pi$ the distribution of states at time $t$ if policy $\pi$ is followed from time $1$ to $t-1$. The average distribution of states if $\pi$ is followed for $T$ steps is therefore

$$d_\pi=\frac{1}{T}\sum_{t=1}^Td_\pi^t$$

Our goal is to find a policy $\hat{\pi}$ which minimises some loss function $\mathcal{L}$ relative to a [[Target]] policy $\pi^*$ on samples from $d_\pi$:

$$\hat{\pi}=\arg\min_{\pi\in\Pi}\mathbb{E}_{s\sim d_\pi}[\mathcal{L(s,\pi,\pi^*)}]$$

Traditional approaches to [Imitation Learning](Imitation%20Learning) instead train a policy to perform well under the distribution encountered by $\pi^\ast$, $d_{\pi^\ast}$. Poor performance can result. A naïve solution would be to iterative train a new policy for each timestep $t$, on the distribution of states induced by all previously-trained policies, but this is extremely computationally intensive.
The generic `DAgger` proceeds as follows:
- Initialise an imitation policy $\hat{\pi}_1$.
- Use $\pi^*$ to gather a dataset $\mathcal{D}$.
- For each subsequent iteration $i$:
  - Use $\pi^*$ to sample $N\times\beta_i$ trajectories, and $\hat{\pi}_i$ to sample $N\times(1-\beta_i$), where $\beta_i\in[0,1]$.
  - For all new trajectories get the corresponding actions from $\pi^*$, and append these to $\mathcal{D}$.
  - Train $\hat{\pi}_{i+1}$ on the augmented dataset.

Starting with $\beta_1=1$ is typically useful because it means we don't have to specify an initial policy $\hat\pi_1$. The only requirement for the evolution of $\beta_i$ is that the average value across all iterations $\rightarrow0$ as $i\rightarrow\infty$. In practice, the best approach seems to be to set $\beta_1=1$ and $\beta_i=0\ \forall i>1$.
A theoretical analysis in the paper demonstrates the robustness of the algorithm, and it is shown to outperform a couple of earlier alternatives for imitation learning.
