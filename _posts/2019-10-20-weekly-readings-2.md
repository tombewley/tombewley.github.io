---
title: 'Weekly Readings #2'
date: 2019-10-20
permalink: /posts/2019/10/weekly-readings-2/
tags:
  - weekly-readings
---

As it stands I'm precisely 13 days into my PhD, which means a lot of reading, and I thought I'd kick this blog off with a weekly rolling 'diary' of things I read, watch and otherwise consume which may have some influence on my [PhD topic](https://tombewley.com/start ). Most of the papers have words pertaining to explanation in there, and that's because I did a massive scrape of papers with that keyword. I figured that would be a reasonable start.

I'm going to try to summarise what I took from each piece of content (which may or may not match the author's intended argument!) in just a few lines, which is obviously a daft and brazen thing to do, but hopefully useful nonetheless.

## 📝 Papers

### Amir, Ofra, Finale Doshi-Velez, and David Sarne. “Summarizing Agent Strategies.” *Autonomous Agents and Multi-Agent Systems* 33, no. 5 (September 2019): 628–44.

Humans are boundedly rational and there's no reason why we should understand the actual reasoning process of an autonomous system. The idea behind strategy summarisation is to provide explainees with some form of overview that demonstrates system behaviour in carefully selected state-action pairs. This allows understanding of likely future behaviour (*ex-ante*) in addition to merely explaining existing decisions (*ex-post*).

---

The strategy summarisation problem is broken down into subcomponents:

- **Intelligent state extraction**: finding state-action pairs to present. There are multiple ways of framing this:
  - Choosing **interesting** examples, where the properties that makes a pair 'interesting' are context-dependent. In an RL context, they may be a function of the *distribution of $Q$ values* for the state. A very large variation between the best and worst action suggests that that state is important. Other desirable properties include wide *coverage* of the state space, and the *likelihood* of actually encountering the chosen states (highly unusual states may or may not be interesting). In a multi-agent system, states at which two agents' policies *disagree* could be of interest.
  - Choosing **informative** examples, that optimise for the ability of a human or another model to reconstruct the agent's policy. There are two algorithmic approaches to reconstruction: imitation learning (IL) and inverse reinforcement learning (IRL). In the former, a supervised model aims to predict actions given states ($\approx$ behavioural cloning). In the latter, the aim is to infer the agent's reward function based on the demonstrations. One hypothesis is that summaries that are useful for either of these two methods, *will also be useful for humans*. But an interesting question here is, do humans do something more like IL or IRL?
  - Getting groups of people to attempt to solve the problem through **manual** policy design, and determine which states and actions are viewed as important.
- **State representation**: determining how to compactly convey information about potentially complex state and action spaces to people with varying levels of expertise.
- **Strategy summary interface**: designing software environments for explainees to interact with summaries, ideally in a collaborative manner with a learning and feedback loop. This interface will potentially allow the explainee to provide preference input to the state extraction process. It is also important to identify instances where the explainee may have erroneously extrapolated from a summary and correcting for the error.

Stress the importance of standardised test environments and performance metrics (e.g. policy reconstruction or action prediction ability, subjective understanding).

Also identify autonomous vehicles as one of the key impact areas for this technique. Other domains include education and healthcare.

### Bryson, Joanna J. “Embodiment vs. Memetics: Does Language Need a Physical Plant?,” 2001, 6.

A central premise of embodied AI is that it will solving the semantic grounding problem by providing biases and constraints for perception and action. Here it is argued that it may not be the only way of doing so.

---

This paper uses careful definitions:

- **Semantics**: how a word is used.
- **Expressed behaviour**: that which impacts the environment and is thus externally visible.
- **Grounded**: associated with a representation that determines an expressed behaviour.
- **Understand**: connect a semantic term to a grounded concept.
- **Embodiment**: the property of having rich interactions with an environment, which lies a continuum of degree.

The assertion of this paper is that human-like semantics can be derived without any significant degree of embodiment, and is just another form of automated perceptual learning. Discusses word embedding in vector space: words that commonly co-occur are located nearby in the space. This requires no grounding.

- Note that humans very frequently transmit semantic information that they don't understand. [Especially in academic circles!]

