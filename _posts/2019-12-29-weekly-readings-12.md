---
title: 'Weekly Readings #12'
date: 2019-12-29
permalink: /posts/2019/12/weekly-readings-12/
tags:
  - weekly-readings
---

xxx; xxx; xxx

## 📝 Papers

### Bain, Michael, and Claude Sammut. “A Framework for Behavioural Cloning,” 2001.

Describes experiments in automatically cloning reactive agents from human demonstration for the task of flying a simulated aircraft along a specified flight plan. $10$ episodes of demonstration are recorded from each of $3$ human pilots, each with around $1000$ control action datapoints. For each datapoint, the state of the system is recorded, as described by a set of relevant state variables (e.g. aircraft heading, speed, distance to runway…)

Quinlan's C4.5 decision tree induction algorithm is used to fit rule sets to data from each pilot *individually*, since different flying styles are possible. Furthermore, the flight plan is divided into seven sub-tasks corresponding to the instructions given to the participants. Finally, since there are four control dimensions – elevator, rollers, thrust, flaps – a decision tree is fit to each (with actions discretised into bins of equal frequency on a per-pilot basis). Hence in total, $3\times7\times4=84$ trees are induced. Post-pruning is performed to yield more readable, noise-tolerant trees.

Even though trees are learned on a per-dimension basis, they are found to yield smooth and well-coordinated action. But despite the trees being induced for each subtask, the nature of these tasks is not explicitly represented, which is surely a missed opportunity.

To address this shortcoming the authors propose *Goal-directed Reactive Abduction from Inductive Learning* (GRAIL). The approach has the following steps:

- From demonstration data, learn decision trees to map from action variables to *functions of state variables*, which have to be manually defined using domain knowledge. Valid functions might include a difference between the variable's value and a target threshold, which is a parameter. The trees can be converted into logic rules and used in turn to *abduce* an action for a given target.

- From the same data, also learn trees to represent *goal rules*, which determine parameters of state variable functions in terms of the value of certain key state variables (e.g. if distance to runway > $5$km, target elevation = $0$). [The authors claim that they have done preliminary work on this step, but acknowledge that it is extremely challenging.]
- The two sets of rules can now be used for control as follows:
  - Assess the state to determine which goal rule applies and adopt the corresponding state variable function parameter value. 
  - Use the abduction technique to generate an action.

At the time of writing, GRAIL had not yet matched the performance of the conventional cloning method, but some results are reasonable and the representation is far more compact. There is also reason to believe that it should be capable of cloning the entire flight plan without need for manual division into sub-tasks.

The key to making this work: finding the right representations.

### Fumagalli, Mattia, and Roberta Ferrario. “Representation of Concepts in AI: Towards a Teleological Explanation,” 2019.

Outline the prevailing theories of concepts in artificial intelligence:

- **Classical symbolic**: concepts are explicit representations coded in a language. Examples are formal ontologies.
- **Connectionist**: concepts are implicit representations distributed throughout a large number of processing elements, such as the neurons of a neural network.
- **Embodied**: concepts are ephemeral representations arising from the interaction of an embodied agent with its environment. They are secondary to behaviour itself.
- **Others**: procedural (knowledge is algorithmic: the capacity to *do something*); analogical or prototypical (concepts are mental objects isomorphic to those they represent); theoretical.

In light of these existing theories, a further one is proposed: *teleosemantics*. Here, we must consider a system of two components, a producer $P$ and a receiver $C$. The roles of $P$ and $C$ may be played by organisations, humans or artificial devices. 

The function of $P$ is to produce a conceptual representation $R$ that enables $P$ to navigate its state-action space and bring about a specified goal condition $x$. If this is reliably achieved, then $x$ can be said to be *the content of* $R$. Hence, this theory of concepts is teleological. 

The concept of a reward signal is also mentioned briefly, but not elaborated on. It seems a reward (tied to $x$) is necessary to enable $P$ to tailor $R$ so that $C$ can best utilise it. 

It is argued that the components of this theory map very well onto the key issues in explainability.

