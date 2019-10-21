---
title: 'Weekly Readings #2'
date: 2019-10-20
permalink: /posts/2019/10/weekly-readings-2/
tags:
  - weekly-readings
---

Approximately three weeks in, I'm starting to work on a case study project that will allow me to explore some of the key ideas around multi-agent explainability – collision avoidance within a population of autonomous vehicles on road / track networks. As a result, more of my reading this week has focused specifically on the multi-agent context.

## 📝 Papers

### Amir, Ofra, Finale Doshi-Velez, and David Sarne. “Summarizing Agent Strategies.” *Autonomous Agents and Multi-Agent Systems* 33, no. 5 (September 2019): 628–44.

Humans are boundedly rational and there's no reason why we should understand the actual reasoning process of an autonomous system. The idea behind strategy summarisation is to provide explainees with some form of overview that demonstrates system behaviour in carefully selected state-action pairs. This allows understanding of likely future behaviour in addition to merely explaining existing decisions. The problem can be broken down into:

- **Intelligent state extraction**: finding state-action pairs to present. There are multiple approaches here. We could seek *interesting* examples, such as those that have high likelihood, or where there is a large variation in reward between good and bad actions, or where two agents' policies disagree. We could seek *informative* examples, that optimise for the ability of a human or another model to reconstruct the agent's policy (e.g. via imitation learning or inverse reinforcement learning). Finally, we could try getting groups of people to attempt to program the system through *manual* policy design, and determine which states and actions are viewed as important.
- **State representation**: determining how to compactly convey information about potentially complex state and action spaces to people with varying levels of expertise.
- **Strategy summary interface**: designing software environments for explainees to interact with summaries. It is important to learn the explainee's preferences over time, identify instances where they may have erroneously extrapolated from a summary, and correcting for such errors.

The importance of standardised test environments and performance metrics is stressed, and autonomous transport is identified as one of the key impact areas for this technique. 

### Bryson, Joanna J. “Embodiment vs. Memetics: Does Language Need a Physical Plant?,” 2001, 6.

A central premise of embodied AI is that it will solving the semantic grounding problem by providing biases and constraints for perception and action. Here it is argued that it may not be the only way of doing so. The paper uses careful definitions:

- **Semantics**: how a word is used.
- **Expressed behaviour**: that which impacts the environment and is thus externally visible.
- **Grounded**: associated with a representation that determines an expressed behaviour.
- **Understand**: connect a semantic term to a grounded concept.
- **Embodiment**: the property of having rich interactions with an environment, which lies a continuum of degree.

The assertion of this paper is that human-like semantics can be derived without any significant degree of embodiment, and is just another form of automated perceptual learning. This view is motivated by considering word embedding in vector space: words that commonly co-occur are located nearby in the space. This requires no grounding. Note that humans very frequently transmit semantic information that they don't understand. [Especially in academic circles!]

As a result, there's no reason why Searle's Chinese room could not be a fantastically useful tool and valid participant in science and culture. This is not to say that it would be a complete model of human intelligence, which clearly does use grounding, but that's not what we're interested in here. We should try building a Chinese room!

### Dethise, Arnaud, Marco Canini, and Srikanth Kandula. “Cracking Open the Black Box: What Observations Can Tell Us About Reinforcement Learning Agents.” In *Proceedings of the 2019 Workshop on Network Meets AI & ML - NetAI’19*, 29–36. Beijing, China: ACM Press, 2019.

Here the aim is to understand the behaviour of an RL agent used for video bit rate adaptation in streaming platforms. Here the goal is to maximise user enjoyment, which is a function of both the video quality and buffering time; these are in tension. The $25$ input features for the model include the current buffer duration and the download time of the several most recent $4$-second data chunks. The action space is the six possible bit rates. In the end, some relatively standard interpretability methods are employed:

- High-level statistics on selected action and comparison to theoretical optimality;
- LIME for feature importance;

but *when combined with extensive domain knowledge*, this actually provided quite a bit of insight. However, several important questions could not be answered by this approach:

- Finding outliers where performance breaks down;
- Ensuring stability of learning;
- Detecting whether the policy is sub-optimal (local maximum), either during or after learning.

### Garnelo, Marta. “Reconciling Deep Learning with Symbolic Artificial Intelligence: Representing Objects and Relations.” *Current Opinion in Behavioral Sciences*, 2019, 7.

