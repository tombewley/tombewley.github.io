---
title: A Mathematical Framework for Transformer Circuits
permalink: /notes/A Mathematical Framework for Transformer Circuits
collection: notes
---
[2021](2021) #Content/Paper by Nelson Elhage, Neel Nanda, Catherine Olsson, Tom Henighan, Nicholas Joseph, Ben Mann, Amanda Askell, Yuntao Bai, Anna Chen, Tom Conerly, Nova DasSarma, Dawn Drain, Deep Ganguli, Zac Hatfield-Dodds, Danny Hernandez, Andy Jones, Jackson Kernion, Liane Lovitt, Kamal Ndousse, Dario Amodei, Tom Brown, Jack Clark, Jared Kaplan, Sam McCandlish, and [Chris Olah](Chris%20Olah). There's also an accompanying YouTube playlist [here](https://www.youtube.com/watch?v=V3NQaDR3xI4) and walkthrough by Neel Nanda [here](https://www.youtube.com/watch?v=KV5gbOmHbjU)

Since so much of the basic computation done in [transformers](Transformer) is linear algebra, there are many possible factorisations giving rise to different intuitive stories of how they work. This paper advocates for a particular one.

The start of the story is the recognition that individual [attention](Attention) heads operate on low-dimensional projections of the residual stream rather than the full space, allowing them to write to disjoint subspaces with minimal interaction. In turn, we can think of a forward pass as decomposing into mostly-independent paths of computation (i.e. [circuits](Zoom%20In%20-%20An%20Introduction%20to%20Circuits)) weaving in and out of the residual stream. From an interpretability perspective, we may hope that only a few of these are critical to model behaviour in any given situation.
- #Comment - This view seems to de-emphasise the residual stream itself as a target for interpretability. With [Dictionary Learning](Dictionary%20Learning), this is now firmly back on the table.

This perspective is applied to small decoder-only transformer models containing up to two layers of attention heads and *no* fully-connected MLP layers. The complexity of the analysis is built up by adding one layer at a time.

**Zero-layer:** the only path is that defined by the product of the embedding and un-embedding matrices. The optimal behaviour of this path is to approximate a lookup table for the log-likelihood of bigrams [...B] $\rightarrow$ C, and zero-layer transformers actually try to do this in practice.

**One-layer:** for an $n$-head attention layer, there are $n$ computation paths. The optimal behaviour of each path is to learn the log-likelihood of 'skip-trigrams' [...A...B] $\rightarrow$ C. Empirical investigations suggest that simple copying behaviour [...A...B] $\rightarrow$ A is often promoted.

**Two-layer:** the composition of successive attention operations means that much more powerful mechanisms start to emerge at this stage. A prominent example seems to be *induction heads*, which promote the repetition of bigram patterns [...AB...A] $\rightarrow$ B.
- The authors go on to study induction heads in much larger models in [a follow-up paper](In-context%20Learning%20and%20Induction%20Heads).
- Also virtual layers, which they speculate may become important for larger models.