### Harbers, Maaike, Karel van den Bosch, and John-Jules Meyer. “Design and Evaluation of Explainable BDI Agents.” In *2010 IEEE/WIC/ACM International Conference on Web Intelligence and Intelligent Agent Technology*, 125–32. Toronto, AB, Canada: IEEE, 2010.

Represent fire-fighting protocols and expert knowledge as a BDI-like goal hierarchy, in which sub-goals are triggered by belief condition, and leaf nodes represent concrete actions to be taken in pursuit of the ancestral goals. 

Explore a selection of simple explanation algorithms which operate on the goal hierarchy to produce explanation for individual actions, either in terms of (1) the immediately preceding goal; (2) the goal two levels up the hierarchy; or (3) the immediately preceding belief condition. A cohort of $20$ volunteers is asked to indicate which of the candidate explanations is most "useful" for a selection of actions. 

Results indicate that the best explanation is contingent on the type of relation between the action and its ancestral goals and beliefs. In general:

- *"Actions that are executed to follow a rule or procedure are sometimes preferred to be explained by goals and sometimes by beliefs."*
- *"Actions whose execution depends on conditions in the environment are preferred to be explained by beliefs."*

While immediately preceding goals (1) are more often preferred than those two levels up (2), this result is a little arbitrary as there often multiple valid ways of constructing the hierarchy. 

### Kurutach, Thanard, Aviv Tamar, Ge Yang, Stuart J Russell, and Pieter Abbeel. “Learning Plannable Representations with Causal InfoGAN,” 2018.

Classical planning algorithms are extremely effective given the right state representations. *Causal InfoGAN* (CIGAN) is a method for learning plannable representations from high-dimensional observations (e.g. images) of dynamical systems. Here, 'plannable' means amenable to search: via graph search for discrete representations and linear interpolation for continuous representations.

