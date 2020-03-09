---
title: 'Weekly Readings #6'
date: 2019-11-17
permalink: /posts/2019/11/weekly-readings-6/
tags:
  - weekly-readings
---

Modelling other agents; `DAGGER`; evaluating feature importance visualisations; self, soul and circular ethics.

## 📝 Papers

### Albrecht, Stefano V., and Peter Stone. “Autonomous Agents Modelling Other Agents: A Comprehensive Survey and Open Problems.” *Artificial Intelligence* 258 (May 2018): 66–95.

This is a survey of approaches to modelling other agents as a function of the observed interaction history. Models can be used to predict future behaviour and inform action selection. The following notation is used throughout. $H=(o_1,…,o_t)$ is a history of observations up to time $t$, and $P(a_j\vert H)$ is the conditional probability that the modelled agent $j$ will select action $a_j$ at time $t$.

- **Policy reconstruction**: Explicitly modelling the agent's policy, usually by fitting the parameters of a fixed model architecture to best reflect the historic distribution of $P(a_j\vert f(H))$, where $f(H)$ is some representation of the history. Choosing $f$ is tricky, and doing it by hand requires strong assumptions. Attempts have been made to automatically choosing the best representation through some kind of entropy measurement.

- **Type-based reasoning**: The inverse learning of policies from scratch generally requires a lot of data, but if we have some prior knowledge about the kinds of behaviour exhibited, the problem can be reduced to that of selecting from a small set of fixed policy models called *types*, or finding a mixture of several types. Types themselves may be hand-crafted or learned from data. 

- **Property classification and regression**: Sometimes, rather than action-selection probabilities, we are interested in more abstract properties of other agents such as their 'aggressiveness' or 'trustworthiness' for use in planning. This task could be formulated as a supervised learning problem, where ground-truth values are provided via manual annotation. 

- **Plan recognition**: Here the goal is to identify the future *goals* and *plans* (steps to achieve goals) of another agent, which often take a more abstract representation than that of sequences of individual actions. If a plan can be represented as a graph, recognition involves incrementally repairing this graph in response to new observations.

- **Recursive Reasoning**: The nesting of beliefs about other agents, and in turn about their beliefs about ones self, leads to an infinitely-recursive modelling problem. Solutions (e.g. I-POMDP) generally involve approximating the belief nesting down to a fixed recursion depth, at which point some prior distribution (e.g. uniform) is used as input. 

- **Group modelling**: Where agents' policies or plans cannot be modelled as independent functions of their observations it may be necessary to jointly model an entire population. Many existing methods for policy reconstruction and plan recognition can be extended by simply combining all other agents into a single meta-agent, but data sparsity is likely to become an issue . A middle path is to partition the population into sub-groups of agents whose actions are highly correlated. In especially collaborative or competitive contexts, group modelling can actually be more efficient since it is able to capture within-group structure that is invisible at a single-agent level. Prior knowledge of such structure could be harnessed to dramatically reduce the search space. 

Identified open problems include the synergistic combination of the above methods; efficient discovery of decision factors (beyond combinatorial search); and handling partial observability, systems with variable agent populations, and policies that change over time.

### Ross, Stéphane, Geoffrey J Gordon, and J Andrew Bagnell. “A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning,” 2011, 9.

In imitation learning (among other sequential prediction problems), future observations depend on previous actions, which violates the common i.i.d. assumption made in statistical learning. Ignoring this issue compromises learning: mistakes lead the learner to parts of the state space never encountered by the target policy, leading to a compounding of errors. Here an iterative algorithm called `DAGGER` is proposed to find a strong policy under these conditions.

Denote $d^t_\pi$ the distribution of states at time $t$ if policy $\pi$ is followed from time $1$ to $t-1$. The average distribution of states if $\pi$ is followed for $T$ steps is therefore

$$
d_\pi=\frac{1}{T}\sum_{t=1}^Td_\pi^t
$$

Our goal is to find a policy $\hat{\pi}$ which minimises some loss function $\mathcal{L}$ relative to a target policy $\pi^*$ on samples from $d_\pi$:

$$
\hat{\pi}=\arg\min_{\pi\in\Pi}\mathbb{E}_{s\sim d_\pi}[\mathcal{L(s,\pi,\pi^*)}]
$$

Traditional approaches to imitation learning instead train a policy to perform well under the distribution encountered by $\pi^\ast$, $d_{\pi^\ast}$. Poor performance can result. A naïve solution would be to iterative train a new policy for each timestep $t$, on the distribution of states induced by all previously-trained policies, but this is extremely computationally intensive.  

The generic `DAGGER` proceeds as follows:

