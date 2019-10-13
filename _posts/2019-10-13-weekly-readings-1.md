---
title: 'Weekly Readings #1'
date: 2019-10-13
permalink: /posts/2019/10/weekly-readings-1/
tags:
  - weekly-readings
---

As it stands I'm precisely 13 days into my PhD, which means a lot of reading, and I thought I'd kick this blog off with a weekly rolling 'diary' of things I read, watch and otherwise consume which may have some influence on my [PhD topic](https://tombewley.com/start ). Most of the papers have words pertaining to explanation in there, and that's because I did a massive scrape of papers with that keyword. I figured that would be a reasonable start.

I'm going to try to summarise what I took from each piece of content (which may or may not match the author's intended argument!) in just a few lines, which is obviously a daft and brazen thing to do, but hopefully useful nonetheless.

## 📝 Papers

### Andreas, Jacob, Anca Dragan, and Dan Klein. “Translating Neuralese.” *ArXiv:1704.06960 [Cs]*, 2018.

In modern multi-agent communication protocols (e.g. deep communicating policies, DCPs), messages take the form of real-valued state vectors, bearing little resemblance to natural language. Using the idea that messages have similar meanings when they *induce similar beliefs about the state of the speaker*, we can formulate the problem of translating an arbitrary message $z$ to a human-readable one $z$ as that of minimising the expected difference (K-L divergence) between the belief distributions they induce over the speaker's stage, across all contexts. While an analytical solution is intractable, we can approximate by sampling. 

The technique is tried out on several two-agent tasks (relaying information about an unseen colour / image, mutual collision avoidance for cars). By measuring the ability of a *model human listener* network to map translated messages back to states, and the performance of human-machine teams using the translated messages, the method is found to somewhat outperform a more conventional machine translation approach based on supervised learning.

### Bryson, Joanna. “Six Kinds of Explanation for AI (One Is Useless).” (personal blog), 2019.

There are three broad categories of useful explanation for AI: (1) explaining human actions that led to the system being developed and released; (2) elucidating what inputs resulted in what outputs; and (3) seeing exactly how the system works. The latter can be attained by (a) using human-understandable representations throughout; (b) fitting more transparent surrogate models (this is how human explanation works). Each is valid, as long the result is accountability for AI developers. 

Others have posited an additional category: so-called *deep explanation*. This uses the idea that we can only truly understand e.g. a DNN if we know what every weight does. This is wrong, in that it operates at *completely the wrong level of abstraction*. We never ask for explanations of human actions in terms of such low-level dynamics. It is in the interest of deep tech developers to keep the myth of the requirement for – and impossibility of – deep explanation going, because it provides a justification for their lack of accountability and transparency.

### Fox, Maria, Derek Long, and Daniele Magazzeni. “Explainable Planning.” *ArXiv Preprint ArXiv:1709.10256*, 2017.

One of the challenges of XAI is to understand what constitutes an explanation. A simple re-writing of the decision making algorithm in natural language is not a satisfactory answer to the question of **why did you do that?**; neither is a response that effectively states that *that* maximises reward. A strong answer may point to a future desirable state that is enabled by this decision. Crucially, the answer must demonstrate causality among actions. Other questions that should be answerable include:

- **Why didn't you do something else?** Here an alternative is made explicit. A good answer may demonstrate a flaw in this alternative, which may require an internal simulation to be run using that alternative.
- **Why is what you propose faster/safer/cheaper/… than something else?** Similar to the above but requests that the explanation be given in terms of a specific metric.
- **Why can't you do that?** There are two reasons why one action can not be applied in a given state. Either because the current state does not satisfy the action precondition; or because the application of that action would prevent achieving the goal from the resulting state. The first is easy to explain, while the latter is challenging; proving un-solvability is notoriously challenging. 
- **Why do I (not) need to re-plan at this point?** A suitable answer may point to a specific factor that has diverged from expectation, or in the negative case, that may appeared to have diverged but actually remains within the expected distribution.

### Greydanus, Sam, Anurag Koul, Jonathan Dodge, and Alan Fern. “Visualizing and Understanding Atari Agents.” *ArXiv:1711.00138 [Cs]*, 2017.

