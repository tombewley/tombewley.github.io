---
title: Attention
permalink: /notes/Attention
---
*Note: traditional attention was first used as a mechanism to improve the performance of [RNN](RNN)s. The [Attention is All You Need](Attention%20is%20All%20You%20Need) paper proposed self-attention as a complete replacement for the RNN itself, which has subsequently proven to be more performant as well as faster due to the lack of reliance on sequential processing.*

https://peterbloem.nl/blog/transformers

Just like RNNs and 1D CNNs, self-attention is a sequence-to-sequence operation. Let $\textbf{X}$ be a length-$l$ sequence of $n$ features. The core of self-attention is a matrix multiplication $\textbf{Y}=\textbf{W}(\textbf{XV})$, where $\textbf{W}$ is the *attention weight* matrix of size $l\times l$, and $\textbf{V}$ is an $n\times n$ *value* matrix that performs a linear transformation in feature space ($\textbf{Y}$ is thus a sequence of the same shape as $\textbf{X}$). $\textbf{V}$ is learnt as a single set of parameters, as in a traditional linear model, but $\textbf{W}$ is decomposed as follows:
$$
\textbf{W}=\text{softmax}\left(\frac{(\textbf{XQ})(\textbf{XK})^\top}{\sqrt{n}}\right)=\text{softmax}\left(\textbf{X}\left(\frac{\textbf{QK}^\top}{\sqrt{n}}\right)\textbf{X}^\top\right).
$$
Here, $\textbf{Q}$ and $\textbf{K}$ perform two additional linear transformations in feature space, the $\text{softmax}$ ensures that attention weights sum to $1$, and the division by $\sqrt{n}$ is a trick to prevent vanishing gradients after the $\text{softmax}$. Intuitions for the meaning of $(\textbf{XQ})(\textbf{XK})^\top$ include:
- Something similar to the computation of user-item similarity in recommender systems.
- A kind of [autocorrelation](https://en.wikipedia.org/wiki/Autocorrelation) operation between the transformed versions of $\textbf{X}$ (more visible in the rearrangement on the right).

The typical intuition for the entire operation $\textbf{W}(\textbf{XV})$ is:
- A soft version of a key-value lookup dictionary. For this reason, $\textbf{XQ}$ is often called the *query*, $\textbf{XK}$ is the *key*, and $\textbf{XV}$ is the *value*.

In a practical self-attention module, the operation is batched across multiple input sequences. In addition, it is common to implement multiple parallel *heads* with independent $\textbf{Q}$, $\textbf{K}$ and $\textbf{V}$ matrices, enabling the encoding of multiple ways in which instances can relate to each other. Since the vast majority of computation is matrix multiplication, attention modules can be cheaply parallelised, which in turn makes it practical to stack many end-to-end in large architectures. 

The basic self-attention mechanism is really more of a *set-to-set* operation than a sequence-to-sequence one, because no explicit positional information is used. This means that permuting the input results in an identical but permuted output. In many domains positional information is important. A simple way of reintroducing this is to simply add an embedding vector representing the position to the feature vector for each instance, as a kind of positional *watermark*. The embedding can either be learnt (simple but no guarantee of generalisation beyond sequence lengths encountered during training) or hand-coded (the "is all you need" authors used a sinusoidal representation). Recent work has also explored using relative positional embeddings.

Additionally, basic self-attention allows each instance to attend to any other, but many sequential applications have a *causal* constraint that they should only be able to look backwards. This is done using masking arrays.

The term *transformer* doesn't have a clear definition, but in general is used to refer to any neural sequence-to-sequence model where the *only* interaction between instances is through attention. They also make use of basic feedforward layers with nonlinear activations, where a lot of the representational heavy lifting happens, and layer normalisation.