Deep learning alone has three major shortcomings: data inefficiency; poor generalisation; and lack of interpretability. These align with the strengths of symbolic AI [and vice versa!] Reconciliation of the connectionist and symbolic paradigms is today's greatest challenge in AI. This paper is a review of recent attempts at integrating two key aspects of symbolic AI into connectionist systems: compositionality and relationality:

- **Compositionality** is an essential principle in linguistics, but there is no equivalent constraint on the representations inside a deep learning model. It appears that by default, gradient descent tends to produce distributed and entangled representations, whose component parts have little or no meaning in isolation. Solutions include incentivising disentangled representations in the loss function (as is done in a variational autoencoder); and imposing compositional structure on the representations from the outset.
- Most work on disentanglement has focused on images containing a single object; additional work is needed to consider **relations** between multiple objects for propositional reasoning. Relation networks and self-attention networks are two kinds of multi-network model that can learn pairwise relations between a fixed set of $n$ objects. They can be used to answer questions such as "how big is the sphere that is the same colour as the small cube?"

While these areas of work are interesting and appear to create 'logic-like' representations if we squint, they lack the full expressive power of actual, crisply-defined logic, particularly the presence of **variables** and **quantification**, and proper multi-step **inference** mechanisms.

### Hoffman, Robert, Tim Miller, Shane T. Mueller, Gary Klein, and William J. Clancey. “Explaining Explanation, Part 4: A Deep Dive on Deep Nets.” *IEEE Intelligent Systems* 33, no. 3 (2018): 87–95.

Global explanation is valuable so that the explainee can build a mental model of the system, but often what we require is a local, instance-specific explanation. Some researchers argue that *all* local explanation questions can be framed as counterfactual ones. 

The proposal here for is to *use adversarial examples as contrast cases, and frame the explanation problem as one of scientific exploration*. Here we achieve explainability by seeing how the system operates near its 'boundary conditions'. The specific domain considered is that of images. We can imagine manipulating test images in a controlled way (e.g. by adding filters and noise, compositing or swapping with another image) and seeing how the network's prediction changes. If a given manipulation has a similar effect on the predictions of a human, this is good evidence that a robust representation has been learnt.

A common kind of local explanation question is "why is this instance classified as an $X$ even though it really is a $Y$?" This could be answered by finding a collection of images that are maximally different from the target instance (this is the tricky bit!) but are also classified as $X$, and another collection that are maximally similar but are classified as $Y$. Displaying both collections could give insight into the specific common feature that has caused the error.

### Huang, Sandy H., David Held, Pieter Abbeel, and Anca D. Dragan. “Enabling Robots to Communicate Their Objectives.” *AUTONOMOUS ROBOTS* 43, no. 2, SI (February 2019): 309–26.

The aim here is to enable explainees to anticipate robot behaviour in novel situations, by providing insight into its objective function. The specific example used is that of an autonomous driving in realistic scenarios. 

We assume that the agent's reward function is parameterised by $\theta^\ast$. The explainee has a prior belief $P(\theta)$ which is updated as they observe a set of *optimal* trajectories $\xi^{\theta^*}_{E_{1:n}}$ in environments $E_{1:n}$. Our goal is to determine the best $E_{1:n}$. The update process is modeled by Bayesian inference:
$$
P(\theta | \xi_{E_{1: n}}^{\theta^{*}}) \propto P(\xi_{E_{1: n}}^{\theta^{*}} | \theta) P(\theta)=P(\theta) \prod_{i=1}^{n} P(\xi_{E_{i}}^{\theta^{*}} | \theta)
$$
Assuming we know $P(\theta)$, the problem reduces to modeling $P(\xi|\theta)$. If inference were exact, the explainee would assign probability $0$ to any trajectory that is not perfectly optimal given $\theta$, which in turn would give that $\theta$ a probability of $0$ and permanently eliminate it from the belief. A positive constant belief (e.g. $1$) would be assigned to all optimal trajectories observed. Assuming a uniform $P(\theta)$, the resulting distribution would be uniform across all remaining $\theta$s, and this set would progressively reduce in size with more observations. Clearly humans cannot perfectly evaluate optimality, so we can relax the assumption in one of two ways:

- Being more **conservative** about which $\theta$s are eliminated. This can be done by defining a *distance metric* $d$ between trajectories, and assigning probability $0$ only if the distance to the optimal trajectory exceeds some value $\tau$.
- Letting trajectories have a **probabilistic** effect on beliefs about $\theta$: instead of setting probabilities to zero, they are progressively decremented. Again the distance metric $d$ is used, and we can set $P(\xi_{E}^{\theta^{*}} \vert \theta) \propto e^{-\lambda \cdot d(\xi_{E}^{\theta}, \xi_{E}^{\theta^{*}})}$.

