---
title: Feature importance and the fundamental matrix
permalink: Feature Importance in Absorbing Markov Chains
---

#Logbook for #Interaction on 30/06/21.

The canonical form of the conditional transition matrix for an absorbing [Markov Chain](Markov%20Chain) with $m$ transient states and $r$ absorbing states is 

$$P=\left[\begin{array}{cc}Q&R\\\textbf{0}_{r\times m}&I_r\end{array}\right],$$

where $\textbf{0}_{r\times m}$ is a matrix of zeros and $I_r$ is the $r\times r$ identity matrix. The expected number of times the chain visits transient state $j$ starting from transient state $i$ is the $(i,j)$ entry of the *fundamental matrix*

$$N=\sum_{t=0}^\infty Q^t=(I_m-Q)^{-1}.$$

If we denote transient state $1$ as the sole *initial state* of the Markov chain, for which all inbound transition probabilities are zero, $N_{1,i}$ is the total expected number of visits to transient state $i\in\{2..m\}$ before absorption. Let $\textbf{n}=N_{1,2..m}$ denote the vector of visitation counts, and $\boldsymbol{\mu}=\frac{\textbf{n}}{\vert\vert\textbf{n}\vert\vert_1}$ be the normalised *visitation distribution* for the Markov chain; the total proportion of time spent in each state (other than the initial one) before absorption. 

The preceding equations describe a generative model for state visitation given a transition matrix, which we denote by $N=f(P)$ and $\textbf{n}=f_1(P)$.

Now suppose we have two Markov chains over a common set of states, with transition matrices $P^p$ and $P^q$ and fundamental matrices $N^p$ and $N^q$. We want to know: which transition probabilities provide the strongest *causal explanation* for observed differences in $N^p$ and $N^q$? We could develop this line of enquiry in at least three directions:
- **Local**: For a pair of transient states $i,j$, identify causes of the difference 

$$\Delta_{i,j}(p,q)=N_{i,j}^p-N_{i,j}^q= f(P^p)_{i,j}-f(P^q)_{i,j}.$$

- **Global**: Identify causes of overall dissimilarity in the visitation distributions, as per a measure such as the Jensen-Shannon divergence  

$$\Delta_{\text{glob}}(p,q)=\text{JSD}(\boldsymbol{\mu}^p,\boldsymbol{\mu}^q)=\text{JSD}\left(\frac{f_1(P^p)}{\vert\vert f_1(P^p)\vert\vert_1},\frac{f_1(P^q)}{\vert\vert f_1(P^q)\vert\vert_1}\right).$$

- **Reward**: Given a vector $\textbf{r}$ specifying a scalar *reward* for each of the non-initial transient states $2..m$, identify causes of the difference in expected future reward starting from transient state $i$,

$$\Delta_{\text{rew}(i)}=\textbf{r}^\top(N_{i,2..m}^p-N_{i,2..m}^q)=\textbf{r}^\top(f(P^p)-f(P^q))_{i,2..m}.$$

To answer these questions we model the effect of *interventions* on the transition matrices $P^p$, specifically ones that involve *swapping* transition probabilities from one Markov chain to the other. For an intervention $x$, let $P^{p\vert\text{do}(x)}$ equal $P^p$ aside from some targeted modification to a subset of the transition probabilities. 

There are many possible intervention models:

- **State-wise**, $x=i$: Let $P^{p\vert\text{do}(i)}$ equal $P^p$, but with the $i$th row ($i\leq m$) swapped out for the $i$th row of $P^q$. Since the only constraint on the transient rows of a transition matrix is that they individually sum to $1$, $P^{p\vert\text{do}(i)}$ remains a valid transition matrix and state-wise interventions can be made independently. 
- **Transition-wise**, $x=(i,j)$:  Let $P^{p\vert\text{do}(i,j)}$ equal $P^p$, but with the $(i,j)$ entry swapped out for the $(i,j)$ entry of $P^q$. Requires some normalisation scheme...

---

# Feedback
- Transition-wise interventions require too many assumptions, and are less meaningful from a feature selection/importance standpoint, so focus on the state-wise case from now on. These count as *rank 1 modifications* of the transition matrix, about which there is a decent amount of existing literature.
- Can also analyse the partial effect of a row-wise blending between two transition matrices. At every point in a linear interpolation, we retain a valid transition matrix.
- Also a note on the semantic context: it is very likely that we can treat $p$ and $q$ asymmetrically, treating $p$ as a *fact* case and $q$ as a *foil*. This means that we only need to consider interventions in one direction, and therefore don't need to worry about the problem of combining influences from both directions.