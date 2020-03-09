---
title: 'Weekly Readings #4'
date: 2019-11-03
permalink: /posts/2019/11/weekly-readings-4/
tags:
  - weekly-readings
---

Decision trees for state space segmentation; lightweight manual labelling as a 'seed' for interpretability;  the dangerous of homogenous distributed control; AI and the climate crisis.

## 📝 Papers

### Hayes, Bradley, and Julie A. Shah. “Improving Robot Controller Transparency Through Autonomous Policy Explanation.” In *Proceedings of the 2017 ACM/IEEE International Conference on Human-Robot Interaction - HRI ’17*, 303–12. Vienna, Austria: ACM Press, 2017.

As method is presented that enables robots to describe their policies and answer targeted queries from human collaborators. [It requires a fair amount of manual labour.]

Code-level annotation is implemented using function decorators, which provide natural language descriptions of each functional element of the program. As the program executes, state information is assembled from logs of these annotations. A graphical model is constructed from the observed code execution paths.

Explanations are constructed from a hand-made collection of natural language statements, each of which is grounded in a logical predicate implemented as a Boolean classifier. The problem of succinctly describing a set of target states is approached as one of finding the smallest expression of these logical predicates that precisely covers them. An algorithm is presented for solving this problem. 

Once these logical expressions have been established, a selection of bespoke secondary algorithms can be used to manipulate them into answers to queries such as *"why didn't you do action $x$?"*,  *"in what situations do you do action $y$?"* and *"what do you in situation $z$?"*. Summarising the entire policy amounts to answering a query of the latter form, where $z$ is the entire state space. An answer looks something like this:

> "I move north when I am south of a delivery area and have the part. I move east when I am west of a delivery area and have the part and not near a human zone. I move west when I am at a human zone. I do not perform move south. I pick the part when I am near a human zone and west of the delivery area and south of the delivery area. I place the part when I am at the delivery zone."

The method is model-agnostic, and is demonstrated on simple robotics problems with three controller types: tabular and approximate Q-learning, and hard-coded conditional logic. 

### Pyeatt, Larry D. “Reinforcement Learning with Decision Trees,” 2003, 6.

A decision tree is used as part of the function approximation pipeline in Q-learning, specifically to partition the observation space into discrete states more flexibly than can be achieved with the standard tabular approach. Given an observation vector $v_t$, the tree maps it to a state label $s_t$, then a tabular representation of $Q$ is consulted to determine $a_t$. The tree is grown in an on-policy manner using the following algorithm:

- Start with a single leaf node (i.e. a single state)
- On each timestep $t$:
  - Receive $v_t$ and reward $r_t$
  - Run $v_t$ through the extant tree to determine $a_t$
  - Use the Bellman equation to determine $\Delta Q(s_{t-1},a_{t-1})$ and update $Q(s_{t-1},a_{t-1})$
  - Also add $\Delta Q(s_{t-1},a_{t-1})$ to a *history list* for the leaf corresponding to $s_{t-1}$
  - If the length of the history list for $s_{t-1}$ > a minimum length:
    - Compute the mean $\mu$ and standard deviation $\sigma$ of the history list
    - If $\vert\mu\vert<2\sigma$:
      - Split this leaf using e.g. information gain Gini coefficient, t-statistic…

The approach is compared favourably with tabular and NN-based methods on the standard mountain car and pole balance problems, as well as a race car simulator that is too large to be solved by a vanilla tabular approach. A leaf splitting function based on the t-statistic is found to yield the best performance.

### Rolnick, David, Priya L. Donti, Lynn H. Kaack, Kelly Kochanski, Alexandre Lacoste, Kris Sankaran, Andrew Slavin Ross, et al. “Tackling Climate Change with Machine Learning.” *ArXiv:1906.05433 [Cs, Stat]*, June 10, 2019.

This is an in-depth overview of the many ways in which those with ML expertise can help tackle the climate crisis. Key areas include:

- **Energy**: Generation and demand forecasting, optimised scheduling and resource allocation (perhaps via decentralised market-based systems). Enhanced data analysis pipelines to accelerate research in material science (batteries, carbon capture solar cells, turbine blades…) and nuclear fusion. 
- **Transportation**: Optimisation of processes such as freight routing and electric car charging, and general service improvements for low-carbon options such as rail and cycling. Shared mobility platforms, autonomous vehicles and alternative fuel research  are all risky, as too much innovation may increase demand.

- **Infrastructure and industry:** Smart buildings and infrastructure with reduced emissions and greater resilience. Optimisation of supply chains and industrial processes, and research into new materials, generative design methods and additive manufacturing. Technologies for precision agriculture and automated management of protected landscapes (especially drones).

- **Monitoring and resilience**: Data analysis (especially satellite images) for tracking ecosystems and biodiversity, spotting deforestation, predicting and reacting to natural disasters, and forecasting crop yields.

- **Tools for individuals**: Impact calculators to increase understanding, and personal behavioural models paired with nudge interventions to facilitate change.

In addition, some techniques seem to be generally useful in many domains: 

- Modeling, forecasting and prediction of complex dynamical systems (emissions, transport demand, impact of geoengineering, effect of climate change on economies, migration…)
- Transfer learning and integration of domain knowledge to enable working with sparse data.
- Interpretability and uncertainty quantification.

### van der Waa, Jasper, Jurriaan van Diggelen, Karel van den Bosch, and Mark Neerincx. “Contrastive Explanations for Reinforcement Learning in Terms of Expected Consequences.” *ArXiv:1807.08706 [Cs, Stat]*, July 23, 2018.

