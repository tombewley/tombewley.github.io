---
title: 'Weekly Readings #23'
date: 2020-03-29
permalink: /posts/2020/03/weekly-readings-23/
excerpt: 'Explanatory debugging; latent canonicalisations; the perceptual user interface; automatic curriculum learning.'
tags:
  - weekly-readings
---


## 📝 Papers

### Kulesza, Todd, Margaret Burnett, Weng-Keen Wong, and Simone Stumpf. ‘Principles of Explanatory Debugging to Personalize Interactive Machine Learning’. In *Proceedings of the 20th International Conference on Intelligent User Interfaces - IUI ’15*, 126–37. Atlanta, Georgia, USA: ACM Press, 2015.

This paper sits within the field of *interactive machine learning*, and aims to tune learning models through and iterative train-explain-feedback-correct loop. In order for this to work well, the explanations need to be sound and complete, but not filled with overwhelming detail. The model also needs to able to actually correct itself based on the feedback given.

The method proposed here, called *EluciDebug*, is deployed in the context of topic classification for a document $d$. The classification model is basic multi-class Naive Bayes, which computes the probability of each topic $c$ by independently considering the probability $P(w\vert c)$ of each word $w_n$ in the document:

$$
P(w_n\vert c)=\frac{p_{nc}+f_{nc}}{\sum_{x=1}^N(p_{xc}+f_{nc})}
$$

where $N$ is the number of words in the corpus, $f_{nc}$ is the number of occurrences of $w_n$ in documents of topic $c$, and $p_{nc}$ is a smoothing term (usually $1$) to prevent the equation from yielding $0$. The product of these values for all words in $d$ is combined it with the prior $P(c)$ via Bayes rule to obtain $P(c\vert d)$. 

The model is explained by choosing a foil class $c'$ and showing a bar chart comparing $P(w_n\vert c)$ and $P(w_n\vert c')$ for a selection of the most important words by information gain. These charts is interactive: users can drag bars up and down according to their views on word relevance, and also add words to / remove words from the model's consideration. This feature-based feedback is honoured by increasing or decreasing the smoothing terms $p_{nc}$. In order to prevent this feedback from decreasing in importance as more data are added to the training set, the smoothing terms are constantly recalculated to keep $\sum f_{xc} / \sum p_{xc}$ constant. Users can also provide instance-based feedback to reclassify a document, in which case that document is added to the training set.

User experiments showed *EluciDebug* leads to $50\%$ faster improvement of the classifier (by F1 score) than a control without the explanatory visualisations, and builds better models amongst the users as measured by their ability to predict classifications.

### Litany, Or, Ari Morcos, Srinath Sridhar, Leonidas Guibas, and Judy Hoffman. ‘Representation Learning Through Latent Canonicalizations’. *ArXiv:2002.11829 [Cs, Stat]*, 26 February 2020.

The key to low-dimensional representation learning is a good choice of regularisation. Here, the regularisation is on *the way the representation can be manipulated* rather than on the structure of the representation itself. The idea is to instil the property that supposed latent generative factors can be individually manipulated through simple linear transformations of the representation.

The implementation uses, among others, a dataset of digits. The latent generative factors considered are the rotation, scale and vertical/horizontal positioning of the digits. 

The core of the model is an autoencoder, to which a noised image $\bar{x}$ is fed as input (adding noise is commonly done to create more robust representations). The $m$-dimensional representation $z$ is then transformed by one or more $m\times m$ matrices called *canonicalisers*, each of which represents one of the generative factors, producing a modified vector $z_c$. Either $z$ or $z_c$ can be fed into the decoder. The system is trained with three losses:

- L2 distance between the decoder output given $z$ and the raw input image $x$. This is the vanilla loss for a denoising autoencoder.
- L2 distance between the decoder output given $z_c$ and a manually "canonicalised" version of the raw input image $x_c$, which means one that has been modified to set the latent factors associated with the applied canonicalisers to a fixed value. For example, if the rotation canonicaliser has been applied, $x_c$ is a straightened version of the input image.
- Error of a classifier that uses $z$ to make predictions about the content of $x$. For the digits dataset, this is just the digit identity. 

The three losses are added in a weighted sum, and optimised jointly. In addition to the parameters of the decoder, encoder and classifier, the canonicaliser matrices are themselves learned.

Performance is quantified, and compared to simpler baselines, in terms of the classifier accuracy. It is shown to outperform these baselines, especially when the size of the available dataset is limited. Good sim2real performance (train on synthetic images, test on real ones) is also demonstrated.

### Mark, Justin T., Brian B. Marion, and Donald D. Hoffman. ‘Natural Selection and Veridical Perceptions’. *Journal of Theoretical Biology* 266, no. 4 (October 2010): 504–15. 

