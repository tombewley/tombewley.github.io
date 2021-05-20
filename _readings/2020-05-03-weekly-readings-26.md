---
title: 'Weekly Readings #26'
date: 2020-05-03
permalink: /posts/2020/05/weekly-readings-26/
excerpt: 'Terminological quagmires; (mis)interpreting interpolation; interaction is paramount.'
tags:
  - weekly-readings
---

## 📝 Papers

### Atkeson, Christopher G., and Stefan Schaal. *Robot Learning From Demonstration*, 1997.

This paper describes implementation of a model-based kind of imitation learning to perform the pendulum swing-up task by acceleration-based control of the horizontal position $x$ of a physical robot hand. The pendulum starts at angle $\theta=\pi$ and a successful swing-up moves it to $\theta=0$.

The approach makes use of a **task model** and a **imitation-based cost function** to be used by an **optimal control planner**. For the task model, the authors use a discrete-time parametric model of the angular velocity of an idealised pendulum attached to a horizontally-moving hand:

$$
\dot{\theta}_{k+1}=\left(1-\alpha_{1}\right) \dot{\theta}_{k}+\alpha_{2}\left(\sin \left(\theta_{k}\right)+\ddot{x}_{k} \cos \left(\theta_{k}\right) / g\right)
$$

The two parameters $\alpha_1$ and $\alpha_2$, corresponding to the viscous damping and $\Delta g/l$ respectively ($\Delta$ is the timestep), are learned from data by linear regression. An alternative nonparametric *locally-weighted learning* model, to predict $\dot{\theta}_{k+1}$ as a function of $(\theta_{k}, \dot{\theta}_{k}, x_{k}, \dot{x}_{k}, \ddot{x}_{k})$, is also learned.

These models are used by an optimal control planner to minimise a cost function that penalises deviations from a demonstration trajectory and squared acceleration:

$$
r\left(\mathbf{x}_{k}, \mathbf{u}_{k}, k\right)=\left(\mathbf{x}_{k}-\mathbf{x}_{k}^{\mathrm{d}}\right)^{\mathrm{T}}\left(\mathbf{x}_{k}-\mathbf{x}_{k}^{\mathrm{d}}\right)+\mathbf{u}_{k}^{\mathrm{T}} \mathbf{u}_{k}
$$

where the state is $\mathbf{x}=(\theta, \dot{\theta}, x, \dot{x})$, $\mathbf{x}^{\mathrm{d}}$ is the demonstrated motion, $k$ is the sample index, and the control is $\mathbf{u}=(\ddot{x})$.

With both parametric and non-parametric models, this approach successfully imitates human demonstrations with one back-and-forth motion of the pendulum, but it fails at the more difficult task of "pumping" the pendulum twice before swinging it up. 

It is suggested that this is likely due to a mismatch between the model structure and the true system. To combat this, an additional free parameter is introduced: allowing the target angle used by the planner to vary away from $\theta=0$. Searching across a range of values identifies a value which allows the more complex task to be learned.

### Bhattacharyya, Raunak P., Derek J. Phillips, Changliu Liu, Jayesh K. Gupta, Katherine Driggs-Campbell, and Mykel J. Kochenderfer. ‘Simulating Emergent Properties of Human Driving Behavior Using Multi-Agent Reward Augmented Imitation Learning’. In *ArXiv:1903.05766 [Cs]*, 2019.

Both imitation learning and reinforcement learning are challenging and unstable in multi-agent domains where undesirable emergent properties may develop. The authors propose to tackle this problem by augmenting the generative adversarial imitation learning (`GAIL`) approach with prior knowledge in the form of hand-crafted rewards to disincentivise visiting a set of undesirable state-action pairs $U$.

`GAIL` uses an adversarial two-model setup, whereby a discriminator network $D_\psi$ is trained to output a high score given state-action pairs from a demonstration policy $\pi^\ast$, and a low score given pairs from a learner policy $\pi_\theta$.

Rather than applying the reward augmentation as a hard constraint (which makes optimisation much more difficult), it is added as a regularisation term to the `GAIL` objective:

$$
\underset{\theta}{\min}\ \underset{\psi}{\max}\ \mathbb{E}_{s,a\sim d_{\pi}^\ast}\left[D_{\psi}(s,a)\right]-\mathbb{E}_{s,a\sim d_{\pi_\theta}}\left[D_{\psi}(s,a)\right]+r \mathbb{E}_{\pi_{\theta}}\left[\mathbf{1}_{U}\right]
$$

This objective is solved in two iterative steps:

- Optimise the discriminator parameters $\psi$ using data from new rollouts.
- Use *Trust Region Policy Optimisation* to update the policy parameters $\theta$. Part of the loss comes from the discriminator, and part comes from the reward augmentation term.