The distance metric can be defined in terms of either the reward with respect to $\theta$, or the trajectories themselves:

- **Reward-based**: $d\left(\xi_{E}^{\theta}, \xi_{E}^{\theta^{*}}\right)=\theta^{\top} \phi\left(\xi_{E}^{\theta}\right)-\theta^{\top} \phi\left(\xi_{E}^{\theta^{*}}\right)$ where $\phi$ are features derived from trajectories.
- **Euclidean-based**: $d\left(\xi_{E}^{\theta}, \xi_{E}^{\theta^{*}}\right)=\frac{1}{T} \sum_{t=1}^{T}\left\|s_{E, t}^{\theta}-s_{E, t}^{\theta^{*}}\right\|_{2}$ (state dimensions should be normalised).
- **Strategy-based**: cluster trajectories into a number of *strategies*, and set $d\left(\xi_{E}^{\theta}, \xi_{E}^{\theta^{*}}\right)=0$ if $\xi_{E}^{\theta}$ and $\xi_{E}^{\theta^{*}}$ are in the same strategy cluster, and $\infin$ otherwise.

This means that we have six possible approximate inference models in addition to the exact one. When testing with the exact inference model, found that the choice of trajectories does not matter. With the approximate models, the Euclidean distance metric produces the most robust results.

Also tested with real people from MTurk (got them to pick which of four trajectories seems to best fit the car's strategy, and provide a confidence score). Found that:

- Quality > quantity; increasing the number of examples has little effect on performance.
- Euclidean-based distance best models real inference and reward-based is the worst.
- There is little difference between conservative / probabilistic belief updating. 
- Performance only becomes significantly better than random examples when an extra term is added to the objective function to incentive a large number of strategy clusters in the examples: good coverage is very important!

### Kraus, Sarit, Amos Azaria, Jelena Fiosina, Maike Greve, Noam Hazon, Lutz Kolbe, Tim-Benjamin Lembcke, Jörg P. Müller, Sören Schleibaum, and Mark Vollrath. “AI for Explaining Decisions in Multi-Agent Environments.” *ArXiv:1910.04404 [Cs]*, October 10, 2019.

Take the view that:

> …explanations should aim to increase user satisfaction, taking into account the system’s decision, the user’s and the other agents’ preferences, the environment settings and concepts such as fairness, envy and privacy. 

Open problems include:

- **Efficient algorithms** for (real-time) explanation generation. Envisage these following a two-stage process: (1) explanation *generation*; and (2) *down-selection* based on the explanation context. 
- **Explainee modeling** for increased satisfaction, which may continue during sustained interaction. The authors couldn't find any prior work on preference elicitation for this specific purpose. Suggest that extensive data collection could be beneficial here.
- **Interactive explanation** through dialogue, which potentially provides an alternative to explainee modeling by allowing them to guide the process in a direction that is personally meaningful. It may be beneficial to *model the dialogue as a POMDP* where the uncertainty is about the explainee's beliefs.
- **Managing incomplete and extraneous information**: as more agents are added to a MAS, the proportion of information that is irrelevent to any given event increases, as does the probability that the explainee is missing certain background knowledge required to understand an explanation. 

Some more points made along the way:

- Most explainability work lacks experiments with people, and in turn provides little evidence of any increase in trust or understanding. We should look to the *psychology literature* for guidance.


- Meta-issues include the importance of privacy, its tension with the ethics of withholding information, and the value of open source code and public datasets.

- Explainability is not just an issue with fashionable AI techniques such as deep learning; we should also seek this property when developing more traditional control and optimisation algorithms.
- The automated generation of *graphical explanations* is an interesting direction: this could enable compact summarisation of large amounts of information. 

### Lee, Jung Hoon. “Complementary Reinforcement Learning towards Explainable Agents.” *ArXiv:1901.00188 [Cs, Stat]*, January 1, 2019.

Existing work on RL interpretability has all been post-hoc. Here a method is proposed for deriving a rule-based explainable agent (called a *quasi-symbolic* (QS) agent) from an NN-based actor-critic RL agent.

QS agents learn (by observing RL agents’ behaviors) the values of state transitions, identify the most valuable as *hub* and search for action sequences to reach one. If such a plan cannot be found, the best action is chosen by comparing the values of immediate transitions.

A QS agent consists of two single-layer networks, that are sequentially connected. The first of these, called the *matching network*, seeks to memorise state transition $s\rightarrow s'$. It takes the state transition vector ($\Delta s=s-s'$) as input and computes the cosine similarity between it and a number of stored transitions. If all similarities are below a threshold $\theta$, the transition is considered novel and is itself stored for future comparison. A new input node is also added to the second network – the *value network* – so that the two remain compatible. The connection weight between the two new nodes is initialised to equal the reward obtained by the RL agent with the selected action. If, on the other hand, the input matches one of the previously-stored transitions (i.e. $\theta$ is exceeded), the connection to the corresponding value network node is updated by simply adding the current reward.

