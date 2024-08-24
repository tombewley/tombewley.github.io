---
title: Dictionary Learning
permalink: /notes/Dictionary Learning
---
One of three approaches to alleviating superposition suggested in Anthropic's [toy models](Toy%20Models%20of%20Superposition) blog post, which has a long history in the sparse coding literature and may even be [a strategy employed by the brain](Sparse%20coding%20with%20an%20overcomplete%20basis%20set:%20A%20strategy%20employed%20by%20V1?).

It was initially most vigorously pursued in a series of reports culminating in [Sparse Autoencoders Find Highly Interpretable Features in Language Models](Sparse%20Autoencoders%20Find%20Highly%20Interpretable%20Features%20in%20Language%20Models). Anthropic then came out with the [towards monosemanticity](Towards%20Monosemanticity%20-%20Decomposing%20Language%20Models%20With%20Dictionary%20Learning) and [scaling monosemanticity](Scaling%20Monosemanticity%20-%20Extracting%20Interpretable%20Features%20from%20Claude%203%20Sonnet) posts, which are detailed demonstrations of essentially the same technique at increasing scales. Work in this area has since exploded, making it the hottest ticket in [mechanistic interpretability](mechanistic%20interpretability) as of mid-2024.

---

The preeminent model for dictionary learning is a sparse autoencoder (SAE), which has a single latent layer whose dimensionality is (unconventionally) much *higher* than that of the representation space being studied.

Let $x\in \mathbb{R}^D$ be the representation at a particular point in a model (for transformers, often the residual stream in a middle-ish layer), normalised so the mean L2 norm of each dimension is constant (typically $\sqrt{D}$ or $1$). The encoder part of the SAE maps $x$ to a vector of $F\gg D$ *latents*:
$$
f(x) \coloneqq \sigma(W^{enc}x + b^{enc}),
$$
which are always non-negative due to the activation function $\sigma$ (JumpReLU seems SoTA?). The decoder is a linear mapping of the latents back into a reconstruction of $x$:
$$
\hat{x} \coloneqq W^{dec} f(x) + b^{dec}.
$$
We can interpret $W^{dec}$ as associating each latent $i\in\{1,\dots,F\}$ with a direction in the representation space, that we can call a *feature*:
$$
\text{feature}_i = \frac{W^{dec}_{:, i}}{\|W^{dec}_{:, i}\|_2}
$$
The activation of feature $i$ for representation $x$ can be defined as 
$$
\text{activation}_i(x) = f_i(x) \cdot \|W^{dec}_{:, i}\|_2
$$
SAEs are trained with a loss function combining an L2 penalty on the reconstruction loss and a sparsity penality:
$$
\mathcal{L}=\mathbb{E}_x\Big[\|x-\hat{x}\|_2^2 + \lambda\ \text{sparsity}(x)\Big]
$$

[This Anthropic blog post](https://transformer-circuits.pub/2024/april-update/index.html#training-saes) uses an L1 penalty on feature activations (but they may now accept this is no longer SoTA):
$$
\text{sparsity}(x)=\sum_i |f_i(x)| \cdot \|W^{dec}_{:, i}\|_2.
$$
 The [Gemma Scope](Gemma%20Scope:%20Open%20Sparse%20Autoencoders%20Everywhere%20All%20At%20Once%20on%20Gemma%202) paper, which open-sources over $400$ learnt dictionaries for several layer of the Gemma 2 models, uses an L0 penalty on latent activations ([straight-through estimation](straight-through%20estimation) is required to make backprop work with this):
$$
\text{sparsity}(x)=\|f(x)\|_0.
$$

---

Find dataset examples with maximum $\text{activation}_i(x)$, compare to random examples. Interpret through manual inspection or another LM.

cosine similarity between feature vectors maps roughly onto conceptual relatedness. 

---

The Gemma Scope paper outlines many open problems, of which I find the following most interesting:

1. Exploring the structure and relationships between SAE features, as suggested in [Relational composition in neural networks - A gentle survey and call to action](Relational%20composition%20in%20neural%20networks%20-%20A%20gentle%20survey%20and%20call%20to%20action).
2. Comparisons of residual stream SAE features across layers, e.g. are there persistent features that one can match up across adjacent layers?
3. Better understanding the phenomenon of feature splitting, where high-level features in a small SAE break apart into several finer-grained features in a wider SAE.
4. We know that SAEs introduce error, and completely miss out on some features that are captured by wider SAEs. Can we quantify and easily measure “how much” they miss and how much this matters in practice?
5. Using SAEs to improve performance on real-world tasks, e.g. through steering.
6. Do SAEs really find the “true” concepts in a model? How robust are claims about the interpretability of SAE features? How can we measure intepretability?
7. Can SAEs be extended to find *nonlinear* features, such as those that live in low-rank subspaces [Not All Language Model Features Are Linear](Not%20All%20Language%20Model%20Features%20Are%20Linear), or even those that don't?
8. Understand how features contribute to circuits, e.g. [Sparse feature circuits - Discovering and editing interpretable causal graphs in language models](Sparse%20feature%20circuits%20-%20Discovering%20and%20editing%20interpretable%20causal%20graphs%20in%20language%20models).