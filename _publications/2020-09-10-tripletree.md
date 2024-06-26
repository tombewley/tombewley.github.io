---
title: "TripleTree: A Versatile Interpretable Representation of Black Box Agents and their Environments"
pubtype: "conference"
collection: publications
permalink: /publication/tripletree
excerpt: 'Introducing a new decision tree model of black box agent behaviour, which jointly captures the policy, value function and temporal dynamics.'
date: 2020-09-10
venue: '35th AAAI Conference on Artificial Intelligence (AAAI 2021)'
paperurl: 'https://arxiv.org/abs/2009.04743'
citation: 'Bewley, Tom and Lawry, Jonathan. &quot;TripleTree: A Versatile Interpretable Representation of Black Box Agents and their Environments&quot; <i>35th AAAI Conference on Artificial Intelligence (AAAI 2021)</i>. 2021.'
redirect_from: 
  - /tripletree
---
In explainable artificial intelligence, there is increasing interest in understanding the behaviour of autonomous agents to build trust and validate performance. Modern agent architectures, such as those trained by deep reinforcement learning, are currently so lacking in interpretable structure as to effectively be black boxes, but insights may still be gained from an external, behaviourist perspective. Inspired by conceptual spaces theory, we suggest that a versatile first step towards general understanding is to discretise the state space into convex regions, jointly capturing similarities over the agent’s action, value function and temporal dynamics within a dataset of observations. We create such a representation using a novel variant of the CART decision tree algorithm, and demonstrate how it facilitates practical understanding of black box agents through prediction, visualisation and rule-based explanation.

![](http://tombewley.com/images/TripleTree_poster.png)