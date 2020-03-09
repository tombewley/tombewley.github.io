---
title: 'Weekly Readings #19'
date: 2020-02-23
permalink: /posts/2020/02/weekly-readings-19/
tags:
  - weekly-readings
---

Symbols and cognition; robust AI through hybridisation; causal modelling via RL interventions; environment as an engineered system.

## 📝 Papers

### Harnad, Stevan. “Computation Is Just Interpretable Symbol Manipulation; Cognition Isn’t.” *Minds and Machines* 4, no. 4 (November 1994): 379–90.

Harnad defines **computation** as the manipulation of symbols, based on rules which are themselves based on the symbols' (arbitrary) shapes alone, but which can be ascribed a grounded meaning by an external observer. The arbitrariness of the symbol shapes is another way of claiming substrate independence. On the other hand, in **cognition**, thoughts are *about* something intrinsically and directly, without any mediation. This is due to the fact that cognitive systems are physically and causally *grounded* in the external world through sensorimotor transduction. A substrate-independent simulation of this highly substrate-dependent property does not amount to the real thing, just as a simulated plane does not really fly.

### Mandler, Jean M. “How to Build a Baby: On the Development of an Accessible Representational System.” *Cognitive Development* 3, no. 2 (April 1988): 113–36. 

Unlike adults, infants are generally thought to be reactive agents who represent the world using low-level sensorimotor data. They lack the capacity to form abstract symbolic concepts, which are the basis of recall and sophisticated cognition. This view is largely attributable to Piaget. We should be wary of most experimental evidence that seems to disprove this. Behaviour that appears to respect conceptual categories does not mean those concepts are actually instantiated, and we may instead be merely projecting our own knowledge.

However, a couple of particular types of finding are more persuasive. Firstly, the reliable use of gestures in particular contexts (e.g. "I've finished my food"). Secondly, the ability to recall the locations of hidden and moved objects after a delay. Both of these behaviours require the storage of information in a form that is *accessible at a later time*. Mandler argues that this form must be symbolic. 

Those who believe that infants lack symbolic representations must explain how they can be eventually constructed from sensorimotor data alone. If we allow for some innate symbolic processes, the problem seems less daunting, and is one of increasing complexity and detail rather than a qualitative transition. 

It is important to note that there is no requirement for the early symbolic representations to have any verbal translations, which come later as the requirement for communication incentivises us to use common symbols. A lack of appreciation of this fact may have obscured our thinking in the past.

### Marcus, Gary. “The Next Decade in AI: Four Steps Towards Robust Artificial Intelligence,” February 14, 2020.

Marcus believes that it is not "human-level" AI that we should aim for per se, nor "general" AI, but *robust* AI which generalises gracefully within and across similar domains, and does not fall down at seemingly-innocuous edge cases. He frequently points to language models such as GPT-2 as examples of brittle systems, whose performance is mostly impressive but occasionally terrible. This is because their model-free learning induces only a thin shadow of true understanding, built on correlation rather than causation.

This paper advocates a form of hybrid AI that can perform both flexible data-driven learning and rigid symbolic manipulation. Such a hybrid should be build according to good engineering principles, in a hierarchy of complexity rooted in a few primitive, modular functions (also called *priors*). We don't currently know what these primitive functions should be, but cognitive science tells us that tools for reasoning about *time*, *space* and *causality* are good candidates. In addition, we may need a core, axiomatic knowledge database from which new facts can be derived, as per the ambition of Lenat et al's CYC project. Learning from data will certainly remain an important element, but it will be informed and guided by these innate structures. Achieving this goal will require a lot of tough human labour; far more than today's hardcore deep learning enthusiasts are likely to be comfortable with.

### Volodin, Sergei, Nevan Wichers, and Jeremy Nixon. “Resolving Spurious Correlations in Causal Models of Environments via Interventions.” *ArXiv:2002.05217 [Cs, Stat]*, February 12, 2020. 

Given an environment $\mu$ in which an agent has access to observations, and a mapping from the history of (observation, action, reward) tuples to a vector of high-level features $f\in\mathbb{R}^d$,  the goal of this work is to learn a linear structural causal model over these high-level features. This model consists of a directed graph $G$ with $d$ nodes, one for each feature, and labels on each edge describing the interaction coefficient, and the number of timesteps it takes for the parent node to influence the child. 

Many algorithms exist for learning causal models from data (here the simple *Granger 1-step causality* method is used) but what policy $\pi$ should we execute to discover the true model efficiently? In the case where an admissible model perfectly fits the history data, a random policy is sufficient. Otherwise, targeted *interventions* are required to resolve spurious correlations. 

