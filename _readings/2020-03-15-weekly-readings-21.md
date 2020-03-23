---
title: 'Weekly Readings #21'
date: 2020-03-15
permalink: /posts/2020/03/weekly-readings-21/
excerpt: 'Constraining embeddings with side information; latent actions; RL with abstract representations and models; fuzzy state prototypes; index-free imitation.'
tags:
  - weekly-readings
---

Constraining embeddings with side information; latent actions; RL with abstract representations and models; fuzzy state prototypes; index-free imitation.


## 📝 Papers

### T. Adel, Z. Ghahramani, and A. Weller, “Discovering Interpretable Representations for Both Deep Generative and Discriminative Models,” in *Proceedings of the 35th International Conference on Machine Learning*, 2018.

This paper introduces one novel idea, and two methods of implementing it. The idea is to map a non-interpretable representation $z$ of data $x$ (e.g. that produced by a VAE), along with human-sourced semantic side information $s$ for a small proportion of datapoints, to a new representation $z^\ast$ that is 'interpretable'. Interpretability is defined here as a *linear dependence* between $s$ and $z^\ast$.

The first method is called the *interpretable lens variable model* (ILVM). Here, we learn a transformation from $z\rightarrow z^\ast$ in the form of normalising flows, which are a series of *invertible transformations*. Invertibility means that we can do the transformation in both directions, with no loss of reconstruction fidelity. The mapping is optimised (by variational inference) to make the dependence between $z^\ast$ and $s$ as linear as possible for those datapoints where $s$ is provided. This method enables a kind of active learning for choosing the next most useful datapoint for which to obtain side information. Roughly speaking, this involves finding the point $j$ for which the individual values of $z^\ast_j$ *disagree most* about $s_j$. 

The second method is called the *jointly learnt variable model* (JLVM). Here the idea is for $z^\ast$ to be maximally expressive about $s$ while being maximally compressive about the data $x$. The objective is optimised by minimising $\textbf{I}(z^\ast,s)-\beta\textbf{I}(z^\ast,x)$ (or rather a variational approximation). This approach imagines $z^\ast$ as being an *information bottleneck* between $s$ and $x$. Unlike ILVM, JLVM trades off interpretability and reconstruction fidelity. 

In experiments, the authors consider the case of having a single $z^\ast$ per dimension of $s$, so the aim is effectively to approximate each piece of side information for unlabeled datapoints. Because the methods are explored in the context of GANs, a specified $z^\ast$ can then be used to generate an appropriate image sample. Examples of this include:

- Digit identity and thickness of MNIST characters;
- Brightness of images in a Google Street View dataset;
- Two axes of rotation of chairs.

In general, JLVM seems to produce slightly better disentangled representations, but the active learning method in ILVM is found to improve interpretability more quickly than random selection.


### Edwards, Ashley D., Himanshu Sahni, Yannick Schroecker, and Charles L. Isbell. “Imitating Latent Policies from Observation.” *ArXiv:1805.07914 [Cs, Stat]*, May 13, 2019.

Here the task is to infer latent policies from noisy state observations alone (*without* access to the underlying actions or a reward signal), then use a small number of environmental interactions to determine a further mapping between latent actions $z$ and real actions $a$. The approach assumes discrete action spaces.

To learn the latent policy we require a model with three components: a state embedding $E_p(s_t)$ ["trained concurrently"], a forward dynamics model $G_\theta(E_p(s_t),z)$ that learns to predict the transition $\Delta_t=s_{t+1}-s_t$, and the policy network itself $\pi_\omega(z\vert s_t)$. $G_\theta$ is trained using the following loss:

$$
\mathcal{L}_\text{min}=\min _{z}\left\|\Delta_{t}-G_{\theta}\left(E_{p}\left(s_{t}\right), z\right)\right\|^{2}
$$

Because it is not known which latent action is taken, this loss takes whichever is currently closest. In addition, both the policy and dynamics model should be trained to maximise the probability of the observed data:

$$
\mathcal{L}_\text{exp}=\vert\vert s_{t+1}-\widehat{s}_{t+1}\vert\vert^{2}\ \ \ \text{where}\ \ \ \hat{s}_{t+1}=\sum_{z} \pi_{\omega}(z \vert s_{t}) \cdot G_{\theta}(E_{p}(s_{t}), z)
$$

