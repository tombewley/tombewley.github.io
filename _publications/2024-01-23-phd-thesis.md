---
title: "Tree Models for Interpretable Agents"
pubtype: "thesis"
collection: publications
permalink: /publication/phd
excerpt: 'Exerpt.'
date: 2024-01-23
paperurl: 'https://research-information.bris.ac.uk/en/studentTheses/tree-models-for-interpretable-agents'
citation: 'Bewley, Tom. &quot;Tree Models for Interpretable Agents.&quot; PhD Thesis, University of Bristol, 2024.'
redirect_from: 
  - /phd
---
As progress in AI impacts all sectors of society, the world is destined to see increasingly complex and numerous autonomous decision-making agents, which act upon their environments and learn over time. These agents have many practical applications, but also pose risks that demand ongoing human oversight. The field of AI interpretability builds tools that help human stakeholders understand the structure and origins of agent behaviour. This aids various downstream tasks, including verifying whether that behaviour is safe and reliable. In this thesis, we take several new perspectives on the interpretability problem, developing models that give insight into how agents respond to the state of their environments and vice versa, how they learn and change over time, and how this process is guided by the objectives supplied by humans themselves. While shifting between these perspectives, we maintain a coherence of approach by basing all of our methods on a theory of abstraction with rule-based models called trees.

We begin this thesis by formalising the tree abstraction framework and investigating its foundations. We then instantiate concrete examples of tree models for representing the behaviour of an agent not just in terms of its state-to-action policy, but also via its value function and state dynamics. We exploit the rule-based tree structures to generate textual explanations of agent actions over time and propose novel visualisations of behavioural trends across the environment state space. From this point, we further develop the concept of trees as dynamics models, using a contrastive objective uncover the changes that occur during agent learning. We visualise these models with graphs and heatmaps, and show how prototype trajectories can be identified to summarise an agent’s behaviour at each stage of learning.

In the second half of the thesis, we shift perspective to use trees as reward functions for training agents themselves, which provides an interpretable grounding for learnt behaviour. Furthermore, we show how reward trees can be learnt from human feedback, thereby drawing a connection between interpretability and the literature on human-agent alignment. We establish the efficacy of reward tree learning via experiments with synthetic and real human feedback on four benchmark tasks, then explore its interpretability benefits, showing how it enables detailed monitoring of an agent’s learning progress. After further refining the reward tree learning method, we evaluate it in the industrially-motivated use case of aircraft handling and develop a new interpretability technique that is synergistic with model-based agent architectures.

By blending quantitative and qualitative evaluations across a range of environments, we aim to show how our methods are broadly applicable and provide complementary insights that could be combined in a unified interpretability toolkit. We view both our individual tree models, and our diverse but cohesive research strategy, as meaningful contributions to the interpretability community. However, much work remains to be done, including completing thorough user evaluations in real-world domains, developing more scalable and optimal tree learning algorithms, and extending our methods to systems of multiple interacting agents.


