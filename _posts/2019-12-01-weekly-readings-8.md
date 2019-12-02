---
title: 'Weekly Readings #8'
date: 2019-12-01
permalink: /posts/2019/12/weekly-readings-8/
tags:
  - weekly-readings
---

State representation learning; emotions and qualitative regions for heuristic explanation; causal reasoning as a middle ground between statistics and mechanics; deep learning and neuroscientific discovery.

## 📝 Papers

### Jonschkowski, Rico, and Oliver Brock. “Learning State Representations with Robotic Priors.” *Autonomous Robots* 39, no. 3 (October 2015): 407–28.

Here the state representation learning problem is addressed in the mobile robot context by incorporating knowledge of the environmental physics in the form of domain-specific *robotic priors*. The state representations are then used to enable efficient and generalisable reinforcement learning.

We assume Markov observations, and thus the problem of learning an observation-state mapping $s_t=\phi(o_t)$. The learning process is constrained by the following five robotic priors:

1. **Simplicity**: for a given task, only a small number of world properties are relevant (approx. Occam's Razor). This is implemented by enforcing the state representation to be of fixed low dimensionality.

2. **Temporal coherence**: task-relevant properties of the world change gradually over time (approx. Newton's 1st law). For a dataset $\mathcal{D}$, this is quantified as

   $$
   L_t(\mathcal{D},\phi)=\mathbb{E}_{t\in1:\vert\mathcal{D}\vert-1}\left[\vert\vert s_{t+1}-s_t\vert\vert^2\right]
   $$

3. **Proportionality**: the amount of change in task-relevant properties resulting from an action is proportional to the magnitude of the action (approx. Newton's 2nd law). This is quantified as 

   $$
   L_p(\mathcal{D},\phi)=\mathbb{E}_{t\in1:\vert\mathcal{D}\vert-1}\left[(\vert\vert s_{t_2+1}-s_{t_2}\vert\vert-\vert\vert s_{t_1+1}-s_{t_1}\vert\vert)^2\ \vert\ a_{t_1}=a_{t_2}\right]
   $$

4. **Causality**: the task-relevant properties, together with the action, are enough to determine the resulting reward, thus different rewards given the same action imply dissimilar states. This is quantified as

   $$
   L_p(\mathcal{D},\phi)=\mathbb{E}_{t\in1:\vert\mathcal{D}\vert-1}\left[\text{sim}(s_{t_1},s_{t_2})\ \vert\ a_{t_1}=a_{t_2},\ r_{t_1+1}\neq r_{t_2+1}\right]
   $$

   where $\text{sim}$ is any differentiable similarity function. Here, the squared exponential is used: $\text{sim}(s_{t_1},s_{t_2})=e^{-\vert\vert s_{t_2}-s_{t_1}\vert\vert^2}$.

5. **Repeatability**: the task-relevant properties, together with the action, are enough to determine the resulting change in these properties, thus the same action in similar states produces similar effects. This is quantified as 

   $$
   L_r(\mathcal{D},\phi)=\mathbb{E}_{t\in1:\vert\mathcal{D}\vert-1}\left[\text{sim}(s_{t_1},s_{t_2})\cdot\vert\vert (s_{t_2+1}-s_{t_2})-(s_{t_1+1}-s_{t_1})\vert\vert^{2}\ \vert\ a_{t_{1}}=a_{t_{2}}\right]$
   $$

   where again the squared exponential similarity measure is used.

Crucially, while generally useful, each of these priors is regularly contradicted in real experiments. The proposed method is robust to these counterexamples, since all priors (apart from 1) are implemented as soft targets rather than hard constraints. They are combined linearly into a single loss function $L(\phi,D)$ using weights $\omega$, hand-chosen so that the terms provide appropriate gradients.

- Note: since the causality prior directly opposes the other three, its gradient should be as large as the other three combined.

The proposed method learns a **linear observation-state mapping** $s_t=\phi(o_t)=W(o_t-\mu_o)$ where $\mu_o$ is the mean of all observations in $\mathcal{D}$. The weight matrix $W$ is adapted by performing gradient descent on a regularised loss function:

$$
W^*=\arg \min_W\left[L(\mathcal{D},\phi)+\lambda l_1(W)\right]
$$

where $l_1(W)=\sum_{i,j}\vert W_{i,j}\vert$ is the regularisation term.

In experiments (simulated and real-world robot navigation tasks), the learned state representation is fed into a standard Q-learning RL agent. The representation and policy are learned semi-concurrently: after each step of the representation learning process, the Q-learning agent is run for $20$ episodes. 

During learning, there is a very strong correlation between representation loss and RL reward. The learned representations are largely invariant to perspective: given both an egocentric and top-down view of a simulated environment, the resultant 2D state representations are very similar and resemble the environment itself. Given the correct dimensionality, the method is robust to distractors: in a racing track environment with two cars, only one of which is controllable, the 2D representation is independent of the non-controllable car (note: the two cars are in different lanes so never need to interact). Overall, RL performance with learned representations far exceeds that using raw observations or principle components, and comes very close to using the ground-truth pose.

In summary, it has been suggested by some that generic priors can be used to solve arbitrary task environments, but this seems overly optimistic. A handful of domain-specific (but still pretty simple) priors have been shown to be effective for several robotics tasks. Plenty more work could go into formulating more…

### Kaptein, Frank, Joost Broekens, Koen Hindriks, and Mark Neerincx. “The Role of Emotion in Self-Explanations by Cognitive Agents.” International Conference on Affective Computing and Intelligent Interaction, 2017.

It is argued that computational models of emotion could provide concise heuristics for diagnosing, explaining and predicting action in agent-based systems. 

Consider a set of propositions $\mathcal{P}$. An agent's *belief* function maps each $p\in\mathcal{P}$ to a *certainty* value in $[0,1]$ and a *desire* function maps each $p$ to a *utility* value in $[0,1]$. Finally, an *emotion* function maps each $p$, in conjunction with an emotion label $\theta\in\Theta$ to an *intensity* value in $[0,1]$ which indicates how strongly $\theta$ applies to $p$. For example, $(\theta=fear$, $p=dog\ in\ my\ house$, $intensity=0.1)$   means that the agent is not very scared of having a dog in their house.

The agent's *mental state* $m_t$ is fully characterised by their beliefs, desire and emotion functions at time $t$. Mental states are updated over time, which we can assume is a Markovian process. It is proposed that we explain an action taken on the interval $t\rightarrow t+1$ in emotional terms by finding the single emotion $\theta^*$ whose  intensity value is increased the most (noting that negative emotions have negative intensities) between $m_t$ and $m_{t+1}$, or by finding a set of appropriate emotions.

Assuming that an overall emotional state is some aggregation of the proposition-directed emotion intensities, we can explain this state itself using a selection of the most highly-contributing propositions.

### Kurumatani, Koichi. “Generating Causal Networks for Mobile Multi-Agent Systems with Qualitative Regions.” In *IJCAI*, 1750–1756, 1995.

A causal influence diagram is constructed to describe the macro-scale behaviour of a swarm of simple mobile agents (simulating an ant colony). In the diagram, nodes represent macro-scale properties and edges represent positive / negative monotonic relationships between those properties. 

The properties used are based on *qualitative regions*: spatial regions of the environment with certain qualitative properties (e.g. containing ants in 'search' mode; with pheromone concentration above a certain threshold). Transition rates of ants between various behaviour modes can be modeled in terms of the areas and populations of these regions. 

The diagram can be used to predict behavioural trends, and particularly feedback loops (either through manual inspection or by application of logical inference in Prolog). In the example application, a closed path is found containing the size of the high-pheromone region, indicating that there is likely to be positive feedback on this variable. This result is observed in simulation. 

### Lesort, Timothée, Natalia Díaz-Rodríguez, Jean-François Goudou, and David Filliat. “State Representation Learning for Control: An Overview.” *Neural Networks* 108 (December 2018): 379–92.

State representation learning (SRL) is a special case of representation learning in which the features to learn evolve through time, influenced by actions or interactions. Given an *observation* representation $O$, the objective of SRL is to reconstruct a *state* representation $S$ that serves as a useful and efficient input for a control policy. Active learning through exploration, as well as prior knowledge of physical and mechanistic properties, can aid the reconstruction process. It is often desirable for the state representation to be Markovian, low-dimensional and generalisable, and for its features to have non-overlapping semantic meanings.

SRL uses a nomenclature very similar to that of reinforcement learning. A time $t$, the environment has a true state $\tilde{s}_t$ but we / the agent only have access to an observation $o_t$. The agent's action is $a_t$. We aim to learn a mapping $\phi$ such that $s_t=\phi(o_t)$ captures the salient properties of $\tilde{s}_t$. This paper introduces four formulations of the SRL problem.
1. **Reconstructing the observation**. Here the problem is framed in terms of minimising a distance measure between $\hat{o}_t$ and $o_t$ where $\hat{o}_t=\phi^{-1}(s_t)=\phi^{-1}(\phi(o_t))$, subject to constraints on $s_t$ such as sparsity, dimensionality and independence. This approach can be implemented with an autoencoder architecture.
2. **Learning a forward model**. Here we have a two-step model: the mapping $\phi$ from $o_t$ to $s_t$, and a transition model $f$ from $s_t$ (and $a_t$) to $s_{t+1}$. The idea here is that we cannot compute any error on $s_t$, but we can compute one between $\hat{s}_{t+1}=\phi(o_{t+1})$ and $s_{t+1}=f(\phi(o_t),a_t)$. The error is back-propagated through both $f$ and $\phi$. An advantage of this method is that we can impose structural constraints on $f$ if these are known (linear dynamics are commonly assumed).

3. **Learning an inverse model**. This model is also a two-step one; the mapping $\phi$ from $o_t$ to $s_t$, an inverse model to recover $a_t$ given $s_t$ and $s_{t+1}$. The error is computed between $a_t$ and the true action $\hat{a}_t$ and back-propagated. It has been argued that this formulation may be easier than the forward one, since actions are likely to be more low-dimensional than states.
4. **Using prior knowledge to constrain the state space**. This approach involves constraining the representation space using priors about properties such as temporal smoothness (consecutive states should be similar) and repeatability (the same action in similar states should produce similar results). Priors are defined as loss functions to be minimised over a dataset of observations.

Several works have aimed to hybridise two or more of these approaches. Often a forward and inverse model are learned in parallel, both mutually contributing to each other's loss function. A general piece of advice given is to attempt to integrate as many priors and learning objectives as possible.

Where reward are available, these can be used to further guide the representation learning process. For example, we may modify the loss function to incentivise representations that allow accurate prediction of the reward / value for a given state. Alternatively, if we have very different rewards after performing the same action in two timesteps, the two corresponding states should be significantly differentiated in representation space. 

It is noted that there is currently no standard evaluation method for SRL. We may wish to use some kind of disentanglement or interpretability metric, or alternatively care only about performance on a specific task or range of tasks.

### Schölkopf, Bernhard. “Causality for Machine Learning.” *ArXiv:1911.10500 [Cs, Stat]*, November 24, 2019.

Argues that many of the hard open problems in ML and AI are related to causality.

Almost all progress in ML has been on problems which are i.i.d. For such problems, statistical learning theory can provide strong convergence guarantees. Machines tend to perform poorly on non-i.i.d. problems, even those that seem trivial to humans. In particular, the i.i.d. assumption is violated when we *intervene* on a system rather than passively observe it. If we are given observations alone, we cannot meaningfully predict the effect of an intervention without making additional assumptions.

The conceptual basis of statistical learning is a joint distribution $p(X_1,...,X_n)$, where one or more of the $X_i$ is considered a *response* variable and denoted $Y$. Causal learning seeks to exploit the fact that the joint distribution possesses a unique latent causal factorisation, whereby each variable is conditionally independent of all others given a set of parents: $p(X_i\vert\textbf{PA}_i)$. By further pursuing structural equation modelling, we attempt to learn a functional description of the dependencies, which includes independent noise terms to account for ignorance or inherent randomness.

If we are able to obtain the correct causal factorisation, we can make use of all manner of invariances (e.g. the distribution of a cause variable is independent of the mechanism producing its effect variable). With the wrong factorisation, no such properties exist.

We can think of causal learning as lying **somewhere between the extrema of statistical analysis and mechanistic mathematical modelling** (e.g. via differential equations). The inclusion of structural equations moves the position closer towards the latter.

Ideas from machine learning (e.g. optimisation algorithms, assumptions about functional classes) can help us to tackle causality problems. Perhaps more interestingly, however, the same is true vice versa. Knowledge of the causal direction allows us to predict what information is should be possible to learn in a given context. Causal models should also be far more robust to adversarial attacks.

RL is closer to causality research than other ML fields in that it sometimes effectively directly estimates do-probabilities (on-policy learning), although issues of causality become subtle in the off-policy setting. Two major weakness of RL can be phrased as questions:

- Why is RL on the original high-dimensional Atari games harder than on down-sampled versions? For humans, reduced resolution makes the problem harder. This is because we have strong methods for deciding what constitutes an *object*.
- Why is RL easier if we permute the replayed data? For humans, temporal order contains useful information.

Traditional causal discovery and reasoning assumes up front that the variables are the correct ones for building a disentangled causal model. The emerging field of *causal representation learning* seeks to assemble these variables (denoted $S$) from more fine-grained data, over variables $X$ which may themselves be tangled. Some kind of autoencoder architecture may be able to achieve this:

- The encoder maps $X$ into the noise variables $U$, which should be statistically independent. We can think of it as recognising the causal drivers in the world.
- We then need to find the mapping $S=f(U)$ where the structural assignments $f_1,…,f_n$ are independent. 
- The decoder acts as a causal generative model, aiming to reconstruct $X$ again from $U$. 

### Tanaka, Hidenori, Aran Nayebi, Niru Maheswaranathan, Lane McIntosh, Stephen Baccus, and Surya Ganguli. “From Deep Learning to Mechanistic Understanding in Neuroscience: The Structure of Retinal Prediction.” In *Advances in Neural Information Processing Systems 32*, 8535–8545. Curran Associates, Inc., 2019.

Do deep (convolutional) neural networks provide a useful explanatory model for the brain's (retina's) computational mechanisms or are we just replacing one inscrutable black box with another? Here the aim is to put the deep network framework on firmer theoretical foundations.

The specific focus is on understanding how a deep CNN is able to accurately reproduce various real neural responses, given a history of visual stimulus (i.e. several recent timesteps simultaneous) as input. Is it only accurate on an input-output level, or is it also a good model of the underlying mechanisms?

The approach taken is that of *model reduction*. Importance values are computed *with respect to a specific stimulus type* for each unit in the first hidden layer on the CNN, and a minimal circuit model (feedforward network with one hidden layer) is constructed from the most important units. This is done separately for each stimulus type, yielding a different minimal circuit for each. The specialised reduced models prove effective at replicating the neural responses.

Hence, we have a promising way forward for revealing computational structure in the brain:

1. Gather large amounts of neural data from various contexts;
2. Train a large and complex neural network model on these data;
3. Apply model reduction to understand how *parts* of the model account for various kinds of response.

## 📚  Books

### Dennett, D. & Hofstadter, D. (2001). *The Minds' I: Fantasies and Reflections on Self and Soul*. Basic Books.

A fundamental change of perspective occurs when I realise that a person being talked about is *me*. While during most of my life I suppress this fact, there is an irreconcilable difference between the nature of other people (their status as a part of the objective world, their mortality, their ownership of a head...) and that of myself.

While the biological sciences have rushed to explain the mind in ever more reductionist, physical terms, quantum physics (particularly the Copenhagen interpretation) has led us to a view of the universe in which subjective observation is itself fundamental, perhaps more so than the objects of observation themselves. Is our whole scientific worldview at risk of becoming one big circular definition? The many-worlds interpretation is little better, since it implies distributed and continuously-branching identities. 

## 🗝️  Key Insights

- State representation learning is likely to be a pivotal aspect of nontrivial explainability work - we rarely know up front what the best representation is! The MDP formulation, with its feedback loops and interactivity, may actually present an easier representation learning problem than traditional classification and regression tasks. Regardless, prior assumptions are required to constrain the learned representations towards something generalisable and semantically meaningful.

- Other interesting areas of explainability research for agent-based systems include the use of emotional labels as understandable heuristics for justifying action, and macro-scale causal influence diagrams for predicting emergent behaviour. These methods are both pretty hard-coded by default.

- The notion of causal reasoning lying at the middle of a spectrum from raw statistical analysis to rigid mathematical modelling is a compelling one, and helps to show its potential benefits to researchers currently working at either end of the spectrum.

- One possible way of dealing with the black box nature of deep learning for neuroscience [and elsewhere?] is to initially embrace it, then progressively piece apart the learned representation into something simpler: a kind of two-stage approach to scientific investigation.

  