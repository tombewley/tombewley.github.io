---
title: 'Weekly Readings #25'
date: 2020-04-26
permalink: /posts/2020/04/weekly-readings-25/
excerpt: 'Imitation learning using value or reward.'
tags:
  - weekly-readings
---

## 📝 Papers

### Abbeel, Pieter, and Andrew Y. Ng. ‘Apprenticeship Learning via Inverse Reinforcement Learning’. In *Twenty-First International Conference on Machine Learning - ICML ’04*, 1. Banff, Alberta, Canada: ACM Press, 2004.

In IRL, we observe a target policy $$\pi_E$$ demonstrating a task, imagine it as trying to maximise a *linear* reward function $$R^\ast$$ of known state-derived features $$\phi:S\rightarrow[0,1]^k$$, estimate that latent function as $$R$$, and output a policy $$\tilde{\pi}$$ that attains performance close to $$\pi_E$$ on $$R$$.

Assume there is some true reward function $$R^\ast(s)=w^\ast\cdot\phi(s)$$, where $$\vert\vert w^\ast\vert\vert_1\leq1$$ keeps rewards bounded by $$1$$. The value of a policy $$\pi$$ is

$$
\mathbb{E}_{s_0\sim D}[V_{\pi}(s_0)]=w^\ast\cdot\mathbb{E}\left[\sum_{t=0}^\infty\gamma^t\phi(s_t)\ \Big\vert\ \pi\right]=w^\ast\cdot\mu(\pi)
$$

Here, the RHS expectation is taken with respect to the random state sequence $$s_0,s_1,...$$. The compact notation $$\mu(\pi)$$ is used to denote the discounted expectation for the features. For a target policy $$\pi_E$$, this expectation can be empirically estimated by simply observing trajectories in the environment. Denote this estimate $$\mu_E$$.

The imitation learning problem reduces to finding a policy $$\tilde{\pi}$$ such that $$\left\|\mu(\tilde{\pi})-\mu_{E}\right\|_{2} \leq \epsilon$$. For such a $$\tilde{\pi}$$, the constraint on $$w^\ast$$ means that the difference in expected policy values is also bounded by $$\epsilon$$.

The algorithm for solving this problem proceeds as follows:

- Randomly initialise $$\tilde{\pi}^{(0)}$$ and estimate $$\mu^{(0)}=\mu(\pi^{(0)})$$.

- For each iteration $$i$$:

  - Compute 

    $$
    t^{(i)}=\max _{w:\|w\|_{2} \leq 1}\left[\ \min _{j \in\{0 . .(i-1)\}} \left[w\cdot(\mu_{E}-\mu^{(j)})\right]\ \right]
    $$

    and let $$R^{(i)}=w^{(i)}\cdot\phi$$, where $$w^{(i)}$$ is the value that attains this maximum.

    - $$t^{(i)}$$ is effectively the *margin* by which $$\pi_E$$ does better on $$R^{(i)}$$ than any of the $$i$$ policies found previously.
    - This problem can be posed as a quadratic program, similar to that of finding the maximum-margin hyperplane in support vector machines. It can also be approximated as a simpler linear projection problem; in practice we get similar results.

  - Use RL to find a policy $$\pi^{(i)}$$ that optimises $$R^{(i)}$$, and estimate $$\mu^{(i)}=\mu(\pi^{(i)})$$.

  - If $$t^{(i)}\leq\epsilon$$, terminate.

IRL is demonstrated in gridworld and lane driving environments. The biggest area identified for future work is the handling of reward functions that are nonlinear in the features.

### Bansal, Mayank, Alex Krizhevsky, and Abhijit Ogale. ‘ChauffeurNet: Learning to Drive by Imitating the Best and Synthesizing the Worst’. *ArXiv:1812.03079 [Cs]*, 7 December 2018.

In this paper, the authors have the ambitious goal of getting imitation learning to work well (though still not as well as traditional motion planning algorithms!) in real-world driving. The key to their success lies in simulated perturbations of the target demonstrations, and adding heuristic losses to discourage undesirable behaviour.

The aim is to train a driving model from human demonstrations ($$26$$ million examples; $$60$$ days of driving). The aim is to do this purely offline because we don't want to expose human demonstrators to exploratory/dangerous situations, or perform costly RL. However, traditional behavioural cloning is found not to work, due to the covariate shift problem.

Rather than using raw sensor data, the model operates with a mid-level input (top-down visual representation of the environment), and output (target trajectory). The first module is a CNN for constructing a vectorised state representation, and the second is an RNN which outputs three things (1) a prediction of successive points in the driving trajectory; (2) the future bounding box of the vehicle as a heatmap; and (3) the future heading. It is trained end-to-end on demonstration data.

The following tricks are used to get the system to work:

