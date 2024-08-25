---
title: Toy Models of Superposition
permalink: /notes/Toy Models of Superposition
---
[2022](2022) #Content/Blog by Nelson Elhage, Tristan Hume, Catherine Olsson, Nicholas Schiefer, Tom Henighan, Shauna Kravec, Zac Hatfield-Dodds, Robert Lasenby, Dawn Drain, Carol Chen, Roger Grosse, Sam McCandlish, Jared Kaplan, Dario Amodei, Martin Wattenberg, and [Chris Olah](Chris%20Olah).

This post operates on the basis of the [linear representation hypothesis](linear%20representation%20hypothesis) that semantic features can be understood as directions in models' activation spaces (alternative perspectives: [Not All Language Model Features Are Linear](Not%20All%20Language%20Model%20Features%20Are%20Linear), [Interpreting Neural Networks through the Polytope Lens](Interpreting%20Neural%20Networks%20through%20the%20Polytope%20Lens)).

It begins by carefully defining three terms:
- **Polysemanticity**: The empirically-verified phenomenon that single dimensions in activation spaces ("neurons") often correlate with multiple unrelated features.
- **No privileged basis**: One hypothesised contributor to polysemanticity, namely that the basis defined by the neurons has limited meaning to the model.
	- However, subtle properties of activation functions, regularisers and optimisers (especially Adam) means that it often does have some meaning. This may explain why we can sometimes find monosemantic "Jennifer Aniston neurons".
- **Superposition**: Another hypothesised contributor to polysemanticity, namely that the number of features $F$ that the model "wants" to represent exceeds the number of neurons $D$, requiring them to be non-orthogonal.
	- Note: the Johnson–Lindenstrauss lemma says that it's possible to pack $\exp(D)$ "almost orthogonal" ($<\epsilon$ cosine similarity) vectors into a $D$-dimensional space.

It then uses theory and toy model experiments to demonstrate that superposition never emerges in linear models, but *does* emerge in neural networks with nonlinear activation functions.
- One reason why this okay: the thresholding of ReLU activations can "silence" small interferences.

Initially assuming that all features have uniform importance in the data, it is shown that models achieve the lowest amount of *interference* (non-orthogonality) by partitioning feature directions into mutually-orthogonal subspaces. This arrangement is called a *tegum product*. Furthermore, within each subspace (called a *tegum factor*), features are arranged in regular polytopes, strongly resembling solutions to the [Thomson problem](https://en.wikipedia.org/wiki/Thomson_problem).
- Note: if a given tegum factor has as many dimensions as it contains features, its polytope can be a simplex, which has zero interference.

As features start to have non-uniform importance, the polytopes are smoothly deformed away from regular to prioritise the orthogonality of important features, up to critical phase changes where the representation snaps to a different polytope. This snapping may collapse one or more low-importance features to zero.

Correlated features are those that commonly occur together and anticorrelated features are those that rarely occur together. Models prefer to represent anticorrelated features with opposite directions and correlated ones with orthogonal directions (i.e. in different tegum factors). If they can't achieve this, models prefer correlated features to have positive dot products rather than negative ones. Finally, if two features become "too" correlated, the model collapses them into the same direction. This seems to be quite a strong phenomenon.
- Later work [The Geometry of Categorical and Hierarchical Concepts in Large Language Models](The%20Geometry%20of%20Categorical%20and%20Hierarchical%20Concepts%20in%20Large%20Language%20Models) also seems to support this idea.

As a result, (not-too-)correlated features may form an (almost-) orthogonal local basis. *"If this result holds in real neural networks, it suggests we might be able to make a kind of "local non-superposition" assumption, where for certain sub-distributions we can assume that the activating features are not in superposition. This could be a powerful result, allowing us to confidently use methods such as PCA which might not be principled to generally use in the context of superposition... However, if our goal is to eventually make useful statements about the safety of models, we need mechanistic accounts that hold for the full distribution (and off distribution). Local bases seem unlikely to give this to us."*

Some additional points:
- [This figure](https://transformer-circuits.pub/2022/toy_model/index.html#learning-geometric) is an absolutely beautiful case study of how these various geometric structures emerge in a stepwise fashion over learning.
- Superposition of unrelated features might partly explain why adversarial examples exist.
