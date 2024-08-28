---
title: Transformer
permalink: /notes/Transformer
collection: notes
---
The term "transformer" doesn't have a fully precise definition, but in general is used to refer to any neural sequence-to-sequence model where the *only* interaction between positions is through a sequence of multi-head [attention](Attention) layers that iteratively update a central embedding called a *residual stream* by addition.

Each attention head operates on a lower-dimensional linear projection of the residual stream embedding. The sum of the outputs of all heads in an attention layer are embedded (via another linear map) back into the residual stream. 

Transformers also include:
- (In decoder-only models, which are now dominant) causal masking in the attention heads to prevent earlier positions in the sequence attending to later ones. 
- (For domains involving tokenisation, e.g. language), embedding/un-embedding layers at the start/end to map between the token space and the residual stream.
- A positional encoding/embedding matrix, which is added to the residual stream immediately after the embedding layer.
- Fully-connected MLP layers that process each position in the sequence separately and again write their outputs to the residual stream by addition. This is where a lot of the representational heavy lifting happens.
	- MLP layers are typically alternated with the attention layers, with one such pair known as a *residual block*.
- Layer normalisation, which (much to the despair of interpretability researchers) screws with the nice almost-linearity of the whole network.
