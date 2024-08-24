One of three approaches to alleviating superposition suggested in Anthropic's [[Toy Models of Superposition|toy models]] blog post, which has a long history in the sparse coding literature and may even be [[Sparse coding with an overcomplete basis set: A strategy employed by V1?|a strategy employed by the brain]].

It was initially most vigorously pursued in a series of reports culminating in [[Sparse Autoencoders Find Highly Interpretable Features in Language Models]]. Anthropic then came out with the [[Towards Monosemanticity - Decomposing Language Models With Dictionary Learning|towards monosemanticity]] and [[Scaling Monosemanticity - Extracting Interpretable Features from Claude 3 Sonnet|scaling monosemanticity]] posts, which are detailed demonstrations of essentially the same technique at increasing scales. Work in this area has since exploded, making it the hottest ticket in [[mechanistic interpretability]] as of mid-2024.

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
 The [[Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2|Gemma Scope]] paper, which open-sources over $400$ learnt dictionaries for several layer of the Gemma 2 models, uses an L0 penalty on latent activations ([[straight-through estimation]] is required to make backprop work with this):
$$
\text{sparsity}(x)=\|f(x)\|_0.
$$

---

Find dataset examples with maximum $\text{activation}_i(x)$, compare to random examples. Interpret through manual inspection or another LM.

cosine similarity between feature vectors maps roughly onto conceptual relatedness. 

---

The Gemma Scope paper outlines many open problems, of which I find the following most interesting:

1. Exploring the structure and relationships between SAE features, as suggested in [[Relational composition in neural networks - A gentle survey and call to action]].
2. Comparisons of residual stream SAE features across layers, e.g. are there persistent features that one can match up across adjacent layers?
3. Better understanding the phenomenon of feature splitting, where high-level features in a small SAE break apart into several finer-grained features in a wider SAE.
4. We know that SAEs introduce error, and completely miss out on some features that are captured by wider SAEs. Can we quantify and easily measure “how much” they miss and how much this matters in practice?
5. Using SAEs to improve performance on real-world tasks, e.g. through steering.
6. Do SAEs really find the “true” concepts in a model? How robust are claims about the interpretability of SAE features? How can we measure intepretability?
7. Can SAEs be extended to find *nonlinear* features, such as those that live in low-rank subspaces [[Not All Language Model Features Are Linear]], or even those that don't?
8. Understand how features contribute to circuits, e.g. [[Sparse feature circuits - Discovering and editing interpretable causal graphs in language models]].