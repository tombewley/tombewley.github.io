---
title: 'Weekly Readings #5'
date: 2019-11-10
permalink: /posts/2019/11/weekly-readings-5/
tags:
  - weekly-readings
---

The theory of why-questions; fidelity versus accuracy; trees and programs as RL policies; partially-interpretable hybrids. 

## 📝 Papers

### Alvarez-Melis, David, Hal Daumé III, Jennifer Wortman Vaughan, and Hanna Wallach. “Weight of Evidence as a Basis for Human-Oriented Explanations.” *ArXiv:1910.13503 [Cs, Stat]*, October 29, 2019.

Machine explanations omit several properties that philosophers have claimed are so essential to human explanation. Explanations should:

1. be **contrastive**: explain why the output $y$ is produced instead of an alternative $y'$ rather than merely in absolute terms.
2. be **modular and compositional**: the ordering of *explanans* (attributes that can be included in the explanation) should not affect the result.
3. **not confound base rates** with the influence of the specific input. 
4. be **exhaustive**: explain with respect to every possible alternative $y'$. 
5. be **minimal**: all things being equal, the simpler of two explanations should be preferred, and if omission of some details improves intelligibility, then this should be done.

The *weight of evidence* (WoE) for a hypothesis $h$ in the presence of evidence $e$ and background information $c$ is defined as

$$
\text{woe}(h:e\vert c)=\log\frac{P(e\vert h,c)}{P(e\vert\neg h,c)}
$$

In general, if $\text{woe}(h:e|c)>0$ then $h$ is more likely under $e$ than marginally, i.e. the evidence speaks in favour of it. We can also calculate the WoE for $h$ in contrast to a specific alternative $h'$ as follows:

$$
\text{woe}(h/h':e)=\text{woe}(h:e|h\or h')=\log\frac{P(e\vert h,h\or h')}{P(e\vert h,h\or h')}
$$

Note how this definition already satisfies the first three desiderata. It is contrastive (1), normalised by base rates since it is conditioned on $h\or h'$ (3), and can also be shown to be compositional (2) in that

$$
\text{woe}\left(h / h^{\prime}: e_{1} \wedge e_{2} \wedge \cdots \wedge e_{n}\right)=\sum_{i=1}^{n} \log \frac{P\left(e_{i} \vert e_{i-1}, \ldots, e_{1}, h\right)}{P\left(e_{i} \vert e_{i-1}, \ldots, e_{1}, h^{\prime}\right)}
$$

In regression and classification, the obvious choice of hypothesis class is that of model outputs. The choice of explanans is restricted here to subsets of the raw input features $x$, but could be extended in future to higher-level representations of the input or properties of the model itself. The explanation process consists of computing the individual WoE for each attribute $e_i$ (enabled by decomposability). A selection of the only most positively-contributing attributes are identified and presented to the explainee, thereby satisfying the desideratum of minimality (5).

Where the number of possible outputs is large or continuous, it does not seem particularly meaningful for $h$ to be the actual prediction, and $h'$ to be the union of all other possibilities. In order to satisfy the desideratum of exhaustiveness (4), it is suggested that we cast explanation in this context as a sequential process, whereby a subset of the possible outcomes is expounded away in each step. For example, we might first explain why it's an animal not a plant, then why it's a bird not a reptile, then why it's a starling not a crow.

### Johansson, Ulf, Cecilia Sönströd, and Tuve Löfström. “Oracle Coached Decision Trees and Lists.” In *Advances in Intelligent Data Analysis IX*, edited by Paul R. Cohen, Niall M. Adams, and Michael R. Berthold, 6065:67–78. Berlin, Heidelberg: Springer Berlin Heidelberg, 2010.

The idea here is to build an opaque model called an oracle, then use this to make predictions for unlabeled 'production' data (which is seen as more easily accessible). *Both* the original training data and the oracle-labeled production data, are in turn used to train a transparent model. This method improves predictive performance compared to standard model induction using training data alone.

### Roth, Aaron M., Nicholay Topin, Pooyan Jamshidi, and Manuela Veloso. “Conservative Q-Improvement: Reinforcement Learning for an Interpretable Decision-Tree Policy.” *ArXiv:1907.01180 [Cs]*, July 2, 2019.

Rather than training a decision tree to explain a black box model, the aim here is to use the tree itself as an interpretable policy for an RL agent. The proposed algorithm is called *conservative Q-improvement* (CQI). 