A method is proposed for generating saliency maps for deep RL agents that use raw visual input to solve Atari 2600 games. The maps provide four kinds of insight: (1) identifying common features of successful strategies; (2) seeing how policies evolve during training; (3) detecting when an agent is earning high rewards for the "wrong reasons"; (4) and debugging poorly-performing agents by identifying the basis of their poor decisions. A key advantage over e.g. t-SNE is that the results are intuitive for non-experts.

Here, the focus is on actor-critic models, and saliency maps are constructed for both the actor $\pi$ and the critic $V_\pi$. The maps are *perturbation-based*, meaning they measure how the models' outputs change when an input image $I_k$ is doctored (specifically, by adding a localised Gaussian blur centred at pixel coordinates $(i,j)$). Taking the actor $\pi$ as the example: the logits $\pi_u(I_{1:t})$ input to the final softmax activation are used for computing the saliency of the region around $(i,j)$. The saliency metric for this location at time $t$ is

$$
\mathcal{S}_{\pi}(t, i, j)=\frac{1}{2}\left\|\pi_{u}\left(I_{1: t}\right)-\pi_{u}\left(I_{1: t}^{\prime}\right)\right\|^{2}
$$

where

$$
I_{1: k}'=\left\{\begin{array}{ll}{\Phi\left(I_{k}, i, j\right)} & {\text { if } k=t} \\ {I_{k}} & {\text { otherwise }}\end{array}\right.
$$
A map is constructed by computing the saliency for a range of $i$ and $j$ values. [My concern: when interpreting their saliency maps, the authors do appear a little prone to confirmation bias. This technique seems to have some value, but can certainly not be relied upon in isolation.]

### Klein, Gary. “Explaining Explanation, Part 3: The Causal Landscape.” *IEEE Intelligent Systems* 33, no. 2 (2018): 83–88.

The *causal landscape* concept attempts to deal with the complexities of causality: mixtures of enabling and trigger causes, and first-, second- and third-order effects. Given a particular outcome that we wish to explain, the overall idea is to portray the wide range of relationships as a network, and for each cause rate both its *impact* (would reversing it have prevented the event?) and *reversibility* (how much effort would it take to reverse it?) By combining these scores [how?] we can identify the most influential causal pathways and construct a compact explanation that is maximally-informative. 

[The method seems like it could make for a practically-useful heuristic tool, but it isn't very clearly defined. There's no reference to the more rigorous causal diagrams pioneered by Judea Pearl, who I suspect would have his own ideas about how to generate compact explanations of outcomes.] 

### Langley, Pat, Ben Meadows, Mohan Sridharan, and Dongkyu Choi. “Explainable Agency for Intelligent Autonomous Systems.” In *Twenty-Ninth IAAI Conference*, 2017.

The task of *explainable agency* is defined as follows. Given a set of objectives that require extended activity to attain, and background knowledge about relevant categories and relations, produce: (1) *records* of decisions made by the agent; (2) human-readable summary *reports* of the agent’s internal and external activity, presented at various levels of abstraction; and (3) comprehensible *answers* to questions about the reasoning behind specific decisions.

Communication must be done in a language that uses human concepts such as beliefs, desires and intentions, though this does not necessarily imply the agent's entire reasoning framework must use these concepts. The recent emphasis on data-driven statistical learning, which lacks any such concepts, has made it more difficult to provide this kind of explicatory functionality, but there are nonetheless various subfields of AI that have plenty to offer in the service of this goal.

### Nair, Suraj, Yuke Zhu, Silvio Savarese, and Li Fei-Fei. “Causal Induction from Visual Observations for Goal Directed Tasks.” *ArXiv:1910.01751 [Cs, Stat]*, 2019.

The lack of causal modelling is a possible cause of poor generalisation in deep learning systems. Here, a learning-based agent is endowed with causal reasoning. It performs two kinds of operation: (1) causal *induction*, the discovery of cause and effect relations via performing actions and observing their outcomes; and (2) causal *inference*, the use of the acquired causal relations to guide action selection in the servie of a goal. The causal model $\hat{C}$ is explicitly encoded as an $N\times N$ DAG expressing the cause-effect relationships between $N$ actions and $N$ state variables. The system is intended to generalise to various environments with the same state and action spaces, but different transition dynamics (i.e. $p(s_{t+1}\vert a_t,s_t))$. The specific state space considered in experiments is that of vision: high-dimensional RGB pixel values