On each training step, the first loss is used to update $\theta$, then these parameters are held constant while the second loss is used to update $\omega$.

The second stage is action remapping, which involves learning a function $\pi_{\xi}(a_t \vert z, E_{a}(s_{t}))$ where $E_a$ is another concurrently-trained embedding. This is done by collecting a relatively small history of $(s_t,a_t,s_{t+1})$ triples and using the pre-trained $G_\theta$ to find the action $z$ that produces the next-state whose embedding is *most similar* to $E_p(s_{t+1})$ by L2-distance. Training $\pi_\xi$ is then treated as a straightforward classification problem using cross-entropy loss.


### François-Lavet, Vincent, Yoshua Bengio, Doina Precup, and Joelle Pineau. “Combined Reinforcement Learning via Abstract Representations.” *ArXiv:1809.04506 [Cs, Stat]*, November 18, 2018. 

This is an ambitious combination of model-free and model-based methods for reinforcement learning using learned state representations. The architecture consists of an *encoder* network $e$ (parameters $\theta_e)$, which takes $s_t$ as input and whose output $x_t$ is the input to a $Q$-network (parameters $\theta_Q$). $x_t$ is also fed alongside $a_t$ into two further models (parameters $\theta_\rho$ and $\theta_\tau$) that predict the reward $r_t$ and next abstract state $x_{t+1}$ respectively. This architecture is trained using a selection of carefully-chosen losses.

- An auto-encoder is not used here; it is suggested that the requirement for reconstruction of $s_t$ is too strong of a constraint and incentivises the capture of details that are not task-relevant. 

The model-free component of learning is *double DQN*, which has an associated loss $\text{mf}$ based on the error in $Q$-value prediction. The model-based component has three additional losses: one for learning the reward $\rho$, one for the state transition $\tau$ and one for the discount factor $\text{g}$ [not sure why the last one is needed]. There are additional regularising losses that encourage $e$ to have high entropy (i.e. different states get different representations) and representation feature values to remain within the unit sphere. These are collectively called the representation loss $\text{d}$. Finally, an *interpretability loss* $\text{interpr}$ encourages each action to have a consistent effect in the representation space by measuring the cosine similarity between the transition vector from $x_t$ to $x_{t+1}$ and a hand-crafted embedding vector $v(a_t)$.  

At each iteration, each term in the following sum of these losses is minimised using batch gradient descent:

$$
\mathcal{L}=\alpha\Big[\mathcal{L}_\text{mf}(\theta_e,\theta_Q)+\mathcal{L}_\rho(\theta_e,\theta_\rho)+\mathcal{L}_\text{g}(\theta_e,\theta_\text{g})+\mathcal{L}_\tau(\theta_e,\theta_\tau)+\mathcal{L}_\text{d}(\theta_e)+\mathcal{L}_\text{interpr}(\theta_e,\theta_\tau)\Big]
$$

The architecture effectively combines a reactive policy with an ability to *plan* using its model-based component. Planning can be done by selecting the $n$ actions with highest predicted value for the next timestep, and using the reward and transition models to forward-simulate a short trajectory of $T$ timesteps for each. The action yielding highest simulated return is chosen for actual execution.

In a grid world experiment (pixel inputs), the learned 2D representation corresponds to the layout of the map. Introducing the $\mathcal{L}_\text{interpr}$ term to incentivise left-right-up-down actions to have their respective directional effects causes the representation to be better aligned.
### Huang, Jianfeng, Plamen P. Angelov, and Chengliang Yin. “Interpretable Policies for Reinforcement Learning by Empirical Fuzzy Sets.” *Engineering Applications of Artificial Intelligence* 91 (May 2020): 103559.

This paper contains an interesting architecture for action-value function approximation in reinforcement learning. [While I found it rather hard to read, ] the idea seem to be to discretise the state and action spaces. For each location in the discretised space, the value is estimated using `AnYa`, a fuzzy rule-based system. The consequent of each rule is a $Q$ value estimate for state-action pairs 'close to' each pair.

To get $Q$ for any arbitrary state-action pair, the rules are defuzzified by taking the average consequents weighted by the value of a Cauchy membership function for each rule. During learning, a modified SARSA($\lambda$) algorithm is used to update the $Q$ values. 

In addition to this, a clustering algorithm called `ALMMo` is used to find *prototype* points in state space. The policy consists of an action to take for each prototypes. At a given timestep, the single nearest prototype is found, again using the Cauchy membership function. The action with maximum $Q$ value according to the `AnYa` system is used to update the policy for that prototype.

