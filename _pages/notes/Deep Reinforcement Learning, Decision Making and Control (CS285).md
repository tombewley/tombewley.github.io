---
title: Deep Reinforcement Learning, Decision Making and Control (CS285)
permalink: /notes/Deep Reinforcement Learning, Decision Making and Control (CS285)
---

#Content/Course by [Sergey Levine](Sergey%20Levine) and others at [UC Berkeley](UC%20Berkeley).

[http://rail.eecs.berkeley.edu/deeprlcourse/](http://rail.eecs.berkeley.edu/deeprlcourse/)

## Lecture 1: Introduction and Course Overview
Deep learning helps us *handle unstructured environments* but is traditionally used merely for pattern recognition; reinforcement learning provides a *general formalism for behaviour* in terms of observations, actions and rewards, that aligns well with animal behaviour and experimental neuroscience. Deep RL combines the two, providing an end-to-end method for learning behaviour and decision making. There is a strong analogy to how computer vision has switched from hand-crafted processing stages to end-to-end deep learning. Deep RL is our current best bet for the 'master' algorithm that can solve the problem of intelligent behaviour in general.

The end-to-end learning of representations, informed by the final task application, is the key feature of the deep learning paradigm. This distinguishes it from traditional approaches in which the representation hierarchy is constructed by hand. Deep RL brings end-to-end representation learning into the control context.
- Most problems we think of as AI problems can be cast as RL, although this is not always the most efficient thing to do.

For most interesting real-world control problems, external rewards are extremely sparse and exploration is hard. We need more than just the reward-maximising policy update logic of RL, and [Inverse Reinforcement Learning](Inverse%20Reinforcement%20Learning), [Imitation Learning](Imitation%20Learning), [Transfer Learning](Transfer%20Learning) and [Meta-learning](Meta-learning) are all important pieces of the puzzle. Results from [Cognitive Science](Cognitive%20Science) also point to the importance of prediction for control. This motivates work on [Model-based Reinforcement Learning](Model-based%20Reinforcement%20Learning).

Open problems: deep RL is currently slow, transfer learning to reuse past knowledge is far from solved, it's not always clear what the reward function should be.

## Lecture 2: Supervised Learning of Behaviours

### OLD

Given an observation $o_t$ of an underlying state $s_t$ at time $t$, we are interested in producing an action $a_t$ via a policy function $\pi_\theta(a_t\vert o_t)$, which is parameterised by $\theta$. The trickiness comes from the fact that our choice of action will influence what $o_{t+1}$ will be. States satisfy the Markov property, but since observations may be incomplete or corrupted, they do not in general.

Given a dataset of $o$s and $a$s produced by some other system (e.g. a human), we can try to learn a mapping using standard supervised learning techniques. This is called *behavioural cloning*. The method is quite brittle, since any noise in observations lead us to veer ever further away from any single training trajectory and produce unpredictable behaviour. This stability problem is an example of *distributional shift*. In theory, this could be solved by the following procedure called [DAgger](A%20Reduction%20of%20Imitation%20Learning%20and%20Structured%20Prediction%20to%20No-Regret%20Online%20Learning):

1. Train $\pi_\theta(a_t\vert o_t)$ from target system (human) data $\mathcal{D}=\{o_1,a_1,...,o_N,a_N\}$.
2. Run $\pi_\theta(a_t\vert o_t)$ to get dataset $\mathcal{D}_\pi=\{o_1,...,o_M\}$ (only observations needed).
3. Ask human to label $\mathcal{D}_\pi$ with actions.
4. Aggregate $\mathcal{D}\leftarrow\mathcal{D}\cup\mathcal{D}_\pi$ and repeat.

Though in practice step 3 is clearly going to be very labour intensive if we are indeed using humans as the target, and also doesn't work if the initial learned policy is so bad that it produces trajectories that we can't even label properly.

Can we make behavioural cloning work without more data? Theoretically no, but practically yes through hacks such as sampling a wider range of trajectories from the target system, including those that are intentionally sub-optimal. 

Why can't we use behavioural cloning to solve everything? Well, humans can only provide a limited amount of data, and we're not good at everything. To go beyond this, we need to introduce the idea of costs and rewards.

### NEW

In this course we adopt the POMDP formalisation with Markovian states $s_t$, possibly non-Markovian observations $o_t$, actions $a_t$, and policies $\pi_\theta(a_t\vert o_t)$ which are observation-conditioned distributions over actions parameterised by $\theta$. Here is a useful causal DAG representation:

![Screenshot from 2021-04-19 20-13-01.png](Screenshot%20from%202021-04-19%2020-13-01.png)

How can we learn policies? The most obvious solution to those familar with supervised learning is [Behavioural Cloning](Behavioural%20Cloning): collect $(o,a)$ pairs from an expert demonstrator and train a vanilla supervised learning model. This is the most basic form of [Imitation Learning](Imitation%20Learning).

BC suffers from a stability problem called [Covariate Shift](Covariate%20Shift) ($p_{data}(o_t)\neq p_{\pi_\theta}(o_t)$). It is theoretically proven that [DAgger](A%20Reduction%20of%20Imitation%20Learning%20and%20Structured%20Prediction%20to%20No-Regret%20Online%20Learning) progressively mitigates this problem over time. 

We can also improve imitation learning by simply trying to fit the expert data better. 
- If the expert policy is non-Markovian, we may benefit from using a longer observation history, although this can actually exacerbate the problem of [Causal](Causal) confusion (see [Causal Confusion in Imitation Learning](Causal%20Confusion%20in%20Imitation%20Learning).
- If the expert policy is multi-modal: we can think carefully about how to parameterise our imitation policy, for example using a mixture distribution or autoregressive discretisation.

But ultimately, the fundamental approach of imitation learning is limited by the quality of the expert demonstrator and the availability of data. If humans can learn autonomously from their own experience, can machines do the same?

## Lecture 3: TensorFlow and Neural Nets Review Session
*Skipped*

## Lecture 4: Introduction to Reinforcement Learning
An MDP augments the definition of a [Markov Chain](Markov%20Chain) (state space $\mathcal{S}$, transition operator $\mathcal{T}:\mathcal{S}\times\mathcal{S}\rightarrow[0,1]$) with an action space $\mathcal{A}$ and reward function $r:\mathcal{S}\times\mathcal{A}\rightarrow\mathbb{R}$. A POMDP further  augments this with an observation space $\mathcal{O}$ and emission probabilities $p(o_t\in\mathcal{O}\vert s_t\in\mathcal{S})$. We use $\theta$ to denote the parameters of an MDP policy $\pi$. Given a policy, the joint distribution over state-action sequences $\tau$ of length $T$ can be decomposed via the Markov property: 

$$p_\theta(\tau)=p_\theta(s_1,a_1,...,s_T,a_T)=p(s_1)\prod_{t=1}^T\pi_\theta(a_t\vert s_t)p(s_{t+1}\vert s_t,a_t).$$

The objective of RL is to find a policy that maximises the expectation of the sum of reward (return) over trajectories:

$$\theta^\ast=\underset{\theta}{\text{argmax}}\ \mathbb{E}_{\tau\sim p_\theta(\tau)}\sum_{t=1}^Tr(s_t,a_t)=\underset{\theta}{\text{argmax}}\ J(\theta).$$

An important fact is that even if the reward function is discontinuous, this expectation can still be smooth and differentiable in $\theta$, because the policy itself is smooth and differentiable (for neural networks at least).

The generic cycle followed is (1) Generate samples by running a policy, (2) Fit a predictive model to those samples (i.e. dynamics or value model) (3) Improve the policy based on the model predictions. These three steps may be cheap or expensive depending on exactly how they are implemented.

The Bellman equation is a crucial decomposition of the return, used by many RL algorithms: 

$$J(\theta)=\mathbb{E}_{\tau\sim p_\theta(\tau)}\sum_{t=1}^Tr(s_t,a_t)=\mathbb{E}_{s_1\sim p_\theta(s_1)}[\mathbb{E}_{a_1\sim\pi(a_1\vert s_1)}[r(s_1,a_1)+\mathbb{E}_{s_2\sim p(s_2\vert s_1,a_1)}[...\vert s_1,a_1]\vert s_1]].$$

What if we *knew* the value inside the second expectation? Let us call this $Q^\pi(s_1,a_1)$. $$\mathbb{E}_{s_1\sim p_\theta(s_1)}[\mathbb{E}_{a_1\sim\pi(a_1\vert s_1)}[Q^\pi(s_1,a_1)\vert s_1]].$$ In this case, the decision about how to improve $\pi_\theta(a_1\vert s_1)$ (step 3 of the generic cycle) would be easy: simply move in the direction of increasing $Q$! Many RL algorithms involve the estimation of $Q$ functions from data, so that such updates can be performed approximately.

A whirlwind tour of RL algorithms:
- Policy gradient: *directly* differentiate the RL objective to learn a policy
- Value-based: estimate a $Q$ (or $V$) function and represent policies *implicitly* (e.g. as an $\text{argmax}$).
- Actor-critic: a *hybrid* in which a learned $Q$/$V$ function is used as part of the policy update step.
- Model-based: estimate the transition model and use it either for direct planning, policy improvement via backpropagation, generation of synthetic experience for a model-free learner, or something else (many variants).

None of these is universally best, and many tradeoffs exist: 
- Sample efficiency (off-policy algorithms are generally more efficient because they can reuse old data) and wall clock time (not the same thing!) 
- Stability and ease of use (understanding the convergence properties of many popular RL algorithms remains an open problem).
- Assumptions (stochastic vs deterministic environments, continuous vs discrete actions, finite vs infinite horizon, full vs partial observability).
- Particularities of the environment affecting the easy of policy, value and model representation.

## Lecture 5: Policy Gradients
In order to use gradient-based methods to maximise the RL objective $J(\theta)$, we need to know its derivative. For notational convenience, let us rewrite $J(\theta)=\mathbb{E}_{\tau\sim p_\theta(\tau)}\sum_{t=1}^T r(s_t,a_t)=\int p_\theta(\tau)r(\tau)d\tau$. We can now write the derivative as

$$\nabla_\theta J(\theta)=\int \nabla_\theta p_\theta(\tau)r(\tau)d\tau.$$

Next, we make use of a convenient identity: $p_{\theta}(\tau) \nabla_{\theta} \log p_{\theta}(\tau)=p_{\theta}(\tau) \frac{\nabla_{\theta} p_{\theta}(\tau)}{p_{\theta}(\tau)}=\nabla_\theta p_\theta(\tau)$. Applying this identity in reverse,

$$\nabla_\theta J(\theta)=\int p_{\theta}(\tau) \nabla_{\theta} \log p_{\theta}(\tau)r(\tau)d\tau=\mathbb{E}_{\tau\sim p_\theta(\tau)}\nabla_{\theta}\log p_{\theta}(\tau)r(\tau).$$

Returning to the definition of $p_{\theta}(\tau)$ and taking the logarithm:

$$\log p_\theta(\tau)=\log p(s_1)+\sum_{t=1}^T\log\pi_\theta(a_t\vert s_t)+\log p(s_{t+1}\vert s_t,a_t).$$

Now taking the derivative w.r.t. $\theta$, all of the $p$ terms disappear:$$\nabla_\theta\log p_\theta(\tau)=\sum_{t=1}^T\nabla_\theta\log\pi_\theta(a_t\vert s_t).$$We arrive at the following equation for the policy gradient:

$$\nabla_\theta J(\theta)=\mathbb{E}_{\tau\sim p_\theta(\tau)}\left(\sum_{t=1}^T\nabla_\theta\log\pi_\theta(a_t\vert s_t)\right)\left(\sum_{t=1}^Tr(s_{t},a_{t})\right).$$

All of these terms we can either query directly, or estimate from experience. A useful intuition for the policy gradient objective is as a *weighted maximum likelihood*; we want to make good trajectories (high $r(\tau)$) more likely, and bad trajectories less likely.
- If we follow this derivation for partially-observable environments, we end up with exactly the same result! Vanilla policy gradient can therefore be used in POMDPs without modification.

The `REINFORCE` algorithm performs a basic gradient descent update on the policy gradient: $\theta\leftarrow\theta+\alpha\nabla_\theta J(\theta)$. It is not used very often in practice, because of the high variance of empirical estimates of the gradient.

One "free lunch" way of reducing variance is to introduce the simple causal fact that behaviour at time $t$ cannot affect reward at time $t'<t$, so any apparent relationship will cancel out in expectation. 

$$\nabla_\theta J(\theta)=\mathbb{E}_{\tau\sim p_\theta(\tau)}\sum_{t=1}^T\nabla_\theta\log\pi_\theta(a_t\vert s_t)\left(\sum_{t'=t}^Tr(s_{t'},a_{t'})\right)$$

By removing terms from the sum we reduce variance, because there are fewer places to go wrong! The quantity in the reduced inner sum is sometimes called the *reward-to-go*, and is given the symbol $\hat{Q}$.

Another form of variance comes from the lack of invariance to reward translation: if all rewards are increased or decreased by a constant, the empirical policy gradient can change, even though such translation has no effect on the optimal policy or the direction of the gradient in expectation. A common way of resolving the translation problem is to use a *baseline*, which subtracts a carefully-chosen constant $b$ from $r(\tau)$ so as to reduce the empirical variance. Now consider the definition of the variance:

$$\text{Var}[J(\theta)]=\mathbb{E}_{\tau\sim p_\theta(\tau)}[(\nabla_{\theta}\log p_{\theta}(\tau)(r(\tau)-b))^2]-\mathbb{E}_{\tau\sim p_\theta(\tau)}[\nabla_{\theta}\log p_{\theta}(\tau)(r(\tau)-b))]^2.$$

We can ignore the second term, which will be the same for any $b$, since we know that baselines are unbiased in expectation. By taking the derivative and setting it to zero, we find that the optimal variance-minimising baseline is


$$b=\frac{\mathbb{E}_{\tau\sim p_\theta(\tau)}[(\nabla_\theta\log p_\theta(\tau))^2r(\tau)]}{\mathbb{E}_{\tau\sim p_\theta(\tau)}(\nabla_\theta\log p_\theta(\tau))^2}$$

The optimal baseline is actually a vector with a different component for every parameter in $\theta$, so is a little unweildy to use. 
- In practice, it is far more common to estimate the state value function $V^\pi(s)$ and use this as a baseline. In this case, the baseline-translated reward-to-go is called the *advantage* $A^\pi(s,a)$.

The other major problem with vanilla policy gradient is that it is strictly *on-policy*. We must throw away all of our old samples whenever the policy is changed! This can be very inefficient. If we want to use off-policy samples (i.e. from parameters $\theta'\neq \theta$), we can use a technique called *importance sampling*. This adds a reweighting term to the objective:

$$\nabla_\theta J(\theta)=\mathbb{E}_{\tau \sim p_{\theta}(\tau)}\left[\left(\prod_{t=1}^{T} \frac{\pi_{\theta}\left(a_{t}\vert s_{t}\right)}{\pi_{\theta'}\left(a_{t}\vert s_{t}\right)}\right)\left(\sum_{t=1}^{T} \nabla_{\theta} \log \pi_{\theta}\left(a_{t}\vert s_{t}\right)\right)\left(\sum_{t=1}^{T} r\left(s_{t}, a_{t}\right)\right)\right]$$

The variance of the importance sampling term increases exponentially with $T$. There are several practical first-order approximations that don't give the correct policy gradient, but might still be reasonable if $\theta\approx\theta'$ (more on these later).

## Lecture 6: Actor-Critic Algorithms
Actor-critic algorithms augment the policy gradient approach with value functions.

In vanilla policy gradient algorithms, the reward-to-go $\hat{Q}(s_t,a_t)$ serves as an estimate of the expected sum of future reward if we taken action $a$ in state $s$. These algorithms use a single sample in place of this expectation, which can have very high variance if the policy and dynamics have significant stochasticity. We can reduce variance, at the cost of some bias, by learning a function to approximate the expectation $Q^\pi$.
- The key idea of function approximation is generalisation: information "leaks out" to affect predictions for nearby states, hopefully yielding better estimates than if no leakage

Recall the common use of the state value function $V^\pi(s_t)$ as a baseline, which yields the advantage function $A_\pi(s_t,a_t)$. Is it better to learn $V^\pi$, $A^\pi$ or $Q^\pi$ for this implementation? Consider their relationship:

$$A^\pi(s_t,a_t)=Q^\pi(s_t,a_t)-V^\pi(s_t)=\mathbb{E}_{s_{t+1},r_t}[r(s_t,a_t)+V^\pi(s_{t+1})]-V^\pi(s_t)$$
For a particular sample, we can make an approximation and use the *actual* reward and next state in place of the expectation:

$$A^\pi(s_t,a_t)\approx r(s_t,a_t)+V^\pi(s_{t+1})-V^\pi(s_t)$$

This is written entirely in terms of $V^\pi$, so let's just learn this! (Alternatives considered later.)

The most basic way of learning $V^\pi$ is using training data of the form $\{(s_t,\sum_{t'=t}^Tr(s_{t'},a_{t'})\}$ (i.e. Monte Carlo samples). By defining the loss as (for example) the mean squared error, we have a standard regression problem. 

There's still a lot of variance in this approach, specifically in the training data itself. We can eliminate even more variance using a technique known as *bootstrapping*, in which $V^\pi$ is trained iteratively, using its own predictions for $s_{t+1}$ to construct labels. Training data at iteration $k$ now have the form $\{(s_t,r(s_t,a_t)+V^\pi_{\phi_{k-1}}(s_{t+1})\}$, where $\phi_{k-1}$ are the parameters of $V^\pi$ at iteration $k-1$. Although the labels will initially be very biased, the hope is that the process will converge to good estimates.
- In infinite-horizon problems, it becomes important to introduce a discount factor $\gamma$ at this point to prevent bootstrapped value estimates from continually increasing. Training data then have the form $\{(s_t,r(s_t,a_t)+\gamma V^\pi_{\phi_{k-1}}(s_{t+1})\}$.
	- One way of thinking about discounting is as modifying the MDP to introduce the concept of [Mortality](Mortality) via an absorbing zero-reward "death" state that is transitioned to from every state with probability $1-\gamma$.

For practical implementation of actor-critic algorithms, we face the problem that training data collected online will be highly-correlated. A common approach is to have multiple *workers* that deploy the current policy in parallel to collect partially-decorrelated data for central retraining. This may be done synchronously (update all workers at the same time) or asynchronously (update at different times, which can be made more efficient but slightly violates the on-policy assumption). The use of asychronous workers is the central feature of the [A3C](A3C) algorithm. 

Note that $V^\pi$ can be used in *two ways* to assist in policy learning (note $\gamma$ now included):
- As a baseline to subtract from the Monte Carlo return:
	- Note that this has *zero* bias, because it is a constant with respect to the parameters $\theta$.

$$\nabla_\theta J(\theta)=\mathbb{E}_{\tau\sim p_\theta(\tau)}\sum_{t=1}^T\nabla_\theta\log\pi_\theta(a_t\vert s_t)\left(\left(\sum_{t'=t}^T\gamma^{t'-t}r(s_{t'},a_{t'})\right)-V^\pi(s_t)\right)$$

- To replace the baselined return with a [TD error](TD%20error) (lower variance than above but additional bias):

$$\nabla_\theta J(\theta)=\mathbb{E}_{\tau\sim p_\theta(\tau)}\sum_{t=1}^T\nabla_\theta\log\pi_\theta(a_t\vert s_t)\left(r(s_t,a_t)+\gamma V^\pi(s_{t+1})-V^\pi(s_t)\right)$$

We can generalise these two approaches to use $n$-step Monte Carlo returns before switching to $V^\pi$ , giving us the ability to control the tradeoff between variance (first term) and bias (second term):

$$\nabla_\theta J(\theta)=\mathbb{E}_{\tau\sim p_\theta(\tau)}\sum_{t=1}^T\nabla_\theta\log\pi_\theta(a_t\vert s_t)\left(\left(\sum_{t'=t}^{t+n}\gamma^{t'-t}r(s_{t'},a_{t'})\right)+\gamma^nV^\pi(s_{t+n})-V^\pi(s_t)\right)$$

And we can generalise even further to take a weighted average over all possible $n$. If we take the weights $w_n\propto\gamma^{n-1}$ where $\gamma<1$ (i.e. exponential falloff), it is possible to write this weighted average as

$$\nabla_\theta J(\theta)=\mathbb{E}_{\tau\sim p_\theta(\tau)}\sum_{t=1}^T\nabla_\theta\log\pi_\theta(a_t\vert s_t)\left(\sum_{t'=t}^{T}(\gamma\lambda)^{t'-t}\left(r(s_{t'},a_{t'})+\gamma V^\pi(s_{t'+1})-V^\pi(s_{t'})\right)\right)$$

This approach is called *generalised advantage estimation* (GAE).

## Lecture 7: Value Function Methods
We start our journey here by noticing that by definition, the $\text{argmax}$ of the true advantage $A^\pi(s_t,a_t)$ is *at least as good* as sampling from the current policy $\pi$, regardless of what $\pi$ actually is. This means that as long as we have a good estimate of the advantage, we should be able to iteratively improve our policy by taking the $\text{argmax}$ in this way. As a result, we never actually need to represent a policy explicitly, and can omit direct learning via the policy gradient. This general approach is called *policy iteration*. 

What form of the value function should we learn to perform policy iteration? Consider the two options for learning from transition samples $(s,a,r,s')$:

$$V^\pi(s)\leftarrow r+\gamma\mathbb{E}_{s'\sim p(s'\vert s,\pi(s))}[V^\pi(s)]$$

$$Q^\pi(s,a)\leftarrow r+\gamma\mathbb{E}_{s'\sim p(s'\vert s,a)}[Q^\pi(s',\pi(s'))]$$

Notice how to learn the state value function $V^\pi$, we need to sample from the transition dynamics given the policy $p(s'\vert s,\pi(s))$. This requires a *model of the environment*. Crucially, however, for $Q^\pi$, we can just use the *actual* action $a$ and next state $s'$ from the collected sample, so no such model is required. So let's use $Q^\pi$!

If for the $\pi(s')$ sample we deterministically take the $\text{argmax}$ of the current $Q^\pi(s',a')$ estimate, policy iteration reduces to *value iteration*. In the deep RL context, it tends to be referred to as *fitted Q-iteration* (FQI). Letting $\phi$ be the parameters of our learned $Q$ function, the FQI update given a batch of $n$ samples $(s_i,a_i,s'_i)$ is

$$\phi\leftarrow \phi-\alpha\sum_{i=1}^n\frac{\partial}{\partial\phi}(Q_\phi(s_i,a_i)-[r(s_i,a_i)+\gamma\max_{a'}Q_\phi(s'_i,a')])$$

- Two parameters of FQI are how many value function updates to complete before collecting more data with the updated ($\text{argmax}$) policy, and how many samples $n$ to collect each time. If both of these parameters $=1$, we have a fully online algorithm.
- At a theoretical level FQI allows us to get away with using *off-policy* data, because the only part of the update that depends on $\pi$ is the sampling of $a'$, which is done at learning time. 
	- However, in practice we do still require the data to cover the state and action spaces relatively thoroughly (*broad support*), otherwise we may fail to discover better actions to take or have large errors in unvisited states. This motivates the introduction of randomness into the data-collecting policy, with simple approaches being $\varepsilon$-greedy and a softmax function over $Q$ values (Boltzmann exploration).
		- Much more on exploration later...

The lecture then goes on to discuss [Convergence of Value-based RL](Convergence%20of%20Value-based%20RL).

## Lecture 8: Deep RL with $Q$-functions
Practical deep RL algorithms that use value functions have to tackle two problems that hamper the stability of $Q$-learning:
- **Online samples are strongly correlated**: This violates the i.i.d. assumption of gradient-based optimisation, and gives the network time to *locally overfit* to the most recent data. We could parallelise data collection as in actor-critic, but more common is to use a *replay buffer* from which we sample batches i.i.d. Any data collection policy will work as long as it has broad support, but it's a good idea to gradually refresh the buffer with data from a policy close to the one being learned.
- **$Q$ learning is only semi-gradient descent**: We don't compute the gradient through the target value $[r(s_i,a_i)+\gamma\max_{a'}Q_{\phi}(s_i',a')]$, which effectively "changes out from under us". Depending on the number of gradient steps we take on each update, we either don't converge at all; or converge to the wrong targets. The solution is a compromise, achieved by maintaining a second *target $Q$ network* with parameters $\phi'$ that are infrequently updated to match $\phi$. By using the target network to create $\max_{a'}Q_{\phi'}(s',a')$ for regression, we achieve much more stable learning.
	- More recently it has been popular to update $\phi'$ in a lagging way using Polyak averaging in parameter space. While in general neural networks to be highly nonlinear in their parameters, there is some partial theoretical justification for this being a reasonable thing to do, as long as $\phi$ and $\phi'$ remain reasonably close.

These additions (plus the decision to update $\phi$ on every timestep with a single sampled batch) lead us to the classic deep $Q$ learning algorithm `DQN`. We can also present $Q$ online learning as a special case with a replay buffer of size $1$, and zero lag in the target parameters $\phi'$.
- In general, a whole family of $Q$ learning algorithms is defined by varying the rates of three processes: (1) buffer refreshing, (2) $Q$ function regression, (3) target parameter update.

An interesting thing to note is that while the ordering of learned $Q$ values across the action space tends to converge to the true ordering in successful learning, **the absolute values are often systematically way too high**! This problem, known as *overestimation in $Q$ learning*, is actually pretty easy to get our heads around:
- For any two random variables $X_1,X_2$, we have that $\mathbb{E}[\max(X_1,X_2)]\geq\max[\mathbb{E}[X_1],\mathbb{E}[X_2]]$ because the former systematically selects for positive deviations from the average. This generalises to any number of variables. 
- Therefore, $\mathbb{E}\max_{a'}Q_{\phi'}(s',a')=\mathbb{E}Q_{\phi'}(s',\text{argmax}_{a'}Q_{\phi'}(s',a'))\geq\max_{a'}\mathbb{E}Q_{\phi'}(s',a')$.

The solution is to *partially decorrelate* the selection of $a'$ from the evaluation of its value. We could do this by using two pairs of value and target networks with parameters $\phi_A,\phi'_A,\phi_B,\phi'_B$, but in practice the common approach is even simpler: just use $\phi$ to select $a'$! The update becomes

$$\phi\leftarrow \phi-\alpha\sum_{i=1}^n\frac{\partial}{\partial\phi}(Q_{\phi}(s_i,a_i)-[r(s_i,a_i)+\gamma\max_{a'}Q_{\phi'}(s'_i,\text{argmax}_{a'}Q_{\phi}(s',a'))])$$

This practically-trivial modification yields the `Double DQN` algorithm, which does a pretty good, if incomplete, job of mitigating the overestimation problem.

As in actor-critic, another trick that can be used to improve $Q$ learning algorithms is to use $n$-step returns in the target values. This allows us to control the bias-variance tradeoff. Using $n$-step returns is **only strictly valid in the on-policy setting** because multi-step returns are policy-dependent. Common responses are:
- Ignore the problem;
- Dynamically choose $n$ to only include returns where actions match the greedy ones;
- Importance sampling.

Can we extend $Q$-learning to continuous actions? The difficulty comes when trying to find the $\text{max}_{a'}$ over $Q(s',a')$. A very simple approach is to approximate this with the max over a finite set of randomly-sampled actions. Fancier approaches include:
- Cross-entropy sampling (CEM; more on this when discussing model-based methods).
- Constraining the functional form of the $Q$ function to make analytical maximisation possible (e.g. quadratic in $a$).
- Learning an approximate maximiser. Although commonly presented as an actor-critic algorithm, this is actually exactly what `DDPG` does!

$Q$-learning is often harder to stabilise than policy gradient methods. Some practical tips:
- Large replay buffers help.
- Expect a long time spent doing no better than random early in learning.
- Start with high exploration and gradually reduce.
- Bellman error gradients can be large; clipping gradients or using the Huber loss can help.
- Double Q-learning helps a lot in practice. It's super easy to implement and has almost no downsides.
- $n$-step returns can also help early in training, but does have a downside as it biases the objective.
- Scheduled learning rates and optimisers such as `Adam` can help.
- Run multiple random seeds; learning can be very inconsistent.

## Lecture 9: Advanced Policy Gradients
We can reinterpret policy gradient methods as doing something quite similar to policy iteration - alternating between advantage evaluation and policy update - but performing a much *gentler* update than jumping to the $\text{argmax}$. This might be desirable when we are uncertain about the accuracy of our advantage estimate.

This lecture we dig a little deeper: when and why do policy gradient methods work? First, let us restate the fundamental RL objective (now including the discount factor $\gamma$):

$$J(\theta)=\mathbb{E}_{\tau\sim p_\theta(\tau)}\sum_t\gamma^tr(s_t,a_t)=\mathbb{E}_{s_0\sim p(s_0)}V^{\pi_\theta}(s_0).$$

By definition, policy improvement means maximising $J(\theta')-J(\theta)$. We can show that this difference is exactly the expectation of the advantage function for $\theta$, under the trajectory distribution for $\theta'$:

$$J(\theta')-J(\theta)=\mathbb{E}_{\tau\sim p_{\theta'}(\tau)}\sum_t\gamma^tA^{\pi_\theta}(s_t,a_t).$$

To do this requires a few tricks. First, we notice that we can freely change the expectation distribution, because initial state probabilities are policy-independent. Next, we add and subtract values for all other $t\geq 0$, which has no effect on the result because everything cancels out:

$$J(\theta')-\mathbb{E}_{s_0\sim p(s_0)}V^{\pi_\theta}(s_0)=J(\theta')-\mathbb{E}_{\tau\sim p_{\theta'}(\tau)}V^{\pi_\theta}(s_0)=J(\theta')-\mathbb{E}_{\tau\sim p_{\theta'}(\tau)}\left[\sum_{t=0}^\infty\gamma^tV^{\pi_\theta}(s_t)-\sum_{t=1}^\infty\gamma^tV^{\pi_\theta}(s_t)\right].$$

Now, we refactor the terms in the two infinite sums:

$$J(\theta')-\mathbb{E}_{\tau\sim p_{\theta'}(\tau)}V^{\pi_\theta}(s_0)=J(\theta')+\mathbb{E}_{\tau\sim p_{\theta'}(\tau)}\left[\sum_{t=0}^\infty\gamma^t(\gamma V^{\pi_\theta}(s_{t+1})-V^{\pi_\theta}(s_{t}))\right].$$

Finally, we substitute in the definition of $J(\theta')$ and regroup again:

$$\mathbb{E}_{\tau\sim p_{\theta'}(\tau)}\sum_{t=0}^\infty\gamma^tr(s_t,a_t)+\mathbb{E}_{\tau\sim p_{\theta'}(\tau)}\left[\sum_{t=0}^\infty\gamma^t(\gamma V^{\pi_\theta}(s_{t+1})-V^{\pi_\theta}(s_{t}))\right]=\mathbb{E}_{\tau\sim p_{\theta'}(\tau)}\left[\sum_{t=0}^\infty\gamma^t(r(s_t,a_t)+\gamma V^{\pi_\theta}(s_{t+1})-V^{\pi_\theta}(s_{t}))\right].$$

The stuff inside the brackets is exactly the definition of the advantage function! 

But hold up... in policy gradient methods the expectation is taken under the trajectory distribution for the *old* parameters $\theta$. Practical algorithms rely on the fact that we can assume this distribution mismatch is small, because $p_\theta$ is close to $p_{\theta'}$ when $\pi_\theta$ is close to $p_{\theta'}$. 
- How can we show this is true? For the simple case when $\pi_\theta$ is deterministic (but $\pi_{\theta'}$ may not be), an identical analysis to that for [../../../Roam/Covariate Shift](../../../Roam/Covariate%20Shift) in behavioural cloning allows us to show that $p_{\theta'}(s_t)-p_\theta(s_t)\leq2\epsilon t$, where $\epsilon$ is the maximum probability that $\pi_{\theta'}$ takes a different action to $\pi_\theta$ in any state. For the general case, let $\pi_{\theta'}$ be *close* to $\pi_\theta$ if $\vert\pi_{\theta'}(a_t\vert s_t)-\pi_{\theta}(a_t\vert s_t)\vert\leq\epsilon\ \forall s_t$, where $\vert\cdot\vert$ denotes the total variation divergence. In this case, a bit of careful though reveals that the probability of a "mistake" is still just $\epsilon$, so again, $p_{\theta'}(s_t)-p_\theta(s_t)\leq2\epsilon t$.

This theoretical analysis demonstrates the importance of ensuring that $\vert\pi_{\theta'}(a_t\vert s_t)-\pi_{\theta}(a_t\vert s_t)\vert\leq\epsilon$. If we can do that for small enough $\epsilon$, the policy gradient update is guaranteed to give us a positive $J(\theta')-J(\theta)$. The total variation divergence is a little unweildy to work with (partly because the absolute value operator is non-differentiable), but it turns out that it is upper bounded by the KL divergence $D_\text{KL}(\pi_{\theta'}\vert\vert\pi_\theta)$, so we can use that instead. 

There are several ways of enforcing a KL divergence constraint during policy learning, but one of the most popular is to take the second-order Taylor expansion $D_\text{KL}(\pi_{\theta'}\vert\vert\pi_\theta)\approx\frac{1}{2}(\theta'-\theta)\textbf{F}(\theta'-\theta)$, where $\textbf{F}$ is the Fisher information matrix. Since vanilla gradient descent already effectively regularises under the L2 norm, this approximate constraint can be enforced by a simple reweighting, yielding the *natural gradient*:

$$\theta'=\theta+\alpha\textbf{F}^{-1}\nabla_\theta J(\theta),$$

with $\alpha=\sqrt{\frac{2\epsilon}{\nabla_\theta J(\theta)^T\textbf{F}\nabla_\theta J(\theta)}}$. The effect of $\textbf{F}$ is to apply a linear transformation to the gradient vector according to the influence of each parameter on the policy. $\textbf{F}$ can be found approximately using samples, allowing this method to be usable in practical algorithms such as `TRPO`.

## Lecture 10: Model-based Planning
In this lecture we switch gears to talk about how *known* models of the environmental dynamics $p(s_{t+1}\vert s_t,a_t)$ can be used for optimal control and planning. Typically, solutions to this problem do not explicitly talk about policy functions, but just about action sequences $a_1,...,a_T$ over some time horizon $T$. For the case of deterministic transition dynamics $f$, the objective can be written as 

$$\underset{a_1,...,a_T}{\text{argmax}}\sum_{t=1}^T\Big(r(s_t,a_t)\ \text{s.t.}\ s_{t+1}=f(s_t,a_t)\Big),$$

and can be generalised to stochastic dynamics as follows:

$$\underset{a_1,...,a_T}{\text{argmax}}\ \mathbb{E}\left[\Big(\sum_{t=1}^Tr(s_t,a_t)\Big)\Big\vert a_1,...,a_T\right].$$

*Open-loop* planning algorithms attempt to tackle the objective all in one go, solving for a sequence of actions $a_1,...,a_T$ which is then executed in full:
- **Random shooting**: Sample many action sequences from some distribution (e.g. Gaussian) and evaluate the return for each. Actually works pretty well for low-dimensional systems and can easily be parallelised (good for deep learning systems).
- **Cross-entropy method (CEM)**: Start with random shooting, then iteratively update the sampling distribution toward those samples that give higher return. A common approach here is to refit the distribution to the top-performning $x\%$ of the samples, which are called the *elites*.
	- Check out [CMA-ES](CMA-ES) as an extension of CEM that uses momentum and keeps track of inter-timestep covariances.
- **Derivative-based methods**: Rather than sampling, attempt to obtain an analytical solution by differentiating known dynamics equations. 
	- This often faces stability challenges as derivatives with respect to earlier actions are likely to be much higher than later ones. We call such an optimisation problem *poorly conditioned*.
	- A special case that does not suffer from this issue is the **Linear-quadratic regulator (LQR)**, devised for linear deterministic transition functions and quadratic reward functions (common in robotics). The equations can be solved by some fairly verbose, but not too complicated, linear algebra. The general idea is to iterate backward from the planning horizon to obtain a full expression for the policy in matrix form, then iterate forward from the current timetep, plugging states into these matrices and recovering the optimal actions. 
		- Note that if LQR is being used in an MPC control scheme (below), we only need to run forward one timestep, though the speed gain from this is negligible.
		- The LQR can be extended to stochastic dynamics under certain assumptions. For example, if noise is Gaussian, it provably cancels out during the backward iteration step, which therefore remains unchanged. The only difference is that we keep the entire policy structure and look up based on the actual state encountered at each timestep.
		- It can also be extended for nonlinear dynamics, in which case it is known as *differential dynamic programming* (DDP) or iterative LQR (iLQR). This involves taking a second-order Taylor expansion around a given state and action, approximating the system as locally linear/quadratic, finding the optimal solution, and iteratively repeating until convergence.

However, in the stochastic case, choosing a whole sequence of actions in an open-loop manner is very bad idea, because it is likely that information will be revealed to us in future that reduces our uncertainty about future states. *Closed-loop* planning algorithms attempt only to return the single next action $a_1$, and are re-run on every timestep:
- **Model-predictive control (MPC)**: A generic name for a broad family of algorithms that use some open-loop planning method (e.g. LQR), but then discard all but the first action $a_1$. 
- **Monte Carlo tree search (MCTS)**: At each depth, simulate a baseline policy from each leaf and evaluate return. Many algorithms exist for deciding whether or not to expand a node further on the basis of average return and number of evaluations (as a measure of uncertainty). Note that the stochastic nature of MCTS makes it very difficult to analyse theoretically, and the algorithm offers few theoretical guarantees, but it often works very well in practice. 

## Lecture 11: Model-based Reinforcement Learning
Now we consider the case where a dynamics model is not known, and we instead want to construct it from data using supervised learning. When attempting to deploy the most obvious naive approach to model learning, using a dataset collected from an exploration policy $\pi_0$ and using the result to construct a policy $\pi_f$, we immediately re-encounter the problem of distributional shift: $p_{\pi_f}(s_t)\neq p_{\pi_0}(s_t)$. `DAgger`-like approaches again tend to be successful in mitigating this problem.

We should always expect some error in a learned dynamics model, so while more expensive, closed-loop control methods such as MPC tend to be far more robust. In general, the more often we re-plan, the less perfect each individual plan needs to be, so even random sampling can work well.

Overfitting is a major problem with learned models, because any spurious peaks and troughs are likely to be mercilessly exploited by a planning algorthm. This motivates introducing some form of *uncertainty estimation*, which in turn allows us to plan actions that have high value in expectation or within some lower confidence bound. How can we build uncertainty-aware neural network models?
- Bad idea: Use output entropy (e.g. if model parameterisation is a softmax distribution over discrete states or a Gaussian over continuous ones). This is problematic because the entropy is itself subject to estimation error, and can also be exploited by a planner! The output entropy is the *wrong kind of uncertainty*: [aleatoric instead of epistemic](../../../Aleatoric%20and%20Epistemic%20Uncertainty), which is actually what we care about here.
- What we really want is to represent a distribution over model parameters, which is the realm of [../../../Roam/Bayesian](../../../Roam/Bayesian) learning. Using a [Bayesian neural network](Bayesian%20neural%20network) is the principled way of doing this, but far simpler (and seemingly more effective for model-based RL!) is to train an ensemble of models on independently-sampled subsets of the training set and combining their outputs.
	- In fact, the combination of random network initialisation and minibatch sampling in SGD are often enough to yield sufficiently diverse models, so we can even train them on exactly the same data!
	- In formal terms, the ensemble method approximates the model parameter distribution as a mixture of Dirac deltas centred on the particular weights in each trained network.
		- Crucially, when combining the outputs of an ensemble of (e.g.) Gaussian models, we should not just take the mean prediction across all models, but treat the overall model as a mixture of Gaussians.

Given a model that is aware of epistemic uncertainty (whether Bayesian network or ensemble), the general approach to planning is to first sample a set of parameters $\theta$ (for ensembles this amounts to picking one at random), run the planning algorithm, repeat $N$ times, and accumulate the average return for each candidate action sequence.

How can we learn models in environments with image observations? This is a hard problem because images have high dimensionality, lots of redundancy, and are almost always only partial observations of the true environmental state. A common approach is to attempt to separately learn an emission model $p(o_t\vert s_t)$ and a latent state space model $p(s_{t+1}\vert s_t,a_t)$. Let $\phi$ denote the conjunction of parameters from both of these models. In standard (fully-observed) model learning, the objective is 

$$\underset{\phi}{\max}\frac{1}{N}\sum_{i=1}^N\sum_{t=1}^T\log p_\phi(s_{i,t+1}\vert s_{i,t},a_{i,t}),$$

but in latent space model learning, we have an additional expectation:

$$\underset{\phi}{\max}\frac{1}{N}\sum_{i=1}^N\sum_{t=1}^T\mathbb{E}_{s,s'\sim p(s,s'\vert o_{i,1:T},a_{i,1:T})}\Big[\log p_\phi(s'\vert s,a_{i,t})+\log p_\phi(o_{i,t}\vert s)\Big].$$

Many options exist for learning $p(s,s'\vert o_{i,1:T},a_{i,1:T})$, which is often referred to as the *encoding* distribution. Solutions range from conditioning only on the current observation $o_{i,t}$ (single-step encoder; simplest but least accurate) to conditioning on the entire state-action sequence (required when observations are heavily partial).

- Considering the doubly-simple case of a deterministic single-step encoder $s_{i,t}=g_\psi(o_{i,t})$, the objective equation reduces to a fully-differentiable form that can be trained with backpropagation.

	$$\underset{\phi,\psi}{\max}\frac{1}{N}\sum_{i=1}^N\sum_{t=1}^T\log p_\phi(g_\psi(o_{i,t+1})\vert g_\psi(o_{i,t}),a_{i,t})+\log p_\phi(o_{i,t}\vert g_\psi(o_{i,t})).$$
	
An alternative to latent space models, which has become a little more popular recently is to learn the dynamics directly in image space. This requires more data and bigger models, but less principled forethought about their structure (i.e. the classic deep learning tradeoff).

## Lecture 12: Model-based Policy Learning
The MPC approach to closing the control loop is suboptimal, because we don't directly factor the possibility of obtaining more information in the future. The action we actually execute, $a_1$, is chosen contingent on us having the same information for the rest of the trejactory. Instead of using a model to directly choose actions, can we use it to construct a *policy*, which is more versatile?

In principle, if we have a differentiable dynamics model (and continuous actions) we can backpropagate through it to learn a policy by gradient descent. Unfortunately, this approach faces a similar challenge to gradient-based open-loop planning methods, namely a massive variation in gradient magnitudes between earlier and later actions (poor conditioning). It therefore tends to perform poorly.

What's the solution?
- Use model-free RL algorithms, with the model used to generate synthetic samples, essentially performing a data augmentation role. This seems weirdly backwards but actually works very well.
	- Interestingly, the quantity we are trying to optimise in the unstable differentiable-dynamics case is also just the policy gradient, but the method has much higher variance than `REINFORCE`.
	- If we use Q-learning as the model-free algorithm here, we obtain some variant on the `Dyna` approach. For every real timestep in the environment, we generate $K$ synthetic transitions from states sampled from a replay buffer, and update on those as well. We optionally continue to rollout each synthetic trajectory for $N$ steps.
		- The actions used in the synthetic transitions could also be sampled from the buffer, chosen by the current policy, or selected at random. There are advantages to each of these.
- Taking inspiration from LQR, learn a local linear dynamics model for each timestep, which decouples the timesteps and allows us to use second-order methods for policy learning (policy will also be linear). We often then want to add a little noise to the actions to improve exploration for learning the model itself. 
	- The linear approximation is clearly only valid if the dynamics do not change too drastically as a result of updates. As in Lecture 9, we can ensure this by imposing a KL divergence constraint on the policy. 
	- The *guided policy search* algorithm results from learning a separate linear policy for a variety of initial states, using samples generated from these policies to *distill* a global neural network policy, and iterating. A KL divergence constraint is added to each local policy, to keep it close to the global one.
		- As an aside, the general approach of distillation (using an ensemble of models to train a single one) is gaining traction in RL, for example for multi-task transfer. 

## Lecture 13: Exploration (Part 1)
Humans do not find the Atari game Montezuma's revenge particularly challenging, because we understand the semantics of the on-screen sprites so can make up-front inferences about which action sequences are promising. Unequipped with such semantics, RL agents reliably struggle because of the necessity of a very lucky sequence of exploratory actions in order to obtain the first reward. 

Deriving good strategies for exploration is hard, and there's a spectrum of theoretical tractability from $k$-armed bandits to large infinite MDPs. In the latter we have very few theoretical guarantees, but can take inspiration from strategies developed in the former.

In the $k$-armed bandit setting, we assume the reward of action $i$, $r(a_i)$, is sampled from a parameterised distribution $p_{\theta_i}(r_i)$. The goodness of an exploration strategy upto time $T$ can be measured in terms of *regret*: the difference in summed reward obtained versus having selected the optimal action $a^*$ throughout:

$$\text{reg}_T=T\mathbb{E}[r(a^*)]-\sum_{t=0}^T r(a_t)$$

The exploration problem can be cast as a POMDP, where the state is the true parameter vector $[\theta_1,...,\theta_k]$ (always transitions back to itself) and the belief state is $\hat{p}(\theta_1,...,\theta_k)$. Solving the POMDP yields the optimal exploration strategy, but this is often overkill and we can do very well with much simpler strategies, such as:
- **Optimistic exploration**: Keep track of the mean $\mu_a$ and variability (not necessarily standard deviation!) $\sigma_a$ of reward  for each action $a$, and pick $a_t=\text{argmax}_a\mu_a+C\sigma_a$ at all times $t$. $C$ is a parameter governing the degree of optimism. A commonly-used option (for rewards in $\{0,1\}$?) is UCB, in which $C=1$ and $\sigma_a=\sqrt{\frac{2\ln t}{N(a)}}$, where $N(a)$ is the number of times that $a$ has been tried. Regret here is $O(\log T)$, which is provably as good as any other strategy.
- **Probability matching/posterior sampling/[Thompson sampling](Thompson%20sampling)**: Explicitly maintain a belief state $\hat{p}(\theta_1,...,\theta_k)$. At each $t$, sample a parameter vector from the belief state, pretend that these parameters are the true ones, and take the optimal action. This is harder to analyse theoretically but can work very well empirically.
- **Bayesian experimental design**: The general approach of choosing actions that will maximise the expected information gain (reduction in entropy) of our estimate of some variable $z$, where $z$ might be the identity of the optimal action, or its expected reward. Many different variants have been proposed.

These ideas can all be extended to MDPs, in the hope that (despite the lack of guarantees) they work similarly well in practice:
- **Optimistic exploration**: Define $r^+(s,a)=r(s,a)+\mathcal{B}(N(s,a))$ (or $N(s)$), where $\mathcal{B}$ is some monotonically decreasing *bonus* function, and use $r^+(s,a)$ instead of $r(s,a)$ during learning. The bonus function must be carefully tuned to prevent learning instability caused by nonstationary reward. 
	- The notion of a *count* for a state or state-action pair doesn't scale to infinite MDPs, so instead we need to fit a density model to the historic visitation distribution. Lots of interesting options have been proposed for density model implementations (which often look quite different to density models in other contexts because they don't need to produce samples). See the slides for the equation used to convert from density to a "psuedo-count" for each state in an infinite MDP.
- **Thompson sampling**: The MDP analogue of the belief state over rewards is a $Q$ function with uncertainty estimation, or often in practice, an ensemble of networks. By sampling a $Q$ network from the ensemble to use for an entire episode, we obtain a randomised but internally-consistent form of exploration that differs in kind from action noise and is better at discovering temporally-extended deviations from the historic distribution of the kind needed in Montezuma's revenge. While this is nice in that it requires no change to the reward structure and automatically manages the exploration-exploitation tradeoff as the ensemble becomes less diverse over time, it often isn't quite as effective as optimistic exploration with reward bonuses.
- **Bayesian experimental design**: Here we need to choose the variable $z$ whose information gain we want to maximise. A good, if heuristic, proxy is the parameters $\theta$ of a dynamics function  $p_\theta(s'\vert s,a)$. Regardless of what is being estimated, information gain is generally intractable, but it can be approximated by the *change* in the posterior distribution over $z$ after a new observation is made. For a dynamics function, we can measure this using the KL divergence $D_\text{KL}(p(\theta\vert h,s_t,a_t,s_{t+1})\vert\vert p(\theta\vert h))$, where $h$ is the history of observations made to date. A probabilistic estimate of $\theta$ is obtained by implementing the dynamics function as a [Bayesian neural network](Bayesian%20neural%20network).

## Lecture 14: Exploration (Part 2)
What if we want to recover diverse behaviour **without any reward function at all**? This may be useful to allow us to learn a bank of skills without supervision, that can be assembled to accomplish unknown future tasks. 

There is no canonical formulation of this problem, but concepts from information theory are prevalent in this space. In particular, we make use of a measure of dependency called mutual information $I(x;y)=D_\text{KL}(p(x,y)\vert\vert p(x)p(y))$, which increases as a joint distribution becomes more different from the product of marginals. It can also be written as $H(p(y))-H(p(y\vert x))$: the reduction in the entropy of $y$ achieved after observing $x$.

One application of mutual information is to construct a quantity called *empowerment*, $I(s_{t+1};a_t)=H(s_{t+1})-H(s_{t+1}\vert a_t)$, which measures the amount of "control authority" that the agent has. When empowerment is large, there are a number of actions available which reliably lead to very different states. 

One formulation of the exploration problem supposes that the unknown future task will consist of a particular goal observation $o_g$ (or less generally, state) that the agent needs to reach. A possible approach is to learn a generative model of observations, such as a VAE. The agent can randomly sample a latent vector $z_g\sim p(z)$, map to a hypothetical goal $o_g$, learn a goal-conditioned policy $\pi(a\vert o, o_g)$, use collected data to update the generative model, and repeat. How can we ensure diversity in the goal sampling process here? The key is to *weight* the data used to train the generative model, up-weighting observations that have low density according to the current model. It's possible to prove that this will always increase the entropy of sampled goals. This mechanism, called `Skew-Fit`, is conceptually very similar to count-based exploration.
- What is the *objective* of the process described above? Well, we've already said we want to maximise the entropy of goals, $H(o_g)$, but we also want to learn a good policy. A good policy is one for which the entropy of the goal being pursued is low, given the final observation $o_T$ reached by the agent at the end of an episode. Hence the objective is $\max H(o_g)-H(o_g\vert o_T)=\max I(o_T;o_g)$: maximising the mutual information between the end observation and goal!

Another problem formulation is *state marginal matching*, in which we assume we have some target state distribution $p^\ast(s)$. At step $k$, given a fitted density estimator $p_k(s)$, we set the reward function to $r_k(s)=\log p^\ast(s)-\log p_k(s)$. Crucially, if $p_k$ is fitted only to data from the current policy $\pi_k$, we get an undesirable "tail chasing" behaviour, so instead we should fit it to *all data* seen so far. Game theory also tells us that the optimal exploring policy is a mixture of all policies that the agent moves through during learning, $\pi^\ast(a\vert s)=\sum_k\pi_k(a\vert s)$.
- What's a good choice for $p^\ast(s)$? If we accept *Eysenbach's theorem* (it's really just a heuristic!) that at test time an adversary will choose the worst possible goal state, the optimal strategy is to maximise the entropy of $p^\ast(s)$, i.e. use the uniform distribution.

A third problem formulation is to try to learn diverse *skills*, which is more general than reaching diverse states, since not all behaviours can be captured by goal-reaching. An interesting approach here is to define a *diversity-promoting* reward function. For a finite number of skill indices $z\in\{1..Z\}$, we train a classifier to predict which skill is being performed given a state, $p(z\vert s)$, set the skill-conditioned reward to $r(s\vert z)=\log p(z\vert s)$, and train a skill-conditioned policy to maximise this reward. Again, this process can be framed as a process of maximising mutual information, in this case between $z$ and $s$.
- See [Variational Intrinsic Control](Variational%20Intrinsic%20Control), and the more popular (and simpler?) follow-up  [../../../Diversity is All You Need - Learning Skills without a Reward Function](../../../Diversity%20is%20All%20You%20Need%20-%20Learning%20Skills%20without%20a%20Reward%20Function).

## Lecture 15: Offline Reinforcement Learning
The RL methods studied so far are fundamentally active: the agent needs to collect its own data, and make its own mistakes, in order to learn a good policy. This paradigm may not be particularly applicable to real-world applications, where such mistakes may be unsafe or expensive. Motivated by this concern, offline (or batch) RL aims to learn a policy entirely using a static pre-collected dataset $\mathcal{D}=\{\tau_1,...,\tau_N\}:\tau_i=\{s_i^t,a_i^t,r_i^t\}_{t=1}^H$. Note that unlike imitation learning, it is assumed that rewards are visible and included in the data.
- Some notation: $\mathcal{D}(s)$ is the marginal state distribution in  $\mathcal{D}$ and $\mathcal{D}(a\vert s)$ is the state-conditioned action distribution. If we assume that data are generated by a static behaviour policy $\pi_\beta$, we can estimate $\pi_\beta(a\vert s)=\mathcal{D}(a\vert s)$.

Unlike conventional supervised learning, it is theoretically possible for offline RL to yield policies that perform *better* than $\pi_\beta(a\vert s)$. The intuition for why this is the case is that it can "stitch" promising trajectory segments together in arrangements that never appear in full in $\mathcal{D}$.

What does offline RL look like in practice? We start by recognising that off-policy RL algorithms don't explicitly require data in the replay buffer to come from a prior iteration of the same agent's policy. Most classic offline RL algorithms are thus variants of off-policy methods, often with importance sampling playing a central role.

As is so often the case, in the deep RL setting things become more complicated and convergence is harder to come by. Why is it that we see offline RL methods fail, even in contexts where imitation learning works well? We can place a lot of the blame on an especially pernicious consequence of distributional shift:
- Recall that the target value in Q learning involves a maximisation over actions: $Q(s_t,a_t)\leftarrow r_t+\gamma \max_{a'} Q(s_{t+1},a')$. 
- This target value could be greatly overestimated for actions $a'$ outside of the distribution seen in $\mathcal{D}$, leading to erroneous backups.
- In the online setting, such errors are (generally) corrected over time due to exploration, but in the offline setting, there is no such error correction mechanism.

To address the distributional shift problem a common approach is to constrain the learned policy $\pi_\theta$ to keep it close to $\pi_\beta$ according to some measure $D$. Out-of-distribution actions are therefore never considered for $a'$. Since adding a policy constraint affects the definition of optimal performance, we generally want the constraint to be as unrestrictive as possible. Different choices of $D$ can lead to quite different solutions:
- Among others, options include *distribution matching* (e.g. using KL divergence) and *support matching*, which says that $\pi_\theta$ should have high probability only in areas where $\pi_\beta$ has some probability, but can have lower entropy, allowing convergence to much better performance. 
- Theoretically, support matching should do much better than distribution matching when $\pi_\beta$ has high entropy, but in practice there's often little difference, and performance depends heavily on hyperparameter tuning.

The general approach of policy constraint is predicated on the assumption that we can construct an accurate empirical estimate of $\pi_\beta(a\vert s)$ from $\mathcal{D}(a\vert s)$, and can also be too conservative: in states where all actions do equally badly, enforcing a constraint gives no benefit, while "eating up the capacity" of the function approximator. A more sophisticated approach is to recognise that not *all* out-of-distribution actions are bad; they are bad only if their values are overestimated. This leads us to consider algorithms that are explicitly pessimistic about the value function:
- The model-based approach here is to construct a "pessimistic" MDP (PMDP), with dynamics learned by a model and a pessimistic reward function $\tilde{r}(s,a)=r(s,a)-\lambda u(s,a)$, with $u(s,a)$ being higher in state-action pairs that are rarely seen in $\mathcal{D}$. In existing approaches, $u$ is the variance or covariance of next state predictions over an ensemble of dynamics models. Policy optimisation is then done with the learned model and reward function.
- In model-free conservative Q learning (CQL), a modified value function $Q_\text{CQL}$ is learned with the aim of avoiding state-action values that are higher than the values of actions seen in the data: 

$$Q_\text{CQL}=\min_Q\Big[\max_\pi\mathbb{E}_{a\sim\pi(a\vert s)}[Q(s,a)]-\mathbb{E}_{a\sim \mathcal{D}(a\vert s)}[Q(s,a)]\Big]$$

- $Q_\text{CQL}$ is then used in policy updates. CQL provably leads to a state value function $V_\text{CQL}$ that is a lower bound on the true $V$ function.

Finally, it is noted that most existing evaluations of offline RL have used data collected from partially-trained online RL policies, which tend to be substantially easier to work with than data from the real world. At this point, the lecturer ([Aviral Kumar](Avril%20Kumar)) plugs his D4RL respository of benchmark datasets.

## Lecture 16: Introduction to RL Theory
Metrics
- **Sample complexity**: how many episodes or timesteps. Assumes no exploration bottlenecks, e.g. in the case of offline RL with a dataset that has good coverage.
- **Regret**: Difference in expected *initial state value* versus the optimal policy, $\mathbb{E}_{s_0\sim\rho}[V^\ast(s_0)]- \mathbb{E}_{s_0\sim\rho}[V^{\pi_i}(s_0)]$, summed over the sequence of policies induced $\pi_0,...,\pi_i,...,\pi_N$. This can be interpreted as the area between the typical learning curve and a horizontal line at optimal performance. A sign of good performance is for regret to be $O(\sqrt{N})$.

Assumptions used in RL analyses: separate exploration from learning given the available data. For the latter, perform analysis under a learned dynamics model used to generate transitions. Use concentration inequalities (Hoeffsing's inequality or more complex variants) to bound errors in sample estimates and do worst case analysis of dynamics model. 

Want to bound errors in $Q$ estimates as a function of errors in dynamics. 

Matrix-vector representation ==DELETE THESE IMAGES AFTER==

![../../../Attachments/Screenshot from 2021-08-04 11-21-40.png](../../../Attachments/Screenshot%20from%202021-08-04%2011-21-40.png)

Bound infinity norm (max element) of $Q^\pi-\hat{Q}^\pi$.
![../../../Attachments/Screenshot from 2021-08-04 11-25-09.png](../../../Attachments/Screenshot%20from%202021-08-04%2011-25-09.png)

![../../../Attachments/Screenshot from 2021-08-04 11-27-38.png](../../../Attachments/Screenshot%20from%202021-08-04%2011-27-38.png)

Takeaway: small error in dynamics implies small error in $Q$, but error compounds (note $(1-\gamma)^2$ in denominator).

---
Part 2: optimisation error in FQI. Sampling error. Difference between empirical $\hat{T}$ and theoretical Bellman backup operator $T$. Combines concentration of reward and dynamics. First bound individually:
![../../../Attachments/Screenshot from 2021-08-04 11-34-00.png](../../../Attachments/Screenshot%20from%202021-08-04%2011-34-00.png)

Assume reward in $\{-R_{\max},R_{\max}\}$

When combining, introduces constants $c_1$ and $c_2$. Something to do with max.
![../../../Attachments/Screenshot from 2021-08-04 11-35-41.png](../../../Attachments/Screenshot%20from%202021-08-04%2011-35-41.png)

Then optimisation error ==(LOTS OF TWO STEPS AT A TIME)==
![../../../Attachments/Screenshot from 2021-08-04 11-35-41 1.png](../../../Attachments/Screenshot%20from%202021-08-04%2011-35-41%201.png)

Use fact that $Q^\ast$ is fixed point of $T$ and triangle inequality again

Then 
![../../../Attachments/Screenshot from 2021-08-04 11-40-49.png](../../../Attachments/Screenshot%20from%202021-08-04%2011-40-49.png)

Combining the above
![../../../Attachments/Screenshot from 2021-08-04 11-41-54.png](../../../Attachments/Screenshot%20from%202021-08-04%2011-41-54.png)

Takeaway: error compounds.  Especially a problem in offline RL where sampling error component may be very high.

Dependency on $\infty$-norm is a bit weird in infinite state spaces as cannot enumerate. Can do for other $p$-norms but a bit more complicated.

---
So have have looked at approximate dynamics model, learned assuming oracle/query access to MDP. What about more realistic exploration case? More complex, so just focus on bandit algorithm.

Regret
$$\operatorname{Reg}(T)=T \bar{r}\left(a^{*}\right)-\sum_{t=1}^{T} \bar{r}\left(a_{t}\right)$$

UCB strategy 
$$a_{t}:=\arg \max _{i=1, \cdots, N}\left(\tilde{r}^{t}\left(a_{i}\right)+\sqrt{\frac{\log (2 N T / \delta)}{2 n^{t}\left(a_{i}\right)}}\right)$$
$n$ and $\tilde{r}$ empirical. Where does this bonus ($b$) come from? Uses Hoeffding's inequality.
![../../../Attachments/Screenshot from 2021-08-04 11-50-11.png](../../../Attachments/Screenshot%20from%202021-08-04%2011-50-11.png)
extra term (why?)
![../../../Attachments/Screenshot from 2021-08-04 11-52-25.png](../../../Attachments/Screenshot%20from%202021-08-04%2011-52-25.png)

---
Final, RL with function approximation, can't obtain guarantees.

## Lecture 17: Deep RL Algorithm Design
In this lecture we discuss currently-topical algorithmic questions around the implementation of deep reinforcement learning.

For Q-learning algorithms, Sutton's *deadly triad* of bootstrapping, off-policy sampling and function approximation are liable to cause divergence of the $Q$ function to extreme values. A large part of RL theory is focused on mitigating divergence. However, large neural networks are *less* prone to divergence than smaller ones, on some metrics look increasingly similar to the guaranteed-stability tabular case. Perhaps not a big issue.

Overfitting to finite samples. Less of a problem with *fewer* gradient steps per environment steps, and *larger* batch sizes. Benefits of larger replay buffer often seem to outweigh technical drawback of being increasingly off-policy.

Why can performance degrade with more training?
- In the supervised setting, gradient descent with deep networks places an implicit regularisation on the network weights. This is often presented as a positive result, but when training a $Q$ function with bootstrapping, excessive regularisation leads to a loss of expressivity over time, meaning we don't use the full capacity of the network and become less and less capable of eventually fitting the optimal $Q$ function. This can be called *implicit under-parameterisation*.
- In environments with finite state and action spaces, this can be measured as a loss of effective rank ($\text{srank}_\delta$) of the "feature matrix" $\Psi$, which is the $\vert\mathcal{S}\vert\vert\mathcal{A}\vert\times d$ matrix of all $d$-dimensional feature vectors on the penultimate layer of the $Q$ network (with the final layer outputting $Q(s,a)=w^\top\phi(s,a)$). The effective rank of $\Phi$ can be obtained by taking the singular value decomposition $\Phi=U\text{diag}(\boldsymbol{\sigma})V^\top$, and calculating 

$$\text{srank}_\delta(\Phi)=\min\left\{k:\frac{\sum_{i=1}^k\boldsymbol{\sigma}_i}{\sum_{i=1}^d\boldsymbol{\sigma}_i}\geq 1-\delta\right\}.$$

- Compounding effect when regressing to targets with increasingly low rank.

What makes a good data distribution for learning, and how to we obtain one?
- High entropy. Contrary to theoretical results we've seen so far, this suggests that replay buffers, which effectively contain a mixture of off-policy distributions, may sometimes be *better* than using the on-policy distribution. There is clearly a tradeoff though, which can be modulated by altering the replay buffer size.
- In the presence of function approximation, where $Q$ values for states are correlated according to their proximity in feature space, on-policy data can be insufficient for correcting errors. Infrequently-visited states do not get their values corrected, and the Bellman backup means these erroneous values end up polluting the value estimates for more frequently-visited states. When learning on a higher-entropy distribution, this becomes less of a problem.

Policy gradient saddle points, depends a lot on initialisation and reward scaling.

## Lecture 18: [../../../Variational Inference](../../../Variational%20Inference) and Generative Models
The term *probabilistic model* refers to a very general class of models that represent probability distributions, which may be marginal $p(x)$ or conditional $p(y\vert x)$. A *latent variable model* is a probabilistic model in which there are known to be variables $z$ other than the evidence $x$ and the query $y$, which must be integrated out in order to evaluate probabilities. For marginal models,

$$p(x)=\int p(x\vert z)p(z)dz,$$

where $p(z)$ is a prior on the latent variable. 

Latent variable models are powerful because they allow us to decompose complicated distributions into integrated products of simpler ones whose parameters we can learn. 
- A mixture model is a type of latent variable model where $z$ is a categorical indicator. In this course, we've already encountered mixture models in the form of skill-conditioned policies. 
- We've also seen latent variable models in the context of model-based RL in POMDPs.

How do we train latent variable models? Given data $x_1,...,x_N$ and model parameters $\theta$, the obvious objective is the maximum log-likelihood:

$$\underset{\theta}{\text{argmax}}\frac{1}{N}\sum_{i=1}^N\log p_\theta(x_i)=\underset{\theta}{\text{argmax}}\frac{1}{N}\sum_{i=1}^N\log\int p_\theta(x_i\vert z)p(z) dz,$$

which is sadly intractable in general because of the integral. But now we apply the popular trick for introducing a new quantity that's not already present in an equation: multiply and divide by that same quantity. We use this to introduce a new distribution $q_i(z)$ for each $x_i$, which has a simple form such as a Gaussian:

$$\log\int p_\theta(x_i\vert z)p(z) dz=\log\int p_\theta(x_i\vert z)p(z) \frac{q_i(z)}{q_i(z)}dz=\log\mathbb{E}_{z\sim q_i(z)}\left[\frac{p_\theta(x_i\vert z)p(z)}{q_i(z)}\right].$$

At this point, we apply the *variational approximation*, which uses  [Jensen's inequality](Jensen's%20inequality) to show that $\mathbb{E}[\log X]\leq \log\mathbb{E}[X]$. Hence, the log-likelihood is lower bounded by the more tractable *expected* log-likelihood:

$$\log\mathbb{E}_{z\sim q_i(z)}\left[\frac{p_\theta(x_i\vert z)p(z)}{q_i(z)}\right]\geq \mathbb{E}_{z\sim q_i(z)}\left[\log\frac{p_\theta(x_i\vert z)p(z)}{q_i(z)}\right]$$
$$=\mathbb{E}_{z\sim q_i(z)}\left[\log p_\theta(x_i\vert z)+\log p(z)\right]-\mathbb{E}_{z\sim q_i(z)}\left[\log q_i(z)\right]=\mathbb{E}_{z\sim q_i(z)}\left[\log p_\theta(x_i\vert z)+\log p(z)\right]-H(q_i).$$

Every term in this expression, often called the variational, or evidence, lower bound (ELBO)  $\mathcal{L}_i(p_\theta,q_i)$, can be tractably estimated for any $q_i$. If the bound is sufficiently tight, this means we indirectly maximise our original objective. But how do we achieve a tight bound $\mathcal{L}_i(p,q_i)\approx \log p(x_i)$? It turns out this is achieved by minimising the KL divergence between $q_i(z)$ and the posterior $p(z\vert x_i)$:

$$D_\text{KL}(q_i(z)\vert\vert p(z\vert x_i))=\mathbb{E}_{z\sim q_i(z)}\left[\log\frac{q_i(z)}{p(z\vert x_i)}\right]=\mathbb{E}_{z\sim q_i(z)}\left[\log\frac{q_i(z)p(x_i)}{p_\theta(x_i\vert z)p(z)}\right]$$
$$=-\mathbb{E}_{z\sim q_i(z)}\left[\log p_\theta(x_i\vert z)+\log p(z)\right]+H(q_i)+\cancel{\mathbb{E}_{z\sim q_i(z)}}\log p(x_i)=-\mathcal{L}_i(p,q_i)+\log p(x_i).$$
$$\therefore\log p(x_i)=D_\text{KL}(q_i(x_i)\vert\vert p(z\vert x_i))+\mathcal{L}_i(p,q_i).$$

- Note that the rearrangement on the first line here makes use of Bayes' rule.

Maximising the ELBO with respect to $\theta$ (given samples from $q_i$) improves the model fit, and maximising with respect to the parameters of $q_i$ (e.g. mean and variance for a Gaussian) tightens the bound by lowering KL divergence. Practical algorithms therefore alternate between these two steps, similar to the EM algorithm.

So far, we've imagined maintaining a separate $q_i$ for every $x_i$, meaning the number of parameters to estimate scales linearly with $N$. The more scaleable approach of *amortized variational inference* instead uses a single conditional model $q_\phi(z|x_i)$, perhaps implemented as a neural network, which is often called the *inference network* or the *approximate posterior*. The ELBO is slightly rewritten as 

$$\mathcal{L}_i(p_\theta,q_\phi)=\mathbb{E}_{z\sim q_\phi(z\vert x_i)}\left[\log p_\theta(x_i\vert z)+\log p(z)\right]-H(q_\phi).$$

For Gaussian conditional models with mean $\mu_\phi$ and standard deviation $\sigma_\phi$, the entropy term is easy as it has a closed form solution, but the first term (let us write this more compactly as $\mathbb{E}_{z\sim q_\phi(z\vert x_i)}\left[r(x_i,z)\right]$) presents a challenge. How do we evaluate the derivative of an expectation of terms that don't depend on $\phi$? A clever solution is to use the *reparameterisation trick*, which makes the terms depends on $\phi$, but the expectation operation independent of it:

$$\mathbb{E}_{z\sim q_\phi(z\vert x_i)}\left[r(x_i,z)\right]=\mathbb{E}_{\epsilon\sim \mathcal{N}(0,1)}\left[r(x_i,\mu_\phi(x_i)+\epsilon\sigma_\phi(x_i))\right].$$

This expression can be maximised in practice by sampling $M$ points $\epsilon_j\sim \mathcal{N}(0,1)$ then use standard automatic differentiation software to compute

$$\frac{1}{M}\sum_{j=1}^M\nabla_\phi r(x_i,\mu_\phi(x_i)+\epsilon_j\sigma_\phi(x_i)).$$

## Lecture 19: Reframing Control as an Inference Problem

Rational behaviour can be *defined* as that which optimises a well-defined utility function. Much of classical economics and psychology is concerned with using optimal control theory as a model of human behaviour. Such behaviour is stochastic (at least in a realistic observability context), but a core rationality assumption is that better behaviour is more likely. This assumption can be called *soft optimality*.

Here is one possible model of soft-optimal behaviour, which provides a good match for empirical experiments with [human and animal behaviour](Ethology), and can be used to recover many of the RL equations we've seen already. Given an episodic MDP with termination time $T$, let $\mathcal{O}_{1:T}\in\{0,1\}^T$ be a set of binary variables (one per timestep) that indicate whether an agent's action is optimal in that timestep. Furthermore, let $p(\mathcal{O}_t\vert s_t,a_t)=\exp(r(s_t,a_t))$. This is a valid relationship if rewards are all negative, and encodes an assumption that *critical mistakes are less likely*. Given this model, the probability of a trajectory $\tau\in(\mathcal{S}\times\mathcal{A})^T$ given that it is optimal (i.e. $\mathcal{O}_{1:T}$) is

$$p(\tau\vert\mathcal{O}_{1:T})=\frac{p(\tau,\mathcal{O}_{1:T})}{p(\mathcal{O}_{1:T})}\propto p(\tau)\prod_t\exp(r(s_t,a_t))=p(\tau)\exp\left(\sum_tr(s_t,a_t)\right),$$

so for a uniform prior $p(\tau)$, the probability of a trajectory is exponential in its return.

We can do inference in this model. The common first step is to perform a *backward pass* through the model, for each $t$ computing $\beta_t(s_t,a_t)=p(\mathcal{O}_{t:T}\vert s_t,a_t)$, the probability that we can be optimal from $t$ onwards given that we take $a_t$ in $s_t$. We can use conditional independence relationships to derive a two-step recursive expression:

$$\beta_t(s_t,a_t)=p(\mathcal{O}_{t:T}\vert s_t,a_t)=\int p(\mathcal{O}_{t:T},s_{t+1}\vert s_t,a_t)ds_{t+1}=\int p(\mathcal{O}_{t+1:T}\vert s_{t+1})p(s_{t+1}\vert s_t,a_t)p(\mathcal{O}_t\vert s_t,a_t)ds_{t+1}$$
$$=p(\mathcal{O}_t\vert s_t,a_t)\mathbb{E}_{s_{t+1}\sim p(s_{t+1}\vert s_t,a_t)}[p(\mathcal{O}_{t+1:T}\vert s_{t+1})]=\exp(r(s_t,a_t))\mathbb{E}_{s_{t+1}\sim p(s_{t+1}\vert s_t,a_t)}[\beta_t(s_t)]$$
$$\text{where}\ \ \ \beta_t(s_t)=p(\mathcal{O}_{t+1:T}\vert s_{t+1})=\int p(\mathcal{O}_{t+1:T}\vert s_{t+1},a_{t+1})p(a_{t+1}\vert s_{t+1})da_{t+1}=\mathbb{E}_{a_{t+1}\sim p(a_{t+1}\vert s_{t+1})}[\beta_{t+1}(s_{t+1},a_{t+1})]$$

Somewhat suggestively, let $V_t(s_t)=\log\beta_t(s_t)$ and $Q_t(s_t,a_t)=\log\beta_t(s_t,a_t)$. This leads to:
- With a uniform action prior $p(a_t\vert s_t)$, $V_t(s_t)=\log\int\exp(Q_t(s_t,a_t))da_t$, which is a kind of "soft" max function (not the same as "softmax") which approaches $\max_{a_t}Q_t(s_t,a_t)$ as the values get larger.
	- It can be shown that the uniform action prior assumption does not sacrifice generality, as it can be recovered by appropriately scaling the rewards.
- $Q_t(s_t,a_t)=r(s_t,a_t)+\log\mathbb{E}[\exp(V_{t+1}(s_{t+1}))]$, which looks fishily like a Bellman backup, and but is only strictly one if the dynamics are deterministic (only one successor state in the expectation).
	- Defining the backup in this way can cause an undesirable optimism bias, because the log of the expected exponentiated values is always larger than the regular expectation ([Jensen's inequality](Jensen's%20inequality)) and is likely to be dominated by the "luckiest". More on this later.

Given all the $\beta_t$ values computed on the backward pass, we can then compute the soft-optimal policy $\pi(a_t\vert s_t)=p(a_t\vert s_t,\mathcal{O}_{1:T})$:

$$\pi(a_t\vert s_t)=p(a_t\vert s_t,\mathcal{O}_{1:T})=\frac{p(s_t, a_t\vert\mathcal{O}_{1:T})}{p(s_t\vert\mathcal{O}_{1:T})}=\frac{p(\mathcal{O}_{1:T}\vert s_t,a_t)p(s_t,a_t)/\cancel{p(\mathcal{O}_{1:T})}}{p(\mathcal{O}_{1:T}\vert s_t)p(s_t)/\cancel{p(\mathcal{O}_{1:T})}}=\frac{\beta_t(s_t,a_t)}{\beta_t(s_t)}p(a_t\vert s_t).$$

Again assuming a uniform action prior, we therefore have 

$$\pi(a_t\vert s_t)=\frac{\beta_t(s_t,a_t)}{\beta_t(s_t)}=\frac{\exp Q_t(s_t,a_t)}{\exp V_t(s_t)}=\exp(Q_t(s_t,a_t)-V_t(s_t))=\exp A_t(s_t,a_t)$$

where $A_t$ is the advantage function. Hence under this model, the soft-optimal policy follows the Boltzmann distribution in the advantage. Adding in a temperature parameter $\pi(a_t\vert s_t)=\exp(\frac{1}{\alpha}A_t(s_t,a_t))$ allows us to smoothly interpolate between hard and soft optimality.

A derivation is also given for *forward messages* of the form $\alpha_t(s_t)=p(s_t\vert \mathcal{O}_{1:t-1})$, and it is shown that the state marginal distribution $p(s_t)\propto\beta_t(s_t)\alpha_t(s_t)$. Informally, $\alpha_t$ gives states with high probability of being reached from the initial state under optimal behaviour, and $\beta_t$ gives states from which there is high probability of achieving the agent's goal, so this result tells us that states are likely to extend that *both* of these hold. This makes a lot of sense, and aligns with empirical results from human and animal experiments.

Let's return to the optimism bias problem, in which the Bellman-like backup is dominated by the single highest-value successor state. What this is effectively doing is skewing the transition probability distribution towards high-reward outcomes. We can correct for this bias using the tools of variational inference presented in the previous lecture.

For this analysis, let the observed variables $x=\mathcal{O}_{1:T}$ and the latent variables $z=(s_{1:T},a_{1:T})$. Furthermore, let us add some additional structure by defining $q(z)=q(s_{1:T},a_{1:T})=p(s_t)\prod_tp(s_{t+1}\vert s_t,a_t)\pi(a_t\vert s_t)$. Assuming $p(s_t)$ and $p(s_{t+1}\vert s_t,a_t)$ are known, the only free variable to be inferred is the policy $\pi$. Plugging these factors into one rearrangement of the ELBO equation:

$$\log p(x)\geq \mathbb{E}_{z\sim q(z)}\left[\log p(x,z)-\log q(z)\right]$$
$$\log p(\mathcal{O}_{1:T})\geq \mathbb{E}_{(s_{1:T},a_{1:T})\sim q}\left[\cancel{\log p(s_1)}+\cancel{\sum_{t=1}^T\log p(s_{t+1}\vert s_t,a_t)}+\sum_{t=1}^T\log p(\mathcal{O}_t\vert s_t,a_t)\right.$$
$$\left.-\cancel{\log p(s_1)}-\cancel{\sum_{t=1}^T\log p(s_{t+1}\vert s_t,a_t)}-\sum_{t=1}^T\log \pi(a_t\vert s_t)\right]= \mathbb{E}_{(s_{1:T},a_{1:T})\sim q}\left[\sum_{t=1}^T\left(r(s_t,a_t)-\log \pi(a_t\vert s_t)\right)\right]$$
$$=\sum_{t=1}^T\mathbb{E}_{(s_t,a_t)\sim q}\left[r(s_t,a_t)+H(\pi(\cdot\vert s_t))\right].$$

So we recover an objective that looks very much like the original RL objective, with an additional term. The probability of optimality is maximised by maximising the sum of return and policy entropy.

How do we do the maximisation? Again we consider a backward recursive method, starting at $t=T$:

$$\log p(\mathcal{O}_{T})=\mathbb{E}_{(s_T,a_T)\sim q}\left[r(s_T,a_T)-\log \pi(a_T\vert s_T)\right].$$

A standard result for expressions of this form is that they are maximised when 

$$\pi(a_T\vert s_T)=\frac{\exp(r(s_T,a_T))}{\int \exp(r(s_T,a)) da}=\exp(Q_T(s_T,a_T)-V_T(s_T))=\exp A_T(s_T,a_T).$$ Substituting this back in, we have 

$$\mathbb{E}_{(s_T,a_T)\sim q}\left[\cancel{r(s_T,a_T)}-\cancel{r(s_T,a_T)}+\log\int\exp(r(s_T,a))da\right]$$
$$=\mathbb{E}_{(s_T,\cdot)\sim q}\left[V_T(s_T)\right]=\mathbb{E}_{s_T\sim p(s_T\vert s_{T-1},a_{T-1})}\left[V_T(s_T)\right].$$

Then performing the backwards recursion,

$$p(\mathcal{O}_{T-1:T})=\mathbb{E}_{(s_{T-1},a_{T-1})\sim q}\left[r(s_{T-1},a_{T-1})-\log \pi(a_{T-1}\vert s_{T-1})\right]+\mathbb{E}_{s_T\sim p(s_T\vert s_{T-1},a_{T-1})}\left[V_T(s_T)\right]$$
$$=\mathbb{E}_{s_{T-1}\sim p(s_{T-1}\vert s_{T-2},a_{T-2})}\left[\mathbb{E}_{a_{T-1}\sim \pi(a_{T-1}\vert s_{T-1})}\left[r(s_{T-1},a_{T-1})-\log \pi(a_{T-1}\vert s_{T-1})+\mathbb{E}_{s_T\sim p(s_T\vert s_{T-1},a_{T-1})}\left[V_T(s_T)\right]\right]\right]$$
$$=\mathbb{E}_{s_{T-1}\sim p(s_{T-1}\vert s_{T-2},a_{T-2})}\left[\mathbb{E}_{a_{T-1}\sim \pi(a_{T-1}\vert s_{T-1})}\left[Q_{T-1}(s_{T-1},a_{T-1})-\log \pi(a_{T-1}\vert s_{T-1})\right]\right]$$

which is again maximised by 

$$\pi(a_{T-1}\vert s_{T-1})=\exp(Q_{T-1}(s_{T-1},a_{T-1})-V_{T-1}(s_{T-1}))=\exp A_{T-1}(s_{T-1},a_{T-1}),$$

and the recursion continues similarly. Note that now we have a regular Bellman backup, without the undesirable log-expectation-exponential operation.

This derivation provides a foundation for soft Q-learning and soft policy gradient algorithms, and [SAC](Soft%20Actor-Critic%20Algorithms%20and%20Applications) is the actor-critic counterpart to soft Q-learning. At the end of the lecture, examples are used to demonstrate the advantages of the soft optimality framework: maintaining exploration, improving robustness, and providing a principled approach to breaking ties.

## Lecture 20: [Inverse Reinforcement Learning](Inverse%20Reinforcement%20Learning)

So far we have assumed that the reward function is manually specified to define a task. Here we consider the problem of *learning* a reward function through observation of an expert demonstrator. We assume the demonstrator is (approximately) optimising some parameterised reward function $r_\psi$, then try to infer the $\psi$ that best explains our observations. 

In the standard IRL setup, we assume access to a trajectory dataset $\{\tau_i\}$ sampled from the *optimal policy* $\pi^\ast$. The problem is challenging because it is underspecified; many reward functions can explain the same behaviour. For this reason, popular approaches use strong inductive biases. In the classic *feature matching* IRL setup, we assume a linear reward function $r_\psi(s,a)=\psi^\top f(s,a)$, where $\psi$ is a vector and $f$ is a feature function. Let $\pi_\psi$ be the optimal policy under the inferred $r_\psi$. One possible objective is to match the state-action marginals: $\mathbb{E}_{\pi_\psi}[f(s,a)]=\mathbb{E}_{\pi^\ast}[f(s,a)]$. This can work okay in practice, but is still ambiguous as there are many policies with identical marginals. An alternative is to maximise the margin between the expected reward of $\pi^\ast$ and that of all other policies:

$$\underset{\psi,m}{\text{max}}\ m\ \ \ \text{s.t.}\ \ \ \psi^\top\mathbb{E}_{\pi^\ast}[f(s,a)]\geq\underset{\pi\in\Pi\setminus\{\pi^\ast\}}{\text{max}}\psi^\top\mathbb{E}_{\pi}[f(s,a)]+m,$$

although this is a bit arbitrary. It's also not obvious how to evaluate this objective over very large or infinite policy spaces $\Pi$, and we need to somehow "weight" the margin by the similarity between $\pi^\ast$ and $\pi$. The [SVM](SVM) trick can be adopted to obtain a tractable algorithm here.

Another alternative makes use of the soft optimality framework from the previous lecture to build a probabilistic model of demonstrated behaviour. Recall that the key equation of this framework is $p(\mathcal{O}_t\vert s_t,a_t)=\exp(r_\psi(s_t,a_t))$. Given $N$ observed trajectories from a soft-optimal policy $\pi^\ast$, the maximum likelihood $\psi$ is

$$\underset{\psi}{\text{max}}\frac{1}{N}\sum_{i=1}^N\log p(\tau_i\vert\mathcal{O}_{1:T},\psi)=\underset{\psi}{\text{max}}\frac{1}{N}\sum_{i=1}^N\log \left(\cancel{p(\tau_i)}\exp\sum_{t=1}^Tr_\psi(s_t,a_t)\right)=\underset{\psi}{\text{max}}\frac{1}{N}\sum_{i=1}^N r_\psi(\tau_i),$$

where the prior $p(\tau)$ can be safely ignored as it is independent of $\psi$. However, we don't just want to find the maximum likelihood $\psi$, because this can lead to a function that gives high reward everywhere, even far away from the demonstrated data. For this reason, we add a term $-\log Z:Z=\int p(\tau)\exp(r_\psi(\tau)) d\tau$ which penalises high reward in trajectories sampled from the prior. Taking the derivative of the two-term objective function with respect to $\psi$,

$$\nabla_\psi\mathcal{L}=\frac{1}{N}\sum_{i=1}^N \nabla_\psi r_\psi(\tau_i)-\frac{1}{Z}\int p(\tau)\exp(r_\psi(\tau)) \nabla_\psi r_\psi(\tau) d\tau=\frac{1}{N}\sum_{i=1}^N \nabla_\psi r_\psi(\tau_i)-\int p(\tau\vert\mathcal{O}_{1:T},\psi)\nabla_\psi r_\psi(\tau) d\tau,$$

where the rewriting of the second term uses a relationship derived in the previous lecture. This objective can now be expressed in terms of expectations,

$$\nabla_\psi\mathcal{L}=\mathbb{E}_{\tau\sim p(\tau\vert \pi^\ast)}[\nabla_\psi r_\psi(\tau)]-\mathbb{E}_{\tau\sim p(\tau\vert\mathcal{O}_{1:T},\psi)}[\nabla_\psi r_\psi(\tau)]$$

which has a very intuitive interpretation of the difference between the expected reward of trajectories sampled from $\pi^\ast$, and that of samples from *the soft-optimal policy under the current reward estimate*. This provides the basis for a tractable algorithm. For known dynamics, the derivations in the previous lecture tell us that the state-action marginal probabilities of the soft-optimal policy is given by the product of the forward and backward messages: $\mu_t(s_t,a_t)=\beta(s_t,a_t)\alpha(a_t)$. Furthermore, in finite state-action spaces, we can express both $\mu_t$ and $r_\psi$ as vectors. This allows us to write the second term of the gradient expression as 

$$\mathbb{E}_{\tau\sim p(\tau\vert\mathcal{O}_{1:T},\psi)}[\nabla_\psi r_\psi(\tau)]=\sum_{t=1}^T\mu_t^\top\nabla_\psi r_\psi$$

This leads us to the classic [maximum entropy inverse reinforcement learning](Maximum%20Entropy%20Inverse%20Reinforcement%20Learning) algorithm. The name of this algorithm derives from the fact that in the case where $r_\psi(s,a)=\psi^\top f(s,a)$, we provably obtain the maximum-entropy $\pi_\psi$ that matches the feature expectations of $\pi^\ast$. This is desirable because it minimises the undue assumptions made.

The maximum entropy IRL requires us to solve for the soft-optimal policy in an inner loop, and to enumerate all state-action tuples for visitation frequency and gradient. This makes it impractical in large and continuous spaces. It also can't handle unknown dynamics. However, the expectations can be approximated using samples: $N$ from $\pi^\ast$ and $M$ from $\pi_\psi$. Also, rather than running inner-loop policy optimisation to convergence every time $\psi$ is updated, a policy can be learnt "lazily" using any soft RL algorithm. The distribution bias that this introduces can be corrected using importance weights. These approximations give us the gradient

$$\nabla_\psi\mathcal{L}\approx \frac{1}{N}\sum_{i=1}^N\nabla_\psi r_\psi(\tau_i)-\frac{1}{\sum_j w_j}\sum_{j=1}^M\nabla_\psi w_j r_\psi(\tau_j),$$

where $w_j=\frac{p(\tau_j)\exp r_\psi(\tau_j)}{p(\tau_j\vert \pi)}=\frac{\exp r_\psi(\tau_j)}{\prod_t \pi(a_t\vert s_t)}$. If policy learning is effective, importance weighting should become less and less important over time. This objective is used in the [guided cost learning](Guided%20Cost%20Learning:%20Deep%20Inverse%20Optimal%20Control%20via%20Policy%20Optimization) algorithm. 

There is an interesting connection between guided cost learning and [GAN](GAN)s, in that the objectives of both are structured like games. The samples from $\pi^\ast$ correspond to the "true" data distribution, the lazy soft-optimal policy $\pi_\psi$ serves as a generator which is updated to make it *harder* to discrimination it from the demonstrations, and $\psi$ is updated to *improve* the discrimination. It is possible to write out the guided cost learning objective in the same terms as the GAN objective, with a slightly unusual objective for the disciminator. 
- Furthermore, by using the regular disciminator objective we obtain not an IRL problem but an [imitation learning](Imitation%20Learning) one. This gives us [generative adversarial imitation learning](Generative%20Adversarial%20Imitation%20Learning).

## Lecture 21: Transfer Learning and Multi-Task Learning
Prior understanding of problem structure can help humans to solve complex tasks quickly. In RL, prior knowledge could be encoded in a $Q$ function, a policy, a dynamics model, or (most subtly) features and hidden states within any of these networks. *Transfer learning* is the general approach of using prior knowledge obtained from one set of tasks (the *source* domain) for faster learning and better performance on a new task (the *target* domain). The number of *shots* is the number of learning attempts allowed in the target domain. In RL, a "task" is an MDP. 

Initially, let us consider the case where there is just one task in the source domain. Transfer is typically completed as a finetuning operation, possibly with a separate head head, and possibly with fixed lower layers. Challenges:

- A change of domain changes the representation distribution. We can make an *invariance assumption*, which states that everything that is different between the source and target domains is irrelevant to the task. Letting $x$ denote the representation and $y$ denote the task, this is equivalent to claiming the existence of some $z=f(x)$ such that $p(y\vert z)=p(y\vert x)$, but $p(z)$ is invariant across domains. Building on this idea, we can (somewhat arbitrarily) pick a layer in our network to use as $z$, and force it to have the same population-level distribution in both domains. We can achieve this with a GAN-like approach: train a discriminator to classify the domain given $z$ and backpropagate gradients through the representation network to maximise confusion. This idea is called domain confusion, or domain-adversarial neural networks, and can naturally be applied in RL as an additional loss.
- A more context-specific challenge of finetuning in RL is possible qualitative differences in the dynamics $p_\text{source}$ and $p_\text{target}$. If these are known ahead of time, these can be handled by augmenting the reward function in the source domain with an additional term, 
$$\Delta r(s,a,s')=\log p_\text{target}(s'\vert s,a)-\log p_\text{source}(s'\vert s,a),$$
but this is a little weird because it assumes known dynamics: why use RL? A clever way of computing an unbiased estimate is to train *two* discriminators, $D_1$ and $D_2$, the first of which predicts the domain given $s,a,s'$ and the second of which predicts it given only $s,a$:
$$\Delta r(s,a,s')=[\log D_1(\text{target}\vert s,a,s')-\log D_2(\text{target}\vert s,a)]-[\log D_1(\text{source}\vert s,a,s')-\log D_2(\text{source}\vert s,a)].$$
This general approach is useful when there are dynamics that are possible in the source domain but not in the target domain, but *not* vice versa as the opportunities to learn never arise.
- Another RL-specific challenge is the risk of loss of entropy during training in the source, which prevents sufficient exploration to learn effectively in the target. Maximum-entropy RL methods are effective here as they can learn to solve the source task in a variety of ways.

Now let's turn our attention to the multi-task transfer case, where all tasks simultaneously act as sources and targets (the resultant networks may then go on to be finetuned for a subsequent downstream task, and the increased source variety often improves the likelihood of success). An important observation is that multi-task RL corresponds to single-task RL in a *joint MDP*, in which task context information $z$ is added to the state and remains constant throughout an episode. So why not just employ conventional RL in the joint MDP?
- Gradient interference: becoming better on one task can make you worse on another. This in turn can lead to a widely observed winner-take-all problem, where the agent starts to prioritise a single task on which early performance is best.
- This can be partially mitigated using a policy distillation approach: learn an independent policy for each task, while simultaneously training a single centralised policy via supervised learning using data from all tasks. Alone this provides no knowledge transfer, but this can be achieved in a soft way by adding a loss term to encourage each task-specific policy to resemble the centralised policy.

Finally, we can focus on a more narrow, concrete problem setting with a single source and target. Let us assume that the dynamics are the same in both domains, but the *reward function* is different. What is the best object to transfer in this setting? Clearly, in model-based RL we can trivially transfer the model (although we still may face a distributional shift problem). On the other end of the spectrum, policies are generally tricky to transfer because they contain no explicit dynamics information. A value function is not straightforward to transfer as-is, as it couples dynamics, rewards and policies, but progress can be made using the [Successor Representation](Successor%20Representation) decomposition (see separate notes).

## Lecture 22: [Meta-learning](Meta-learning)
Building on the ideas of the previous lecture, can we use multiple source domain tasks not to learn value functions, policies and representations, but to learn something about the *learning process itself*, which includes intelligent exploration and feature acquisition? The act of "learning to learn" is called meta-learning, and the equivalent of a test set is the entire training process of an RL agent in the target domain.

$$\underset{\theta}{\text{argmax}}\sum_{i=1}^n\mathbb{E}_{\tau\sim\pi_{\phi_i}}[R(\tau)]\ \ \ \text{where}\ \ \ \phi_i=f_\theta(\mathcal{M}_i)$$

Assume that during both meta-train and meta-test time, MDPs are sampled i.i.d.


Can be thought of inferring task context information $z=\phi_i$ in multi-task joint MDP (see previous lecture!).

Representation learning over space of experience

$f_\theta(\mathcal{M}_i)$ should (1) improve the policy with experience and (2) choose how to explore.

 This effectively makes the entire meta-learning problem a POMDP. Three perspectives:
- Recurrent policy (a variety of architectures have been explored), whose hidden state is **not reset** between episodes. Optimising total reward over the entire *meta-episode* with a recurrent policy leads the agent to automatically learn to explore. This approach is conceptually simple and easy to apply, but is vulnerable to meta-overfitting, and optimisation can be unstable in practice.
- Thirdly, explicitly learn posterior over $z$ via variational inference, Thompson sampling. Conceptually very similar to recurrent method, but with stochastic $z$. PEARL algorithm. Similar advantages and disadvantages to the recurrent method.
- Thirdly, (bit of a stretch) $\theta=z$, bi-level optimisation problem, *model-agnostic meta learning* (MAML). This approach is conceptually elegant, but can be complex to implement because of the second derivatives, and requires many samples to work well.

Model-based meta-RL. Meta-training set is pairs $\{(D_i^{tr},D_i^{te})\}_{i=1}^n$ where each $D_i^{tr},D_i^{te}$,  are two sets of $(s,a,s')$ tuples sampled from *different dynamics* (e.g. before and after the agent loses a body part or gets a sensor miscalibration).

Finally, an intruiging hypothesis: what if the variety of human problem solving modes (e.g. apparently model-free RL, episodic recall, causal inference, model-based planning) are all [emergent phenomena](Emergence) resulting from an overarching process of meta-RL? There is some early experimental evidence that meta-RL can give rise to structures that look like dynamics models or causal reasoning modules.

## Lecture 23: Challenges and Open Problems

- Not enough focus on generalisation.