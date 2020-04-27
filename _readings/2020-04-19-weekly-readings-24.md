---
title: 'Weekly Readings #24'
date: 2020-04-19
permalink: /posts/2020/04/weekly-readings-24/
excerpt: 'Trustworthy AI; unifying imitation and policy gradient; soft decision trees; SRL with dimension specialisation.'
tags:
  - weekly-readings
---


## 📝 Papers

### Brundage, Miles, Shahar Avin, Jasmine Wang, Haydn Belfield, Gretchen Krueger, Gillian Hadfield, Heidy Khlaaf, et al. ‘Toward Trustworthy AI Development: Mechanisms for Supporting Verifiable Claims’. *ArXiv:2004.07213 [Cs]*, 15 April 2020.

There is growing interest in the problem of AI safety: ensuring deployed AI is safe, secure, fair, privacy-preserving, and ultimately beneficial to humanity.

This paper is the output of an April 2019 [workshop](www.towardtrustworthyai.com), and aims to go beyond good intentions and "ethics washing" to claims that are **verifiable** (through arguments and evidence) about the trustworthiness of AI systems. It is acknowledged that this forms just one part of the solution to AI safety.

Viewing AI development as a sociotechnical system, the authors divide the discussion into three areas.

Firstly, they consider institutional mechanisms to shape the incentives and constrain the behaviour of people. Many of the ideas are taken from the cybersecurity industry.

- Problem: The AI development process is often opaque to those outside a given organisation, making scrutiny and claim verification difficult.
  - Solution: **Third-party auditing** against agreed-upon standards of institutional behaviour.  
- Problem: AI development has many "unknown unknown" risks, whose discovery is not directly incentivised.
  - Solution: **Red team exercises**, in which groups adopt an adversarial mindset and methods in an attempt to reveal flaws and vulnerabilities. Red teams could even be permanently embedded within research groups.
- Problem: There is little incentive for unaffiliated individuals to seek out and report problems of AI bias and safety.
  - Solution: **Bias and safety bounties**, with appropriate compensation rates for different severities of issue. It may be challenging to implement these without introducing perverse incentives.
- Problem: Cases of undesirable behaviour by AI are rarely shared publicly, thereby preventing widespread learning from mistakes.
  - Solution: **Centralised infrastructure for incident reporting**, managed by a trusted, transparent third party, which protects organisations from undue reputational harm, and publishes useful, actionable information.

The second category of mechanisms concern the AI software itself. Key technical issues are robustness to distributional shift and adversarial examples, the accurate characterisation of error profiles, and statistical agnosticism with respect to protected variables (e.g. demographic).

- Problem: We do not record the steps taken throughout the design and development of AI systems, leading to a lack of accountability.
  - Solution: **Audit trails** for safety-critical applications, similar to those used in the aviation and nuclear industries. Version control tools may be an important part of the picture.
- Problem: Opaque internal mechanisms make it difficult to verify claims about black-box AI systems.
  - Solution: Additional funding for interpretability research, with a focus on practically facilitating auditing and risk assessment. Beyond well-studied feature attribution methods, the authors suggest:
    - Further clarification of the *objectives* of interpretability research;
    - Studying the *provenance* of a learned model as a function of its training data, architecture and optimisation algorithm, rather than treating it as fixed;
    - Constraining models to be interpretable by *default* rather than attaching post-hoc mechanisms.
- Problem: AI developers typically lack the skills for implementing privacy safeguards, and the standards for evaluating them.
  - Solution: Widespread education on, and robust open-source frameworks for, **Privacy-preserving ML** techniques such as federated learning, differential privacy and encrypted computation.

The final set of mechanisms relate to computing hardware.

- Problem: Specialised ML hardware lacks many security features seen on commodity systems.
  - Solution: Industrial-academic collaborations to develop the required **hardware security**. 
- Problem: There are no standards for measuring computational resource use during AI development, making it hard to verify claims and reproduce results from publications.
  - Solution: Pilot experiments with **detailed accounting of resource use** for some case study projects. This will hopefully highlight the key challenges.
