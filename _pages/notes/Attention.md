---
title: Attention
permalink: /notes/Attention
---
*Note: traditional attention was first used as a mechanism to improve the performance of [RNN](RNN)s. The [Attention is All You Need](Attention%20is%20All%20You%20Need) paper proposed self-attention as a complete replacement for the RNN itself, which has subsequently proven to be more performant as well as faster due to the lack of reliance on sequential processing.*

Just like [RNN](RNN)s and 1D [CNN](CNN)s, self-attention is a sequence-to-sequence operation. Let $X\in\mathbb{R}^{l\times d}$ be a length-$l$ sequence of length-$d$ feature vectors. The core of self-attention is a matrix multiplication $Y=W(XV)$, where $W\in\mathbb{R}^{l\times l}$ is an *attention weight* matrix and $V\in\mathbb{R}^{d \times d}$ is a *value* matrix that performs a linear transformation in the feature space. $Y$ is thus a sequence of the same shape as $X$.

$V$ is a single matrix of parameters, as in a traditional linear model, but $W$ is decomposed as follows:

$$
W=\text{softmax}\left(\frac{(XQ)(XK)^\top}{\sqrt{d}}\right)=\text{softmax}\left(X\left(\frac{QK^\top}{\sqrt{d}}\right)X^\top\right).
$$

Here, $Q$ and $K$ perform two additional linear transformations in the feature space, the $\text{softmax}$ ensures that attention weights sum to $1$, and the division by $\sqrt{d}$ is a trick to prevent vanishing gradients after the $\text{softmax}$. Intuitions for the meaning of $(XQ)(XK)^\top$ include:
- Something similar to the computation of user-item similarity in recommender systems.
- A kind of [autocorrelation](https://en.wikipedia.org/wiki/Autocorrelation) operation between the transformed versions of $X$ (more visible in the rearrangement on the right).

The typical intuition for the entire operation $W(XV)$ is that it is **a soft version of a key-value lookup**. For this reason, $XQ$ is often called the *query*, $XK$ is the *key*, and $XV$ is the *value*.
- [This LessWrong post](https://www.lesswrong.com/posts/euam65XjigaCJQkcN/an-analogy-for-understanding-transformers) further asks us to imagine elements of the sequence as people stood in a line. We can think of the query as a question that each person in the line shouts out to everyone else, the interaction between queries and keys determining who replies, and the values being the content of these replies. 

In a practical self-attention module, the operation is batched across multiple input sequences. In addition, it is common to implement multiple parallel *heads* with independent $Q$, $K$ and $V$ matrices, enabling the encoding of multiple ways in which elements of the sequence can relate to each other. Since the vast majority of computation is matrix multiplication, attention modules can be cheaply parallelised, which in turn makes it practical to stack many end-to-end in large architectures. 

The basic self-attention mechanism is really more of a *set-to-set* operation than a sequence-to-sequence one, because no explicit positional information is used. This means that permuting the input results in an identical but permuted output. In many domains positional information is important. A simple way of reintroducing this is to simply add an embedding vector representing the position to the feature vector for each instance, as a kind of positional *watermark*. The embedding can either be learnt (simple but no guarantee of generalisation beyond sequence lengths encountered during training) or hand-coded (the "is all you need" authors used a sinusoidal representation). Recent work has also explored using relative positional embeddings.

Additionally, basic self-attention allows each instance to attend to any other, but many sequential applications have a *causal* constraint that they should only be able to look backwards. This is done using masking arrays.