- Initialise an imitation policy $\hat{\pi}_1$.
- Use $\pi^*$ to gather a dataset $\mathcal{D}$.
- For each subsequent iteration $i$:
  - Use $\pi^*$ to sample $N\times\beta_i$ trajectories, and $\hat{\pi}_i$ to sample $N\times(1-\beta_i$), where $\beta_i\in[0,1]$. 
  - For all new trajectories get the corresponding actions from $\pi^*$, and append these to $\mathcal{D}$.
  - Train $\hat{\pi}_{i+1}$ on the augmented dataset.

Starting with $\beta_1=1$ is typically useful because it means we don't have to specify an initial policy $\hat\pi_1$. The only requirement for the evolution of $\beta_i$ is that the average value across all iterations $\rightarrow0$ as $i\rightarrow\infty$.

- In practice, **the best approach seems to be to set $\beta_1=1$ and $\beta_i=0\ \forall i>1$**.

A theoretical analysis in the paper demonstrates the robustness of the algorithm, and it is shown to outperform a couple of earlier alternatives for imitation learning.

### Samek, Wojciech, Alexander Binder, Grégoire Montavon, Sebastian Bach, and Klaus-Robert Müller. “Evaluating the Visualization of What a Deep Neural Network Has Learned.” *ArXiv:1509.06321 [Cs]*, September 21, 2015.

Feature importance visualisations *feel* intuitive, but is there anyway to measure their quality? In this paper, three visualisation techniques (sensitivity analysis, deconvolution, layerwise relevance propagation) are compared. The evaluation process proceeds as follows:

- For $L$ iterations:
  - Remove information from a region of the input image, chosen in order of the importance given to each region by the visualisation being evaluated. 
    - In the paper, individual pixels are used as the input features, and the information removal process consists of replacing all pixels in a $9\times9$ region around the target one with uniform random noise. $100$ different noise settings are also used to reduce the effect of randomness.
  - Feed the degraded image $x^L$ into the model, get the prediction $y^L$, and compute $p=y^0-y^L$.
- Compute the average value of $p$ over all $L$ iterations.

The intuition here is that a better visualisation technique should assign greater importance to regions that have a larger effect on the output. LRP is found to perform best by this metric, and also produces 'simpler' visualisations as measured by the compressed file size [clever!]

## 📚  Books

### Dennett, D. & Hofstadter, D. (2001). *The Minds' I: Fantasies and Reflections on Self and Soul*. Basic Books.

The introduction of this book asks: am I a brain, or do I *have* a brain? Science is increasingly suggesting that *all* of my brain is not *me*, since there is so much computation going on of which I am unaware. Perhaps that computation is still conscious, but just not to me. Only just started this one, but what will follow is a series of essays from leading thinkers.

### Singer, P. (2011). *Practical Ethics*. Cambridge University Press; 2nd Edition.

In the penultimate chapter, we ask whether we need to obey the law when we feel it prevents us from pursuing morally desirable outcomes. This question is especially relevant to the issue of civil disobedience. In an idealised view of democracy, the law is a reflection of the majority view of the population, so the question now seems to ask whether it is acceptable to act counter to the majority. There is a pretty strong argument in favour of majority rule and one-person-one-vote: it is equally acceptable to all, and is thus uniquely stable. For this reason, we should only disobey an uncoerced and accurately-measured majority decision in extreme circumstances.

Finally: why should we bother to act ethically in the first place? Some have attempted to argue that to act rationally *is* to act ethically, but the reasoning doesn't fully hold up to scrutiny. Others have claimed that moral persons can attain higher life satisfaction, so ethics can be justified from a selfish perspective, but the existence of psychopathy means such a claim is not universally true. Ultimately, pretty much all we can say is that many people choose to behave ethically because they feel drawn in that direction, and that it's a good thing that that's the case. 

## 🗝️  Key Insights

- As it stands there is no grand unifying theory for modelling other agents in a multi-agent system, but it seems that, if attainable, full policy reconstruction is the most general. Data sparsity issues force us to consider higher-level concepts such a goals and plans.
- `DAGGER` is a remarkably simple but rigorously-verified method of performing stable imitation learning.
- Quantitative evaluation of interpretability methods remains a contentious issue, but framing it in terms of the influence of identified features on the model's output seems like a reasonable approach. 
- Until Freud, essentially no consideration was given to the idea that some of our cognitive processes may be hidden from consciousness. Since then, however, the trend has been towards accepting an ever-increasing proportion, with conscious thought now considered a rare special case.
- As unsatisfying as it may be, it isn't possible to formulate an ethical argument for being ethical without some kind of circularity (this has quite a Gödelian flavour).