- Problem: An increasing gap in computing resources between industry and academia, which makes it difficult to scrutinise technical claims made by industrial developers.
  - Solution: increased government funding of **hardware for academia**, and potentially centralised national computing infrastructure.

### Cheng, Ching-An, Xinyan Yan, Nolan Wagener, and Byron Boots. ‘Fast Policy Learning through Imitation and Reinforcement’. *ArXiv:1805.10413 [Cs, Stat]*, 25 May 2018.

Some prior attempts have been made to bring value information into imitation learning, but they lack theoretical bases or guarantees. The authors propose that unification of imitation learning and (policy gradient) reinforcement learning is possible through the framework of *mirror descent*, with the difference being in the direction of the update. 

For policy gradient, the loss is derived from an *advantage* estimate 

$$
A_\pi(s,a)=Q_\pi(s,a)-V_\pi(s)
$$

and for imitation learning, the loss comes from an estimate of *proximity* (e.g. MSE, MAE, KL divergence...) to an oracle policy $$\pi^\ast$$. Policy gradient yields a monotonically-improving policy sequence, while imitation gradient generates a policy sequence that improves on average.

The `LOKI` algorithm combines the two: first perform $$k$$ steps of mirror descent with an imitation gradient, then switch to policy gradient for the rest of the steps. This is shown to have a similar effect to running policy gradient directly from the oracle policy $$\pi^\ast$$. 

During the imitation phase, the `DAgger` approach is followed, whereby the training data $$\mathcal{D}_n$$ are collected online by rolling out the current policy $$\pi$$. In parallel, the advantage function $$A_\pi$$ is also learned.

During the reinforcement phase we switch to traditional policy gradient, initially using the $$A_\pi$$ we have already, but updating this continually alongside $$\pi$$.

Experiments show that `LOKI` initially follows the quick imitation learning path of `DAgger`, but then continues learning beyond the performance of $$\pi^*$$. The result is a rate of learning far higher than performing RL from scratch, as well as a couple of prior attempts to integrate value into IL. It's also really simple!

### Olaru, Cristina, and Louis Wehenkel. ‘A Complete Fuzzy Decision Tree Technique’. *Fuzzy Sets and Systems* 138, no. 2 (September 2003): 221–54.

This paper proposes a new fuzzy decision tree method called *soft decision trees* (SDT). It includes growing and pruning process. The stated motivation for using fuzzy decision trees is the increased parameter-level stability compared with crisp trees.

In a fuzzy decision tree, both classification and regression problems can be framed in terms of prediction of membership. For multi-class problems, the authors propose a forest of SDTs, with one per class.

STD induction comprises three stages:

- **Growth**: a tree structure is grown outwards from the root in the same order as in a crisp decision tree. At each decision node, the optimal crisp splitting variable, threshold $$\alpha$$ and left and right child labels $$L_L$$ and $$L_R$$ are determined using the impurity method from CART. The departure comes through the introduction of a width parameter $$\beta$$, which changes the membership function from a step to piece-wise linear (similar results were obtained with sigmoidal). A *Fibonacci search* is conducted find the optimal $$\beta$$, recomputing $$L_L$$ and $$L_R$$ for each candidate value. This approach is rather naive, because it assumes the optimal values for $$\alpha$$ and $$\beta$$ are independent, but experiments suggest the assumption is not too unreasonable.

- **Pruning**: once a stopping criterion is met (not too important; just needs to be large enough), a recursive pruning process is followed (similar to MCCP) which creates a nested sequence of sub-trees. The one which minimises mean absolute error on a pruning set is chosen. It is acknowledged that there are plenty more avenues for improvement of this stage.

