---
title:	pandoc with amsthm
author:	Kolen Cheung
date:	\today
keywords:	pandoc, amsthm, LaTeX 
toc:	true
toc-depth:	5
lang:	en
papersize:	letter
fontsize:	12pt
documentclass:	memoir
classoption:	oneside, article
geometry:	inner=1.5in, outer=1.5in, top=1.5in, bottom=1.75in
fontfamily:	lmodern
colorlinks:	true
linkcolor:	blue
citecolor:	blue
urlcolor:	blue
toccolor:	blue
---

# Theorem #

<!--\begin{theorem}--> <div latex="true" abc="test" class="theorem">
$$\nabla \times \mathbf{E} = - \frac{\partial \mathbf{B}}{\partial t}$$
<!--\end{theorem}--> </div>

<!--\begin{lemma}--> <div latex="true" abc="test" class="lemma">
$$\nabla \times \mathbf{E} = - \frac{\partial \mathbf{B}}{\partial t}$$
<!--\end{lemma}--> </div>

<!--\begin{proposition}--> <div latex="true" abc="test" class="proposition">
$$\nabla \times \mathbf{E} = - \frac{\partial \mathbf{B}}{\partial t}$$
<!--\end{proposition}--> </div>

<!--\begin{corollary}--> <div latex="true" abc="test" class="corollary">
$$\nabla \times \mathbf{E} = - \frac{\partial \mathbf{B}}{\partial t}$$
<!--\end{corollary}--> </div>

<!--\begin{definition}-->  <div latex="true" abc="test" class="definition">
$$E=mc^2$$
<!--\end{definition}--></div>

<!--\begin{conjecture}-->  <div latex="true" abc="test" class="conjecture">
$$E=mc^2$$
<!--\end{conjecture}--></div>

<!--\begin{example}-->  <div latex="true" abc="test" class="example">
$$E=mc^2$$
<!--\end{example}--></div>

<!--\begin{postulate}-->  <div latex="true" abc="test" class="postulate">
$$E=mc^2$$
<!--\end{postulate}--></div>

<!--\begin{problem}-->  <div latex="true" abc="test" class="problem">
$$E=mc^2$$
<!--\end{problem}--></div>

<!--\begin{remark}--> <div latex="true" abc="test" class="remark">
$$\nabla \times \mathbf{E} = - \frac{\partial \mathbf{B}}{\partial t}$$
<!--\end{remark}--> </div>

<!--\begin{note}--> <div latex="true" abc="test" class="note">
$$\nabla \times \mathbf{E} = - \frac{\partial \mathbf{B}}{\partial t}$$
<!--\end{note}--> </div>

<!--\begin{case}--> <div latex="true" abc="test" class="case">
$$\nabla \times \mathbf{E} = - \frac{\partial \mathbf{B}}{\partial t}$$
<!--\end{case}--> </div>

<!--\begin{proof}-->  <div latex="true" abc="test" class="proof">
$$E=mc^2$$
<!--\end{proof}--></div>

<!--\begin{case}--> <div latex="true" abc="test" class="case test">
$$\nabla \times \mathbf{E} = - \frac{\partial \mathbf{B}}{\partial t}$$
<!--\end{case}--> </div>


<div class="totally nonsense" latex="false">
shouldn't be in env.
</div>