During causal induction, an image is encoded into a lower-dimensional state $s$ and the state residual $R$ – the difference in $s$ from the previous timestep – is computed. $R$ is concatenated with the corresponding action $a$ and fed into an edge decoder whose output is an update to the edge weights $\Delta\hat{C}$. This update has the form of a $1\times N$ vector of edge weight changes $\Delta e$ and a $1\times N$ soft *attention* vector $\alpha$ which weights which nodes in the causal graph the update should be applied to.

During causal inference, the policy $\pi_G$ takes as its input the current image encoding $s$ and a goal image $g$. It outputs another $1\times N$ attention vector $\alpha$ over the 'effects' in the causal graph. This vector is used to perform a weighted sum over the graph's outputs, resulting in a $N\times 1$ vector of the selected edges $e$. The selected edges and visual encodings are used to output the ﬁnal action. Most mapping operations are performed using fully-connected networks, and those which take images as inputs are CNNs.

In the experiment, the task is to control $N$ lights with $N$ switches using only this visual input, and reach a specified lighting goal which is itself expressed as an image. The structure of switches-to-light connections is unknown to the agent. Generalisation is tested by using different connection structures. The agent outperforms a model-free RL agent which has direct access to the ground-truth light states. The attention mechanism is found to improve generalisation as it encourages independent updates.

### Rudin, Cynthia. “Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead.” *Nature Machine Intelligence* 1, no. 5 (2019): 206.

The author differentiates post-hoc *explainable* ML from inherently *interpretable* ML before asserting that the former is problematic, since there is no guarantee of reliability. The latter must be used where safety and trust is important. The accuracy-interpretability tradeoff is a myth, particularly *when the data naturally have a good representation* (such as one that humans would use). In addition, explainability methods provide explanations that are inaccurate and incomplete, since they necessarily involve fidelity reduction, and this is simply not acceptable in high-stakes situations. "Explanation" is really the wrong word here; the methods can be more accurately be described as providing rough *summaries of predictions*. 

Despite these factors, discrete explanation modules still seem to be preferred over inherently interpretable models. There are numerous possible reasons for this, including that corporations make profit from the IP inside black boxes, and that interpretable models can take significant effort and expertise to construct. If we are serious about big impactful applications of ML, we must be prepared to put this effort in. A concrete proposal for responsible ML policy: no black box model should be deployed when there exists an interpretable model with the same level of performance. 

### Sheh, Raymond. “'Why Did You Do That?' Explainable Intelligent Robots,” 2017.

Advocates for the potential of behavioural cloning (from human demonstration or a complex search-based policy) for generating explainable agents. This approach is more broadly applicable than that of expert systems: it is easier to demonstrate strong behaviour than to codify it. Decision trees are particularly good models to use for the clone, since we already have a strong understanding of how to extract meaningful explanations from them, and pruning methods can be used to reduce limit complexity in a controlled manner. The cloning technique is applied to the problem of controlling a mobile robot to traverse rough terrain. 

## 📚  Books

### Pearl, J. (2009). *Causality*. Cambridge University Press; 2nd Edition.

I'm just starting this one this week. So far, we've had an introduction to Bayesian networks, and to the *d-separation* criterion as a visual test for conditional independence. *Causal* Bayesian networks are those whose variable ordering captures the direction of time and causation. If a network has a causal ordering, we can assess the impact of an *intervention* $do(X_i=x_i)$, which consists of setting a variable subset $X_i$ to a specific value $x_i$, thereby severing any links from its parents $PA_i$. To test whether $X_i$ has causal influence on another subset $X_j$, we compute the marginal distribution of $X_j$ under a range of $do(X_i=x_i)$ interventions, and test whether the distribution is sensitive to $x_i$. 

A functional causal model consists of a set of equations each of the form $X_i=f_i(PA_i,U_i)$, where $U_i$ represent errors or uncertainties due to omitted factors. If we augment a causal Bayesian network with a functional causal model, we can answer *counterfactual* questions. Given a causal model $M$ and observed evidence $e$, we apply the following steps to compute the probability of $Y=y$ under a hypothetical condition $X=x$: 

