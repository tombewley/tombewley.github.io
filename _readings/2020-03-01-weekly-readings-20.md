---
title: 'Weekly Readings #20'
date: 2020-03-01
permalink: /posts/2020/03/weekly-readings-20/
tags:
  - weekly-readings
---

Rule-based regularisation; DeepSHAP for augmenting GAN training; image schemas as conceptual primitives; imitating DDPG with a fuzzy rule-based system.

## 📝 Papers

### Burkart, Nadia, Marco Huber, and Phillip Faller. “Forcing Interpretability for Deep Neural Networks through Rule-Based Regularization.” In *2019 18th IEEE International Conference On Machine Learning And Applications (ICMLA)*, 700–705, 2019.

Here a bidirectional relationship is established between a neural network and a rule-based surrogate. The surrogate is trained simultaneously with the neural network to imitate it, and a metric quantifying its degree of explainability is fed back into the network's loss function as a regularisation term.

The approach is implemented on binary classification tasks. The network uses continuous-valued features, while the rule-based model (*Scalable Bayesian rule lists*, SBRL) uses categorical features which requires preprocessing into bins. The regularisation term used, denoted $\Omega$, is the *total number of antecedents* in the rule base (plus $1$, which aids stability).

This term is non-differentiable, so in order to train the main network by gradient descent a clever trick is used: training a proxy neural network $S$ to map the main network's parameters $\theta$ to the value of $\Omega$. The training dataset for the proxy is created during training itself. Every $s$ steps a new surrogate is trained and a $(\theta,\Omega)$ datapoint is created; every $r>s$ steps a new $S$ is trained on the enlarged dataset. In practice, $S$ is given a bit of time to pre-train before the regularisation term is first added, and old, unreflective $(\theta,\Omega)$ pairs are discarded from the dataset, similarly to the use of a fixed-length buffer in off-policy reinforcement learning.

*Note that this proposal is heavily inspired by Wu et al's 2018 paper "Beyond Sparsity: Tree-based Regularization of Deep Models for Interpretability", where a decision tree is used as the surrogate and $\Omega$ is the average decision path length.*

Experiments on a selection of datasets show that the approach is effective at reducing complexity, and produces correspondingly less complex rules than the tree-based regularisation from Wu et al [though it's hard to compare the two surrogate model classes directly].

### Graves, Laura, Vineel Nagisetty, Joseph Scott, and Vijay Ganesh. “LogicGAN: Logic-Guided Generative Adversarial Networks.” *ArXiv:2002.10438 [Cs, Stat]*, February 24, 2020.

In standard GAN training, the discriminator provides a single value of feedback for each instance. Here, a Shapley value explanation module called *DeepSHAP* is used to approximate feature importance values for the discriminator, which can be used as a mask to scale the loss gradient used by the generator for learning. The intuition here is that performance should improve more quickly if the generator is given the 'reason' for the discriminator's decision. [I'm not sure this is really "logic-guided" though…]

In experiments with generating MNIST digits, training of the augmented model appears to be 13-40% more data-efficient than for a standard GAN, and remains stable with higher learning rates. The quality of samples at convergence stays about the same, though. It is suggested that the use of explanation modules during the training process may allow for greater human control and understanding.

### Mandler, Jean M. “How to Build a Baby: II. Conceptual Primitives.” *Psychological Review*, 1992, 587–604.

How are adult concepts derived from the sensory primitives available to infants? Mandler's answer is that children actually have access to more than sensory primitives. They have an innate capacity for *perceptual analysis*, that is for creating condensed re-descriptions of their perceptions. Without language in place yet, these re-descriptions are phrased in terms of purely spatial notions called *image schemas*. Proposed schemas include *paths* of motion with a beginning, end and particular shape; *links* between paths that represent their dependencies and causality; *containment* of one entity by another (plus derived ideas of opening and closing); and *support* of one entity by another.

These basic concepts are the earliest meanings that the mind represents, and can be used to make the kinds of distinctions that infants perform in the early months of life, such as between inanimate motion (simple path, with a visible causal link that initiates it) and inanimate motion (complex path with no visible inward link). The representations are continuous and dynamic rather than discrete and propositional as in language, but form the foundation of language acquisition. This, Mandler claims, represents a smaller step than going directly from sensory to conceptual representations. In positive news for this proposal, we know that children learn words which fit naturally into image schemas, such as "in" and "on", early on and in a virtually errorless fashion. It may be that these 'schema-friendly' words are the initial kernels of language that bootstrap the remainder of acquisition. 

### Nageshrao, Subramanya, Bruno Costa, and Dimitar Filev. “Interpretable Approximation of a Deep Reinforcement Learning Agent as a Set of If-Then Rules.” In *2019 18th IEEE International Conference On Machine Learning And Applications (ICMLA)*, 216–21, 2019.

A DDPG agent is trained to perform vehicle-following behaviour, based on three features: distance to the vehicle in front, relative speed, and the applied acceleration at the previous timestep. The output is also an acceleration. The results are competitive with two classic following models including the *intelligent driver model* (IDM).

This agent is cloned into a *first-order Takagi-Sugeno fuzzy rule-based system*. This model comprises a set of $R$ rules, where the $i$th rule has the form of 
$$
\textbf{if}\ \ x_1\sim\mathcal{N}(\mu_1^{(i)},\sigma_1^{(i)})\ \ \textbf{and}\ \ ...\ \ \textbf{if}\ \ x_n\sim\mathcal{N}(\mu_n^{(i)},\sigma_n^{(i)})\ \ \textbf{then}\ \ y^{(i)}=\alpha_0^{(i)}+\alpha_1^{(i)}x_1+...+\alpha_n^{(i)}x_n
$$
where $x$ is the input vector and each $\alpha$ is a coefficient. The firing level of this rule is
$$
\tau_{i}=p(x_{1}\vert\mu_1^{(i)},\sigma_1^{(i)}) \times ...\times p(x_n\vert\mu_n^{(i)},\sigma_n^{(i)})
$$
i.e. the product of the probability densities for each feature value within the corresponding normal distribution. The overall output of the model is 
$$
y=\frac{\sum_{i=1}^{R} \tau_{i}y_i}{\sum_{i=1}^{R} \tau_i}
$$
Fitting this model to demonstration data from the DDPG policy consists of two separate steps: (1) learning the focal points of each rule; (2) learning the coefficients of each linear sub-model. The *evolving Takagi-Sugeno* (ETS) method [reference 5] is used to solve this problem.

The resultant model imitates the DDPG controller's behaviour almost exactly, and can be completely written out in about half a page of text. 

## 🗝️  Key Insights

- The central idea of Burkart et al's work (and Wu et al's paper which inspired it) is a beautifully simple one: a bidirectional feedback loop between a black box model and its rule-based approximation. I feel there's something really powerful here. It is also remarkable to me that further approximating the rule base's size using a *second* black box works at all. If interpretability is truly our aim, this approach doesn't seem ideal.
- Graves et al's work on using DeepSHAP to enrich discriminator feedback in a GAN has a similar flavour of using interpretation tools as an active part of the learning process. In their context it seems to help with data efficiency, if not asymptotic performance. I'm sure there is much more work that could be done here.
- Mandler's paper provides a strong argument in favour of innateness of core semantic concepts in human infants. These primitives are not linguistic, but rather spatial.
- Nageshrao et al's approach to cloning a DDPG policy using fuzzy rules is startlingly effective in their chosen experimental context. Perhaps if we want to build high-fidelity imitations of black box agents, we must be willing to accept a bit of fuzziness.