There's no reason why Searle's Chinese room could not be a fantastically useful tool and valid participant in science and culture. This is not to say that it would be a complete model of human intelligence, which clearly does use grounding, but that's not what we're interested in here. We should try building a Chinese room!

Non-grounded, but still useful, semantic knowledge is referred to as *memetic* knowledge.

Given that it seems complex semantics seems to be derivable from raw statistics, how come humans are the only species with significant culture. Bryson's answer is that we are the only known species with the ability to both (1) model relationships between individuals *not including ourselves* (most other primates do this); and (2) precisely control and imitate vocal sounds, thereby enabling a high-dimensional communication substrate (birds do this). 

### Dethise, Arnaud, Marco Canini, and Srikanth Kandula. “Cracking Open the Black Box: What Observations Can Tell Us About Reinforcement Learning Agents.” In *Proceedings of the 2019 Workshop on Network Meets AI & ML - NetAI’19*, 29–36. Beijing, China: ACM Press, 2019.

Here the aim is to understand the behaviour of an RL agent used for video bit rate adaptation for streaming platforms. Here the goal is to maximise user enjoyment, which is a function of both the video quality and buffering time; these are in tension. The $25$ input features for the model include the current buffer duration and the download time of the several most recent $4$-second data chunks. The action space is the six possible bit rates.

End up doing some simple stuff:

- High-level statistics on selected action and comparison to theoretical optimality;
- LIME for feature importance (only a small subset are used heavily);

Combined with some extensive domain knowledge, this actually provided quite a bit of insight. However, several unanswered questions are identified:

- Finding outliers where performance breaks down;
- Ensuring stability of learning;
- Detecting whether the policy is sub-optimal (local maximum), either during or after learning.

### Garnelo, Marta. “Reconciling Deep Learning with Symbolic Artificial Intelligence: Representing Objects and Relations.” *Current Opinion in Behavioral Sciences*, 2019, 7.

Deep learning alone has three major shortcomings: **data inefficiency**; **poor generalisation**; and **lack of interpretability**. These shortcomings align with the strengths of symbolic AI [and vice versa!] Reconciliation of the connectionist and symbolic paradigms is today's greatest challenge in AI. This paper is a review of recent attempts at integrating two key aspects of symbolic AI into connectionist systems: compositionality and relationality.

---

**Compositionality** is an essential principle in linguistics, but there is no compositionality constraint on the intermediate representations inside a deep learning model. On the contrary, it appears that gradient descent tends to produce distributed and entangled representations, whose component parts have little or no meaning in isolation. Solutions include:

- Incentivising disentangled representations in the loss function (as is done in a variational autoencoder);
- Imposing compositional structure on the representations from the outset.

---

Most work on disentanglement has focused on images containing a single object; additional work is needed to consider **relations** between multiple objects for propositional reasoning. 

*Relation networks* *self-attention* networks are two kinds of multi-network model that can learn pairwise relations between a fixed set of $n$ objects. They can be used to answer questions such as "how big is the sphere that is the same colour as the small cube?"

---

While these areas of work are interesting and appear to create 'logic-like' representations if we squint, they lack the full expressive power of actual, crisply-defined logic, particularly the presence of **variables** and **quantification**, and proper multi-step **inference** mechanisms.

### Hoffman, Robert, Tim Miller, Shane T. Mueller, Gary Klein, and William J. Clancey. “Explaining Explanation, Part 4: A Deep Dive on Deep Nets.” *IEEE Intelligent Systems* 33, no. 3 (2018): 87–95.

Explainability in DNNs can be achieved by seeing how they operate near their 'boundary conditions', which can be investigated using adversarial examples.

---

Global explanations seek to answer the broad question of how a system does what it does, with the goal of *helping the explainee to develop a robust mental model*. They should be phrased in terms of the training data, chosen architecture and algorithms, performance metrics and known boundary conditions and failure modes.

But often what we require is a local, instance-specific explanation. Some researchers that *all* local explanation questions can be framed as counterfactual ones. 

The proposal here for DNN explanation is to *use adversarial examples as contrast cases, and frame the explanation problem as one of scientific exploration*. We can imagine manipulating test images in a controlled way (e.g. by adding filters and noise, compositing or swapping with another image) and seeing how the network's prediction changes. If a given manipulation has a similar effect on the predictions of a human, this is good evidence that a robust representation has been learnt.