- **Dropout** of timesteps in the demonstration trajectories to prevent the model 'cheating' by recognising correlations in actions between timesteps. This correlation-causation confusion would lead to poor behaviour in closed-loop control.
- Augment the dataset with **perturbed** trajectories, where a smooth curve is fitted to bring them back in line. It is actually beneficial if this fitted curve implies a collision, because it shows the model what poor performance looks like. Perturbed data is given a $$10$$x lower weight during training.
  - Such meaningful perturbations are only possible because of the mid-level representation.
- Adding several **specialised losses** using domain knowledge, which penalise the predicted bounding box going off-road or intersecting with any entity in the environment, and reward fitting the demonstrated trajectory shape independent of the speed profile. 
- Training two extra networks **parallel** to the RNN which use the same representation to solve auxiliary tasks: predicting future positions of multiple cars, outputting a binary road/non-road mask.

Closed-loop performance is evaluated in challenging 'set piece' environments: nudging around a parked car, recovering from a swerve and slowing down for a slow car. We see a general improvement versus ablated versions of the model where some features are removed. 

Open-loop performance is also evaluated. It is interesting to see that from the perspective of  prediction on the training distribution, plain old behavioural cloning does best. However, The full model outperforms it when perturbed test data are used.

### Hester, Todd, Matej Vecerik, Olivier Pietquin, Marc Lanctot, Tom Schaul, Bilal Piot, Dan Horgan, et al. ‘Deep Q-Learning from Demonstrations’, 8, 2018.

The algorithm proposed in this paper (`DQfD`) uses small sets of demonstration data, and a combination of TD and imitation losses, to accelerate the RL process for discrete action spaces.

The algorithm takes demonstration data as input. Pre-training is done on these data alone, before any action is taken in the environment. Demonstrations are also permanently retained in the replay buffer throughout training, and given a priority bonus to boost their sampling frequency.

A weighted sum of of four losses is used:

- $$1$$-step TD;
- $$n$$-step TD;
- L2 regularisation to prevent overfitting;
- A 'large margin' supervised loss that pushes the value of the demonstrator’s actions above the other action values. Clearly, this loss is only applied to demonstration data.

The policy used is $$\varepsilon$$-greedy.

Experiments in the Atari Arcade Learning Environment compare DQfD to traditional DQN learning and supervised IL. Several thousand timesteps of human demonstration are used (only a few minutes of gameplay!), which is quickly dwarfed by the learner's own interaction data. Despite this modest data augmentation, initial DQfD learning is much faster than DQN; it takes the latter tens of millions of timesteps to catch up on average. It is also usually faster than IL, by virtue of the improved generalisation ability provided by the TD loss. DQfD achieves state-of-the-art performance on $$11$$ of the $$42$$ games.

Ablation studies show that the precise implementation is important: the combination of all four losses during pre-training, and the weight-boosting of demonstration data to ensure it is used later in training.

### Syed, Umar, and Robert E Schapire. ‘Imitation Learning with a Value-Based Prior’, 2007, 8.

This paper carves a middle path between imitation learning and RL for learning policies in episodic MDPs with known initial-state distributions.

Given a dataset $$\mathcal{D}$$ of demonstrations provided by an unknown target policy $$\pi^\ast$$, the MAP estimate  of that policy can be written as

$$
\hat{\pi}=\underset{\pi}{\operatorname{argmax}}\Big[ \log P(\mathcal{D} | \pi)+\log P(\pi)\Big]=\underset{\pi}{\operatorname{argmax}}\Big[\sum_{s, a, t} K_{s a t} \log \pi_{s a}^{t}+\log P(\pi)\Big]
$$

where $$K_{sat}$$ is the number of appearances of $$(s,a)$$ at time $$t$$ in $$\mathcal{D}$$. This paper proposes a prior term $$P(\pi)$$ that gives greater weight to policies that have higher value in the MDP:

$$
P(\pi)=\exp (\alpha V(\pi))\ \ \ \text{so}\ \ \ \hat{\pi}= \underset{\pi}{\operatorname{argmax}}\Big[\sum_{s, a, t} K_{s a t} \log \pi_{s a}^{t}+\alpha V(\pi)\Big]
$$

This prior encodes the assumption that the target is doing a reasonable (but not necessarily optimal) job at solving the MDP. The higher the true value of $$\pi^\ast$$, the higher the parameter $$\alpha$$ should be set. In practice, the approach appears to be effective over a wide range of $$\alpha$$ values, and when the target’s value is up to $$20\%$$ below optimal.

Unlike previous attempts to use priors in IL, this is not a prior over the policy itself (a strong assumption), but over its *performance*. We remain agnostic about actual action probabilities.

The optimisation problem here is challenging, since we have to estimate the value function for each policy under consideration. To make it tractable, a method is proposed (similar to the EM algorithm) that optimises for each episode timestep of in turn, keeping all the others constant. This algorithm is shown to converge to a local minimum in most reasonable cases.

