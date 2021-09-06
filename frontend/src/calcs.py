"""
Functions to calculate probabilities and HeLO scores.
"""
import math


def _calc_probability(h1, h2, *args, **kwargs):
    """Calculates the probability of winning for the better team.

    Args:
        h1 (int): HeLO score of the better team
        h2 (int): HeLO score of the worse team

    Returns:
        float, float: probability for better ranked team (h1)
                        and worse ranked team (h2) between [0, 1]
    """
    assert h1 > 0 and h2 > 0
    # difference of the HeLO scores
    diff = h1 - h2
    # make sure not to exceed the maximum difference of 400
    if diff > 400:
        diff = 400
    # round the probability to three decimal places
    prob = round(0.5*(math.erf(diff/400) + 1), 3)
    return prob, 1 - prob



def calc_new_score(h1, h2, score, a1=40, a2=40, c=1, number_of_players=50):
    """Calculates the new HeLO score based on a given game score.

    Args:
        h1 (int): HeLO score of the better team
        h2 (int): HeLO score of the worse team
        score (str): Game score, in format "X-Y", where X are the points of team 1 with h1
                        and Y are the points for team 2 with h2
        a1 (int, optional): amount factor, for the overall number of games played (team 1). Defaults to 40.
                            If the number of games exceeds 30, a1 should be set to 20.
        a2 (int, optional): amount factor, for the overall number of games played (team 2). Defaults to 40.
                            If the number of games exceeds 30, a2 should be set to 20.
        c (int, optional): competitive factor, possible values = {0.5, 0.8, 1, 1.2}. Defaults to 1.

    Returns:
        int, int: new HeLO score for team 1 and team 2
    """
    try:
        # calculate the probabilities for the teams
        prob1, prob2 = _calc_probability(h1, h2)
        # casting the score from a "X-Y" string into integer
        points1, points2 = int(score.split("-")[0]), int(score.split("-")[1])
        # check if points don't exceed maximum points, which are possible in HLL
        assert points1 + points2 <= 5
        # calulate the new HeLO scores
        # for debugging
        # print(f"h1: {h1}, a1: {a1}, c: {c}, number of players: {number_of_players}, points: {points1}, prob: {prob1}")
        h1_new = h1 + a1 * c * (math.log(number_of_players/50, a1) + 1) * (points1 / 5 - prob1)
        h2_new = h2 + a2 * c * (math.log(number_of_players/50, a2) + 1) * (points2 / 5 - prob2)
        return round(h1_new), round(h2_new), None
    except AssertionError as e:
        return None, None, e

