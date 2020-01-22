---
title: 'Weekly Readings #14'
date: 2020-01-19
permalink: /posts/2020/01/weekly-readings-14/
tags:
  - weekly-readings
---

Integrating knowledge and machine learning; folk psychology and intentionality; soft decision trees; conceptual spaces.

## 📝 Papers

### Bouraoui, Zied, Antoine Cornuéjols, Thierry Denœux, Sébastien Destercke, Didier Dubois, Romain Guillaume, João Marques-Silva, et al. “From Shallow to Deep Interactions Between Knowledge Representation, Reasoning and Machine Learning (Kay R. Amel Group).” *ArXiv:1912.06612 [Cs]*, December 13, 2019.

Many recent works have called for deeper integration of discrete, semantic knowledge representation and logical reasoning on one hand, and data-driven machine learning on the other. But we are finding this tricky because the two areas of AI have been developed in *almost complete isolation* from each other, and there is a belief in a strong, irreconcilable dichotomy.

Much of this belief comes from the fact that the representations and mathematics used in the two paradigms appear so different: definite, symbolic propositions for knowledge-based reasoning and (most often) vectors of real numbers for machine learning, which make numerical optimisation practical. But conceptualised in the right way, the overall objectives are really very similar.

Here a selection of meeting points are brought together, including:

- Injecting prior knowledge into learning through *biases*, either over the space of functions that can be expressed, or over the strategy for search within this space.
- Neuro-symbolic reasoning: training neural architectures to approximate logic programs.
- Fuzzy rules and reasoning, in which reasoning is temporarily brought into a realm of continuous calculation before being defuzzified back into definite propositions.
- Conceptual spaces, Gärdenfors' idea for a midpoint between the vector spaces of machine learning and the symbolic representations of logic, in which much of reasoning takes place [see talk below]. This broad idea underlies work in disentangled representation learning and vector embeddings (e.g. word2vec).

### Coppens, Youri, Kyriakos Efthymiadis, Tom Lenaerts, and Ann Nowe. “Distilling Deep Reinforcement Learning Policies in Soft Decision Trees.” In *Workshop on Explainable Artificial Intelligence*, 7, 2019.

Here a *soft decision tree* (Frosst and Hinton, 2017) is used to clone a reinforcement learning policy $\pi$ in a Mario game environment. In a soft decision tree, each branching node consists of a single perceptron that linearly maps the features to a probability of traversing to the right child node. The leaf nodes learn softmax distributions over the output classes. Training loss is based on the entropy between the leaf predictions and RL agent's action distribution $\pi(s)$, as well as a regularising cost to encourage balanced usage of the various branches of the tree.

In the Mario game, each game frame is mapped to a $10\times10$ grid, where the integer in each cell represents the kind of object present in that cell (e.g. $0=$ empty, $11=$ ground). [To me this imposes a weird artificial ordering between the object types!] Each branching node effectively filters the input grid with different weights, and these filters can be visualised as heat maps which the authors interpret as something like an attention visualisation. Some [semi-convincing] discussion is presented along these lines, though the clone performs significantly worse than the target agent, with only slight improvement with tree depth. 

### De Graaf, Maartje MA, and Bertram F. Malle. “How People Explain Action (and Autonomous Intelligent Systems Should Too).” In *2017 AAAI Fall Symposium Series*, 2017.

Assert that if we are to generate explanations of autonomous systems' behaviour that ordinary people understand, we must replicate the way humans themselves explain, by leaning into concepts from *folk psychology*, most importantly that of *intentionality*.

Intentionality is the hub of people's theory of mind and behaviour. Broadly speaking, we divide events into two categories: **intentional** and **unintentional**. To explain the former, we prefer to use **belief-desire-intention** (BDI) reasoning. For the latter, we use **causal** reasoning. Since it is well known that people ascribe intentionality to autonomous systems, we should seek to primarily implement BDI explanation, resorting to causes only when events are genuinely unintentional (e.g. when things go wrong). It is therefore important that an autonomous system is capable of differentiating between the two.

The BDI process describes a kind of 'folk rationality': considering an agent's beliefs and desires, it 'makes sense' to use for it to act in a particular way. Since BDI is in some sense anti-causal or *teleological*, it seems likely that a system that produces BDI-based explanations will need a predictive *forward model*. For the secondary causal explanation process, other abilities are required, such as reasoning about interventions and counterfactuals. Clearly, technical developments in knowledge representation and natural language processing are also required.

In either case, completeness of explanation is not the aim. We must select information according to some kind of contextual relevance criterion, in order to **generate maximal coherence within the explainee's structure of preexisting knowledge**. This is where things get really complicated; what is required in effect is a rich theory of mind for the explainee.

It is essential that we primarily use human judgement to evaluate proposed explanation frameworks. This work is as much an exercise in *understanding humans* as of understanding AI. In the longer term, once we have achieve all of the above, the next step is to enable humans to provide dynamic feedback in light of the explanations they receive, thereby transforming explainable AI into teachable AI.