### Judah, Kshitij, Alan Fern, Prasad Tadepalli, and Robby Goetschalckx. ‘Imitation Learning with Demonstrations and Shaping Rewards’. In *Proceedings of the Twenty-Eighth AAAI Conference on Artificial Intelligence*, 7, 2014.

Up to this point, shaping rewards haven't been used in imitation learning. This paper introduces a method called *Shaped IL* (SHAIL), which is intended to improve learning efficiency.

In addition to training dataset $$\mathcal{D}$$, the learner is provided with a shaping reward function $$R_s$$ and a simulator $$M$$ of the MDP with which it can interact to evaluate its policy $$\pi_\theta$$. The objective of SHAIL is

$$
\underset{\theta}{\operatorname{argmax}}V_{R_s}(\pi_\theta)\ \ \ \text{s.t.}\ \ \ \sum_{(s, a) \in \mathcal{D}} n_{s, a} \log \pi_{\theta}(s, a)\geq \bar{L}
$$

where $$V_{R_S}(\pi_\theta)$$ is the value function of $$\pi_\theta$$ under $$R_s$$. The second term imposes a constraint on the log likelihood of $$\mathcal{D}$$ given $$\pi_\theta$$ ($$n_{s,a}$$ is the number of appearances of $$(s,a)$$ in $$\mathcal{D}$$), to ensure the use of $$R_s$$ doesn't *reduce* the faithfulness compared with conventional behavioural cloning. 

This constrained optimisation problem is solved by following a scheme of Lagrangian relaxation, with policy gradient RL as an inner loop.

Experiments on CartPole and a lane-changing traffic environment (with some very simple shaping rewards), demonstrate an improvement over both behavioural cloning and RL alone, even when the shaping reward is inconsistent with the expert. This is due to the use of the likelihood constraint.

### Reddy, Siddharth, Anca D. Dragan, and Sergey Levine. ‘SQIL: Imitation Learning via Reinforcement Learning with Sparse Rewards’. *ArXiv:1905.11108 [Cs, Stat]*, 25 September 2019.

This paper presents an approach to imitation learning for matching demonstrations over a *long horizon*, which is effectively an alternative to "beyond-BC" techniques such as IRL, GAIL and DAgger. For all of these methods, the aim is not just to imitate demonstrated actions, but also to visit demonstrated states.

It's marvellously simple in comparison. The problem is framed as an RL one, with $$R_{t+1}=1$$ if $$(S_t,A_t)$$ appear in the training set, and $$R_{t+1}=0$$ otherwise. With any positive $$\gamma$$, this (sparse) reward function has the effect of incentivising actions that lead back to the demonstration distribution. Note that no knowledge of the underlying reward function is required. The approach is called *soft Q imitation learning* (SQIL).

The learning procedure is a variant of off-policy RL (specifically soft Q-learning). The replay buffer is initialised with expert demonstrations, then as new experience is accumulated these are added to the buffer with a constant $$r=0$$. In each training batch, the ratio of demonstration experiences and new experiences are kept balanced at $$50:50$$. This keeps the reward gradients reasonable even as the RL policy gets closer and closer to the demonstration policy.

A theoretical analysis shows that SQIL is almost equivalent to a variant of BC that uses a regularisation term to propagate low loss values to states 'nearby' to demonstrated ones (this would require knowledge of the environment dynamics so isn't itself practical).

Various experiments indicate SQIL is much better than BC at handling out-of-distribution situations (e.g. initialising a vehicle in a rotated position not seen in demonstrations). It is competitive to GAIL, while being much simpler to implement.

## 🗝️  Key Insights

All of the papers from this week explore ways to improve imitation learning by incorporating some notion of value or reward, or alternatively to improve RL by using imitation. In super-brief terms, these approaches are:

- Abbeel and Ng: In the absence of knowledge of the target policy’s reward function, assume it has a simple relationship to the state, and iterate between estimating the function from data and performing RL to optimise for it.

- Mayank et al: Augment the typical imitation learning pipeline with a number of ‘tricks’: timestep dropout, perturbed trajectories, hand-crafted heuristic losses and auxiliary tasks. 

- Hester et al: Directly integrate RL and imitation updates into the same training loop by mixing demonstration data with self-generated data. The imitation update can clearly only be applied to demonstration data, but the value update is applied to both.

- Syed and Schapire: Adopt a Bayesian perspective and place a prior over policies before looking at demonstration data. This prior gives greater weight to those with higher value in the MDP. 
- Judah et al: Define a shaping reward function that captures the desired performance as well as possible, and use predictive accuracy vs the target as a hard constraint on RL updates.

- Reddy et al: Wrap the entire imitation learning problem in a ‘meta-MDP’, where positive rewards are accessed by visiting the state-action pairs in the demonstration data. This encourages matching of the state distribution as well as the per-state actions.