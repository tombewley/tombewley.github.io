---
title: 'Weekly Readings #15'
date: 2020-01-26
permalink: /posts/2020/01/weekly-readings-15/
tags:
  - weekly-readings
---

xxx; xxx.

## 📝 Papers

### Chernova, Sonia, and Manuela Veloso. “Confidence-Based Policy Learning from Demonstration Using Gaussian Mixture Models.” In *Proceedings of the 6th International Joint Conference on Autonomous Agents and Multiagent Systems - AAMAS ’07*, 1. Honolulu, Hawaii: ACM Press, 2007.

Introduce the  *confident execution framework* for the interactive learning of behavioural policies from demonstration (in this case, by a human). For each action in the discrete action space, the student agent periodically re-fits a Gaussian mixture model over the state space using the expectation-maximisation algorithm. Initially, it does this using collected observation data alone, but once its prediction accuracy exceeds a threshold, the training process moves into the 'confident execution phase'. Here, the agent itself chooses actions to take (by identifying the maximum-likelihood Gaussian mixture), unless its confidence is below a fixed value, in which case it defers to the human teacher, adds the newly-created datapoint to its training set, and re-fits. Thus we have a system of *variable autonomy* that can be smoothly modulated via the choice of thresholds.

The trickiest technical aspect of the training process is the choice of number of components for each Gaussian mixture (which may differ between actions). This is addressed by concurrently fitting a range of models with different numbers, and picking the optimal one using the *Akaike Information Criterion*. 

