---
title: 'Weekly Readings #3'
date: 2019-10-27
permalink: /posts/2019/10/weekly-readings-3/
tags:
  - weekly-readings
---

This week didn't involve very much reading since I focused instead on my practical investigation of the traffic coordination problem. Nonetheless, I encountered a variety of fascinating ideas.

## 📝 Papers

### Lakkaraju, Himabindu, Ece Kamar, Rich Caruana, and Jure Leskovec. “Interpretable & Explorable Approximations of Black Box Models.” *ArXiv:1707.01154 [Cs]*, July 4, 2017.

A model-agnostic framework is proposed for approximating black box classifiers using a *two-level decision set* (i.e. nested if-then statements) $\mathcal{R}$. The outer conditions $q$ are named the *neighbourhood descriptors* and the inner conditions $s$ are named the *decision logic*. Rule $i$ applies to an instance $x$ if that instance satisfies both $q_i$ and $s_i$. In this case, a class label $c_i$ is assigned. Three desirable properties are identified:

- **Fidelity**: accurately mimic the black box function $\mathcal{B}$ across the feature space. 
- **Unambiguity**: provide a single, deterministic rationale for every instance. 

- **Interpretability**: use a compact representation with few rules and few features.

These desiderata are quantified using a selection of [intuitively-derived?] formulae, which are in turn combined into a single optimisation problems using weights $\lambda$.

It is assumed that we already have banks of candidate conditions for both the neighbourhood descriptors $\mathcal{ND}$ and the decision logic $\mathcal{DL}$. These could be mined by an algorithm such as $\texttt{apriori}$. A user's interest in a subset of features $\mathcal{U}$ can be incorporated by setting $\mathcal{ND}$ to only contain conjunctions comprising those features. This provides interactivity.

The resultant system did better than baselines (interpretable decision sets and Bayesian rule lists) in studies where humans were asked to answer questions about neural network model deployed on a depression diagnosis dataset. The interactive capability improved performance.

### Nisbett, Richard E., and Timothy DeCamp Wilson. “Telling More Than We Can Know: Verbal Reports on Mental Processes.” *Psychological Review* 84, no. 3 (1977).

A wide range of experimental results are presented which demonstrate that people cannot reliably describe the causality of their decisions, ideas or actions. The theory that best explains all these results refers back to Tversky and Kahneman's work on cognitive biases: specifically the **representativeness** (statistical prominence and plausibility) and **availability** (visceral / emotional saliency) heuristics. 

Explanations are *not*, for the most part, produced by introspection. They are produced from *mental models* about how we (and people in general) tend to make decisions, which are in turn derived from culture and empirical observation. **Instead of inspecting our actual cognitive processes, we simply use our prior model to make calculations about representativeness (biased by availability)**. This means that in many cases, *observers* are just as effective at generating explanations for action as the actors themselves. A slight caveat applies where there are important idiosyncratic or contextual factors to which the observer has no access.

- Correct explanations really are *coincidences* in the purest sense: they are examples of coincidence between model and specific circumstance.

- We are 'aware' of our mental processes to the extent our explanations perform better than those produced from the representativeness / availability model alone.

Some additional considerations:

- We should expect our explanations to be especially bad when our mental processes themselves are subject to cognitive biases, since we know already that our intuitive models do not include them.
- Saving face: people may provide explanations to others that differ from the ones they would give themselves, because of an awareness of social status or norms.
- Expertise: when decision-making processes are formalised (e.g. clinical / legal settings) and rigorously followed, we should expect explanations to better align with actual reasoning.

Why don't we acknowledge any of this? Because it's uncomfortable.

## 📚  Books

### Molnar, C. (2019). *Interpretable machine learning. A Guide for Making Black Box Models Explainable*.

I've made my way through this book over the past couple of months, finishing it this week. It gives a great overview of current approaches to ML interpretability:

- **Interpretable models**: linear models, decision trees, rule sets.
- **Model-agnostic methods**: PDPs, ICEs, ALEs, feature importance, global and local surrogates, Shapley values.
- **Example-based explanations**: counterfactuals, adversarial examples, prototypes and criticisms, influential instances.
- **Neural network interpretation**: feature visualisation, network dissection.

Molnar finishes with some predictions. The goal of a machine learning model can never be perfectly specified, and *interpretability is necessary to close the mis-specification gap*. In sectors where safety and performance is critical, interpretability will be the catalyst for widespread adoption. Machine learning will be increasingly automated, and for this reason, *model-agnostic interpretability methods will be the focus*; it is easier to automate and scale interpretability when it is decoupled from the underlying model.

### Singer, P. (2011). *Practical Ethics*. Cambridge University Press; 2nd Edition.

This week I've made more progress on this book, which has touched the issues of euthanasia, charitable giving and the climate crisis. The key points I got from these chapters are as follows:

- **Euthanasia**: The utilitarian should also see no fundamental moral distinction between killing and 'letting die'. The latter is currently far more accepted than the former in medical practice, but in fact, it may actually lead to more needless suffering than a quick and deliberate act. Probably the strongest argument against euthanasia is that of the 'slippery slope': giving some the power of life or death over others could lead to Nazi-style extermination programs. The retort to this basically consists of an insistence that if euthanasia is properly regulated and scrutinised and a country remains democratic, there is no reason to expect this to happen.
- **Charitable giving**: The assertion that we should "look after our own" does hold some weight given the existence of a recognised system of responsibilities, which is itself evolutionary in origin. But the current $0.7\%$ target for developed countries' aid budgets still seems ludicrously low from the perspective of equal consideration of interests. In general, Singer strongly argues for giving as much as you can until the incremental (probability weighted) sacrifice exceeds the incremental benefit. What we should publicly advocate for, however, may be more modest, since we need to avoid the risk of demoralising others.
- **Climate change**: Climate change: we are not equipped with the right mental tools for thinking about the undetectable harm produced at a distance (in space and time) by our emissions. Legal obligation seems to be the only robust answer. The promising *cap and trade* idea goes as follows: everyone on earth is entitled to an equal share of the atmosphere, and as such has a fixed quota of carbon emissions ($2$ tonnes $CO_2$ equivalent has been suggested). It is unrealistic to expect industrialised nations to reduce this far in the short term, but many developing countries remain far below this level. A trading scheme, whereby individuals, countries and companies can buy carbon quota from others who will not use it, would lead to: (1) a net flow of money from rich to poor countries; and (2) a universal incentive to keep emissions low in order to retain saleable quota. Issues with this idea include verifiability [Blockchain???] and corrupt actors. But many economists believe that the cap and trade model is more efficient than carbon taxation and dividends.

## 🗝️  Key Insights

- Heuristics and intuition can be effectively deployed to quantify aspects of interpretability, and once we have quantification we can build an objective function. A possible recipe for learned semantics: unsupervised learning + heuristic desiderata. 
- It appears that humans make decisions and explain decisions using largely independent mental models. The latter model is a rough statistical approximation of the former [a kind of surrogate or clone?], though is heavily coloured by cultural norms and expectations.
- Model-agnostic interpretability methods are being developed thick and fast. None can claim to provide all the answers, but a 'toolbox' of many in concert, along with a healthy dose of domain knowledge, is potentially extremely powerful. Developers should focus on generality and modularity: interpretation as a service. 
- Once sufficient effort has been expended describing the core principles of utilitarianism, all manner of practical conclusions follow quite naturally. Increasing automation makes uncompromising implementation of these principles more tractable, but what if we have $0.1\%$ mis-specification error?