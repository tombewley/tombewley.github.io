---
title: Codebook Features - Sparse and Discrete Interpretability for Neural Networks
permalink: /notes/Codebook Features - Sparse and Discrete Interpretability for Neural Networks
collection: notes
---
[2024](2024) [ICML](ICML) #Content/Paper by [Alex Tamkin](Alex%20Tamkin), [Mohammad Taufeeque](Mohammad%20Taufeeque), and [Noah D. Goodman](Noah%20D.%20Goodman).

This paper proposes an alternative solution to the [superposition problem](Toy%20Models%20of%20Superposition) to the one embodied in [Dictionary Learning](Dictionary%20Learning): rather than learning a post hoc sparse representation, enforce one in the model itself.

The basic idea is to replace the activations $a\in\mathbb{R}^D$ in a chosen hidden layer of a pre-trained model with the sum of $k$ *code vectors* $\sum_{i=1}^k c_i:c_i\in\mathbb{R}^D$ taken from a finite *codebook* of size $F\gg k$ (and I think $F \gg D$). The chosen $c_i$ are the members of the codebook with the $k$ highest cosine similarities to the original activation, $\frac{a\cdot c_i}{\|a\|\|c_i\|}$. The model is then fine-tuned with the original training loss, plus a stabilising term that prevents the code vectors from growing in magnitude. [Straight-through estimation](Straight-through%20estimation) is used to enable gradient-based optimisation despite the discrete choice of codes.

It is noted that codebook features embody a view of *features-as-points* rather than the *features-as-directions* perspective of the [Linear Representation Hypothesis](Linear%20Representation%20Hypothesis).

[The Interpretability of Codebooks in Model-Based Reinforcement Learning is Limited](The%20Interpretability%20of%20Codebooks%20in%20Model-Based%20Reinforcement%20Learning%20is%20Limited) seems to suggest that the method doesn't work very well for interpreting RL agent representations.