In a couple of experimental environments (corridor navigation and motorway lane-changing), the main stated benefit of the framework over non-interactive learning is sample efficiency: by focusing on areas of uncertainty, we seem to be able to reduce the amount of demonstration data required to achieve a given prediction accuracy. [In general though, we see remarkably little actual performance improvement. Perhaps this is because by waiting until confidence is below a threshold to train, we risk missing where the critical mistake is made? We've already fallen off the distribution at this point.]

### Hesslow, Germund. “The Problem of Causal Selection.” In *Contemporary Science and Natural Explanation. Commonsense Conceptions of Causality*, edited by Denis J. Hilton. Harvester Press, 1988.

Causal influence propagates along many parallel, arbitrarily-long paths that can be conceptualised in infinitely many ways. Given this reality, how are we able to speak of *the* cause of an explanandum, or more generally, how are we able to weight the relative importance of various candidate explanans? This is called the *causal selection problem*, to which several kinds of answer have been posed in the past:

- Unexpected conditions: we select those explanans that are assumed not to be already known by the explainee. This is quite a Bayesian notion, with the aim being to reduce their degree of 'surprise' that the explanandum occurred. A more formalised variant of this is *deviation from theoretical ideal*: when the explainee has a structured (e.g. scientific, economic) model of the domain of interest, we mention explanans that violate the common assumptions of that model.
- Abnormal conditions: we select those explanans that are unlikely to have been present in the counterfactual scenario where the explanandum does not occur. This is a more objective, frequentist notion than the above.

- Precipitating causes: we select those explanans that are most transient and came most recently before the event.
- Predictive value: we select those explanans that, had they been added to the explainee's knowledge state ahead of time, would have dramatically increased their posterior probability in the explanandum. [I imagine this is often equivalent to unexpectedness.]
- Interest: a more loosely-defined notion relating to the known motivations and objectives of the explainee. What do they hope to *do* with your explanation?

Various attempts have been made to reach a rough compromise between these and other criteria (e.g. van Fraasen, 1980), but Hesslow aims to transcend them by posing a different question. Rather selecting explanans for a given explanandum, we ask **what exactly is the explanandum itself**? If we know the answer to this question, **the relevant selections become logically compelling** and the subjectivity evaporates.

Hesslow claims that when asking for an explanation, we are always implicitly asking a counterfactual question about why an event occurred, while one or more other events (the *reference class*) did not. Hence, **explananda are differences**, which are resolved by providing exactly the information that differs between the two cases.

By analysing cases where different explanations are provided to ostensibly identical queries, we can see that in fact they differ by the choice of reference class. If we compare an event to what is statistically normal, it makes sense to select abnormal conditions. If we compare an event to the states preceding it, it makes sense to select precipitating causes.

The difficulty here clearly comes from the fact that reference classes are very often implicit, and are biased by our experience and education. [An AI explanation system must be able to figure out the explainee's reference class!]

### Rosset, Corbin. “A Review of Online Decision Tree Learning Algorithms,” 2015.

This paper reviews the most impactful online tree induction algorithms:

1. **ID4** (1986): the first substantial step away from batch algorithms. When a new instance arrives we pass it down the tree, re-doing the impurity calculation at each step. If we find that the current split is no longer the most informative, we prune the subtree from this point. When we arrive at a leaf node (either due to pruning or regular propagation), and that node is impure, we try to split it using conventional impurity gain calculations. The split is only accepted if a $\chi^2$ test is passed; this mitigates overfitting. We continue to split recursively until the leaf is pure or the $\chi^2$ test is failed. A risk of ID4 is "thrashing" in which we don't stably converge to any ordering of splits.

2. **ID5R** (1989): here we do a little better, by restructuring rather than discarding inaccurate subtrees. The restructuring step, called a "pull-up", rearranges a subtree so that the desired test attribute is at the root. Unfortunately the paper offers little more detail than this. ID5R is guaranteed to build the same tree as the basic ID3 algorithm, given the same instances.

3. **ID5R version 2, ITI **(1997): this paper does a better job of explaining ID5R, while introducing some minor revisions. When a new instance arrives we pass it to a leaf node. If it matches the majority class, happy days. If not, we consider this to be a 'vote' to split the node and attempt to do so (recursively). Once this is done, we traverse the tree to check that the best attribute is tested at each node. If not, we recursively transpose the tests in each two-level subtree until the best test is at the node [what if the test doesn't exist in the subtree?] If the best attribute is used, but the wrong cut-point is chosen, we adjust it, but then must be careful to redistribute all instances in the subtree to their correct leaves. We then proceed further down the tree and make more adjustments if required. Experiments in the paper show that the computational cost of these revisions is generally much lower than rebuilding from scratch.

4. **Very Fast Decision Tree, VFDT** (2000): Here each new instance triggers an attempt to split the node it reaches, as long as a statistical test based on the *Hoeffding bound* (later replaced with something called the multivariate delta method) is passed. A pruning mechanism is also incorporated. The result is an extremely efficient algorithm that is claimed to outperform batch learners.

5. **Concept-adapting Very Fast Decision Tree, CVFDT** (2001): VFDT assumes stationarity of concepts over time, which is not applicable in all contexts. This minor variant performs all the same calculation, but only considers a moving window of the $n$ most recently-seen instances, effectively forgetting all others.

6. **Online Adaptive Decision Tree, OADT** (2004): This is a novel algorithm for binary classification tree induction that uses ideas from neural networks. Each decision node encodes a decision hyperplane in the feature space, and computes an activation value for its left and right child nodes, which are in turn used to compute their own activations. The final activation of each node is the product of all its predecessors. Unlike most decision trees, this model can be trained by gradient-based methods.

Finally notes that ID5R should be seen as the de facto standard for online tree induction, against which new approaches should be benchmarked. 

### Harmelen, Frank van, and Annette ten Teije. “A Boxology of Design Patterns for Hybrid Learning and Reasoning Systems.” *Journal of Web Engineering* 18, no. 1 (2019): 97–124.

This paper attempts to structure the debate around hybrid AI through a set of *design patterns* that summarise all previously-proposed integrations. In the notation used, `(ML)` refers to a machine learning system, `(KR)` is a knowledge representation system, `[sym]` is 'model-based' (symbolic / relational) knowledge and `[data]` is 'model-free' data. The patterns are:

1. Learning with symbolic input and output (e.g. inductive logic programming, Markov logic networks).

```
[sym]-->(ML)-->[sym]
```

2. From symbols to data and back again (e.g. ML systems that use knowledge graphs as inputs and outputs).

```
[sym]-->(ML)-->[data]-->(ML)-->[sym]
```

3. Learning from data with symbolic output (e.g. ontology learning from text).

```
[data]-->(ML)-->[sym]
```

4. Explainable learning systems.

```
[data]-->(ML)-->[sym]-->(KR)-->[sym]
```

5. Explainable learning systems with background knowledge.

```
					   [sym]
						 |
                         V
[data]-->(ML)-->[sym]-->(KR)-->[sym]
```

6. Explainable learning systems through inspection (cloning).

```
[data]-->(ML)-->[data]
   |              |
   ----->(KR)<-----
           |
           V
  [sym (explanation)]
```

7. Learning an intermediate abstraction for learning (representation learning).

```
[data]-->(ML)-->[sym]-->(ML)-->[data]
```

8. Learning an intermediate abstraction for reasoning (e.g. AlphaGo RL + MCTS).

```[data]-->(ML)-->[sym]-->(ML)-->[data]
[data]-->(ML)-->[sym]-->(KR)-->[sym]
```

9. Deriving an intermediate abstraction for learning (representation construction).

```
		[sym]
		  |
		  V
[data]-->(KR)-->[sym]-->(ML)-->[data]
```

10. Learning with symbolic information as a prior (e.g. logic tensor networks).

```
		[sym]
		  |
		  V
[data]-->(ML)-->[data]
```

11. Learning with derived symbolic information as a prior.

```
[sym]-->(KR)-->[sym]
		         |
		         V
       [data]-->(ML)-->[data]
```

12. Meta-reasoning for control (`(KR)` maintains a symbolic representation of an `(ML)` system).

```
..............................
.                            .
.   [data]-->(ML)-->[data]   .--[sym]-->(KR)
.                            .
..............................
```

13. Learning to reason (observing `(KR)` enables `(ML)` to mimic its behaviour).

```
                                 [sym (query)]
............................            |
.                          .            V
.   [sym]-->(KR)-->[sym]   .--[data]-->(ML)-->[sym]
.                          .            
............................
```

### Zhang, Ying, Tao Xiang, Timothy M. Hospedales, and Huchuan Lu. “Deep Mutual Learning.” *ArXiv:1706.00384 [Cs]*, June 1, 2017.

Small neural networks often have the same representational capacity as large ones, but are more difficult to optimise. Model distillation (large $\rightarrow$ small model via soft class probabilities and/or feature representation) is often able to achieve superior performance compared with direct learning, because it conveys additional information beyond raw class labels. Here the authors propose an alternative to distillation called *mutual learning*, in which a cohort of initially-untrained student models simultaneously learn to solve a task while sharing some representational information in their loss functions.

In this paper we consider a two-model cohort, and classification problems. The loss function for network $\Theta_2$ is
$$
L_{\Theta_{2}}=L_{C_{2}}+D_{K L}\left(\boldsymbol{p}_{1} \| \boldsymbol{p}_{2}\right)
$$
where $L_{C_2}$ is a conventional cross-entropy error and $D_{K L}\left(\boldsymbol{p}_{1} \| \boldsymbol{p}_{2}\right)$ is the KL distance between the softmax output distributions of the two models. The models can be optimised concurrently with stochastic gradient descent. 

Experiments with popular datasets indicate mutual learning significantly outperforms both independent learning and distillation [though the latter comparison is a little unfair as an equally-small network is used as the teacher]. This approach can easily be generalised to larger cohorts by using the mean KL distance in the loss function, and some additional experiments suggest that we get a (sublinear) increase in performance with cohort size.

Why does mutual learning work at all? The suggestion is that the pooling of information incentivises higher posterior entropy. This in turn helps us to find a wider and more robust minima that generalise better to test data (by 'not putting all our eggs in one basket'). This bears resemblance to entropy regularisation approaches.

## 🗝️  Key Insights

- x
- x
- x