"""
Functions to calculate probabilities and HeLO scores.
"""
import math
from statistics import mean


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
        number_of_players (int, optional): Number of players played in the game per team. Defaults to 50.

    Returns:
        int, int, str: new HeLO score for team 1 and team 2, possible error
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
        print("unshared scores", h1_new, h2_new)
        return round(h1_new), round(h2_new), None
    except AssertionError:
        return None, None, "Sum of points in score must be less or equal to 5"


def _calc_coop_score_gain(avg_score1, avg_score2, score, coop1_teams=2, coop2_teams=2, c=1, total_number_of_players=50):
    """Calculates the gain (not the new score) based on an average HeLO score.

    Args:
        avg_score1 (float): Average score of cooperation 1
        avg_score2 (float): Average score of cooperation 2
        score (str): Game score, in format "X-Y", where X are the points of cooperation 1
                        and Y are the points for cooperation 2
        coop1_teams (int, optional): Number of teams participating in the cooperation 1. Defaults to 2.
        coop2_teams (int, optional): Number of teams participating in the cooperation 2. Defaults to 2.
        c (int, optional): competitive factor, possible values = {0.5, 0.8, 1, 1.2}. Defaults to 1.
        total_number_of_players (int, optional): Number of players played in the game per
                                                cooperation (not the sum of both cooperations). Defaults to 50.

    Returns:
        int, int, str: gain per partner (meaning total gain divided by the number of teams in the cooperation)
                        for cooperation 1 and 2, possible error
    """
    # amount factor (a) will be ignored here, default is 40
    # otherwise, because the score will be shared equally among the partners of 
    # the cooperations, these kind of games won't generate a significant score
    new_score1, new_score2, error =  calc_new_score(avg_score1, avg_score2, score, c=c,
                                                    number_of_players=total_number_of_players)
    score_gain1 = new_score1 - avg_score1
    score_gain2 = new_score2 - avg_score2
    return round(score_gain1/coop1_teams), round(score_gain2/coop2_teams), error


def calc_coop_scores(h1s, h2s, score, c=1, total_number_of_players=50):
    """Calculates the scores for every team/partner participating in a cooperation.

    Args:
        h1s (list): HeLO scores for every team/partner in cooperation 1
        h2s (list): HeLO scores for every team/partner in cooperation 2
        score (str): Game score, in format "X-Y", where X are the points of cooperation 1
                        and Y are the points for cooperation 2
        c (int, optional): competitive factor, possible values = {0.5, 0.8, 1, 1.2}. Defaults to 1.
        total_number_of_players (int, optional): Number of players played in the game per
                                                cooperation (not the sum of both cooperations). Defaults to 50.

    Returns:
        list, list, str: lists of the new scores, possible errors
    """
    # calculate the average scores per cooperation
    avg_score1, avg_score2 = mean(h1s), mean(h2s)
    print("avg scores", avg_score1, avg_score2)
    # calculate the score gain for every partner in a cooperation
    gain1, gain2, error = _calc_coop_score_gain(avg_score1, avg_score2, score,
                                                coop1_teams=len(h1s),
                                                coop2_teams=len(h2s),
                                                c=c,
                                                total_number_of_players=total_number_of_players)
    # add the gain
    h1s_new = list(map(lambda x: x + gain1, h1s))
    h2s_new = list(map(lambda x: x + gain2, h2s))
    return h1s_new, h2s_new, error