A common kind of local explanation question is "why is this instance classified as an $X$ even though it really is a $Y$?" This could be answered by finding a collection of images that are maximally different from the target instance (this is the tricky bit!) but are also classified as $X$, and another collection that are maximally similar but are classified as $Y$. Displaying both collections could give insight into the specific common feature that has caused the error.

### Huang, Sandy H., David Held, Pieter Abbeel, and Anca D. Dragan. “Enabling Robots to Communicate Their Objectives.” *AUTONOMOUS ROBOTS* 43, no. 2, SI (February 2019): 309–26.

The aim here is to enable explainees to anticipate robot behaviour in novel situations, by providing insight into its objective function. This is done in a collaborative fashion; the robot behaves in a way that is maximally informative. Hence we have an cooperative inverse reinforcement learning (CIRL) problem, with the additional complication that the human will not be exact in their inference.

---

The specific example used is that of an autonomous driving in realistic scenarios. Only one dimension of the objective function is to be inferred: whether the vehicle is 'aggressive' or 'defensive'.

Let $S$ and $A$ be the continuous domains of states and actions in an environment $E$. At time $t$, we assume the reward $R_t$ is a linear combination of features $\phi$, weighted by some $\theta^*$. The features are themselves arbitrary functions of the initial $s_t$, action $a_t$ and subsequent state $s_{t+1}$. The agent's optimal trajectory $\xi_E^{\theta^*}$ is that which maximises the discounted sum of reward, and is determined by $\theta^*$ and the discount factor $\gamma$. *It is assumed that the agent acts optimally with respect to the objective*.

The explainee is modelled as starting with a prior belief $P(\theta)$ over what $\theta^*$ might be, and updating their belief as they observe the agent act. We don't have direct control over this updating process, rather our aim is to choose a sequence of $n$ environments $E_{1:n}$ such that when the explainee observes optimal trajectories in those environments, their updated belief has maximal density at $\theta^*$. Thus the optimisation problem is:
$$
\text{argmax}_{E_{1:n}}P(\theta^*|\xi^{\theta^*}_{E_{1:n}})
$$

#### Modeling the Explainee

To solve the problem we need a model of the belief update process: it is assumed that this can be modeled by Bayesian inference:
$$
P(\theta | \xi_{E_{1: n}}^{\theta^{*}}) \propto P(\xi_{E_{1: n}}^{\theta^{*}} | \theta) P(\theta)=P(\theta) \prod_{i=1}^{n} P(\xi_{E_{i}}^{\theta^{*}} | \theta)
$$
Assuming we have access to $P(\theta)$, the problem reduces to modeling how probable the explainee would find a given trajectory $\xi$ to be given an objective function parameterised by a given $\theta$ (i.e. $P(\xi|\theta)$).

If inference were exact, the explainee would assign probability $0$ to any trajectory that is not perfectly optimal given $\theta$, which in turn would give that $\theta$ a probability of $0$ and permanently eliminate it from the belief. A positive constant belief (e.g. $1$) would be assigned to all optimal trajectories observed. Assuming a uniform $P(\theta)$, the resulting distribution would be uniform across all remaining candidate $\theta$s, and this set would progressively reduce in size as more trajectories are observed. Clearly, this relies on the explainee being able to perfectly evaluate whether a trajectory is optimal, which is not realistic.

This assumption can be relaxed in one of two ways:

- Being more **conservative** about which $\theta$s are eliminated: the positive constant belief is assigned to all trajectories that seem 'close enough' to optimal. This can be done by defining a *distance metric* $d$ between trajectories, and assigning probability $0$ only if the distance to the optimal trajectory exceeds some value $\tau$.
  - $\tau$ must be chosen manually.
- Letting trajectories have a **probabilistic** effect on beliefs about $\theta$: instead of setting probabilities to zero, they are progressively decremented. Again the distance metric $d$ is used, and we can set $P(\xi_{E}^{\theta^{*}} | \theta) \propto e^{-\lambda \cdot d(\xi_{E}^{\theta}, \xi_{E}^{\theta^{*}})}$.
  - $\lambda$ must be chosen manually.

