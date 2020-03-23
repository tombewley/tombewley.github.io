---
title: 'Weekly Readings #22'
date: 2020-03-22
permalink: /posts/2020/03/weekly-readings-22/
tags:
  - weekly-readings
---

Explanation-based tuning; saliency maps for vision-based policies; RL with differentiable decision trees.

## 📝 Papers

### Lee, Benjamin Charles Germain, Kyle Lo, Doug Downey, and Daniel S. Weld. “Explanation-Based Tuning of Opaque Machine Learners with Application to Paper Recommendation.” *ArXiv:2003.04315 [Cs, Stat]*, March 9, 2020.

Some prior work has been done on manually *tuning* interpretable models to improve their performance based on received explanations [30, 35, 36]. This paper proposes a method for tuning an arbitrary black box model based on information from local or global explanation tools. This is done by retraining the black box on *pseudo-examples*, generated and labelled according to the user's feedback on the explanation.

The method is developed in the context of binary classification, where it assumed we already have a mapping $h':\mathcal{X}\rightarrow \mathcal{X}'$ that transforms the black box's input $x$ into a vector of interpretable binary features $x'$. The first task is imitation learning: finding an interpretable function $g$ such that $g(h'(x))$ approximates the black box $f(x)$. Here, $g$ is a linear model, fitted to the region around a given target $x'$ using `LIME`. This allows a set of the most important interpretable features to be identified according to their weights in the model.

After being provided with this `LIME`-based explanation, the explainee assigns a binary label to one highly-weighted feature $j$ from $x'$. A label of $1$ represents the user's assessment that examples near $x'$ should be positive when feature $j$ is positive; $0$ represents the opposite.

Next we obtain a set of new, unlabelled instances with a positive value for feature $j$, either by sampling from a pool or by using some generative model. Instances in this new set are weighted based on their proximity to $x'$ in the interpretable space and added to the training set, then the black box is retrained.

The approach is tested in the context of a paper recommendation service called Semantic Sanity, which uses a neural network at the core of its prediction model. The interpretable feature space is a set of 20,000 unigrams and bigrams. Users seem to to prefer this tunable system over the baseline algorithm which uses a measure of diversity.

### Shi, Wenjie, Zhuoyuan Wang, Shiji Song, and Gao Huang. ‘Self-Supervised Discovering of Causal Features: Towards Interpretable Reinforcement Learning’. *ArXiv:2003.07069 [Cs]*, 16 March 2020.

This paper concerns the interpretability of a vision-based RL policy $\pi$. The approach is to train a model $f_\theta$, (parameterised by $\theta$) which outputs a saliency-filtered image $\bar{s}_t=f_\theta(s_t)\odot s_t$ highlighting task-relevant information in the input $s_t$. This can be thought of as a kind of soft attention to show where $\pi$ "looks" to make its decision. $\theta$ is optimised to satisfy two desiderata:

- **Maximum behaviour resemblance**: $\underset{\theta}{\min}\vert\vert\pi(\bar{s}_t)-\pi(s_t)\vert\vert_2^2$. Applying the filter to the state has a minimal effect on behaviour.
- **Minimum region retaining**: $\underset{\theta}{\min}\vert\vert f_\theta(s_t)\vert\vert_1$. The filter keeps a minimal part of the image.

$f_\theta$ is implemented as an encoder-decoder architecture. The encoder $f_e$ takes $s_t$ as its input, and produces a low-dimensional representation $e_t$. The decoder $f_d$ maps $e_t$ to a frame of the same dimensions as $s_t$, with values $\in [0,1]$ representing the filtering levels.

An identical copy of $f_e$ is used by $\pi$, followed by a series of fully-connected layers $f_a$ to map the low-dimensional representation to an action. Crucially, this allows it to use **either $s_t$ or $\bar{s}_t$** as its input. During training, $s_t$ is used initially, which allows $f_e$ and $f_a$ to be trained end-to-end. 

The trained policy is used to generate a dataset of state-action pairs $\mathcal{D}$, then the input is switched to $\bar{s}_t$, and the decoder $f_d$ is trained to minimise a loss function that combines the two desiderata:
$$
\mathcal{L}=\sum_{(s_t,a_t)\in\mathcal{D}} \frac{1}{2}\Big\vert\Big\vert \pi\left(f_d(f_e(s_t)) \odot s_t\right)-a_t\Big\vert\Big\vert _{2}^{2}+\alpha\Big\vert\Big\vert  f_d(f_e(s_t))\Big\vert\Big\vert _{1}
$$
During training of $f_d$, both $f_e$ and $\pi$ are fixed. 

The technique is deployed in Atari Pong and Tennis, as well as in a realistic first-person driving simulator. The results look pretty nice, and it is demonstrated that they can be used to diagnose poor performance in the RL agents. It seems that better agents focus their attention more precisely on salient areas of the input, as measured by overlap with manually-annotated filters. The importance of good variety in $\mathcal{D}$ is also made clear: in the driving simulator, $f_d$ does not transfer well between tracks, which in turn leads to reduced performance when $\pi\left(f_d(f_e(s_t)) \odot s_t\right)$ is used.

### Silva, Andrew, Taylor Killian, Ivan Dario Jimenez Rodriguez, Sung-Hyun Son, and Matthew Gombolay. “Optimization Methods for Interpretable Differentiable Decision Trees in Reinforcement Learning.” *ArXiv:1903.09338 [Cs, Stat]*, February 21, 2020.

Decision trees are not typically deployed in RL because they cannot be updated online by gradient descent. This work claims to be the first to explore using Suarez and Lutsko's *differentiable decision trees* (DTs) for both Q-learning and policy gradient RL. For the Q-learning, the parameter update rule is
$$
\begin{aligned}
\Delta \theta\doteq\alpha &\left(R\left(s_{t}, a_{t}\right)+\gamma \max _{a^{\prime} \in A} Q_{\theta}\left(s_{t+1}, a^{\prime}\right)
-Q_{\theta}\left(s_{t}, a_{t}\right)\right) \nabla_{\theta} Q_{\theta}^{\pi}\left(s_{t}, a_{t}\right)
\end{aligned}
$$
When using a DDT as a function parameter for Q-learning, each leaf contains an estimate of $q(s,a)$ for applying each action $a$ when in the region of the state space $s$ dictated by its ancestors. Considering the simple case of a DDT with a single decision node and two leaves:
$$
Q_\theta(s,a)=\mu_\text{left}(s)\cdot q^{\text{left}}_a+(1-\mu_\text{left}(s))\cdot q^{\text{right}}_a\ \ \ \text{where}\ \ \ \mu_{\eta}(s):=\frac{1}{1+e^{-\left(a_{\eta}\left(\beta_{\eta}^{\top} s-\phi_{\eta}\right)\right)}}
$$
Here the learnable parameters are $\theta=(q^{\text{left}}_a,q^{\text{right}}_a,\alpha_\text{left},\beta_\text{left},\phi_\text{left})$, for which the partial derivatives can be found pretty easily to plug into the update rule. For example:
$$
\frac{\partial Q_\theta(s,a)}{\partial q^{\text{left}}_a}=\mu_\text{left}(s)\ \ \ ;\ \ \ \frac{\partial Q_\theta(s,a)}{\partial \alpha_{\text{left}}}=(\partial q^{\text{left}}_a-\partial q^{\text{right}}_a)\cdot \mu_\text{left}(s)\cdot (1-\mu_\text{left}(s))\cdot (\beta_\text{left}^{\top} s-\phi_\text{left})
$$
For policy gradient, the update rule is
$$
\Delta \theta=\alpha \sum_{t} G_{t} \nabla_{\theta} \log \left(\pi_{\theta}\left(a_{t}, \vert s_{t}\right)\right)
$$
where $G_t$ is the discounted return from time $t$. When using a DDT for policy gradient, each leaf estimates the optimal probability distribution over actions $\pi(a\vert s)$ given a state region $s$. Partial derivatives can be found in the same way as above.

A DDT can be discretised by finding the feature $j$ with highest weight $\beta^j_\eta$ at each decision node $\eta$, and modifying $\beta_\eta$ to be one-hot about this index. $\phi_\eta$ then needs to be divided by $\beta^j_\eta$ to normalise. The logistic activation is also swapped out for a step function. For policy gradient, the leaves can also be simplified to return only the highest-probability action.

An analysis with a simple MDP suggests that Q-learning with DDTs might induce an excess of 'critical points' which service to impede gradient descent. For this reason, it is suggested that policy gradient is a more promising approach.

Experiments with policy gradient in a range of Gym environments show that DDT performance is competitive with, and often superior to, using a neural network, and that it is more robust to the exact choice of model architecture. In the discussion, it is also suggested that decision tree policies could be specified as priors using expert knowledge, before being refined by policy gradient learning.
## 🗝️  Key Insights
- While their implementation is rather preliminary, what Lee et al are calling "explanation-based tuning" seems like the logical next step after explainability itself. 
- Shi et al's saliency filters produce nice results with a relatively simple optimisation procedure, and they can help to provide insight about where a poorly-performing policy may be going wrong.
- Differentiable decision trees feel to me like an extremely powerful architecture for interpretable agents, since they have very high representational capacity and can be trained online, but can be 'handed off' to crisp decision trees at any time. It's remarkable that Silva et al seem to be the first people to recognise this picture in its entirety. 