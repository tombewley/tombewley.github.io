---
title: 'Weekly Readings #18'
date: 2020-02-16
permalink: /posts/2020/02/weekly-readings-18/
tags:
  - weekly-readings
---

Formalising interpretation and explanation; operationally-meaningful representations; *Conceptual Spaces* book.

## 📝 Papers

### Ciatto, Giovanni, Davide Calvaresi, Michael I Schumacher, and Andrea Omicini. “An Abstract Framework for Agent-Based Explanations in AI.” In *Proc. of the 19th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2020)*, 4. Auckland, New Zealand, 2020.

The authors propose a nice, agent-oriented distinction between interpretation and explanation. The *interpretability* of an abstract object $O$ for an agent $A$, denoted $I_A(O)$, is a measure of the degree to which $A$ can assign a subjective meaning$^1$ to $O$ (here envisaged as a real number $\in[0,1]$). *Explaining* is the act of mapping $O$ into one with higher interpretability for $A$, denoted $O'$. We can think of this as creating an *ad hoc* metaphor aimed at increasing $A$'s understanding.

In the context of machine learning, the object to be interpreted is the conjunction of a model $M$ and a dataset $X$. Since this conjunction is not something that can be directly perceived, interpretation happens via some *representation* $R(M,X)$. Explaining the model to *fidelity $\delta$* and *clarity $\varepsilon$* consists of finding some other model $M'$ and representation $R'$ such that
$$
\ell(M(X),M'(X))\leq\delta\ \ \ \ \ \text{and}\ \ \ \ \ I_A(R'(M',X))-I_A(R(M,X))\geq\varepsilon
$$
where $\ell$ is a loss function that measures the similarity of the two models' predictions. Notice all the variables upon which the success of this exercise is contingent. In practice, we will be constrained by the classes to which $M'$ and $R'$ can belong; for a given model, certain representations are likely to be more 'natural' than others.

The key claims: interpretability is fully contingent on the explainee agent; explainability is separate from, but heavily dependent on, interpretability; representations are a crucial part of the process.

$^1$ [The biggest weakness of this paper is the lack of clarity as to what this term means. Does each $O$ have a canonical subjective meaning, or could it mean different things to different people? Which meaning(s) is/are 'correct'?]

#### Gallitz, Oliver, Oliver De Candido, Michael Botsch, and Wolfgang Utschick. “Interpretable Feature Generation Using Deep Neural Networks and Its Application to Lane Change Detection.” In *2019 IEEE Intelligent Transportation Systems Conference (ITSC)*, 3405–11, 2019.

The goal of this is to derive an alternative, interpretable representation of the *highD* dataset to better solve the task of lane-change prediction (i.e. classifying left, right or no change several timesteps in advance). 

To do this, a CNN is given a $100$-timestep time series of $6$ basic features (distance to vehicles ahead and behind in each lane) for the period preceding the lane change, which can be viewed as a $6\times100$ image. The first layer ("layer 1") performs 1D convolutions on each row of the image, effectively treating each feature separately. This preserves interpretability as each activation is still associated with a single feature and a single point in time. After this come a number of 2D convolutional and fully-connected layers. The CNN is trained to solve the classification task.

After this, layerwise relevance propagation is used to identify high-influence *hot regions* for each training instance, then a pruning step is used to remove near-duplicates, which leaves $690$ regions remaining. A selection of five hand-crafted features are derived from each (mean pixelwise step difference, mean signal energy, minimum and maximum values, corresponding layer 1 activation), and these $600\times5=3950$ features are used to train and post-prune a binary decision tree. 

Performance is shown to be better than using the original $600$ features (even after down-selection of the $500$ most useful derived features by permutation feature importance). It is also argued that interpretability is enhanced. Some of the new features are pretty indeed interpretable, representing the rate of change, minimum or maximum of one of the original features within a given time window, but the ones derived from signal energy and the layer 1 activations are not so intuitive.

### Khan, Omar Zia, Pascal Poupart, and James P Black. “Minimal Sufficient Explanations for Factored Markov Decision Processes,” 2009, 7.

Here the problem of explanation is framed as that of *demonstrating that an action is optimal*. This is done by exploiting an alternative representation of $V^\pi(s)$, different from the Bellman equation. In this representation, the value of a state $s$ under $\pi$ and with start state $s_0$ is the product of its expected visitation frequency $\lambda_{s_0}^\pi(s)$ and its reward value $r(s)$. This product is denoted $t_{s_0}^\pi(s)$. 

We construct a *minimal sufficient explanation* (MSE) of the optimality of action $a$ in state $s_0$ by computing all $t$ values for the scenario of taking $a$, and following the optimal policy* $\pi^\ast$ *thereafter. We order these $t$ values by magnitude, and pick the top $k$ such that the following relationship holds:

$$
\Bigg(\sum_{i\leq k}t_{s_0}^{\pi^\ast}(s_i)-\sum_{j>k}\lambda_{s_0}^{\pi^\ast}(s_j)\bar{r}\Bigg)>Q^{\pi^\ast}(s_0,a')\ \ \ \forall a'\neq a
$$

where $\bar{r}$ is the minimum possible reward in the environment, i.e. even if all other states gave the minimum reward, this selection of $t$ values is sufficient for us to beat the state-action value of taking any other action.

The MSE has the following form:

​	**"The agent takes $a$ in $s_0$ because"** for $i=1:k$:

​		**"it takes you to $s_i$ about $\lambda_{s_0}^\pi(s_i)$ times"**

​		If this is also more than for any other action:

​			**"which is higher than for any other action"**

This approach clearly requires use to be able to enumerate all states and know the optimal policy, which is not practical for large MDPs.

### Nautrup, Hendrik Poulsen, Tony Metger, Raban Iten, Sofiene Jerbi, Lea M. Trenkwalder, Henrik Wilming, Hans J. Briegel, and Renato Renner. “Operationally Meaningful Representations of Physical Systems in Neural Networks.” *ArXiv:2001.00593 [Quant-Ph]*, January 2, 2020.

The idea here is to produce disentangled, meaningful representations of physical systems by enforcing the need to use them for multiple tasks. The approach bears some similarity to that used in variational autoencoders, except here the regularisation term encourages data-efficient communication between a population of agents. 

Consider a population of agents, including $A$, the *encoding* agent, and $B_1,…,B_K$, the *decoding* agents. $A$ has access to a direct observation $o$ of the environment, and generates a parameterised representation $r=E(o)$. A filtered subset of this representation $\varphi_i(E(o))$ is communicated to each decoding agent $B_i$, which must combine it with a *question* $q_i$ to predict an *answer* $a_i=D_i(\varphi_i(E(o)),q_i)$. We initially assume that the correct answer $a_i^\ast$ is available from the environment, and can be used to assign a loss value $\mathcal{L}_{i}$ to the agent's prediction. 

- As an aside, the authors suggest this could easily be generalised to multiple encoding agents $A_1,…A_L$ which make different measurements of the system. We can further imagine each $A_i$ having a corresponding $B_i$ that act on the same subsystem, in which case it makes sense to think of them as being one and the same agent.

Given this setup, we can pose a learning problem for the population as a whole. We want a low prediction loss across the set of questions, but we want to *minimise the communication* between $A$ and $B_1,…,B_K$. This is done using a second loss term which counts the total number of features transmitted: $\mathcal{L}_f=\sum_i\text{dim}(\varphi_i)$. This second term is an example of what is often called a *prior* in representation learning.

In this paper, both the encoder $E$ and decoders $D_1,...D_K$ are implemented as neural networks. The filter functions $\varphi_1,…\varphi_K$ are not strictly filters, but rather take the form of *selection neurons* which add Gaussian noise of varying degrees to each feature-decoder pair. Very high noise means that the decoder can effectively not make use of that feature. This unusual implementation ensures the filters have differentiable parameters. The whole system is trained by backpropogation of the combined loss.

Experiments are conducted with a simple physical simulation consisting of a two masses $m_1$ and $m_2$, with charges $q_1$ and $q_2$, which must be hit by a third mass and sent to target locations; basically 'particle golf'. $A$ gets access to a dataset consisting of position time series for the masses, questions in the form of initial velocities for the mass being hit, and answers consisting of corresponding angles which ensure the mass reaches the target location. $B_1$ and $B_2$ are tasked with finding a hitting angle for $m_1$ and $m_2$ respectively in the case where their charges do not interact but both are under the influence of gravity. $B_3$ and $B_4$ are given the task in a 2-D plane, but now the charges do interact. If we give the encoder $E$ three output neurons, we find that they end up computing $m_1$, $m_2$ and $q_1\cdot q_2$ (the Coulomb interaction strength) respectively. We also find that the filters keep exactly the variables we would want them to, i.e. $\varphi_1$ discards all but $m_1$, $\varphi_4$ keeps $m_2$ and $q_1\cdot q_2$.  

Next, the authors propose generalising the supervised question $\rightarrow$ answer format to an observation $\rightarrow$ reward one: reinforcement learning! Now the system is trained using a deep RL loss, in addition to the communication-minimisation prior. This idea is explored using a 3D grid world, where each of the three decoding agents can move around a plane to find a goal location in that plane. Again using three output neurons for $E$, we find that they learn the $x,y,z$ coordinates, and that the three agents keep only the two coordinates that are relevant to them [though I couldn't see anywhere what the form of the initial observation $o$ is].

## 📚 Books

### Gärdenfors, Peter. *Conceptual spaces: The geometry of thought*. MIT Press, 2004.

#### 0	Introduction

This book proposes a metatheory of representation based on geometric spaces, which lies between the symbolic and connectionist metatheories that have been dominant thus far. The proposal is meant to be both *explanatory* (of biological cognition) and *constructive* (to help inform artificial cognition).

#### 1	Dimensions

Much of learning is driven by the notion of **similarity**, which is not an inherent component of either symbolism or connectionism. In order to measure the distance between two phenomena, we need one or more **quality dimensions** on which to place them. A dimension doesn't have to be isomorphic to the real line (it could be a bounded segment, or a tree), but there needs to be some way of measuring distance (e.g. path length between two nodes). If the same set of phenomena can be ascribed values for multiple quality dimensions, these dimensions can be grouped into a **conceptual space**. It is important to stress that dimensions and spaces do not need to correspond to objective structures in the physical world; they are phenomenal, not scientific. A good illustrative example is that of colour spaces: many such spaces have been proposed (almost all three-dimensional), but few bare any relation to the photoreceptor architecture of the retina, and none at all are similar to the 'true' physical nature of colour as mixed wavelengths.

Now is time for some notation and terminology:

- $S$ is the set of all points in a conceptual space.
- $B(a,b,c)$ conveys the notion that $b\in S$ lies **between** $a\in S$ and $c\in S$. This property must adhere to a bunch of trivial axioms such as symmetry, which places some constraint on the distance measure used in $S$.
- $E(a,b,c,d)$ conveys **equidistance**: that $a$ is just as far from $b$ as $c$ is from $d$. 
- $d(a,b)$ is a **metric**; a special kind of distance measure which satisfies $d(a,b)\geq0$ with $d=0\iff a=b$ (minimality) $d(a,b)=d(b,a)$ (symmetry) and $d(a,b)+d(b,c)\geq d(a,c)$ (the triangle inequality). The $L_1$ and $L_2$ norms are metrics. A conceptual space with a metric as its distance measure is called a *metric space*.
- Two or more dimensions in a space are **separable** if it is possible to define an individual distance measure for each (e.g. Newtonian spacetime), and **integral** if we can only define distance in terms of all dimensions in combination (e.g. relativistic spacetime).
- A **domain** is a set of integral dimensions that are separable from all other dimensions. A conceptual space is therefore a collection of one or more domains.

The process of learning new concepts often involves adding new dimensions to ones conceptual spaces. This process is sensitive to the evolutionary, functional and cultural context, and the requirement for communication with others. 

Given a set of example phenomena and scores for their similarity (e.g. provided by a group of humans), we can frame the problem of identifying relevant dimensions for reverse-engineering the latent conceptual space as a learning problem, with the aim of best explaining the data. Solving this problem inevitably requires assumptions about the distance measure. Multidimensional scaling (MDS) is one approach commonly used in psychology. 

#### 2	Symbolic, Conceptual and Subconceptual Representations

A major gap in the symbolic paradigm is the lack of any description of where new predicates *come from*, or in what basis they are *grounded*. Connectionist systems (ANNs), on the other hand, have the the capacity to learn new representations but this often requires a large amount of data, and the representations have no semantic interpretations. Our theory of conceptual spaces sits somewhere between these two levels in terms of representational granularity. There is strong evidence that the brain uses such geometric spaces for much of its operation (e.g. topographic maps in the cortex), and the broad 'three levels' idea agrees with several other general theories of cognition previously proposed. The key message of this chapter is that (contrary to the claims of purists) **all three levels are needed**, and that they interact in a complicated manner.

#### 3	 Properties

We now delve further into the theory of conceptual spaces. Many messy and convoluted definitions of the term **property** have been proposed, but here we mean something quite concrete: a convex region $C$ in a single domain of a conceptual space. Here, 'convex' means that for any three points $a,b,c$ satisfying $B(a,b,c)$, if $a$ and $c$ are in $C$ then $b$ must also be in $C$. Note that this definition does not cover all conceivable properties, since we can dream up all manner of disjoint, non-convex property labels, but it does cover a certain class of well-behaved ones that we call *natural*. A central thesis of this book is that most properties expressed by common words in human languages can be analysed as natural properties in this sense.

Of course, what counts as convex, and in turn which properties we deem natural, depends on our choice of dimensions to include in our conceptual space. Again, it is largely evolution, culture and communication that constrains this choice, but rigorous scientific investigation also spawns new dimensions.

One way of constructing properties is to define a set of **prototype** cases within in a domain, and computing the **Voronoi tessellation** of the domain around those prototypes. Prototypes can be located by supervised learning as the average coordinates of labelled examples. As more examples are added, the prototypes move, and the property boundaries adjust in turn. This approach is very data-efficient, since the agent need only remember the locations of the prototypes themselves. A disadvantage of prototype theory is that it ignores any information about the relative size of properties. A possible way of rectifying this is to take the variability of examples (e.g. standard deviation) into account, and computing tessellations around prototype areas rather than points. 

#### 4	Concepts

Properties are a special case of **concepts**, which in general is defined over multiple separable but correlated domains. Consider the concept "apple", which is represented in several domains including colour, shape, texture and taste. Similarity between instances of "apple" requires a composite distance measure across the domains, which is parameterised (in the simple linear case) by a **saliency weight** for each domain. Saliency weights are dynamically influenced by context, and in turn determine which associations and inferences are made within the space. Furthermore, we need an understanding of the interactions between domains, which can be quantified (in the simple linear case) by **correlation** values. We call concepts that are composed of natural properties, saliency weights and correlations *natural*. A tangible **object** is just an infinitesimally-narrow concept, i.e. one whose properties are all collapsed to points.

Given these definitions, we can think about how concepts can be **combined**. We can combine a base concept $B$ with modifier concept $A$ by finding intersections of the regions for the domains of $A$ with the corresponding regions for $B$. This theory explains how the same modifier concept yields very different regions depending on what the base concept is (e.g. *red* skin vs *red* wine vs *red* wood). It has lots of exceptions and complications for different word types; for example, a modifier may even erase domains entirely when they are incompatible (e.g. *stone* lion erases domains related to habitat, diet, …). We can imagine the process of giving information to an agent as that of iteratively adding modifier concepts and thereby shrinking the compatible regions. At any point, the expectation/mental image held by the agent probably lies somewhere near the centre of the extant regions, though this is affected by inter-domain correlations. 

#### 5	Semantics

Semantics concerns the meaning of linguistic expressions. In the cognitive view, semantics is a relation between these expressions and *cognitive structures* rather than objective entities in the outside world. Roughly speaking, basic linguistic terms can be mapped onto the conceptual spaces theory as follows:

- Adjectives are natural properties;
- Verbs are *dynamic* natural concepts (i.e. those which include the time domain);
- Nouns are *static* natural concepts (i.e. those which do not exclude the time domain);
- Prepositions also seem to be best thought of as properties (especially in the spatial domain) that are positioned in relation to a property of a reference object, but things are trickier here because we use the same word to describe many different relations (e.g. picture *on* the wall, apple *on* the tree, smoke *on* the water…)

Metaphors may at first thought seem intimidating, but actually provide great evidence that much of our cognition is done spatially. A metaphor is effectively a recognition of *isomorphism between two domains*, enabling properties to be carried across (exactly the etymology) from one (the *vehicle*) to the other (the *subject*). For example, the phrase "peak of a career" recognises the isomorphism between the height of an object as a function of its spatial extent and professional status as a function of time, and and defines a new property in the latter domain. Trivially, we can only transfer properties that we already have, so we tend to see metaphors going from more fundamental and ingrained domains (e.g. physical space) to less fundamental ones.

Very often, new properties become so culturally ingrained that their metaphorical origins are forgotten, in which case they effectively cease to be metaphors at all. *There is no sharp distinction between literal meaning and metaphor*. A property is metaphorical to the extent that its transfer from elsewhere is culturally salient. 

Given that each agent is responsible for the cultivation of their conceptual spaces, how can we possibly hope to converge to similar concepts and semantics that can be used for communication? In fact, it's the very act of communication itself that imposes a selective pressure favouring concepts that can be shared without distortion. This is the essence of *memetics*. 

#### 6	Induction

Induction is the process of generalising from individual observations. Traditional symbolic / logical induction is a very narrow form of this, since it takes the atomic predicates as given, and it says nothing about which predicates are 'meaningful' and which are frivolous. To understand where meaningful predicates come from, we need to go below the symbolic to the conceptual level. Here, an observation can be defined as *the assignment to a phenomenon of a location in a conceptual space*, and a generalisation is a property or concept that *contains that observation*. We can now tentatively say that a meaningful predicate is one that is constructed from natural properties or concepts. 

Clearly, this makes meaningfulness contingent on the choice of dimensions in the conceptual space. We again turn to the question of how spaces are constructed from raw observations. Computationally speaking, this is an exercise in *dimensionality reduction*. MDS is one approach to tackling this problem; another is using self-organising Kohonen maps. 

Some aspects of induction occur at the conceptual level. These involve recognising *correlations* between concepts across many domains, which can be exploited to make a prediction about one domain given an observation in another. This is a skill that humans appear to have in abundance. Again adopting a computational perspective, this is effectively *pattern completion* problem, for which architectures such as Hopfield networks have been developed.

## 🗝️  Key Insights

- Ciatto et al's formalisation of the interpretability and explainability is surely a simplification, but one that brings clarity, and highlights several important issues such as explainee relativity and the importance of representation.
- Gallitz et al's approach to interpretable feature generation appears to follow a common formula: pass low-level state information through a fairly flexible mapping but apply various hand-crafted constraints and filters to encourage the resulting features to be disentangled and semantically-grounded.

- Khan et al's notion of "explanation as demonstration of optimality" is nice and well-defined, but I'm not convinced it's particularly useful in systems large enough to be interesting.
- Nautrup et al's impressive paper is part of the literature on what might be termed "interpretability *via* multi-agent systems", which is in turn a subset of "interpretability via forced generalisation". The broad idea is that if a feature can be used in a variety of contexts, it must capture some important invariant information.
- Gärdenfors conceptual spaces theory is an extremely powerful one that addresses many of the shortcomings and paradoxes of previous philosophical conceptions of meaning, learning and inference. It's well worth keeping in mind for a long time.
