---
title: "Conversative World Models"
pubtype: "workshop"
collection: publications
permalink: /publication/conservative_world_models
excerpt: 'We propose methods for improving the performance of zero-shot RL methods when trained on sub-optimal offline datasets.'
date: 2023-12-16
venue: 'Seventh Workshop on Generalization in Planning'
paperurl: 'https://openreview.net/pdf?id=6oPZcdzFjW'
citation: 'Jeen, Scott and Tom Bewley and Jonathan M. Cullen. &quot;Conversative World Models&quot; <i>Seventh Workshop on Generalization in Planning</i>. 2023.'
redirect_from: 
  - /conservative-world-models

---

Zero-shot reinforcement learning (RL) promises to provide agents that can perform any task in an environment after an offline pre-training phase. Forwardbackward (FB) representations represent remarkable progress towards this ideal, achieving 85% of the performance of task-specific agents in this setting. However, such performance is contingent on access to large and diverse datasets for pre-training, which cannot be expected for most real problems. Here, we explore how FB performance degrades when trained on small datasets that lack diversity, and mitigate it with conservatism, a well-established feature of performant offline RL algorithms. We evaluate our family of methods across various datasets, domains and tasks, reaching 150% of vanilla FB performance in aggregate. Somewhat surprisingly, conservative FB algorithms also outperform the task-specific baseline, despite lacking access to reward labels and being required to maintain policies for all tasks. Conservative FB algorithms perform no worse than FB on full datasets, and so present little downside over their predecessor. Our code is available open-source [here](https://github.com/enjeeneer/zero-shot-rl).