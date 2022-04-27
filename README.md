# The HeLO-System

Hi, I'm glad you made it. :)
I created an Elo-System for the competitive "Hell Let Loose" scene. Yes, there are competitive teams in the game. However, the strength of each team so far always had to be estimated. I'll give you a short introduction of **how** and **why** I created this. The official website with statistics and other stuff that uses this system can be found [here](https://helo-system.de/).

- [The HeLO-System](#the-helo-system)
  - [What is an Elo System?](#what-is-an-elo-system)
  - [What Factors influence the HeLO Score?](#what-factors-influence-the-helo-score)
  - [Calculating the Probability of a Victory](#calculating-the-probability-of-a-victory)
  - [Calculating the new HeLO Score](#calculating-the-new-helo-score)
  - [Guessing the HeLO Score of a new Team](#guessing-the-helo-score-of-a-new-team)
  - [Full Example](#full-example)
  - [What if more than one team plays together?](#what-if-more-than-one-team-plays-together)
- [Project Overview](#project-overview)
  - [Current State (*deprecated*)](#current-state-deprecated)
  - [Planned Features](#planned-features)

<br />

## What is an Elo System?
The Elo rating system is a method to calculate the relative skill levels of players in zero-sum games such as chess. It is named after its creator Arpad Elo, a Hungarian-American physics professor. If you have ever played chess online or in a competitive tournament you might be familiar with the concept. If not, you can read more about the system on [Wikipedia](https://en.wikipedia.org/wiki/Elo_rating_system).

<br />

## What Factors influence the HeLO Score?
In contrast to chess where you can either win, lose or draw, HLL offers additional outcomes determined by the amount of controlled cap points per team at the end of the match.

There are three main factors influencing the HeLO-Score of a team:
To summarize, there are three main factors:
* the game result
* the number of players
* the match type (competitive or regular)

<br />

## Calculating the Probability of a Victory
Let's dive a little bit deeper into the maths. Based on the current score of each team, we need to know the probabilty of winning, which can be calculated by the following integral (don't worry, I will strongly simplify it):

<img src="https://latex.codecogs.com/svg.image?\bg_white&space;P(D)&space;=&space;\frac{1}{\sigma&space;\sqrt{2\pi}}&space;\int_{-\infty}^D&space;e^{-\frac{t^2}{2\sigma^2}}&space;dt" title="\bg_white P(D) = \frac{1}{\sigma \sqrt{2\pi}} \int_{-\infty}^D e^{-\frac{t^2}{2\sigma^2}} dt" />

<br />

**D** is the difference between the scores of team 1 and team 2. The standard deviation is set to <img src="https://latex.codecogs.com/svg.image?\bg_white&space;\sigma&space;=&space;200&space;\sqrt{2}" title="\bg_white \sigma = 200 \sqrt{2}" /> and the mean is 0. As promised, the integral mentioned above simplifies to:

<img src="https://latex.codecogs.com/svg.image?\bg_white&space;P(D)&space;=&space;\frac{\mathrm{erf}(\frac{D}{400})&plus;1}{2}" title="\bg_white P(D) = \frac{\mathrm{erf}(\frac{D}{400})+1}{2}" />

where **erf(x)** is the Gaussian error function. That's basically it. Let's have a look at a small example. Team A (734) plays against team B (579). The difference is: D = 734 - 579 = 155. Now we just have to insert the numbers in the equation ... and P(D) = 0.708. What does this mean? It means that Team A will win the game with a probability of 70.8%. The probabilty of Team B winning is the counter-probability: 1 - P(D) = 0.292. <br />
Side information: In case the difference **D** should be greater than 400, the system will take 400 as the maximum. Otherwise, the score gain or loss would be either too significant or absolutely irrelevant.

<br />

## Calculating the new HeLO Score
For that I copied the formula from chess, but adjusted a few factors (as mentioned earlier):

<img src="https://latex.codecogs.com/svg.image?\bg_white&space;H'_\mathrm{n}&space;=&space;H_\mathrm{n}&space;&plus;&space;k(S_\mathrm{n}-P_\mathrm{n}(D))" title="\bg_white H'_\mathrm{n} = H_\mathrm{n} + k(S_\mathrm{n}-P_\mathrm{n}(D))" />

<img src="https://latex.codecogs.com/svg.image?\bg_white&space;H'_\mathrm{n}" title="\bg_white H'_\mathrm{n}" /> is the new HeLO score of team n and <img src="https://latex.codecogs.com/svg.image?\bg_white&space;H_\mathrm{n}" title="\bg_white H_\mathrm{n}" /> is the current HeLO score Let's have a closer look on **k**:

<img src="https://latex.codecogs.com/svg.image?\bg_white&space;k&space;=&space;ac&space;\cdot&space;(log_{a}&space;\frac{N}{50}&space;&plus;&space;1)" title="\bg_white k = ac \cdot (log_{a} \frac{N}{50} + 1)" />

* **a**: The "Number of Games" factor.  The default factor for the number of matches/games played is 40. If a team played more than 30 games, this factor changes to 20. It hasn't been mentioned yet, since its only purpose is to accelerate the settling process in order to calculate a reliable score faster.
* **c**: The "Competitive" factor. Off seasonal time is during Christmas and New Year's eve, easter time and during the summer (1st of July until 31st of August).
    * friendly match (off seasonal): c = 0.5
    * friendly match (on seasonal): c = 0.8
    * competitve match: c = 1
    * competitve match (extra sweaty): c = 1.2
* **N**: The "Number of Players" factor. Why is it logarithmic? For me it was not an option to scale the number of players linearly, because it is a huge difference of missing a full squad in a 50v50 game and missing a squad in a 25v25 game. Therefore, this factor decreases even heavier the more players are missing. Fun fact: there have to be at least 3 players on each side. Otherwise the logarithm will be negative (and that is something we don't want to happen).

<img src="https://latex.codecogs.com/svg.image?\bg_white&space;S_\mathrm{n}" title="\bg_white S_\mathrm{n}" /> are the points your team holds at the end of the game normalized to 5.

<br />

## Guessing the HeLO Score of a new Team
New teams start with a HeLO score of 600. To be honest, there will be exceptions to this. In order to reduce the "settling time", I will guess the strength of a team and give them a score between 550 and 650. The affected team will be informed about that.

<br />

## Full Example
Let's have a look at a realistic example. Team A (746) plays a competitive match (extra sweaty) against Team B (613). They play with 45 players on each side. Team A played more than 30 games, but Team B is relatively new on scene (played less than 30 games). Team B (everyone sympathizes for the underdog) wins with a score of 5-0.

1) Calculate the difference: D = 746 - 613 = 133
2) Calculate the probability of winning for Team A: P(121) = 0.681
3) Calculate the probability of winning for Team B: 1 - P(121) = 0.319
4) New HeLO score for Team A: <br />
<img src="https://latex.codecogs.com/svg.image?\bg_white&space;H'_\mathrm{1}&space;=&space;746&space;&plus;&space;20\cdot&space;1.2&space;\cdot&space;(log_{20}&space;\frac{45}{50}&space;&plus;&space;1)&space;(\frac{0}{5}-0.681)&space;\approx&space;730" title="\bg_white H'_\mathrm{1} = 746 + 20\cdot 1.2 \cdot (log_{20} \frac{45}{50} + 1) (\frac{0}{5}-0.681) \approx 730" />
5) New HeLO score for Team B: <br />
<img src="https://latex.codecogs.com/svg.image?\bg_white&space;H'_\mathrm{2}&space;=&space;613&space;&plus;&space;40\cdot&space;1.2&space;\cdot&space;(log_{40}&space;\frac{45}{50}&space;&plus;&space;1)&space;(\frac{5}{5}-0.319)&space;\approx&space;645" title="\bg_white H'_\mathrm{2} = 613 + 40\cdot 1.2 \cdot (log_{40} \frac{45}{50} + 1) (\frac{5}{5}-0.319) \approx 645" />

So Team A loses 16 score points while Team B gains 32 score points for beating a better team.

<br />

## What if more than one team plays together?
This is called a cooperation. Cooperations can consist of teams fielding an equal amount of players, e.g. 25 each, or a different amount of players, e.g. 15 and 35.
We have multiple options here. The most intuitive one is to assign the score changes of that specific game according to the player distributions. This is done by weighing the average. If the easier and less accurate option is used, the player distributions are ignored. The normal average is computed and score changes are shared equally among the participants of the cooperation. This will be used in case no player distributions are given. Check this out:<br />

<img src="https://latex.codecogs.com/svg.image?\overline{x}&space;=&space;\sum_{i=1}^{n}w_i&space;x_i" title="\overline{x} = \sum_{i=1}^{n}w_i x_i" />

where the <i>**w**</i>s are the player fielded by a team normalized to the total number of players. <i>**x**</i> is then the score of the corresponding team. First good thing about this is we can calculate the new score of this specific cooperation with the average as it was the score of "normal" team. And second, we can assign the gain/loss of this game to the teams in the same manner. <br />

<br />

# Project Overview
The HeLO-System has become more than just a hobby. I have created a whole project from it. Here is an overview:
<br />

<a><img src="https://s20.directupload.net/images/220415/5whdwwo2.png" title="Project Overview"></a>

<br />

## Current State (*deprecated*)
At the moment there is a downloadable and executable desktop application. The main window looks like this:

<img width="400" alt="image" src="https://user-images.githubusercontent.com/50017993/148366380-264d8521-8e13-414f-86ae-5e3dfbe466fc.PNG">

Originally, the intention was to grant every team manager Superuser permissions, which are necessary to report game results. Additionally, users that do not have these permissions can request the scores of all teams. There is also some kind of security implemented (e.g. Superusers must authenticate themselves). I'll keep this section small, because I am currently working on major improvements (see "Planned Features"). Soon, all of this will be much better and easier to use.

<br />

## Planned Features
The following features are either planned or already partially implemented:
* **REST API** replacing the downloadable client (see: https://github.com/HeLO-System/HeLO-Server)
* **Discord Bot** with various quality of life features (including easy reporting of game results, request of scores and statistics, simulation mode, betting system, ...)

The Discord Bot's development branch (not public atm) currently runs on my Raspberry Pi and there are not a lot of security mechanism (therefore not public). But you can use the Bot on the HeLO-Discord: https://discord.gg/dmtcbrV7t5, feel free to join and stress test him. <br />
As I write this, there are already 62 teams registered in the HeLO-System. The Discord has more than 480 members. I had no idea that the project would be so well received and I am genuinely thankful for it.

<br />
