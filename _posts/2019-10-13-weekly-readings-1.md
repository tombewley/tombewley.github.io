---
title: 'Weekly Readings #1'
date: 2019-10-13
permalink: /posts/2019/10/weekly-readings-1/
tags:
  - research
---

As it stands I'm precisely 13 days into my PhD, which means a lot of reading, and I thought I'd kick this blog off with a weekly rolling 'diary' of things I read, watch and otherwise consume which may have some influence on my [PhD topic](https://tombewley.com/start ). Most of the papers have words pertaining to explanation in there, and that's because I did a massive scrape of papers with that keyword. I figured that would be a reasonable start.

I'm going to try to summarise what I took from each piece of content in just a few lines, which is obviously a daft and brazen thing to do, but hopefully useful nonetheless.

## 📝 Papers

### Andreas, Jacob, Anca Dragan, and Dan Klein. “Translating Neuralese.” *ArXiv:1704.06960 [Cs]*, 2018.

In modern multi-agent communication protocols (e.g. deep communicating policies, DCPs), messages take the form of real-valued state vectors, bearing little resemblance to natural language. Using the idea that messages have similar meanings when they *induce similar beliefs about the state of the speaker*, we can formulate the problem of translating an arbitrary message $z$ to a human-readable one $z$ as that of minimising the expected difference (K-L divergence) between the belief distributions they induce over the speaker's stage, across all contexts. While an analytical solution is intractable, we can approximate by sampling. 

The technique is tried out on several two-agent tasks (relaying information about an unseen colour / image, mutual collision avoidance for cars). By measuring the ability of a *model human listener* network to map translated messages back to states, and the performance of human-machine teams using the translated messages, the method is found to somewhat outperform a more conventional machine translation approach based on supervised learning.

### Bryson, Joanna. “Six Kinds of Explanation for AI (One Is Useless).” (personal blog), 2019.

There are three broad categories of useful explanation for AI: (1) explaining human actions that led to the system being developed and released; (2) elucidating what inputs resulted in what outputs; and (3) seeing exactly how the system works. The latter can be attained by (a) using human-understandable representations throughout; (b) fitting more transparent surrogate models (this is how human explanation works). Each is valid, as long the result is accountability for AI developers. 

Others have posited an additional category: so-called *deep explanation*. This uses the idea that we can only truly understand e.g. a DNN if we know what every weight does. This is wrong, in that it operates at *completely the wrong level of abstraction*. We never ask for explanations of human actions in terms of such low-level dynamics. It is in the interest of deep tech developers to keep the myth of the requirement for – and impossibility of – deep explanation going, because it provides a justification for their lack of accountability and transparency.

### Fox, Maria, Derek Long, and Daniele Magazzeni. “Explainable Planning.” *ArXiv Preprint ArXiv:1709.10256*, 2017.

### Greydanus, Sam, Anurag Koul, Jonathan Dodge, and Alan Fern. “Visualizing and Understanding Atari Agents.” *ArXiv:1711.00138 [Cs]*, 2017.

### Klein, Gary. “Explaining Explanation, Part 3: The Causal Landscape.” *IEEE Intelligent Systems* 33, no. 2 (2018): 83–88.

### Langley, Pat, Ben Meadows, Mohan Sridharan, and Dongkyu Choi. “Explainable Agency for Intelligent Autonomous Systems.” In *Twenty-Ninth IAAI Conference*, 2017.

### Nair, Suraj, Yuke Zhu, Silvio Savarese, and Li Fei-Fei. “Causal Induction from Visual Observations for Goal Directed Tasks.” *ArXiv:1910.01751 [Cs, Stat]*, 2019.

### Rudin, Cynthia. “Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead.” *Nature Machine Intelligence* 1, no. 5 (2019): 206.

### Sheh, Raymond. “'Why Did You Do That?' Explainable Intelligent Robots,” 2017.



## 📚  Books

### Pearl, J. (2009). *Causality*. Cambridge University Press; 2nd Edition.

Just starting this one off. 

### Russell, S. (2019). *Human Compatible: Artificial Intelligence and the Problem of Control.* Allen Lane 

### Singer, P. (2011). *Practical Ethics*. Cambridge University Press; 2nd Edition.

## 🗝️ Key Points