The problem is defined in a minimax fashion: the graph should not be disproved by even the worse policy at any time. This is similar to the scientific method: we want to learn causal relationships that are true no matter which experiments or actions we perform:

$$
G^\ast=\underset{G}{\text{argmin}}\underset{\pi}{\max}\underset{t}{\max}\ L_{\pi,t}(G)
$$

where $L_{\pi,t}$ is a loss function that measures how well the model fits all data seen until time $t$.  We approximate a solution to this problem using RL with a variable reward function to modify the policy over time. At each policy iteration $i$, we identify an *uncertain* feature of the extant causal model, and set the reward function to reward states that *disprove* that feature. Uncertainty is measured by the variability of the feature when trained on different subsets of the data. Several implementations of this idea are compared

- **Intervention design via edges**: Identify the most uncertain edge, between features $i$ and $j$. If this has a positive coefficient, incentivise states that have high values of $f_i$ and low values of $f_j$. This is done by setting $R=f_i-f_j$ [which seems to assume features have a common range e.g. $[0,1]$]. For negative coefficients, $R=f_i+f_j$ is used.  
- **Intervention design via nodes**: Identify the most uncertain node and reward setting the corresponding feature to a fixed, randomly chosen value, while keeping the distribution of all other features unaltered.

- **Intervention design via loss**: Rather than explicitly selecting an edge or node, simply reward policies which give a high causal graph loss: $R=L_{\pi,t}(G)$. This is similar to curiosity-based approaches.

The approach is tested in a grid-world environment, in which the agent must collect keys to open chests containing reward, and consume to prevent its health dropping to zero. Noise is added to observations so that the agent occasionally observes food in cells where none exists. A ground-truth causal diagram can be drawn between variables such as "at food?", "health", "collected keys?", and the reward value. If the environment is randomly generated for each episode there are no spurious correlations, but in fixed layouts there are and interventions are required. 

*The loss-based intervention method significantly outperforms the others,* which is great because it's also simpler and doesn't require a decision be made about which feature to intervene on. Allowing for $20$ separate interventions, this method learns the true causal model after a median of $1000$ episodes, and fails to learn it at all in just $1$ out of $\sim 15$ runs. 

### Weyns, Danny, Andrea Omicini, and James Odell. “Environment as a First Class Abstraction in Multiagent Systems.” *Autonomous Agents and Multi-Agent Systems* 14, no. 1 (October 18, 2006): 5–30.

In multiagent systems (MAS) research, the environment is typically considered an implicit part of the system that is either given minimal thought or dealt with in an ad hoc way. This leads to missed opportunities and poor engineering practice. This paper aims to direct greater attention to the various roles played by the environment, and encourages us to consider it something that can be explicitly engineered.

Reviewing existing literature on the topic, the authors identify three *levels of support* that can be provided by an environment:

1. Acting as a *direct* interface between the agents and the low-level deployment context, as well as each other (note that it is best to think of agents themselves as unobservable entities).
2. Providing an appropriate layer of *abstraction* to shield the agents from the low-level details of the context.
3. Providing a medium for *interaction* between agents, either by regulating access to shared resources or by mediating communication. At this level, the environment becomes an active entity in the system, managing resource dynamics independent of agent activities.

With this in mind, it is argued that these environmental responsibilities should be brought within the remit of the MAS designer. A high-level functional decomposition of a generic environment is proposed, which depicts it as situated between the agents and their deployment context. 

The proposed generic model has a modular structure, including:

- A *state* module that maintains an abstract representation of the current condition of the deployment context including the quantities of resources.
- *Laws* and *dynamics* that structure how the agents can behave, and how the state evolves independent of their actions.
- Interfaces that provide agents with access to *observations*, allow them to submit *actions*, and collect and deliver messages of *communication*.

Depending on the level of support to be provided by the environment, more or fewer of these modules will be present.

## 🗝️  Key Insights

- Both Harnad and Mandler's papers provide perspectives on the relationship between human cognition and symbolic representations. From the latter we learn that they are an intrinsic (and perhaps *necessary*) component; from the former we learn that they are *not sufficient* and must be augmented with sensorimotor grounding.
- Marcus' analysis of today's ML field is often criticised for lacking actionable substance. Here he hones in on the need for modular, hand-engineered priors for reasoning about time, space and causality, paired with a collection of axiomatic knowledge. This is something that feels a little more concrete.
- Volodin et al's approach of learning a robust causal model by deliberately attempting to disprove its current structure is an elegant and compelling idea, though since it effectively uses RL as an inner learning loop, I expect its current form will be very computationally costly for large environments.
- Weyns et al do a good job of showing why the environments populated by artificial agents are due more attention than they normally get. The picture of "environment as interface with reality" suggests the potential for an entirely new sub-field of environmental engineering. 