Now the challenge becomes that of defining a distance metric between trajectories. This can be done in terms of either the reward with respect to $\theta$, or the trajectories themselves:

- **Reward-based**: $d\left(\xi_{E}^{\theta}, \xi_{E}^{\theta^{*}}\right)=\theta^{\top} \phi\left(\xi_{E}^{\theta}\right)-\theta^{\top} \phi\left(\xi_{E}^{\theta^{*}}\right)$
- **Euclidean-based**: $d\left(\xi_{E}^{\theta}, \xi_{E}^{\theta^{*}}\right)=\frac{1}{T} \sum_{t=1}^{T}\left\|s_{E, t}^{\theta}-s_{E, t}^{\theta^{*}}\right\|_{2}$ (state dimensions should be normalised).
- **Strategy-based**: cluster trajectories into a number of *strategies*, and set $d\left(\xi_{E}^{\theta}, \xi_{E}^{\theta^{*}}\right)=0$ if $\xi_{E}^{\theta}$ and $\xi_{E}^{\theta^{*}}$ are in the same strategy cluster, and $\infin$ otherwise.

This means that we have six possible approximate inference models $\mathcal{M}$, in addition to the exact model.

---

The state of a vehicle in a driving simulator is defined as $\mathbf{x}=[x,y,\theta,v,\alpha]^{\top}$, where $x$ and $y$ are the coordinates, $\theta$ is the heading, $v$ is the speed an $\alpha$ is the steering angle. The control input $\textbf{u}=[u_1,u_2]^\top$ is the change in steering angle $u_1$ and acceleration $u_2$. 

A variety of simulated three-lane merging, braking and tailgating scenarios with one controlled car and one uncontrolled car. As described above, the reward is a weighted sum of a handful of features $\phi$, which are hand-engineered to quantify the distance to the other car, the severity of acceleration and turning, the deviation from a target speed, and the distance to a goal location. The weights $\theta^*$ define whether optimal behaviour is 'aggressive' or 'defensive'.

Results with various inference models:

- With the exact inference model, the choice of trajectories does not matter;
- The Euclidean distance metric produces the most robust results.