This paper provides theoretical and experimental evidence *against* the popular belief that evolution favours truthful perceptions of the external environment. This negative result stems from the fact that in realistic evolutionary scenarios, information is not free, but instead incurs time and energy costs. What fares better is a "user interface" which hides much of the structural and causal complexity of the real world.

Let $X$ be a set of perceptions. Relationships between the perceptions can be represented using a map $\phi$ that takes in $X$, or a subset of $2^X$ denoted $\mathcal{X}$. For example, the distance relationship can be expressed with $\phi:X\times X\rightarrow[0,\infty)$ and probabilistic relationships can be expressed with $\mathcal{X}\rightarrow[0,1]$. Equivalently define $W$, $\mathcal{W}$ and $\psi$ respectively for the states of the objective environment and relationships thereof.

A *perceptual strategy* is a map $g:W\rightarrow X$. The notion of a *more-or-less truthful* perception can be formalised as various kinds of constraint on $g$. In the most extreme case, $g$ is an identity function. 

Various perceptual strategies are explored in the context of simple evolutionary games in which multiple agents must take turns to choose options harbouring finite resources. In the most interesting example, utility is non-monotonic with resource quantity, reflecting the idea that it is possible to have 'too much'. A *truthful* strategy, which observes actual resource quantities, is compared with a *simple* strategy that observes either *red* or *green* depending on whether the quantity is above a threshold, and an *interface* strategy which also observes colours, but with thresholds that are tied to the latent utility rather than the objective quantity. A cost is placed on strategies according to the bits of information in their perceptions, and simpler strategies are allowed to choose first. The overall payoff (cost minus utility from resources) is used  used to modulate reproductive success, and therefore the proportion of agents in the next generation with that strategy.

Long story short, it is shown that in many cases the simple strategy dominates the truthful one, and the interface strategy dominates both. Its perceptions are shaped not to depict reality, but to *reflect utility*. This is far more important from an evolutionary perspective.

### Portelas, Rémy, Cédric Colas, Lilian Weng, Katja Hofmann, and Pierre-Yves Oudeyer. ‘Automatic Curriculum Learning For Deep RL: A Short Survey’. *ArXiv:2003.04664 [Cs, Stat]*, 10 March 2020.

*Automatic Curriculum Learning* (ACL) is the authors' unifying term for mechanisms that continually adapt learning scenarios in response to the capabilities of an RL agent, in order to optimise some surrogate objective for the agent's global learning progress. Such mechanisms may be useful when target tasks cannot be solved directly due to being too complex or having extremely sparse rewards, or for training generalist agents that can work in a variety of task environments. 

Within the remit of ACL are all elements of the broad MDP formulation outside of the agent itself. Previous works surveyed in this paper have explored:

- Taking control of per-episode state initialisation (starting with easier ones, 'closer' to goal states); 
- Shaping the reward function to guide fruitful exploration;
- Modifying the contents of the environment and, if appropriate, the behaviour of other agents; 
- Selecting informative transitions from the agent's replay memory to learn from.

Surrogate objectives to optimise have included short-term reward [though this risks convergence towards trivial tasks], the gradual increase of task difficulty as measured by a third party 'judge' model, and less direct metrics such as state diversity and agent surprise.  

The authors believe that ACL could serve as a significant step towards truly open-ended learning systems, but that far more work is needed to build theoretical understanding through systematic studies. 

### Yampolskiy, Roman V. ‘Unexplainability and Incomprehensibility of Artificial Intelligence’, 2019, 14.

This paper cites a broad range of theoretical results to support the claim that the decisions of superintelligent AI (and even today's large deep learning models) are fundamentally incomprehensible in that a lossless description of them cannot be understood by beings as limited as humans are, and using the conceptual tools available to us. It doesn't really offer any solutions to this conundrum, however.

## 🗝️  Key Insights

- Kulesza et al's implementation of explanatory debugging is simple, but clearly demonstrates how such interaction could be beneficial and help to engender trust. Such interaction needs to go beyond feature importance! 
- Litany et al add to an expanding list of regularisation approaches for creating useful low-dimensional representations, in this case using the idea of basic *transformations* of a state which should have reliable effects. It would be interesting to see how this transfers beyond the image domain. 
- While the situations explored are abstract and basic, Mark et al's paper is a good form of argument in favour of the "user interface" model of representation in evolved systems, where resources are limited.
- Portelas et al help to draw attention towards the value of optimising the environment around a learning agent, in addition to the agent itself. This is likely to be possible only in simulation.
- To me Yampolskiy's paper seems defeatist due to of its excessive ambition. Since when have we understood *any system* in its entirety? We still manage to live save and productive lives regardless.