- **Tuning**: this stage refines the parameters. Two approaches are considered:

  - **Re-fitting**, which optimises the leaf labels only. This problem can be solved by matrix inversion ($$\textbf{q}^\ast$$ is the vector of leaf labels, $$M$$ is the matrix of leaf memberships for a pruning dataset, $$\textbf{y}$$ is the vector of sample labels):

    $$
    \textbf{q}^\ast=(M^\text{T} M)^{-1}M^{\text{T}}\textbf{y}
    $$
    
    **Back-fitting**, which optimises all free parameters. The model is linear in its leaf prediction parameters (hence the matrix technique above) but nonlinear (piecewise linear) in the decision node parameters $$\alpha$$ and $$\beta$$. Loss gradients for these are obtained by backpropagation, and the loss is minimised using the *Levenberg-Marquardt* optimisation technique.

### Pérez-Dattari, Rodrigo, Carlos Celemin, Giovanni Franzese, Javier Ruiz-del-Solar, and Jens Kober. ‘Interactive Learning of Temporal Features for Control’, 2020, 12.

A framework is proposed for robots to learn both state representations and policies using occasional corrective teacher feedback.

The model architecture centres around an LSTM, trained to predict $o_{t+1}$ from $o_t$. The LSTM's hidden state $h_t$ is used as the state representation for $\pi$.s

The entire architecture is trained via various active learning schemes including DAgger, HG-DAgger (teacher chooses when to provide feedback) and Deep COACH (teacher gives only the sign of the action change to make). Experiments are done in simulation with both human and [unspecified] simulated teachers, and on physical robotic systems with human teachers.

### Raffin, Antonin, Ashley Hill, René Traoré, Timothée Lesort, Natalia Díaz-Rodríguez, and David Filliat. ‘Decoupling Feature Extraction from Policy Learning: Assessing Benefits of State Representation Learning in Goal Based Robotics’. *ArXiv:1901.08651 [Cs, Stat]*, 23 June 2019. 

This paper presents experimental results to demonstrate the usefulness of separating state representation learning (SRL) from policy learning (RL).

SRL is completed as a supervised learning task on a dataset of $20,000$ samples from a random policy in the environment. A combination of three losses is used: 

- Inverse dynamics: prediction of $a_t$ given consecutive representations $s_t$ and $s_{t+1}$ and a linear dynamics model.
- Auto-encoder: reconstruction of $o_t$ from $s_t$ (it is noted that this usually needs more dimensions in $s_t$ than is theoretically necessary).
- Reward prediction: prediction of $r_t$ given $s_t$ and $a_t$ [I think].

These losses are combined into a single objective, with weights chosen so as to produce gradients with similar magnitudes. It is found that applying the reconstruction and reward losses to the first $198$ dimensions of $s_t$, and the inverse dynamics loss to the remaining $2$, improves final performance. It seems like enforcing *specialisation* of the dimensions of $s_t$ is beneficial.

When $s_t$ is used as the input to RL (PPO), it yields faster and more robust learning than from raw pixels, coming closer to what's achieved using ground truth state variables. Interestingly, using a completely random low-dimensional representation doesn't do that much worse than a carefully learned one (though obviously this is terrible for interpretability).

## 🗝️  Key Insights

- Brundage et al's thorough review of trustworthy AI makes more concrete proposals than those seen before. It is interesting to see how many of these relate to social and organisational systems. For my area of interpretability, it's interesting to see the suggestion that model provenance should get more focus, rather than just the post-learning state.

- Cheng et al's `LOKI` paper does a good job of showing that imitation learning and policy gradient RL are conceptually rather similar, and that this opens up the possibility of hybrid, best-of-both training schemes.

- Olaru and Wehenkel's fuzzy decision tree variant goes beyond those I've seen before (e.g. Suarez and Lutsko) because it incorporates growth and pruning rather than assuming a fixed tree topology. This seems to be made possible by keeping the constraint of testing one feature per node.

- Raffin et al's work provides more evidence of the value of compact state representations for rapid learning, and it's interesting to see them encoding additional knowledge by encouraging specialisation of particular dimensions. I'm not quite sure what to make of the effectiveness of random state representations though; it suggests most of the benefit is simply in the low dimensionality itself!

  