### Frosst, Nicholas, and Geoffrey Hinton. “Distilling a Neural Network Into a Soft Decision Tree.” *ArXiv:1711.09784 [Cs, Stat]*, November 27, 2017. 

Explicitly motivated by explainability, the authors propose distilling a neural network into a *soft decision tree* with minimal loss of performance. Rather than relying on hierarchical features, as in a neural network, a soft decision tree works using hierarchical decisions about the unmodified input features, thus (it is claimed) is more interpretable. 

In a soft decision tree, each decision node $i$ performs a linear mapping of the input vector $\textbf{x}$ to the probability of taking the rightmost child branch: 

$$
p_i(\textbf{x})=\sigma(\beta\cdot(\textbf{xw}_i+b_i))
$$

where $\sigma$ is the logistic function and $\beta$ is an inverse temperature parameter that moderates the degree of stochasticity in the tree. As $\beta\rightarrow\infty$ it becomes increasingly deterministic, which makes explanations easier at the cost of slightly reduced performance.

Each leaf node $\mathcal{l}$ learns a softmax distribution $Q^\ell$ over the output classes, such that for each class $k$, the probability of outputting that class is

$$
Q^\ell_k=\frac{\exp(\phi^\ell_k)}{\sum_{k'}\exp(\phi^\ell_{k'})}
$$

where $\phi^\ell_k$ is a learned parameter. 

The loss function used during training seeks to minimise the cross entropy between each leaf $\ell$ (weighted by its path probability) and the target distribution. For a single input vector $\textbf{x}$ and target distribution $T$, the loss is

$$
\mathrm{L}(\mathrm{x})=-\log \left(\sum_{\ell} P^{\ell}(\mathrm{x}) \sum_{k} T_{k} \log Q_{k}^{\ell}\right)
$$

where $P^\ell(\textbf{x})$ is the probability of getting to $\ell$ from the root node given $\textbf{x}$.

A regularisation term is added to encourage each decision node to make equal use of both left and right subtrees. This avoids getting stuck in plateaus in which a decision node assigns almost full probability to one of its subtrees, meaning the gradient of the logistic for this decision is always very close to zero. The regularisation cost is calculated as

$$
C=-\lambda\sum_i2^{-d_i}\left[0.5\cdot\log(\alpha_i)+0.5\cdot\log(1-\alpha_i)\right]\ \ \ \text{where}\ \ \ \alpha_{i}=\frac{\sum_{\mathbf{x}} P^{i}(\mathbf{x}) p_{i}(\mathbf{x})}{\sum_{\mathbf{x}} P^{i}(\mathbf{x})}
$$

and $d_i$ is the depth of node $i$, which is used to exponentially decay the penalty for deeper nodes, where probabilities are computed with less data (and thus less certainty). $\lambda$ determines the overall strength of regularisation. In addition, a moving average of the probabilities is used rather than the per-batch values. The window size for the moving average is exponentially *increased* with node depth. 

Unlike most decision tree induction algorithms, the tree topology is fixed, and the parameters $\textbf{w}$, $b$ and $\phi$ are updated by batch gradient descent. 

It is found that training the tree using the softmax outputs of a trained neural network (rather than binary class labels) as the target distribution $T$ leads to less overfitting and better test performance ($94.45\%$ to $96.76\%$) on MNIST, and this is backed up by several other datasets.

### Madumal, Prashan, Tim Miller, Liz Sonenberg, and Frank Vetere. “Explainable Reinforcement Learning Through a Causal Lens.” *ArXiv:1905.10958 [Cs, Stat]*, November 20, 2019.

Here the aim is to use structural causal models (SCMs) for answering factual ("why") and counterfactual ("why not") questions about the action decisions of RL agents in video game environments. This requires a slight extension of the SCM framework to incorporate *action influences*, so that each edge (and in turn each structural equation) is only 'activated' when a particular action is taken. Some of the nodes are also labelled as reward variables; these have no children.

In this work, the qualitative structure of the model has to be hand-defined, but the structural equations themselves are learned (linear, decision tree or neural network) from demonstration data of the agent acting in the environment: the equation for each edge is only updated using timesteps when the associated action is taken.

A complete *factual* explanation of having taken an action $A$ is produced by tracing all causal chains from the variable at the head of the action-edge ($X_h$), out to reward variables ($X_r$), and storing all variables encountered on the way (inclusive) along with their current values. It is supposed that this will yield too much information for the explainee, so all but $X_h$ and $X_r$ themselves, as well as the penultimate variables before $X_r$ (denoted $X_p$) are ignored. These variables and their associated values are synthesised into an explanation using a hand-written natural language template.

A *counterfactual* explanation of having *not* taken an action $B$ is produced by simulating the 'optimal' conditions under which $B$ would have been taken [not too clear how this is done], finding its causal chain as above, and comparing it with the causal chain for the taken action $A$. Any *differences* between these two chains are used to build an explanation.

In an MTurk study with Starcraft II, 'understanding' and 'trust' of the explanation system are evaluated compared with using no explanation, and another approach based on identifying highly-relevant variables. It seems to do a little better in terms of understanding, but no better in terms of trust. 

