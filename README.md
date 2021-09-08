# The HeLO-System

Hi, I'm glad you made it. :)
I created an Elo-System for the competitive "Hell Let Loose" scene. Yes, there are competitive teams in the game. However, the strength of each team so far always had to be estimated. I'll give you a short introduction of **how** and **why** I created this.

<br />

## What is an elo system?
An Elo-System is a rating system, created in 1970s by A. Elo. He designed that to rank chess players.
If you have ever played chess online, you may have noticed this number after your name. That's your elo score.
Have a look at: [Wikipedia](https://en.wikipedia.org/wiki/Elo_rating_system).

I slightly adjusted this system and adapted it to HLL ... and I named it **HeLO score** (short for Hell Let Loose Elo Score).

<br />

## What factors influence the HeLO score?
If you don't have a basic knowledge of how elo systems work, please take a few minutes to read about them. In contrary to chess, the HeLO score depends not only on the final result of the game and your current score. <br />
A victory in HLL can 5-0, 4-1 or 3-2. The latter is closer to a draw in chess than a win. Additionally, we don't rate players but whole teams. So another dependency is the number of players played in a certain game. Last, there are friendly matches and competitive matches between the teams. In my opinion that should be weighted differently, too. <br />
To summarize, there are three main factors:
* the game result
* the number of players
* the competitve factor

<br />

## Calculating the Probability of a Victory
Let's dive a little bit deeper into the maths. Based on the current score of each team, we need to know the probabilty of winning, which can be calculated by the following integral (don't worry, I will strongly simplify it):

<img src="https://latex.codecogs.com/svg.image?P(D)&space;=&space;\frac{1}{\sigma&space;\sqrt{2\pi}}&space;\int_{-\infty}^D&space;e^{-\frac{t^2}{2\sigma^2}}&space;dt" title="P(D) = \frac{1}{\sigma \sqrt{2\pi}} \int_{-\infty}^D e^{-\frac{t^2}{2\sigma^2}} dt"/>