Here the idea is for an RL agent to explain its behaviour in terms of expected consequences. This is enabled by the addition of manually-defined classifier functions that assign Boolean labels $\textbf{C}$ to states $s\in S$ (e.g. *"is the agent next to a forest?"*). States that incur significant positive or negative reward are referred to as *outcomes*, and labels are assigned from a different set $\textbf{O}$. Outcomes are flagged as positive ($o^+$) or negative ($o^-$), so that they can be presented differently in textual explanations.

Given these definitions, it is relatively easy to write an algorithm that can produce a policy description conditioned on a starting state $s$, which could look something like: *"for the next $n$ actions I will mostly perform action $a$, which will lead me into situations $[c_1,c_2,...]$. This will cause  $[o^+_1,o^+_2,...]$, but also  $[o^-_1,o^-_2,...]$"*. This frames the policy description problem as one of predicting future behaviour.

The more ambitious aim is to answer contrastive questions, which consist of a *fact* and *foil* as in the following:

> ”Why do you move up and then right (fact) instead of moving to the right until you hit a wall and then move up (foil)?” 

This is done by deriving a new reward model $R_I$ that initially values the state-action pairs mentioned in the foil, but then gradually transgresses back towards the original reward model. A corresponding value function $Q_I$ is then trained through simulation, and combined with the real learned value function $Q_t$ to obtain a foil value function $Q_f$:
$$
\forall s,a\in S,A\ \ \ Q_f(s,a)=Q_t(s,a)+Q_I(s,a)
$$
This can then be used to define a foil policy $\pi_f$. The stated motivation behind this [computationally expensive!] method is that gradually transitioning back to the learned policy allows the foil to be more realistic with respect to the agent's actual behaviour, instead of being an unrealistic hypothetical. Answers to contrastive queries should focus on the differences (especially in the sets of outcomes) between trajectories derived from the real policy $\pi_t$, and those from $\pi_f$. [The authors claim to have implemented this approach, but no detail is provided.]

### Wachter, Sandra, Brent Mittelstadt, and Luciano Floridi. “Transparent, Explainable, and Accountable AI for Robotics,” 2017.

The very fact that AI is so inscrutable and diverse makes it hard to legally codify our rights with respect to it. GDPR's *right to explanation* is nonbinding, and only vague reference is made to requiring "meaningful information" about the "rationale" and logic" involved in decision making, which is very hard to convert into tangible results. In addition, the safeguards apply only to fully autonomous decisions, thus not those made by human-machine teams, and only to those with "legal" or "significant" effects.

Key technical areas that require further research are identified:

- Design of inherently interpretable systems that don't sacrifice performance.
- Development of tools that allow black box systems to comply with legal requirements.

## 🎤 Talks

### Kent, Tom. “Ignorance Is Bliss: The Role of Noise and Heterogeneity in Training and Deployment of Single Agent Policies for the Multi-Agent Persistent Surveillance Problem.” presented at the UoB Collective Dynamics Seminars, October 30, 2019. 

Training multi-agent policies is hard. Noise, under-modelling and uncertainty is compounded with every additional agent, as are interaction effects. With enormous state and parameter spaces, a large amount of data are needed to make learning approaches work. But do we need to solve the whole problem at once? Can we instead **train single-agent policies in isolation that can be successfully deployed in multi-agent scenarios**? 

The specific scenario considered here is that of persistent surveillance: coverage of a 2D hex grid, where each hex provides a score which decays exponentially with time since last visit. A big problem with deploying homogenous policies in environments like this is that of *policy convergence*: the agents fall into the same exploration pattern! This can be addressed by adding *stochasticity* at one of several points in the observation-decision-action cycle, or by deliberately deploying *heterogenous* policies. Another approach is to only allow agents access to *local knowledge* about their immediate vicinity.

One avenue explored involved combining the local knowledge approach with communication between nearby agents, but this was found to cause agents' beliefs to converge *too well* to the ground truth, and thus reintroduce policy convergence! 

Finally, it is acknowledged that higher-level planning (i.e. algorithms operating at the population level) does seem to be more effective than local policies, though this of course requires better communication and coordination. 

## 🗝️  Key Insights

- A specific explanation query can be thought of as a 'slice' of the generic question *"what is your policy?"*. If an interpretable [logic-based?] representation of the full policy were possible, an answer to any specific question would not be too hard to come by.
- A relatively small amount of manual intervention, namely the definition of some Boolean classifiers to label states, might be enough to imbue a learning system with the semantic content it needs to answer explanation queries.
- There hasn't been a huge amount of work on integrating decision trees into the RL framework, but one possible direction is to use them to slice up the state space into a small number of meaningfully-differentiated states.
- Machine learning can have a large positive impact on efforts to resolve climate crisis, most clearly as a tool for prediction and planning. General efforts to improve handling of sparse data, uncertainty quantification and interpretability will be particularly useful in this context.
- Interpretability methods may in the future be seen as tools that allow black box models to comply with legal requirements that would otherwise prohibit their use. That said, crisply-defined requirements of this sort don't really exist yet.
- Some degree of heterogeneity is desirable in many multi-agent systems since it prevents policy convergence; it can be provided by simply adding noise and, somewhat, paradoxically, limiting communication capabilities. That said, a good global controller would never suffer from the convergence problem – in which circumstances exactly is distributed control actually worth doing?