### Pintelas, Emmanuel, Ioannis E. Livieris, and Panagiotis Pintelas. “A Grey-Box Ensemble Model Exploiting Black-Box Accuracy and White-Box Intrinsic Interpretability.” *Algorithms* 13, no. 1 (January 5, 2020): 17.

Here we have a very simple route towards a purported combination of interpretability and performance: train a black-box ML model, use the most confident predictions of that model to label a secondary unlabeled dataset, retrain with the newly-enlarged labeled dataset, and repeat [until when?]. This process is called *self-training*. Then use the final enlarged dataset to train a white-box ML model (e.g. decision tree), which is then deployed. The resultant model is called a *grey-box*.

Experiments on various datasets suggest that on the whole, this produces somewhat better performance than training the white-box directly on the original dataset, though not as strong performance as the self-trained black-box. Performance of the grey-box is actually *worse* than the white-box on small datasets, however, since there is insufficient data for the black-box to learn a good mapping, so much of the augmented dataset is garbage.

[I also have real doubts about the 'interpretability' of the outcome of this method. Yes, the prediction model may have learned simple rule, but these rules can be partly traced back to something other than ground-truth data, namely an extremely complex black-box learning process.]

## 🎤 Talks

### Gärdenfors, Peter. “The Geometry of Thinking.” presented at Explaining the Mind: Perspectives on Explanation in Cognitive Science. Copernicus Center for Interdisciplinary Studies, June 29, 2015. 

Introduces his theory of *conceptual spaces* as one to bridge the gap between semantics an connectionism.

- A *quality* is a 1-dimensional representation, of which two instances can be assigned a *similarity* value according to some abstract distance metric.

- Qualities are grouped into *domains* (e.g. 3-dimensional space), where an aggregate distance metric can be defined in turn. A naïve option would be to use a weighted Euclidean distance.

- A *property* (roughly, adjective) is a convex region in a single domain. The convexity assumption is crucial here; it says that if two locations $x$ and $y$ both have property $A$, then any location 'in between' (according to the aggregate metric) also has property $A$. Depending on the choice of metric, different locations may be assigned different properties.

- A *concept* (roughly, noun or verb) is a set of properties in a number of domains, together with information about how the domains relate to one another. Concepts are dynamic in that it is possible to learn more about them, refining their constituent property regions and adding new properties from different domains.


Thus we can devise a simple model of semantic learning that works even with very sparse data. Given a set of labeled examples of properties, *prototypes* can be formed as (something like) the per-class averages in domain space. Performing a *Voronoi tessellation* about these prototypes fully partitions the domain into convex regions, which determine how to allocate new, unlabeled examples. The prototypes, and thus the regions, can be refined as more data are added.

This model is clearly a drastic simplification, for example properties are sensitive to context ("hot" bath water is a different region from "hot" tap water). It also offers no explanation of where the basic qualities come from (perhaps they are hard-wired in humans?) But nonetheless, it provides one building block in the bridge that we are so desperate to construct.

## 📚  Books

### Salmon, W. (1998). *Causality and Explanation*. Oxford University Press.

*Causality* is just starting to be defined on a technical level, but the same cannot be said for *explanation* (is a teleological explanation as valid as an efficient causal one?) or *understanding* (which has all manner of formal and informal variants). In this book we focus on specific interpretations of these ambiguous terms — *scientific* explanation and *scientific* understanding — and the role of causal reasoning in their attainment.

#### Introductory Essays: Causality, Determinism and Explanation

Hume argued that when we search for some deep physical connection between cause an effect, we find nothing. To him, causality was nothing more than a repeatedly-observed spatiotemporal contiguity between the cause (always first) and the effect (always second). Most critics of Hume have argued for the necessity of counterfactuals, but Salmon wishes not to involve them because they seem too metaphysical and inaccessible. The best theory of physical causation proposed so far is Dowe's: an interaction (coming-together) of two processes in which physical quantities (e.g. energy and momentum) are *conserved*. Admittedly, all theories are thrown into confusion by quantum mechanics, specifically the existence of action at a distance.

## 🗝️  Key Insights

- Much of the battle with reconciling symbolic logic with machine learning comes down to reconciling our language and notation, and realising we are all interested in the same problems.

- The folk psychology approach to explanation: BDI for intentional actions, causality for unintentional actions. In each case, the contextual selection problem is important.
- There are lots of decision tree variants out there beyond the conventional zero-lookahead greedy induction. Frosst and Hinton's soft decision tree provides an interesting blend with neural networks.
- Causal modelling is a truly elegant method of generating explanations, but as of yet I feel all papers attempting it have required too much hard-coding to be groundbreaking.
- Gärdenfors' conceptual spaces are a nice model for some aspects of reasoning with sparse example, though of course leave many technical questions unanswered.
- In practical work on causality (e.g. Pearl), we rarely stop to think what causality *is*. Salmon himself doesn't seem fully satisfied, but ends up with a very physical definition based on conserved quantities.