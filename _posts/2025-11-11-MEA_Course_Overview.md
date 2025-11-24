---
layout: post
title: "Stochastic Optimization Course for Metropolitan Electricity Authority (MEA)"
author: Parin Chaipunya
date: 2025-11-11
categories: portal
permalink: /_posts/mea_2025
---

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YDJ2EH8F91"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-YDJ2EH8F91');
</script>


# #Metadata

## Instructors
- Parin Chaipunya, KMUTT, Bangkok (parin.cha[at]kmutt.ac.th)
- Michel De Lara, École Nationale des Ponts et Chaussées, Paris (michel.delara[at]enpc.fr)

## Course objectives
- Capacity building. Prepare the practitioners for the current and new trends on energy management that involves more 
and more unpredictable elements --- demand, availability of renewable resources, etc.
<!---->
<!-- ## Prospective attendees -->
<!-- - Fluent in calculation. -->
<!-- - Motivated, not afraid to ask questions, and ready for discussion. -->

## Course organization
- A lecture in the morning of each day.
- In the afternoon, the attendees should prepare the problems from the MEA side to discuss and hopefully to frame them using stochastic optimization.

# #Program

## Week 1 (Preparation)
Lecturer: Parin Chaipunya

### Monday 17 November 2025

#### Morning (08h30--11h30)
This course introduces the foundations of optimization, emphasizing how decision variables, objectives, and constraints are formulated. 
We discuss local and global solutions, highlighting why this distinction matters in nonconvex problems. 
Core problem classes such as linear, quadratic and convex programs are presented as practical and widely used models.
We then illustrate these ideas through deterministic models in power systems: economic dispatch in single and multiple time-step settings, and transmission expansion planning which help improve network capabilities under the balance of investment and load shedding.

[Slides 1]({{ site.baseurl }}/assets/2025_mea/optim_part1.pdf)
[Slides 2]({{ site.baseurl }}/assets/2025_mea/optim_part2.pdf)

#### Afternoon (12h30--15h30)
Modeling session

### Thursday 20 November 2025

#### Morning (08h30--11h30)
We introduce the mathematics of uncertainty through the basic elements of probability and random variables, emphasizing how unpredictable phenomena can be represented, quantified, and incorporated into decision models. 
Building on these foundations, we introduce different approaches to handle randomness in an optimization problem with an emphasis on stochastic optimization.
We then consider examples including pooled blood testing and the newsboy problems.
Finally, we modify the economic dispatch problem by replacing the deterministic expected demand with a random variable describing the uncertain demand.
We discuss in this part the need to introduce the recourse variable to fix the feasibility issue caused by replacing the deterministic demand constraint with a stochastic one.
A Monte Carlo simulation illustrates that the stochastic solution produces less accumulated cost compared to the deterministic sample-averaged approximation approach.

[Slides 3]({{ site.baseurl }}/assets/2025_mea/optim_part3.pdf)
[Slides 4]({{ site.baseurl }}/assets/2025_mea/optim_part4.pdf)


#### Afternoon (12h30--15h30)
Modeling session

### (Optional) Sample codes
<a href="https://parinchaipunya.com/assets/2025_mea/1_first_example.ipynb" download>Pyscipopt introduction (1)</a> \|
<a href="https://parinchaipunya.com/assets/2025_mea/2_second_example.ipynb" download>Pyscipopt introduction (2)</a> \|

<a href="https://parinchaipunya.com/assets/2025_mea/3_econ_dispatch_single.py" download>Economic dispatch --- Single time-step</a> \|

<a href="https://parinchaipunya.com/assets/2025_mea/4_econ_dispatch_multi_indep.py" download>Economic dispatch --- Multiple time-steps, without battery</a> \|

<a href="https://parinchaipunya.com/assets/2025_mea/5_econ_dispatch_multi_dynam.py" download>Economic dispatch --- Multiple time-steps, with battery</a> \|

<a href="https://parinchaipunya.com/assets/2025_mea/6_transmission_expansion.py" download>Transmission extension</a> \|

<a href="https://parinchaipunya.com/assets/2025_mea/7_econ_dispatch_stoc.py" download>Economic dispatch --- Single time-step, with random demand</a>


## Week 2 (Stochastic optimization. Part I)
Lecturers: Michel De Lara, Parin Chaipunya

### Monday 24 November 2025

#### Morning (08h30--11h30)
One-stage stochastic optimization. First examples.

##### Overview
This lecture covers the question of how to commit to produce energy for an uncertain demand.

#### Afternoon (12h30--15h30)
Modeling session

### Thursday 27 November 2025

#### Morning (08h30--11h30)
Two-stage stochastic optimization, scenario decomposition, Progressive Hedging.

##### Overview
How do you commit yourself to produce energy for an uncertain demand and when you can correct your first decision 
by a second decision mobilizing costly energy after the demand has been revealed.
How do you handle demand and production scenarios ?

#### Afternoon (12h30--15h30)
Modeling session

## Week 3 (Stochastic optimization. Part II)
Lecturers: Michel De Lara, Parin Chaipunya

### Monday 15 December 2025

#### Morning (08h30--11h30)
Introduction to multi-stage stochastic optimization, Bellman equation

##### Overview
Answers the question of how to manage a storage (dam, battery) when you make sequential decisions (charge/discharge 
sequence) on a given timespan, under unpredictable demand and renewable sources production.

#### Afternoon (12h30--15h30)
Modeling session

### Thursday 18 December 2025

#### Morning (08h30--11h30)
More advanced methods. Decomposition of large-scale stochastic optimization problems.
Risk measures and optimization.

##### Overview
How to both maximize profit and minimize risk.
Example of smart grid management with multiple storages located on a network. How to avoid high costs with low 
probability by using suitable risk measures.

#### Afternoon (12h30--15h30)
Modeling session

------