Results with real people from MTurk (get them to pick which of four trajectories seems to best fit the car's strategy, and provide a confidence score):

- Quality > quantity: increasing the number of example trajectories seems to have little effect on performance.
- Euclidean-based distance best models real inference and reward-based is the worst.
- There is little difference between conservative / probabilistic belief updating. If anything, conservative appears slightly better.

The whole lot actually doesn't seem to be much better than random, *until* it is observed that people tend to perform well on test cases for strategy clusters where they had seen an example, and badly otherwise. In fact, people do *worse* on a test with strategy $A$ if they have only seen strategy $B$, compared with seeing no demonstration at all! It seems that without good coverage, explainees develop a bias to assume trajectories will always fall into the classes they have observed.

The solution to this is to add an incentive for good *strategy cluster coverage* into the objective function (basically just maximise the number of clusters shown in the examples). This, when combined with the best approximate inference model (conservative belief updates, Euclidean-based distance) yields the best performance in terms of trajectory prediction.

### Kraus, Sarit, Amos Azaria, Jelena Fiosina, Maike Greve, Noam Hazon, Lutz Kolbe, Tim-Benjamin Lembcke, Jörg P. Müller, Sören Schleibaum, and Mark Vollrath. “AI for Explaining Decisions in Multi-Agent Environments.” *ArXiv:1910.04404 [Cs]*, October 10, 2019.

In multi-agent systems:

> …explanations should aim to **increase user satisfaction**, taking into account the system’s decision, the user’s and the other agents’ preferences, the environment settings and concepts such as fairness, envy and privacy. 

The complexity of the goal structure and the presence of multiple sets of preferences in a MAS makes explainability harder, and even more important.

==Note== the primary perspective taken here seems to be that of a global system controller, which must provide explanations to the *human* agents themselves.

---

Most experiments with explainability have taken a computational / engineering approach, which lacks experiments with people, and in turn provides little evidence of any actual increase in trust or understanding. We should look to the *psychology literature* for evidence of how to do this properly.

Open problems include:

- **Efficient algorithms** for (realtime) explanation generation. Envisage these following a two-stage process: (1) explanation *generation*; and (2) *downselection* based on the explanation context. 
- **Explainee modeling** for increased satisfaction, which may continue during sustained interaction. The authors *couldn't find any prior work* on preference elicitation for this specific purpose. Suggest that extensive data collection could be beneficial here.
- **Interactive explanation** through dialogue, which potentially provides an atlternative to explainee modeling by allowing them to guide the process in a direction that is personally meaningful. It may be beneficial to *model the dialogue as a POMDP* where the uncertainty is about the explainee's beliefs.
- **Managing incomplete and extraneous information**: as more agents are added to a MAS, the proportion of information that is irrelevent to any given event increases, as does the probability that the explainee is missing certain background knowledge required to understand an explanation. 

Some more points made along the way:

- Meta-issues include the importance of privacy, its tension with the ethics of withholding information, and the value of open source code and public datasets.

- Explainability is not just an issue with fashionable AI techniques such as deep learning; we should also seek this property when developing more traditional control and optimisation algorithms.
- The automated generation of *graphical explanations* is an interesting direction: this could enable compact summarisation of large amounts of information. 

### Lee, Jung Hoon. “Complementary Reinforcement Learning towards Explainable Agents.” *ArXiv:1901.00188 [Cs, Stat]*, January 1, 2019.

Existing work on RL interpretability has all been post-hoc. Propose a method for deriving a rule-based explainable agent (called a *quasi-symbolic* (QS) agent) from an NN-based RL agent.

---

Reference RL agent: actor-critic with feedforward networks (one hidden layer, $100$ neurons each).

QS agents learn (by observing RL agents’ behaviors) the values of state transitions, identify the most valuable as *hub* and search for action sequences to reach one. If such a plan cannot be found, the best action is chosen by comparing the values of immediate transitions.

A QS agent consists of two single-layer networks, that are sequentially connected. The first of these, called the *matching network*, seeks to memorise state transition $s\rightarrow s'$. It takes the state transition vector (computed as $\Delta s=s-s'$) as input and computes the *cosine similarity* between it and a number of stored transitions. If all similarities are below a threshold $\theta$, the transition is considered novel and is itself stored for future comparison. A new input node is also added to the second network – the *value network* – so that the two remain compatible. The connection weight between the two new nodes is initialised to equal the reward obtained by the RL agent with the selected action. If, on the other hand, the input matches one of the previously-stored transitions (i.e. $\theta$ is exceeded), the connection to the corresponding value network node is updated by simply adding the current reward.

==Why on earth does this need to be implemented as two 'networks'? Speed / parallelisation?==

A final network – the *environment network* – seeks to model the dynamics of the environment. It takes as input the current state vector $s$ and action $s$ and outputs a prediction for the next state vector $s'$.

After some amount of training, any stored transition with a value network weight more than $\alpha$ standard deviations above the mean is identified as a hub. The next step is to search for an action plan to reach one of the hub states. At each state, this is done by recursively calling the RL agent and environment network to predict future sequences of actions and states. At each simulated iteration, the transition vector is examined to see if it matches a hub. If so, they stop planning and execute the current plan of actions. If ten iterations are completed without reaching a hub, the search starts again. Four restarts are allowed, after which point simply the action with the highest immediate value is selected.

---

It is claimed that QS agents are more transparent than RL agents because they have simple, easily-analysed structures. But they rely on RL agents to propose their actions in the first place! At best, this system provides a simplified justification for choosing one inexplicably-derived action over another.

### Madumal, Prashan. “Explainable Agency in Intelligent Agents.” In *AAMAS `19: PROCEEDINGS OF THE 18TH INTERNATIONAL CONFERENCE ON AUTONOMOUS AGENTS AND MULTIAGENT SYSTEMS*, 2432–34, 2019.

Brief overview of his PhD topic.

Makes an implicit distinction between the interpretable ML and explainable agency fields; they definitely seem to be separate communities right now.

Is interested in designing *explainable interfaces* that enable a dialogue between explainer and explainee. Explanation models should be grounded in the way humans explain their actions; otherwise they will not resonate with a human explainee.