Experiments with MountainCar and a simple grid world shows this approach produces models with far fewer parameters than other methods for continuous state spaces, while also providing interpretability due to the transparency of the rule base.


### Le, Hoang M, Yisong Yue, Peter Carr, and Patrick Lucey. “Coordinated Multi-Agent Imitation Learning,” 2017, 9.

This paper proposes a method of imitation learning of $K$ coordinating agents given an expert demonstrator $\pi^\ast$ and a dataset demonstration trajectories $\mathcal{D}_\text{train}$. A key challenge here is the presence of *roles* that can be taken by any one of the agents at any given time – this makes it an *index-free* control problem. Therefore what is required is a dual mechanism for multi-agent imitation learning of per-role policies, and a unsupervised learning of a latent role-assignment model (formulated as a graphical model). To make the problem tractable, these are optimised on an alternating basis. 

The role assignment model takes in an unordered set of *per-agent* state-action trajectories $\{x^k\forall k\in[1..K]\}$ and aims to reshuffle them into ordered *per-role* trajectories (we assume that there are $K$ roles, one per agent). At any given time $t$, it is assumed that agent $k$ is acting according to a latent role $z_t^k$, assigned by a true unknown graphical model $p$ with parameters $\theta$. In principle our aim is to calculate the true posterior $p(z^k\vert x^k,\theta)$, but this is intractable so we formulate an evidence lower bound (ELBO) in terms of the parameters of a *hidden Markov model* $q$ and optimise for these instead. Given a learned $q$, there is then the task of finding the lowest-cost mapping of each role to a unique agent at each timestep. This is a *linear  assignment problem*, which is solved optimally by the Kuhn-Munkres algorithm.

The imitation learning mechanism takes in a dataset of role-ordered demonstration trajectories. It takes a curriculum learning approach, iteratively increasing a prediction horizon $j$. 

- For each $j$,
  - For each 'key step' in the demonstration dataset, separated by $j$ timesteps. 
    - Perform a simulated rollout using the current policy models $\pi_1..\pi_K$, and get the expert demonstrator to relabel each simulated timestep with 
    - Update $\pi_1..\pi_K$ using the relabeled dataset by supervised learning.

The overall learning algorithm is:

- While no improvement in predictive accuracy on a validation set $\mathcal{D}_\text{val}$:
  - Use $q$ to disentangle $\mathcal{D}_\text{train}$ into roles.
  - Perform imitation learning on the role-ordered dataset.
  - Roll out the updated policies $\pi_1..\pi_K$ to obtain a role-ordered trajectory set $\mathcal{D}_\text{roll}$.
  - Update the role assignment model **using $\mathcal{D}_{roll}$ (not $\mathcal{D}_{train}$)**, effectively disregarding the current ordering. *As learning progresses the ordering should begin to converge*.

The approach is implemented in a predator-prey grid world (predators must surround prey from all sides) and on tracking data from a real professional football game. A fascinating result from the latter implementation is that the learned HMM has Gaussian components centred around the positions for a 4-4-2 formation ($x,y$ positions on the pitch are two state variables).

## 🗝️  Key Insights

- The papers by Adel et al and François-Lavet et al cover very different approaches to representation learning. The *reversibility* of the functions used in the former is extremely helpful, as it allows us to do both generative and discriminative reasoning. It also shows how significant value can be squeezed out of a small amount of manual annotation. The latter is a more standard piece of state representation learning work: chain together a lot of different losses, and try to perform both forward modelling in addition to action selection. The way planning is enabled by the forward model is very interesting. 
- Edwards et al make a strong case that it may not be reasonable to know the underlying action taken by an agent being imitated, in which case we must learn from states alone. The use of intermediate latent actions does appear effective, though isn't great for interpretability. A forward dynamics model is again a central component; it seems to be popular to predict transitions rather than next states (more compact distribution?)

- Huang et al's method of delivering interpretability in RL policies, based on fuzzily clustering states according to a small number of prototypes, seems powerful and quite biologically plausible. I like the format of model description that they give in the paper too. 
- Le at al's work demonstrates how for *index-free* multi-agent systems, where agents are homogeneous but behaviour is split according to roles, it make sense to perform imitating learning on a per-role basis and also learn how to assign agents to roles.