A third network – the *environment network* – seeks to model the dynamics of the environment. It takes as input the current state vector $s$ and action $s$ and outputs a prediction for the next state vector $s'$.

After some amount of training, any stored transition with a value network weight more than $\alpha$ standard deviations above the mean is identified as a hub. The next step is to search for an action plan to reach one of the hub states. At each state, this is done by recursively calling the RL agent and environment network to predict future sequences of actions and states. At each simulated iteration, the transition vector is examined to see if it matches a hub. If so, they stop planning and execute the current plan of actions. If ten iterations are completed without reaching a hub, the search starts again. Four restarts are allowed, after which point simply the action with the highest immediate value is selected.

It is claimed that QS agents are more transparent than RL agents because they have simple, easily-analysed structures. [But they rely on RL agents to propose their actions in the first place! At best, this system provides a simplified justification for choosing one black-box-generated action over another.]

### Qin, Zengchang, and Jonathan Lawry. “Prediction Trees Using Linguistic Modelling,” 2005, 6.

Previously proposed an algorithm for learning linguistic decision trees (LDTs). Here, the method is extended to regression problems. 

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

Now consider $n$ input variables for a $k$-class classification problem. Each branch of an LDT is defined by a list of $n$ focal sets, one for each variable, and a probability for each class. For example, one branch $B$ in an LDT with $n=k=2$ may look like this:
$$
B=(\ [\mathcal{F}^B_1:\{small\},\ \mathcal{F}^B_2:\{orange,red\}],\ 0.3,0.7\ )
$$
Suppose we have training data $\mathcal{D}$ with $N$ instances: $\mathcal{D}=\{(\textbf{x}_1,c_1),...,(\textbf{x}_N,c_N)\}$ which has been used to train an LDT with $s$ branches. For a given test datapoint $\textbf{x}$, the probability of a branch $B_b$ for $b\in\{1..s\}$ can be computed as
$$
P(B_b\vert\textbf{x})=\prod_{i=1}^n m_{x_i}(\mathcal{F_i^{B_b}})
$$
The probability of class $C=c$ given $B$ can then be evaluated by 
$$
P(c\vert B_b)=\frac{\sum_{j\in T}P(B_b\vert\textbf{x}_j)}{\sum_{j=1}^NP(B_b\vert\textbf{x}_j)}
$$
where $T$ is the subset of instances in $\mathcal{D}$ with class $c$. According to Jeffrey's rule, the probability of class $c$ given $\textbf{x}$ is therefore
$$
P(c\vert\textbf{x})=\sum_{b=1}^sP(c|B_b)P(B_b\vert\textbf{x})
$$

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
P(\mathcal{F}_y^u\vert\textbf{x})=\sum_{b=1}^sP(\mathcal{F}_y^u\vert B_b)P(B_b|\textbf{x})
$$
To predict $\hat{y}$ for a given unlabeled $\textbf{x}$, we first obtain the probabilities of focal elements as above, then compute
$$
\hat{y}=\sum_uP(\mathcal{F}_y^u\vert\textbf{x})\mathbb{E}(y\vert\mathcal{F}_y^u)
$$
where $\mathbb{E}(y|\mathcal{F}_y^u)$ is calculated through a process of *defuzzification* as follows:
$$
E\left(y\vert\mathcal{F}_y^u\right)=\frac{\int_\mathcal{Y}y\cdot m_{y}\left(\mathcal{F}_y^u\right) dy}{\int_\mathcal{Y} m_y\left(\mathcal{F}_y^u\right) dy}
$$

In experiments, an LDT is shown to match the performance of more black box regression algorithms e.g. $\varepsilon$-SVR, fuzzy Semi-Naive Bayes.

### Trodden, Paul, and Arthur Richards. “Cooperative Distributed MPC of Linear Systems with Coupled Constraints.” *Automatica* 49, no. 2 (February 2013): 479–87.

