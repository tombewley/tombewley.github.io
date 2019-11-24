---
title: 'Weekly Readings #7'
date: 2019-11-24
permalink: /posts/2019/11/weekly-readings-7/
tags:
  - weekly-readings
---

Meta-learning causal relations; decomposing explanation questions; misleading explanations; the critical influence of metrics.

## 📝 Papers

### Dasgupta et al., “Causal Reasoning from Meta-Reinforcement Learning.” 2019.

Here model-free reinforcement learning is applied to meta-learn a learning algorithm for making predictions about a large family of $5$-node causal Bayesian networks (CBNs). In particular, the aim is to make the 'inner' learning algorithm causally-aware, that is: able to implicitly learn the environmental CBN. 

For the task environments, all valid $5$-node CBNs are generated. A root node of the CBN is always hidden to act as an unobserved confounder, so a state observation includes of the values of the remaining $4$. Each episode consists of $5$ timesteps. In the first $4$, called the *information phase*, the available action set allows the agent to choose which of the observable nodes will receive a fixed intervention for the next timestep. In the last timestep, called the *quiz phase*, one observable node is selected at random to be intervened on by the environment, and the agent is provided with a one-hot feature vector indicating which one. In this phase, actions consist of choosing which of the observable nodes will have the *highest value* under this observation. 

Hence, we can imagine two learning loops. In the 'inner' within-episode loop, the aim is to understand the CBM sufficiently to predict the intervention effect. In the 'outer' loop, which continues over many episodes, the aim is to improve the agent's ability to discover causal dependencies through interaction.

The agent is implemented as an LSTM network and trained through asynchronous advantage actor-critic. Performance is compared to that of stripped-back variants that are not capable of choosing interventions, and an optimal algorithm for associative reasoning that has full knowledge of the correlation structure of the environment but cannot do causal reasoning. It outperforms each of these, indicating that it is successfully learning an approximation of do-calculus. 

### Harbers, van den Bosch, and Meyer, “A Theoretical Framework for Explaining Agent Behaviour.” 2011.

The question *"why did you perform this action?"* is too general to be actionable and should instead be decomposed into five sub-questions:

1. *"What goal did you try to achieve?"* (here a *goal* is a tangible event or state)
2. *"Why did you want to achieve this goal?"* (reasons / values / incentives; also higher-level goals)
3. *"Why does this action help achieve this goal?"* (mechanisms)
4. *"Why did you perform this action at this particular time?"* (enabling factors)
5. *"Why did you perform this action and not another?"* (preferences / efficiencies)

To further complicate things, all of these questions can be answered within one of many *contexts*, such as psychological, physical, ethical or organisational, each of which has its own ontology. Some contexts enable informative, useful explanations, but others result in platitudes or excessive complexity.

When developing explanation frameworks, we must be cognisant of which question(s) we are seeking to answer, and with which ontology. 

### Kasirzadeh, “Mathematical Decisions and Non-Causal Elements of Explainable AI.” 2019.

Previous work on explainability has attempted to answer either of the following two explanatory questions:

- What is an *associational* explanation for the output given the input?

- What is a *causal* explanation for the output given the input? 


Both are therefore interested only in the learned function $\hat{f}$ that maps the input $x$ to the output $y$. But several wider questions can be asked about the machine learning pipeline under scrutiny, such as:

- Why are the particular set of *features* used as input to the learned function?

- Why is a particular kind of *statistical thinking* and optimisation appropriate for this problem?

- How does the choice of training *data* (and model *structure*) influence the output?


A hierarchical explanatory framework is proposed to place the various kinds of explanation in order of increasing locality to a specific decision:

1. **Structural**: justification of the chosen problem representation.
2. **Statistical**: choice of data and algorithms.
3. **Associational**: (in)dependencies between aspects of the learned model.
4. **Casual**: causal relations between aspects of the learned model.
5. **Example-based**: given in terms of real or synthetic data instances.

In addition, interpretability is defined very differently as the degree to which a given audience will be able to understand a system based on an explanation. It is extremely context-dependent.