Human explanations are inherently *causal*, so we should be building causal explanation interfaces. Explicitly references Pearl as the authority in this area: why questions demand counterfactual reasoning.

> In the reinforcement learning problem, we model the the causal graph as a DAG which constitutes of state variables and rewards as nodes, actions as edges. Moreover we define actions as interventions that is done to the causal graph. We assume causal Markov condition to the graph. Causal relations of the variables has to be known prior in the given domain. Then we introduce algorithms to generate explanations for why and why not questions. We leverage the policy of the agent in a given snapshot to obtain the state variable values, and then apply them to the causal graph. We can then generate the explanation by 1) Obtaining the explanandum (variable/action that user needs explanation; and 2) Generating the explanans (explanation) by traversing the causal graph through to root reward node. We formalise the problem through structural causal equations, with the variable relation modeled as a linear relation. For evaluation, we choose Starcraft II. 

Tested by using the system to give explanations to humans, then asking the humans to predict further behaviour based on their gained knowledge. Measured quality of these predictions as well as the 'satisfaction' and 'trust' of the participants. Improvements in both quality and satisfaction were statistically significant versus "previous models".

So this is all very well, but if causal relations are already known then we're not doing very much. *Causal discovery* will be explored in future work. Will seek to learn dynamic Bayesian networks as per [7].

### Qin, Zengchang, and Jonathan Lawry. “Prediction Trees Using Linguistic Modelling,” 2005, 6.

Previously [8] proposed an algorithm for learning linguistic decision trees (LDTs). Here, linguistic expressions such as 'small', 'medium' and 'large' are used to build a tree guided by information based heuristics. For each branch, instead of labeling it with a certain class (such as positive or negative) the probability of members of this branch belonging to a particular class is evaluated from a given training dataset. Unlabeled data is then classiﬁed by using probability estimation of classes across the whole decision tree. 

Here, the method is extended to regression problems. 

---

#### Label Semantics

The underlying theory for LDTs is that of *label semantics*. Given a variable $X\in \mathcal{X}$, a specific value of that variable $x$, and a set of linguistic labels $LA$, we imagine an individual $I$ identifying a subset of labels $D_x^I$ that describe $X=x$. If we then allow $I$ to vary across a population $V$, then $D_x^I$ will also vary and generate a random set into the power set of $LA$, denoted $D_x$. The frequency of occurrence of a particular subset of labels $S\in LA$ in $D_x$ can be used to compute a mass assignment:
$$
\forall S\sube LA,\ \ \ m_x(S)=\frac{|\{I\in V:S\in D_x^I\}|}{|V|}
$$
These label semantics are *taken as given* by an LDT. Assuming they have been defined, we can compute the *appropriateness degree* of each label $L$ at a particular $x$, denoted $\mu_L(x)$, as follows:
$$
\forall x\in\mathcal{X},\forall L\in LA,\ \ \ \mu_L(x)=\sum_{S\sube LA:L\in S}m_x(S)
$$
Our final definition is that of a *focal set* for a value $x$: the set of subsets of $LA$ with non-zero mass:
$$
\mathcal{F}=\{S\sube LA:\exist x\in\mathcal{X},m_x(S)>0\}
$$

---

#### Linguistic Decision Trees

Now consider $n$ input variables for a $k$-class classification problem. Each branch of an LDT is defined by a list of $n$ focal sets, one for each variable, and a probability for each class. For example, one branch $B$ in an LDT with $n=k=2$ may look like this:
$$
B=(\ [\mathcal{F}^B_1:\{small\},\ \mathcal{F}^B_2:\{orange,red\}],\ 0.3,0.7\ )
$$
Suppose we have training data $\mathcal{D}$ with $N$ instances: $\mathcal{D}=\{(\textbf{x}_1,c_1),...,(\textbf{x}_N,c_N)\}$ which has been used to train an LDT with $s$ branches. For a given test datapoint $\textbf{x}$, the probability of a branch $B_b$ for $b\in\{1..s\}$ can be computed as
$$
P(B_b|\textbf{x})=\prod_{i=1}^n m_{x_i}(\mathcal{F_i^{B_b}})
$$
The probability of class $C=c$ given $B$ can then be evaluated by 
$$
P(c|B_b)=\frac{\sum_{j\in T}P(B_b|\textbf{x}_j)}{\sum_{j=1}^NP(B_b|\textbf{x}_j)}
$$
where $T$ is the subset of instances in $\mathcal{D}$ with class $c$. According to Jeffrey's rule, the probability of class $c$ given $\textbf{x}$ is therefore
$$
P(c|\textbf{x})=\sum_{b=1}^sP(c|B_b)P(B_b|\textbf{x})
$$