Leaf nodes of the tree represent states. The tree is initialised as a single leaf node, and splits are added when the expected return of the new policy would increase by an amount exceeding a threshold. The threshold is gradually decremented during training, but is reset after each split (this enforces conservative splitting). Note that the method is strictly additive: no mechanism is included for removing splits. This could be a promising direction for future work.

In a given state $s$, an action $a$ is chosen based on the highest Q-values stored on the associated leaf (with added randomness to manage the explore-exploit tradeoff). Once the next state $s'$ is observed, a series of updates are performed:

- Q-values are updated using the Bellman equation.
- Candidate splits are evaluated based on the increase in expected reward, weighted by state visit frequency. 
- If the largest reward increase value exceeds the threshold, the split is made and the threshold is reset, otherwise, the threshold is decayed.

When testing on a simulated robot navigation problem, find that the method produces much smaller trees than the Pyeatt method (2003) without sacrificing performance. The conservative approach is lauded as the cause of this.

### Van Fraassen, Bas C. “The Pragmatic Theory of Explanation.” In *The Scientific Image*, 1980.

A theory of explanation is a theory of why-questions. Attempts have been made to reduce general language utterances to formal logical statements but these have failed, because so much about context is left unsaid, and we can only evaluate meaning relative to a context. 

Consider the following question and responses:

```
Can you get to Victoria both by ferry and by plane? 
	(a) Yes. 
	(b) You can get to Victoria both by ferry and by plane. 
	(c) You can get to Victoria by ferry. 
	(d) You can get to Victoria both by ferry and by plane, but the ferry ride is not to be missed. 
	(e) You can certainly get to Victoria by ferry, and that is something not to be missed. 
```

`(b)` is the purest form of answer here – a *direct* answer – and `(a)` is a *code* for this same answer. `(c)` is a *partial* answer since it is implied by `(b)` but not vice versa. `(d)` is a *complete* answer since it implies `(b)`, and it also says more besides. Note that nothing in this theory is concerned with whether or not a given answer is true. There is a set of direct answers to any question, and much larger sets of partial and complete ones.

A crucial notion is that of *presupposition*. A presupposition of $Q$ is any proposition implied by all direct answers to $Q$. Presuppositions can be denied by a *corrective answer*, which is a new type not seen in the above example (e.g. "there's no such place as Victoria").

Additional presuppositions may be held by the questioner, as part of a theory $T$, but not directly implied by $Q$. The presence of these latent presuppositions can transform an ostensibly irrelevant answer into a partial, or even complete, one.

#### Why-Questions

Now consider the why-question: "why is this conductor warped?". The obvious presupposition here is that the conductor is indeed warped, and we call this proposition $P_k$ the *topic* of the question. 

A *contrast class* $X=\{P_1,...,P_k,...,P_n\}$ is a set of propositions which includes the topic.  In our example, valid contrast classes are that it is *this* conductor rather than any other one, or that this conductor has warped rather than retained its original shape. An answer seeks to differentiate $P_k$ from the rest of $X$. A counterfactually-phrased why-question implies which contrast class to use, but otherwise the answerer must attempt to infer the contrast class.

In addition, there is the rather vague notion of *explanatory relevance*, which determines which propositions count (e.g. prior events, causal mechanism descriptors) as explanatory factors for differentiating $P_k$ from the rest of $X$. The explanatory relevance relation $R$ must also usually be inferred. 

Therefore, the proposition $A$ is a direct answer to a why-question $Q=(P_k,X,R)$ if it has the relevance relation $R$, and $A\implies P_k\and(\forall i\neq k:\neg P_i)$. 

#### Evaluating Explanations

Given a certain body $K$ of accepted background theory, a why-question is said to *arise* if $K$ implies the central presupposition $P_k\and(\forall i\neq k:\neg P_i)$.

Suppose we have a why-question $Q=(P_k,X,R)$ that arises from $K$, and a set of candidate answers $A=\{A_1,...,A_m\}$. How good is each answer $A_i$? There are several factors here:

- The likelihood of $A_i$ being true given $K$;
- The extent to which $A_i$ favours $P_k$ over the rest of $X$ (this component may be given a statistical interpretation);
- The extent to which $A_i$ is made irrelevant by the other candidate answers in $A$.

