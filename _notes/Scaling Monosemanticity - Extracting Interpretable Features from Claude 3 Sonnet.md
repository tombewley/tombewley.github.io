---
title: Scaling Monosemanticity - Extracting Interpretable Features from Claude 3 Sonnet
permalink: /notes/Scaling Monosemanticity - Extracting Interpretable Features from Claude 3 Sonnet
collection: notes
---
[2024](2024) #Content/Blog by Anthropic.

In the *Features as Computational Intermediates* section, it is mentioned that sorting by activation magnitude is a *bad* way to identify important features, especially those with a causal effect on the next token prediction. Instead, they find a causal feature set using much more involved attribution and ablation studies.

*"These features... ==are much harder to find by looking through the strongly active features==... only three out of the ten most strongly active features are among the ten features with highest ablation effect."*

Another way to find features relevant to a particular concept is to filter based on binary activity (ignoring magnitude) in paired sets of positive and negative examples:

*"Often the top-activating features on a prompt are related to syntax, punctuation, specific words, or other details of the prompt unrelated to the concept of interest. In such cases, we found it useful to select for features using sets of prompts, filtering for features active for all the prompts in the set. We often included complementary “negative” prompts and filtered for features that were also not active for those prompts."*