### Lakkaraju and Bastani, “‘How Do I Fool You?’: Manipulating User Trust via Misleading Black Box Explanations.” 2019.

A high-fidelity explanation of a black box ML model, usually learnt through some kind of correlation analysis, may not accurately reflect the causal mechanisms and biases inside. In addition, there may be multiple, qualitatively different, high-fidelity explanations for the same model. As such, optimising for fidelity may produce misleading results, and induce unwarranted trust.

We consider the problem of learning an interpretable model $E$ to approximate a black-box one $B$, which may or may not be trustworthy. A human then may or may not trust $B$ as a result of their interactions with $E$. In this paper, trust worthiness / evaluation are quantified in terms of the presence of desired features in $B$ / $E$ and the absence of prohibited features (e.g. those that enable demographic discrimination). $E$ can be said to be *misleading* to the extent that the degree of trust does not match the trustworthiness. 

The `MUSE` algorithm can be used to produce interpretable explanations in the form of two-level decision sets. Here the algorithm is used to generate potentially misleading explanations by modifying the optimisation problem to ensure no prohibited features appear in $E$, even if they are being used by $B$. Misleading explanations are possible when prohibited features can be *reconstructed* from the remaining ones.

A user study is done with a bail decisions dataset (binary classification) where $B$ is itself an interpretable model, since this allows misleadingness to be evaluated. The prohibited features of race and gender are used by $B$ but not by $E$. Unsurprisingly, unwarranted levels of trust result. It is acknowledged that explanations based on correlation alone are often at risk of being misleading and lacking robustness; **causal explanations** may be needed to address these issues.

## 🎤 Talks

I spent Thursday and Friday at the **[1st International Alan Turing Conference on Decision Support and Recommender Systems](https://dsrs-turing.github.io/)**. In addition to giving a talk myself, I gleaned a variety of tasty morsels from the other speakers and attendees:

- **Prof.  Francisco Herrera (Granada)** presented work on the use of deep learning for weapon detection in video feeds, which highlighted for me how management of the precision / recall tradeoff in classification problems can become a problem of ethics and politics. Is it right to err on the side of the caution when this frames more innocent people as potential suspects?

- **Prof. Peter Flach (Bristol)** gave a series of robust criticisms of common evaluation metrics used in data science, explaining why precision-recall curves lack important linearity properties that are present in ROC curves, and why sigmoidal activation functions do not in general produce meaningful probability values for classification. A lack of theoretical rigour leads to overconfidence and potential compromises in performance, fairness and safety.
- **Haoyuan Zhang (UCL)** discussed how many stages of undocumented data aggregation and transformation within NHS computer systems cause valuable information to be lost and origin to be explored. Better documentation and innovative use of data structures could help to solve this issue.
- A **panel event on ethics, explainability and interpretability** helped to clarify the importance of avoiding conflated terms. Explanation (a communication task) differs from interpretation through transparency; process-based explanations differ from outcome-based ones; one-way, non-interactive explanations are unlikely to be sufficient.

- A general observation from the two days was that commercial implementations of machine learning are, almost without exception, very simple compared with what is studied in the academic literature. Why? Ease-of-understanding, ease-of-bug-fixing, ease-of-communication to corporate leaders, time pressure, diminishing returns from complexity, and many more factors besides.

## 🗝️  Key Insights

- The study of explanation in a computational context remains a relatively undeveloped field, and we are still feeling around for solid definitions of many important terms. Care and vigilance are important here.
- The fact that an explanatory mechanism shows high fidelity with a given problem representation says nothing about the appropriateness of that representation. With the wrong set of candidate explanans, an arbitrarily-high degree of misinformation is possible.
- Remarkably, it does seem to be possible to learn concepts as sophisticated as causal relation using the right kind of deep learning model. But what does the word 'learn' really mean in this context?

- The design of performance metrics is a hugely fraught issue in machine learning. The wrong metric may be not only misleading, but politically and ethically damaging. Could it be possible to *regulate* the model evaluation process?