In the context of a traffic simulator environment with real-world training data, one reward augmentation scheme ("binary") consists of a large penalty $R$ if a vehicle crashes or drives off the road, and a smaller one $R/2$ if it performs a hard brake. An alternative ("smooth") uses a linearly-increasing penalty as a function of distance to the road edge or braking magnitude.

`RAIL` is compared with `GAIL` on various metrics: positional divergence of vehicles from the training data, error rate (collision, off-road, hard-brake), and frequency of emergent phenomena (lane changes, time gaps between vehicles) compared with the training data. During these evaluations, a certain proportion of the vehicles use the learned policy, and the rest follow the training data. `RAIL` is clearly seen to do better.

### Brennen, Andrea. ‘What Do People Really Want When They Say They Want “Explainable AI”? We Asked 60 Stakeholders.’, 2020, 7.

Here the author summarises two key findings from stakeholder interviews.

**Lack of consistent terminology:**

- Identified synonyms for "Explainable" included "Accountable", "Fair", Reliable" and "Verifiable". Some interviewees used terms interchangeably that others insisted were very different. 
- Similarly, the two terms "Interpretability" and "Explainability" were used by some to mean the same thing, and others to describe two alternative approaches. What those alternatives actually were also varied!
- Finally, even "AI" meant different things to different people. Some were interested only in deep learning models, while others extended their definition to incorporate nearly any automated manipulation of data.
- Miscommunication is exacerbated when words have both technical and nontechnical definitions, e.g. "Fairness".

**Multiple motivations for explainability:**

- Most people started with the notion of AI as a *black box*, and that the existence of a *mismatch* between what they wanted to understand and what they currently understood.
- But there are *at least* three very distinct variants:
  - **Debugging models**: explainability as a tool to be used by engineers for improving performance. 
  - **Identifying bias**: explainability to identify problematic data or inferences, important from business and legal perspectives.
  - **Building trust**: explainability to help end-users understand unfamiliar technologies and assuage their anxiety.
- With different explainees and different content requirements, it seems reasonable to expect we'll need different solutions.

Identifying these issues, which hinder discussion and mutual understanding, is the first important step toward mitigating them.

### Elton, Daniel C. ‘Self-Explaining AI as an Alternative to Interpretable AI’. *ArXiv:2002.05149 [Cs, Stat]*, 24 April 2020. 

The *double descent phenomenon* indicates that deep neural networks typically operate by interpolating between data points rather than by extracting a few high level rules as we might have hoped. This is a 'dumb' process: any apparent regularities that appear to be captured internally are properties of the data rather than a self-directed distillation process.

In addition to making failure likely outside the training distribution, this behaviour makes interpretation (which makes the implicit assumption that such latent rules exist) inherently hard. With this in mind, how can we ever hope to trust AI systems? Instead of post-hoc methods, Elton advocates for **self-explaining** AI models. In addition to the prediction itself, a self-explaining model would output:

- A human-understandable explanation; 
- Confidence levels both both prediction and explanation.

Prediction and explanation branches from a shared set of primary layers. How can we trust that the explanation is actually relevant? One possible option is to measure the *mutual information* between the prediction $Y$ and the activation vector of the final shared latent layer $L$, and also between the explanation $E$ and $L$:

$$
\text{Relevance}(E,Y)\doteq\sum_{i=1}^{\vert L\vert}\text{MI}(L_i,Y)\text{MI}(L_i,E)
$$

A disadvantage of this is that mutual information is extremely expensive to compute!

A couple more points made during the discussion:

- The term "black box" should not be used as often as it is, because given enough time and effort we *can* know exactly what's inside a neural network, and how it got there. The issue is that we don't have a good way of relating this knowledge to questions we actually care about. 
- Given that deep neural networks seem to operate using dumb interpolation, there seems to be a direct conflict between the accuracy of an interpretation, and its relevance to the domain of application.

## 🎓  Theses

### Ross, Stephane. "Interactive Learning for Sequential Decisions and Predictions." (2013).

> Learning actively through interaction is necessary to obtain good and robust predictors for sequential prediction tasks. No-regret online learning methods provide a useful class of algorithms to learn efficiently from these interactions, and provide good performance both theoretically and empirically.

This thesis introduces interactive learning methods that address the major limitation of behavioural cloning: the sequential nature of control problems breaks the i.i.d. assumption. Any open-loop error causes the test distribution to diverge from the training one in the closed-loop setting, and poor performance results.

The ideal solution is to train on the distribution that the learned predictor will see in closed-loop, but this is a *chicken-and-egg* problem! A common strategy to deal with such problems is to adopt an iterative training approach, and this is what is done here. Overall, the effect is to **reduce imitation learning (and related problems) to online learning**.

