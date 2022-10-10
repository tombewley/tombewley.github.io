---
title: "Convergence of Value-based RL"
permalink: /notes/Convergence of Value-based RL
---

[https://towardsdatascience.com/mathematical-analysis-of-reinforcement-learning-bellman-equation-ac9f0954e19f](https://towardsdatascience.com/mathematical-analysis-of-reinforcement-learning-bellman-equation-ac9f0954e19f)

We often hear that [reinforcement learning](Reinforcement%20Learning) always converges to a unique fixed point. Why is that?

We are going to prove this using the Banach fixed point theorem by showing that the Bellman optimality operator is a contraction over a complete metric space of real numbers with metric L-infinity norm. For this, we will first discuss the fixed point problem and complete metric spaces with respect to the Cauchy sequence.

Given a [metric space](Sets%20and%20spaces) $(\mathcal{X}, d)$, the infinite sequence $x_1,x_2,x_3...,$ is a *Cauchy sequence* if for *every* $\varepsilon\in\mathbb{R}^+$, there exists an $N\in\mathbb{Z}^+$ such that $d(x_a,x_b)<\varepsilon,a,b>N$. This definition formalises the notion of convergence to a fixed point. A metric space is *complete* if every possible Cauchy sequence among the elements of $\mathcal{X}$ converges to some fixed point that itself lies in $X$. Given a complete metric space $(\mathcal{X},d)$, a function $f:\mathcal{X}\rightarrow \mathcal{X}$ is a *contraction* if applying it to two elements $x,x'\in\mathcal{X}$ moves them closer together by a factor of at least $\gamma\in[0,1)$, i.e.

$$d(f(x),f(x'))\leq\gamma d(x,x')$$

The *Banach fixed point theorem* gives a proof of what is intuitively obvious: repeated application of a contraction induces a Cauchy sequence, and thus converges to a unique fixed point $x^\ast\in\mathcal{X}$.

Bellman optimality operator $\mathbb{B}:\mathbb{R}\rightarrow\mathbb{R}$.

$$\mathbb{B}[V(s)]=\underset{a}{\max}r(s,a)+\gamma\sum_{s'}P(s'\vert s,a)V(s')$$

$\mathbb{B}$ recursive can be used to generate a sequence of value functions. 

Now let us use the infinity norm to define a metric space $(\mathbb{R},\lVert\cdot\rVert\infty)$. If we can show that $\mathbb{B}$ is a contractor in $(\mathbb{R},\lVert\cdot\rVert\infty)$, then we can conclude that it will eventually give a unique optimal value function $V^\ast$ and in turn, a unique optimal policy $\pi^\ast$. First, let's write out the equation for the infinity norm after applying $\mathbb{B}$ to two value functions $V_1$, $V_2$:

$$\lVert\mathbb{B}[V_1(s)]-\mathbb{B}[V_2(s)]\rVert_\infty=\lVert\underset{a_1}{\max}(r(s,a_1)+\gamma\sum_{s'}P(s'\vert s,a_1)V_1(s'))-\underset{a_2}{\max}(r(s,a_2)+\gamma\sum_{s'}P(s'\vert s,a_2)V_2(s'))\rVert_\infty$$

The key trick here is to recognise that ==XXXXXXXXXXXXXXXXXXXX==

$$\leq\lVert\underset{a_1}{\max}(\cancel{r(s,a_1)}+\gamma\sum_{s'}P(s'\vert s,a_1)V_1(s'))-\cancel{r(s,a_1)}-\gamma\sum_{s'}P(s'\vert s,a_1)V_2(s'))\rVert_\infty=\gamma\lVert \underset{a_1}{\max}\sum_{s'}P(s'\vert s,a_1)(V_1(s')-V_2(s'))\rVert_\infty$$

Since the infinity norm returns the maximum value over the entire state space, this is equivalent to

$$=\gamma\underset{s',a_1}{\max}\sum_{s'}P(s'\vert s,a_1)(V_1(s')-V_2(s'))=\gamma\underset{s',\cancel{a_1}}{\max}(V_1(s')-V_2(s'))\cancelto{1}{\sum_{s'}P(s'\vert s,a_1)}=\gamma\lVert V_1(s')-V_2(s')\rVert_\infty$$

So therefore

$$\lVert\mathbb{B}[V_1(s)]-\mathbb{B}[V_2(s)]\rVert_\infty\leq\gamma\lVert V_1(s')-V_2(s')\rVert_\infty$$

which means that $\mathbb{B}$ is a contractor in $(\mathbb{R},\lVert\cdot\rVert_\infty)$.


---

FQI gives no guarantees of convergence to the optimal solution.
- Proof: Mix of contraction under $\infty$-norm and $\ell 2$-norm.
- $Q$ learning is not true gradient descent (semi-gradient) because we don't take the gradient through the target value. Residual algorithms slow and not numerically stable (learning rates).
- Also means that actor-critic won't converge (policy gradient converges to local maximum, just like supervised learning