[The author doesn't seem to have much confidence in how to formalise these considerations exactly.]

### Verma, Abhinav, Vijayaraghavan Murali, Rishabh Singh, Pushmeet Kohli, and Swarat Chaudhuri. “Programmatically Interpretable Reinforcement Learning.” *ArXiv Preprint ArXiv:1804.02477*, 2018.

Here the idea is to represent RL policies using a high-level, domain-specific programming language. This is done by a process inspired by imitation learning: training a conventional deep RL agent as an *oracle*, then conducting program search with the aim of minimising distance from the oracle policy. Note that this is not strict imitation learning because the aim is to learn a high-performing program *guided* by the neural policy, rather than to match the oracle exactly.

The POMDP formalism is used, whereby an observation-action history $h=(o_0,a_0,…,o_{k-1},a_{k-1},o_k)$ is mapped to an action $a_k$ via a policy $\pi$, with the aim of the maximising time-discounted sum of reward $R(\pi)$. In this framework, $h$ is the input for both the deep RL agent and the programmatic RL agent.

The learned programmatic policy is restricted by defining a prior syntactic skeleton called a *sketch* $S$, which permits a set of programs $||S||$. The goal is to find the program $e^*\in||S||$ which maximises reward. 

During program search, a distance measure between the oracle policy $\pi_o$ and the programmatic policy $\pi_p(=e)$ is computed on a set of 'interesting' histories $\mathcal{H}$. A difficulty is that the programmatic policy may encounter histories that are never seen under $\pi_o$. These, which are very likely to be the cases where the most help is needed, would be ignored in the distance measure. The challenge is addressed by gradually augmenting $\mathcal{H}$ with sampled histories from the current $\pi_p$ (e.g. the DAGGER algorithm).

On each iteration, the policy search algorithm generates a neighbourhood of programs that are structurally similar to the current one, and picks whichever minimises the distance from $\pi_o$ on $\mathcal{H}$. Learning stops when the iterative search fails to improve the estimated reward. Since the choice of initial program turns out to have a large effect on performance, the initialisation is itself done by randomly generating several, and choosing the one with minimum distance.

In the concrete example in the paper, the problem is to drive a simulated car quickly around a track by steering and accelerating via PID control. The chosen sketch allows the program to evaluate a set of Boolean conditions over the current sensor readings, then chose among a set of discretised PID controllers. The learned $\pi_p$ performs slightly worse than $\pi_o$ on the training track, but far better on unseen test tracks (on which the neural policy cannot even complete a lap). It is also acknowledged that the transparency and determinism of a programmatic policy allows us to find theoretical bounds on action and performance using conventional verification techniques. This could be very useful in safety-critical domains.

### Wang, Tong. “Gaining Free or Low-Cost Transparency with Interpretable Partial Substitute,” 2019, 10.

The idea here is to learn an interpretable (hybrid rule set; HyRS) model for a subset of data where the full black-box model is 'overkill', to gain interpretability at minimal cost to performance. The result is neither a fully-interpretable model, nor a post-hoc explanation tool, but rather a partially-interpretable hybrid. This idea is motivated by human institutional decision making.

The task of binary classification is considered. A HyRS model $\mathcal{R}$ consists of two sets of rules, $\mathcal{R_+}$ and $\mathcal{R_-}$, which capture positive and negative instances respectively. If a given instance $\textbf{x}_k$ satisfies any positive rules it is classified as positive. Otherwise, if it satisfies any negative rules it is classified as negative. If neither of the above apply, no decision is made and the instance is sent to a black-box model $f_b$. Our aim is to optimise $\mathcal{R}$ in such a way that balances:

- The predictive *performance* of the hybrid, as measured by the misclassification rate on a dataset;
- The *interpretability*, as measured [naïvely] by the total number of rules in $\mathcal{R}$;
- The *transparency*, as measured by the percentage of instances to which $\mathcal{R}$ applies.

The loss function $\mathcal{L}(\mathcal{R})$ used is a weighted linear combination of the above three metrics. A stochastic optimisation algorithm is developed that, on each iteration $t$, seeks to improve one of the three metrics by adding or removing a rule. Whether a rule is added or removed is generally selected at random, but two hard bounds are defined on rule set size and transparency, which, when violated, force the next proposal to be a removal or addition respectively.

The proposed change is accepted with probability 

$$
\exp\left(\frac{\mathcal{L}(\mathcal{R}_t)-\mathcal{L}(\mathcal{R}_{t+1})}{C_0^{1-1/t}}\right)
$$

where the denominator acts as a temperature parameter which decays from an initial value of $C_0$. Promising candidate rules are generated using an off-the-shelf rule miner called `FP-growth`, before being further pruned according to their support on the dataset. The optimisation algorithm searches only within the space of pruned candidates.

In experiments on real binary classification datasets, a surprising degree of transparency is shown to be achievable with minimal loss in predictive performance. The hybrid models always exhibit better performance than pure rule sets alone.

### Zhou, Zhi-Hua. “Rule Extraction: Using Neural Networks or for Neural Networks?” *Journal of Computer Science and Technology* 19, no. 2 (March 2004): 249–53.

Existing research around model distillation [and imitation learning in general?] confuses two goals: (1) obtaining accurate and comprehensible learning systems; and (2) understanding the working mechanism of black box models. It is crucial that in future we distinguish (1) rule extraction *using* complex models from (2) rule extraction *for* complex models.

Rule extraction performance is typically evaluated through some combination of **fidelity** (to the model), **accuracy** (on the underlying data itself), **consistency** (of rule extraction from different datasets) and **comprehensibility** (as measured by rule count and length). This is the *FACC* framework.

We can think of accuracy as the ability to approximate the optimal problem-solving function $h(x)$, and fidelity as the ability to approximate the function learnt by the black box model $f_b(x)$. Unless the model is perfect, optimising for these is not the same problem!

As a consequence, there is a tradeoff between fidelity and accuracy. Which should we care about? It depends on which of the two goals we are pursuing, and in fact, there is an argument for thinking *we should never really care about both*. Thus the FACC framework should be split into (1) ACC and (2) FCC.

## 📚  Books

### Pearl, J. (2009). *Causality*. Cambridge University Press; 2nd Edition.

In the second half of chapter 2 we look at causal discovery when we only have partial observability of the data distribution. A variant of the IC algorithm, called IC*, takes a stable probability distribution and returns a *marked* pattern, which has an additional edge type to represent either a directed path or a latent common cause.  The take-home message of this chapter is: 

> No causes in, no causes out; Occam's razor in, some causes out.

In chapter, 3, we seek to infer causal relationships from a combination of data, experiments, and prior causal assumptions. We start by looking at Markovian models, whose causal diagrams are acyclic and whose noise terms $\varepsilon$ (which are in turn summarisations of unobserved background variables) are independent. An intervention in a Markovian model can be conceptualised in two ways:

- As a *modification* of the structural equations. From this perspective, setting variable $X$ to value $x$ (called the *atomic* intervention and denoted $do(X=x)$) consists of removing the equation entirely.

- As an *augmentation* of the causal diagram with additional variables which serve to modulate the structural equations. Here, $do(X=x)$ consists of conditioning on a value of an additional variable $F$ which serves to render $X$ independent of its parents, for example:

  $$
  X=\left\{\begin{array} ex&\text{if}\ F=force\\f(pa_X,\varepsilon_X)&\text{otherwise}\end{array}\right.
  $$

### Singer, P. (2011). *Practical Ethics*. Cambridge University Press; 2nd Edition.

When it comes to the problem of environmental protection, specifically the prevention of ecosystem destruction, a question quickly arises: to what extent does non-sentient life have moral value? The answer given by so-called *deep ecologists* is "a lot". But a utilitarian rejects the idea, not least because as soon as non-sentient systems are given value, there is no clear reason why the reach should not extend further to every object in the universe. Do not fear though, because the utility of natural ecosystems to sentient beings is more than sufficient for us to have a strong obligation to protect them.

## 🗝️  Key Insights

- What makes explanation such a tricky concept is not some mystical status, but rather its dependence on more factors than mere description. An explanation is not a description; it is an answer to a specific question arising from context $K$, and defined by its topic $P_k$, contrast class $X$ and relevance relation $R$, which are rarely all made explicit.
- The weight of evidence measure is a simple way to quantify feature influence, that satisfies several desiderata derived from consideration of human explanation.
- When deriving an interpretable model from a black box one, we must be aware of our end goal: do we want a high-performing model, or an accurate clone? Optimising for each requires a different approach.
- Pyaett's method of decision tree induction for RL seems to be the *de facto* standard, though it seems interpretability can be further improved by being conservative about the addition of branches.
- Another kind of interpretable policy representation for RL is as a deterministic program. This approach is promising because it enables us to manually instantiate a policy prior, and is amenable to formal verification.

- Hybrid models of interpretable and black-box components are an interesting 'third' class of methods, beyond full interpretability and post-hoc explanation. They afford a smooth tradeoff between performance and comprehensibility.
- Some progress can be made on the causal discovery problem even if we do not have full observability, using the IC* algorithm.