#### Learning Behaviour from Demonstrations

Here we start to tackle the problem of learning good control policies from demonstration. All analysis assumes an episodic MDP of fixed length $T$, but does generalise to discounted infinite-horizon tasks. Performance is quantified in terms of a non-negative cost to be minimised $C(s,a)\in[0,C_{\max}]$, rather than reward $R(s,a)$ which may be positive or negative. This simplifies much of the analysis.

Our ultimate goal is to minimise $J(\pi)$, the expected sum of costs accumulated by $\pi$ over $T$-timestep episodes under the induced state distribution $d_\pi$. Since this is challenging to do directly, we introduce a surrogate loss $\ell(\pi,\pi^\ast)$ that quantifies some measure of deviation from a high-performing *expert* policy $\pi^\ast$. In the special case when we are interested in the learner's ability to predict the expert's actions, $C=\ell$.

Behavioural cloning is the most naive solution to this problem, which simply performs supervised learning on a training distribution generated by $\pi^\ast$. $\epsilon$ the expected loss under this distribution. It can be proven that if $\ell$ is the 0-1 loss (or an upper bound such as the hinge or logistic loss), then $J(\pi) \leq J\left(\pi^{*}\right)+C_{\max } T^{2} \epsilon$, meaning the closed-loop cost of $\pi$ compared with $\pi^\ast$ **grows quadratically** with $T$. This is much worse than the i.i.d. setting, where the cost of classifying $T$ samples grows linearly with $T$.

What follows is a selection of approaches for closing this gap.

##### Forward Training

As a simple starting point, we can imagine training a *sequence* of policies $\pi_1,...,\pi_T$ in order. For each $\pi_t$, we sample multiple $t$-step trajectories, starting in the initial state distribution and continued by executing $\pi_1,...,\pi_{t-1}$. This produces a distribution of states for time $t$. We query the expert for these states and use the results to train $\pi_t$.

By training sequentially in this way, each $\pi_t$ is trained under the distribution of states it's going to encounter during closed-loop execution. If previous policies produce poor predictions, then $\pi^\ast$ will demonstrate the necessary recovery behaviours at future steps.

Iterative forward training attains closed-loop loss that grows linearly with $T$ (the best possible case), but it is impractical when $T$ is large (or the MDP is continuing), and inefficient in that the same or similar behaviours may have to be learned many times over for different timesteps.

##### Stochastic Mixing Training

The two approaches reviewed here achieve similar guarantees by adopting the same general philosophy of *learning gradually*.

`SEARN` works by starting from a policy $\pi_0=\pi^\ast$, i.e. one that just queries the expert. A new policy $\hat{\pi}_1$ is trained to minimise the surrogate loss $\ell$ on data from the execution of $\pi_0$. This is then **stochastically mixed** with $\pi_0$ to obtain the next policy

$$
\pi_1=(1-\alpha)\pi_0+\alpha\hat{\pi}_1
$$

which at every timestep $t$, follows $\hat{\pi}_1$ with probability $\alpha$, and follows $\pi_0$ otherwise. It keeps iterating in a similar fashion, so that

$$
\pi_{n}=(1-\alpha) \pi_{n-1}+\alpha \hat{\pi}_{n}=(1-\alpha)^{n} \pi_{0}+\alpha \sum_{i=1}^{n}(1-\alpha)^{n-i} \hat{\pi}_{i}
$$

After some large number of iterations $N$, `SEARN` terminates and returns a final policy $\pi_N$ that never has to query $\pi^\ast$ by renormalising:

$$
\pi_{N}=\frac{\alpha}{1-(1-\alpha)^{N}} \sum_{i=1}^{N}(1-\alpha)^{N-i} \hat{\pi}_{i}
$$

By default, `SEARN` involves simulating an entire trajectory to collect each training datapoint, which is often impractical. A variant, called `SMILE`, addresses this issue. It keeps the same update relationship between policies, mediated by $\alpha$, but at each step $n$ the training is simply to imitate the expert $\pi^\ast$ on the latest dataset. Hence each $T$-step trajectories yields $T$ datapoints for training instead of one. However, `SMILE` has less strong performance guarantees than `SEARN` or forward training.

Both `SEARN` and `SMILE` also have the disadvantage of requiring a stochastic policy which might be undesirable in practical (safety critical) applications.

##### Dataset Aggregation

This approach, the flagship of the thesis, is shortened to `DAgger`. It can learn deterministic policies, and is even simpler than the preceding methods. 