---

#### Linguistic Decision Trees for Regression

We now move on to considering a continuous target attribute $Y\in \mathcal{Y}$ instead of a class $C$, which has its own set of focal elements $\mathcal{F}_y$. We can start by considering each focal element as a class label, although this introduces a problem since focal elements overlap. This can be rectified by factoring the membership of $Y=y$ for a particular focal element $\mathcal{F}_y^u$, which can be measured as 
$$
\xi_y^u=m_y(\mathcal{F}_y^u)
$$
The probability of $\mathcal{F}_y^u$ given a branch $B$ is therefore
$$
P(\mathcal{F}_y^u|B_b)=\frac{\sum_{j\in T}\xi_y^uP(B_b|\textbf{x}_j)}{\sum_{j=1}^NP(B_b|\textbf{x}_j)}
$$
and in turn
$$
P(\mathcal{F}_y^u|\textbf{x})=\sum_{b=1}^sP(\mathcal{F}_y^u|B_b)P(B_b|\textbf{x})
$$
To predict $\hat{y}$ for a given unlabeled $\textbf{x}$, we first obtain the probabilities of focal elements as above, then compute
$$
\hat{y}=\sum_uP(\mathcal{F}_y^u|\textbf{x})\mathbb{E}(y|\mathcal{F}_y^u)
$$
where $\mathbb{E}(y|\mathcal{F}_y^u)$ is calculated through a process of *defuzzification* as follows:
$$
E\left(y|\mathcal{F}_y^u\right)=\frac{\int_\mathcal{Y}y\cdot m_{y}\left(\mathcal{F}_y^u\right) dy}{\int_\mathcal{Y} m_y\left(\mathcal{F}_y^u\right) dy}
$$

---

In what appears to be a slight tangent, also propose the method of *branch merging* as an alternative to pruning for making more compact trees and preventing overfitting.

---

In experiments, an LDT is shown to match the performance of more black box regression algorithms e.g. $\varepsilon$-SVR, fuzzy Semi-Naive Bayes.

### Trodden, Paul, and Arthur Richards. “Cooperative Distributed MPC of Linear Systems with Coupled Constraints.” *Automatica* 49, no. 2 (February 2013): 479–87.

Propose a form of distributed model predictive control (DMPC) in which agents make decisions locally and cooperation is promoted by local consideration of a greater portion of the system-wide objective and the simulated design of plans for others. No explicit communication takes place. Robustness is guaranteed by only allowing one agent to replan per timestep.

**An interesting point to note: the terms "agent" and "subsystem" are used interchangeably.**

---

In the previously-proposed *tube DMPC* method, a single agent $p$, when faced with a system state $x(k)$, devises a plan $\textbf{u}_p(k)$ consisting of an initial state and a sequence of future control vectors for subsequent timesteps. The plan is subject to local constraints on possible action, and coupling constraints that depend on the plans of other agents, which define a cost function $J_p(\textbf{u}_p)$ to be minimised. All other agents in the system simply adopt the tails of their respective previous plans. The sequence that determines which agent is the optimising one is chosen by the designer.

In the cooperative method developed in this paper, $p$ additionally devises a *hypothetical* plan $\hat{\textbf{u}}_q$ each for other agent $q$ in some cooperating set $\mathcal{N}_p$. The optimisation problem here is
$$
\min_{\{\textbf{u}_p(k),\hat{\textbf{u}}_{\mathcal{N}_p}(k)\}} J_p(\textbf{u}_p)+\sum_{q\in \mathcal{N}_p}\alpha_{pq}J_p(\hat{\textbf{u}}_q)
$$
subject to a bunch of constraints. The cooperating set and weightings $\alpha_{pq}$ are chosen on-the-fly by the optimising agent at each timestep, and are essentially tuning parameters for the level of cooperation (from non-cooperative tube DMPC on one extreme, to something resembling centralised control on the other).