In this framework, a GAN is trained to generate realistic sequential observation pairs $(o,o')$ from the dynamical system. In a vanilla GAN, the input is a noise vector $z$. Here, we view the input as a concatenation of a noise vector with a pair of consecutive abstract states $s$ and $s'$. The abstract states are intended to represent the features important for understanding causality in the system, and the remaining noise models less important variations. 

To learn such representations, the *InfoGAN* method is used: a term is added to the GAN objective that maximises a lower-bound estimate of the mutual information between the generated observations $(o,o')$ and the abstract states $(s,s')$. To encourage the $s\rightarrow o$ mapping to be the same as $s'\rightarrow s$, the mutual information estimate assumes the disentangled posterior $P(s,s'\vert o,o')=P(s\vert o)P(s'\vert o')$. The training data for this process comes from a random exploration policy within the dynamical system.

Given a trained CIGAN model, goal-directed planning is performed as follows:

1. Given a pair of observations $o_{start}$ and $o_{goal}$, encode them into a pair of abstract states $s_{start}$ and $s_{goal}$. The encoding is optimised by a "search over the latent space", though another approach could be to modify the GAN to include an explicit encoder-decoder architecture.

2. Using a model of abstract state transition probabilities learned from data (the form of this depends on whether the representation is one-hot, binary or continuous; see paper for details), and an appropriate planning algorithm, construct a feasible trajectories of states from $s_{start}$  to $s_{goal}$. 
3. Decode the trajectory to a sequence of observations, by passing it through the GAN generator.

The technique is deployed to generate obstacle-avoiding trajectories in a 2D environment, and sequences of images of a strand of rope representing a feasible interpolation between start and end configurations.

## Lyre, Holger. “Concerning the State Space of Artificial Intelligence,” 2019, 27.

Not too much novel in here, but the author takes a stab at mapping the space within which the many possible approaches to artificial intelligence lie. 

This space is obviously very high-dimensional, but three primary 'classes' of dimension are proposed:

1. Generalisation (vs narrowness).
2. Grounding (i.e. semantic properties).
3. Self-$x$-ness, where $x$ could stand for:
   - Learning
   - Repairing
   - Replicating
   - Explanatory
   - Conscious
   - …

It is imagined that human-level intelligence is a point (or compact region) in this space. 

### Páez, Andrés. “The Pragmatic Turn in Explainable Artificial Intelligence (XAI).” *Minds and Machines* 29, no. 3 (September 2019): 441–59. 

Argues that the goal of XAI is not well-defined and should be reformulated in terms of a coherent model of human *understanding*, informed by results from psychology and philosophy. 

Explanation is one of several means to the end of understanding. Others include:

- Causal knowledge obtained from observation, experimentation, manipulation and inference. Such knowledge may be tacit and difficult to articulate.
- Analogical reasoning and exemplification.
- Visual representations such as diagrams, graphs and maps.
- Theoretical or proxy models that approximate the system of interest. These may be local to a specific point in the state space, or may attempt to model a large region.

In the XAI literature, approaches to each of the above have often been called "explanations" but this vague usage of the term ignores many distinctions.

For example, analogies, exemplifications and local models tend to be used for post hoc interpretation of specific decisions, while global models are used for overall functional understanding.

The author argues that approximate mechanistic models, similar in character to those used in scientific investigation, are the most promising path towards understanding. Such models must be absolutely transparent about their limitations, and must manage the fidelity-comprehensibility with care. Experimental research should also be done to compare the human interpretability of various model classes (e.g. decision trees, linear regression, naïve Bayes).

To support the view that approximate mechanistic models are valuable, the author presents the analogy of an engineer using the approximate model of Newtonian physics to solve design problems. Most people would accept that here, the model provides exactly the right kind of understanding for solving challenging real-world problems.

While he doesn't dismiss the approach out of hand, the author argues that post hoc interpretation provides far less breadth of understanding. *Knowing why* a certain output $x$ has been produced by a system $S$ is very different from understanding $S$ *in general,* which could only come from answers to a great many narrow questions.

The paper finishes with a strong warning against merely functional approaches to understanding, which focus only on the statistical (or worse, teleological) relationships between the inputs and outputs of a black box model, without considering the mechanism of the model itself. This approach gives too much trust to the black box, and seems destined to mislead and oversimplify.

### Sharma, Mohit, Kevin Zhang, and Oliver Kroemer. “Learning Semantic Embedding Spaces for Slicing Vegetables.” *ArXiv:1904.00303 [Cs]*, March 30, 2019. 

A task-specific image embedding is learned for the problem of slicing tomatoes and cucumbers with a pair of robotic arms. This is done by first training to optimise for an *auxiliary task*: classifying the thickness of the slice and remaining main fruit/vegetable (*very thin, thin, …*) after a cutting action is taken.

Rather than using raw images from the arm-mounted camera, these images are first segmented into a bounding box for each visible slice using a fine-tuned *MaskRCNN* model. The bounding boxes are then passed individually through the MaskRCNN model again, and mid-level image features are extracted for use as the inputs to an *embedding network*. The *embedding network* $\psi$ (one convolutional layer; several fully connected layers) produces an embedding vector $z$ for a bounding box.

The embedding network is trained for the thickness classification task on a random dataset of images and slice actions (concatenated input vector), by appending a classification network on top [I assumed; not explicitly stated]. It solves this task well, and PCA shows that the embeddings for different thickness classes are nicely clustered. 

A *forward model* $\phi$ is then trained to predict the embeddings of the slice $z^s_{t+1}$ and the remaining main fruit/vegetable $z^o_{t+1}$ given the pre-cut embedding $z_t^o$ and slice action as input. The network is trained to minimise mean squared error on a training dataset. A *curriculum* learning approach is used: initially the forward model is trained for one-step predictions only, but the planning horizon is iteratively increased. The resultant embeddings produced by the forward model appear to show a smooth and ordered dependency on slice thickness, which is interesting since the system has only been given direct access to thickness classes. This suggests it has grasped the semantic meaning of the thickness property.

Given a trained embedding network $\psi$ and forward model $\phi$ capable of multi-step prediction, [experiments](https://sites.google.com/view/learn-embedding-for-slicing/) show how a simple planning algorithm can devise an execute a cutting plan to move between initial and goal images (i.e. cut several slices of various thicknesses).

## 📚  Books

### Dennett, D. & Hofstadter, D. (2001). *The Minds' I: Fantasies and Reflections on Self and Soul*. Basic Books.

#### Section

## 🗝️  Key Insights

- x
- x
- x