- **Abduction**: update the probability $P(u)$ using the available evidence to obtain $P(u\vert e)$: the probability distribution over the error variables in the actually-observed scenario captured by $e$. 
- **Intervention**: replace the equations corresponding to variables in $X$ by the equations $X=x$.  
- **Prediction**: use the modified model and abduced error variable distributions to compute $P(Y=y)$.

### Russell, S. (2019). *Human Compatible: Artificial Intelligence and the Problem of Control.* Allen Lane 

This is also a new starter. In the early chapters, Russell presents the following definitions. Agents are *intelligent* (rational) to the extent they are able to reliably achieve their objectives given the necessary information; they are *beneficial* to the extent they reliably achieve *our* objectives. The latter should be our goal, but the former has been our focus to date. 

All of AI can be thought of working out the details of how to behave rationally, which we usually frame in terms of the maximisation of expected utility. However, almost any problem we care about has exponential complexity and is thus practically intractable, so perfect rationality is unattainable. 

### Singer, P. (2011). *Practical Ethics*. Cambridge University Press; 2nd Edition.

This has been an ongoing read for the past few weeks. At the time of writing, Singer was a *preference* utilitarian, which means he prioritised the maximal satisfaction of preferences (he has since moved towards *hedonistic* utilitarianism: maximising the surplus of happiness over suffering). Some key points so far are as follows:

- There is nothing special about our species. Since we have no direct evidence to suggest that other mammals have a less developed capacity to suffer than humans (both behavioural observation and our understanding of biology points to great similarity) we should consider their interests equally. This does not necessarily lead us away from meat consumption or animal testing in all cases; only those when the benefit to human interests does not exceed the cost to animals. 
- Killing is wrong if and only if it violates the preferences of the individual, or those of others, for continued existence. Beings without a sense of their continuing self cannot have these preferences; this includes unborn babies alongside most animals. However, we might opt to consider the *retroactive* preferences of the surviving individual, such as a human adult, who most certainly would have the survival preference. Whether or not we choose to do this is fundamental to the abortion debate.

- In relation to questions about future beings, there are two general approaches in utilitarianism. In the *total view* we consider the interests/experience of these hypothetical beings the same as extant ones, while in the *prior existence view* we do not assign weight to them at all. The latter aligns more with most people's intuitions but leads to far more contradictions. In preference utilitarianism, an equivalent discussion can be had about the creation of new preferences. Should we assign moral weight to the satisfaction of preferences that are not yet held?

## 🗝️  Key Insights

*This is my first attempt at this kind of über-consolidation exercise, so bear with…*

- The meaning of a message is not intrinsic, but is a function of the mental states it induces in 'speaker' and 'listener' agents. The similarity of meanings can be quantified in terms of belief functions, and this in turn provides a route towards translation.
- There are several useful kinds of explanation, and more still that are not useful. We are led to extremely wrong conclusions if we define explanation at the wrong level of abstraction.
- When seeking explanation, we may wish to know why *don't* or *can't* happen in addition to the converse. It seems that answering any of these queries in an agent-based system requires some kind of predictive model. In addition to answers to specific queries, a concise record of decisions and actions is an important general component of explainable systems.
- Perhaps seeking 'explanation' is the wrong approach where the stakes are high, because all explanations are simplified models of decision making, and all models are wrong. We should focus on developing inherently interpretable models, and we may not even have to sacrifice performance for doing so, but it'll probably be hard work. Behavioural cloning of human policies or complex black-box models, using decision trees, is a promising direction for interpretability research.
- Saliency maps can be applied in RL contexts where the input has a spatial or visual form. They provide some insight, that may be useful for closing the feedback loop during model development, but are a long way from complete explanations of an agent's behaviour.
- Gradient-based learning can be applied to the task of learning causal models (given the necessary structural assumptions), which in turn are useful for problem solving. Causal models provide the only rigorous framework for answering interventional and counterfactual questions, which form the backbone of most theories of explanation.  
- Rationality and intelligence are essentially one and the same; both are defined relative to the available information, and to a stated goal or utility function. Only if this aligns consistently with human interests should we expect an intelligent agent to be beneficial.   

- Utilitarianism, whether of the preference or hedonistic variety, resonates nicely with the scientific viewpoint. It leads to conclusions that are objectionable to some, but it does so in a way that is justified and can easily be queried.