`DAgger` starts by gathering a dataset $\mathcal{D}$ of expert-generated trajectories, trains a policy $\pi_2$ to imitate the expert on those data. Then at iteration $n$, it  proceeds by collecting a dataset at each iteration under $\pi_n$, appends this to $\mathcal{D}$, and trains $\pi_{n+1}$ on the concatenation of all collected datasets. It is a kind of *follow the leader* algorithm in that at each iteration we find the policy that would give the best imitation in hindsight on all previous data.

This basic algorithm can be modified to use a mixture policy at each iteration $n$, that samples from either $\pi_n$ or $\pi^\ast$ according to a parameter $\beta_n$. In practice however, it is found that it's often best to just set $\beta_1=1$ and $\beta_n=0$ for all $n\neq1$.

`DAgger` works with any 'no-regret' online learning algorithm. 

A couple of questions:

- Why not just collect data everywhere, e.g. via a random or noisy policy? Because (1) it's very data-inefficient, and (2) when the policy class $\Pi$ is not expressive enough to fully *realise* the target policy, we need to trade-off accuracy in different regions correctly fitting irrelevant data may actually harm performance.  
- Why not just use the last collected dataset as in policy iteration? This tends to be very unstable and leads to oscillation between multiple mediocre policies. When we constantly append to $\mathcal{D}$, the fraction of new data decreases over time, so the policy will tend to change more and more slowly, and stabilise around some behaviour that produces good predictions under inputs that were collected by similar predictors. We get increasingly close to the 'ideal' of matching training and test distributions.

#### Learning Behaviour using Cost Information

Now consider the case where an expert is present, *and* additional cost information is available. Intuitively, this should enable better performance!

##### Forward Training with Cost-to-Go

Instead of only observing the expert's actions in states reached at time $t$ by execution of $\pi_1,...,\pi_{t-1}$, we instead *explore* actions to perform at $t$, follow $\pi^\ast$ until the end of the episode, and observe the total cost $Q$ of this sequence. Under the assumption that $\pi^\ast$ is a decent policy and that $\Pi$ contains similar good policies, then these $Q$ values give us a rough estimate of what good policies in $\Pi$ will be able to achieve at future steps.

$\pi_t$ is trained to minimise cost on the collected dataset of $(s_t,a_t,Q)$ triples. If we are lucky enough to be able to sample *all* actions from each $s_t$, we have all the information we need for cost-sensitive classification learning. Otherwise, we can reduce the problem to a regression one (predicting cost for a state-action pair) or use importance weighting techniques.

To select exploring actions from an $s_t$, we can simply use a random strategy. Better results might be attained by casting this as a contextual bandit problem. Developing efficient algorithms for this problem is still an open problem.

In cases where the expert is much better than any policy in $\Pi$, then the cost estimates may be very optimistic, and not reflective of the true prospects of the learner. This will not lead to good performance.

##### `DAgger` with Cost-to-Go

A similar idea is used here. At iteration $n$, we collect each of $m$ sample as follows:

- Follow current policy $\pi_n$ from the start of the episode to a randomly-sampled time $t\in\{1..T\}$.

- Execute some exploration action $a_t$ in $s_t$.

- Follow $\pi^\ast$ from $t+1$ to $T$, observing the total cost $Q$ starting at $t$.

After adding the $m$ new samples to $\mathcal{D}$, we train $\pi_{n+1}$ as a cost-sensitive classifier.

By minimising cost, this algorithm is effectively a regret reduction of imitation learning, rather than an error reduction as obtained when minimising classification loss in conventional `DAgger`.

Utilising cost-to-go can often be expensive and impractical compared with simple imitation loss minimisation. A potential combination of the two approaches could be very effective.

## 🗝️  Key Insights

- Atkeson and Schaal’s classic paper, oft-cited in the imitation learning literature, takes quite a heavily model-based approach compared with more recent works.
- That said, Bhattacharyya et al’s much newer `RAIL` model makes use of domain knowledge, in the form of hand-crafted penalties for known failure modes, added as an extra term to the `GAIL` objective.
- Brennen’s review lays bare the concerning lack of consistency or rigour in uses of words such as “interpretability” and “explainability”. With so many potential applications in mind, it might be that both terms are just too broad to be meaningful.
- Elton’s proposal for self-explaining AI is to me less interesting than some of the high-level observations he makes along the way. The term “black box” is really inappropriate when what is missing is not *knowledge* of a neural network’s internal representations, but a way of *relating* them to issues we care about. And this seems doubly challenging if we believe the evidence that such representations encode mere interpolation rules rather than high-level regularities.

- Ross’ thesis gives compelling arguments for the critical importance of interaction when doing imitation learning in dynamic contexts. His `DAgger` algorithm is an easy-to-implement scheme for implementing this interaction. 