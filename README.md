# The HeLO-System

Hi, I'm glad you made it. :)
I created an Elo-System for the competitive "Hell Let Loose" scene. Yes, there are competitive teams in the game. However, the strength of each team so far always had to be estimated. I'll give you a short introduction of **how** and **why** I created this.

<br />

## What is an Elo System?
An Elo-System is a rating system, created in 1970s by A. Elo. He designed that to rank chess players.
If you have ever played chess online, you may have noticed this number after your name. That's your elo score.
Have a look at: [Wikipedia](https://en.wikipedia.org/wiki/Elo_rating_system).

I slightly adjusted this system and adapted it to HLL ... and I named it **HeLO score** (short for Hell Let Loose Elo Score).

<br />

## What Factors influence the HeLO Score?
If you don't have a basic knowledge of how elo systems work, please take a few minutes to read about them. In contrary to chess, the HeLO score depends not only on the final result of the game and your current score. <br />
A victory in HLL can 5-0, 4-1 or 3-2. The latter is closer to a draw in chess than a win. Additionally, we don't rate players but whole teams. So another dependency is the number of players played in a certain game. Last, there are friendly matches and competitive matches between the teams. In my opinion that should be weighted differently, too. <br />
To summarize, there are three main factors:
* the game result
* the number of players
* the competitve factor

<br />

## Calculating the Probability of a Victory
Let's dive a little bit deeper into the maths. Based on the current score of each team, we need to know the probabilty of winning, which can be calculated by the following integral (don't worry, I will strongly simplify it):

$P(D) = \frac{1}{\sigma \sqrt{2\pi}} \int_{-\infty}^D e^{-\frac{t^2}{2\sigma^2}} dt$

![P(D)&space;=&space;\frac{1}{\sigma&space;\sqrt{2\pi}}&space;\int_{-\infty}^D&space;e^{-\frac{t^2}{2\sigma^2}}&space;dt](https://latex.codecogs.com/svg.image?\bg_white&space)

**D** is the difference between the scores of team 1 and team 2. The standard derivation is set to $\sigma = 200 \sqrt{2}$ and the mean is 0. As promised, the integral mentioned above simplifies to:

$P(D) = \frac{\mathrm{erf}(\frac{D}{400})+1}{2}$,

where **erf(x)** is the Gaussian error function. That's basically it. Let's have a look at a small example. Team A (734) plays against team B (579). The difference is: $D = 734 - 579 = 155$. Now we just have to insert the numbers in the equation ... and $P(D) = 0.708$. What does this mean? It means that Team A will win the game with a probability of 70.8%. The probabilty for Team B to win is the counter-probability: $1 - P(D) = 0.292$. <br />
Side information: In case the difference $D$ should be greater than 400, the system will take 400 as the maximum. Otherwise, the score gain or loss would be either too significant or absolutely irrelevant.

<br />

## Calculating the new HeLO Score
For that I copied the formula from chess, but adjusted a few factors (as mentioned earlier):

$H'_\mathrm{n} = H_\mathrm{n} + k(S_\mathrm{n}-P_\mathrm{n}(D))$

$H'_\mathrm{n}$ is the new HeLO score of team n and $H_\mathrm{n}$ is the current HeLO score.