Propose a form of distributed model predictive control (DMPC) in which agents make decisions locally and cooperation is promoted by local consideration of a greater portion of the system-wide objective and the simulated design of plans for others. Robustness is guaranteed by only allowing one agent $p$ to replan per timestep. The main point is that **$p$ determines its own plan by considering what others may be able to achieve**.

In addition to its own plan of actions $\textbf{u}_p$, $p$, devises a *hypothetical* plan $\hat{\textbf{u}}_q$ for each other agent $q$ in some cooperating set $\mathcal{N}_p$. The optimisation problem here is
$$
\min_{\{\textbf{u}_p(k),\hat{\textbf{u}}_{\mathcal{N}_p}(k)\}} J_p(\textbf{u}_p)+\sum_{q\in \mathcal{N}_p}\alpha_{pq}J_p(\hat{\textbf{u}}_q)
$$
where the cost function $J_p$ is defined by various constraints and objectives. The cooperating set and weightings $\alpha_{pq}$ are essentially tuning parameters for the level of cooperation. Following the optimisation, $p$ then communicates information about *only its own optimised plan* $\textbf{u}^*_q(k)$ to some of the other agents. Another agent is chosen to optimise on the next timestep.

In the paper it is proved that this approach has the properties of robust constraint satisfaction and stability. As with any distributed control method, the advantage over centralised control is an increased robustness to agent failure or communication breakdown. In numerical and simulation experiments, showed that as the set of cooperating agents increases in size, the overall solution cost decreases.

## 📚  Books

### Pearl, J. (2009). *Causality*. Cambridge University Press; 2nd Edition.

Moved onto the second chapter this week. Here we look at the problem of learning causal relationships from raw observation, which cannot be done without making assumptions:

- **Minimality principle**: say we have access to a probability distribution $P_O$ over observables $O$, which is only a subset of those $V$ that are in the underlying causal model. Our observations are insufficient to fully define the model. By applying *Occam's Razor*, we aim to find a minimal model: one that is consistent with the dependencies in observed data, but imposes *the fewest additional dependencies*.

- **Stability principle**: this encodes the assumption that all independencies in $P_O$ are stable: they are entailed by the structure of the model $D$ only. A stable distribution is one in which no additional independencies can be produced by merely tweaking the functional parameters $\Theta_D$. 

Following these principles produces a unique equivalence class of DAGs (called *pattern*) for any $P_O$. A pattern is a partially-directed graph. The *inductive causation* (IC) algorithm can be used to find a pattern compatible with $P_O$.

## 🗝️  Key Insights

- Policy summarisation through carefully-selected state-action pairs is a very general technique that can be applied to both the education of humans and the training of cloned algorithms. The definition of a 'good' example to show depends heavily on the purpose.
- One application of policy summarisation is to allow a human to perform inverse reinforcement learning. In this case, we must model their inference process. Bayesian inference is a good idea, but we must relax assumptions of rationality.
- For an agent whose goal is to inform and communicate, there is actually no strong evidence that semantic grounding is necessary. All that matters is that the terms are grounded *somewhere* along the communication pipeline, and that basic relational logic and grammatical rules are understood.
- Relatively simple interpretability tools – and even population-level statistics – are sufficient to provide significant insight if used by somebody with domain expertise.
- The main advantages that symbolic AI brings to the table are compositionality and relationality. Attempts to approximate crisp logic using connectionist models haven't really delivered the true benefits; perhaps the symbolic aspect needs to be explicit.
- As well as being a threat, adversarial examples could provide a useful tool for systematically probing the behaviour black box systems. We should view this like any other kind of scientific experiment.
- Regardless the nature of the underlying model, multi-agent systems are especially challenging, and especially important, targets for explainability research. This is due to issues such as partial observability, circular dependencies and large proportions of irrelevent information.

- Approaches like the quasi-symbolic agent may be useful for constraining the action of an RL system into a manageable number of 'clusters', but in themselves provide no real explanation or insight into the properties of these clusters.
- Linguistic decision trees are an interesting way of building a semantic layer into classification and regression models, while barely impacting their expressive capacity.
- In distributed multi-agent systems, systemwide optimality can be approached if agents plan the likely behaviour of others and determine their own actions accordingly. For stability, it may be important to only allow one agent to do this at any given time.
- While, strictly speaking, causal relationships cannot be learnt from observation alone, a couple of reasonable assumptions allow us to make some progress.