Following the optimisation, $p$ then communicates information about *only its own optimised plan* $\textbf{u}^*_q(k)$ to some of the other agents; its hypothetical plans for others remain internal. The main point is that **the optimising agent $p$ determines its own plan by considering what others may be able to achieve**.

Exactly what must be communicated between agents? It turns out, not the whole of $\textbf{u}^*_q(k)$ need be transmitted in all cases. In order to optimise at timestep $k$, an agent $p$ must have received:

- Full plans from all $q\in\mathcal{N_p}(k)$;
- Compressed messages relating to all the coupling constraints in which $p$ is involved, from each other agent involved $q\in \mathcal{Q}_{p_k}$ (where $\mathcal{Q}_{p_k}$ is set of all other agents coupled to $p$).
- Similar messages from all agents involved in coupling constraints with any of the agents in $\mathcal{N}_p(k)$.

Note that if $\mathcal{N}_p(k)$ is empty, the requirements reduce to just the coupling messages from $\mathcal{Q}_{p_k}$. 

However, in practical applications it may be that agents are unaware who will be optimising next, and which cooperating sets they will use, so if the communication channel allows, the transmission of full plans is always a conservative fallback option.

In the paper it is proved that this approach has the properties of robust constraint satisfaction and stability. As with any distributed control method, the advantage over centralised control is an increased robustness to agent failure or communication breakdown.

---

Did a couple of numerical and simulation experiments: **as the set of cooperating agents increases in size, the over solution cost decreases**. In one example, the greatest jump in benefit was attained by cooperating with just one agent instead of none.

### Zhang, Weiyang, Wenshuo Wang, and Ding Zhao. “Multi-Vehicle Interaction Scenarios Generation with Interpretable Traffic Primitives and Gaussian Process Regression.” *ArXiv:1910.03633 [Cs]*, October 8, 2019.

Use Bayesian nonparametric learning to temporally segment multi-vehicle interaction scenarios into interpretable building blocks called *traffic primitives*.

One of the biggest challenges of autonomous driving lies in the proper interaction with human drivers in complex scenarios. In addition to being efficient and obeying the constraints, planned trajectories must be *human-like* in order to be predictable.

The underlying observation is that human driver behaviour appears to be decomposable into fundamental building blocks. The aim is to automatically extract such primitives from demonstrated interaction scenarios with minimal prior knowledge, and use these to plan realistic driving behaviour.

---

A driving scenario is modelled as a Markov process where the observation of all $N$ vehicles involved at time $t$ is denoted $\textbf{s}_t=[s_t^1,…s_t^n]$. In order for the Markov property to hold, we assume that each observation contains *all* historic positions and velocities from the start of the scenario. It is assumed that $\textbf{s}_t$ is drawn from a distribution conditioned on a discrete hidden state $z_t$, which represents which traffic primitive it belongs to. This distribution has parameters $\theta_{z_t}$. The transition probability from traffic primitive $z_i$ to $z_j$ is denoted $\pi_{i,j}$. The transition distribution $\pi_i$ is modeled as a *hierarchical Dirichlet process* (HDP), which allows there to be a *countably infinite* number of primitives.

The model is used to learn primitives from a dataset of real-world pairwise vehicle interactions. The moment during a scenario where the latent traffic primitive switches is identified as a *changepoint* at which it can be inferred some critical decision or behavioural change has occurred. Analysis of the results indicates that changepoints are located at places where the trend of vehicle velocity over time changes (i.e. acceleration and turning), which seems to make sense.

---

Don't really understand the method by which they harnessed the changepoints for generative trajectories, but anyway it seemed to aid realism.

## 📚  Books

### Pearl, J. (2009). *Causality*. Cambridge University Press; 2nd Edition.



### Russell, S. (2019). *Human Compatible: Artificial Intelligence and the Problem of Control.* Allen Lane 



### Singer, P. (2011). *Practical Ethics*. Cambridge University Press; 2nd Edition.



## 🗝️  Key Insights

- X
- X