"""
Functions to calculate probabilities and HeLO scores.
"""
import math
from statistics import mean
import numpy as np


def get_win_prob(score1, score2):
    """Calculates the probability of winning for the better team.

    Args:
        score1 (int): HeLO score of one team
        score2 (int): HeLO score of the other team

    Returns:
        float, float: probability for better ranked team (score1)
                      and worse ranked team (score2) between [0, 1]
    """
    assert score1 > 0 and score2 > 0
    # difference of the HeLO scores, make sure not to exceed the maximum difference of 400
    diff = min(400, abs(score1 - score2))
    # round the probability to three decimal places
    prob = round(0.5*(math.erf(diff/400) + 1), 3)
    # prob is the winning probability for the better score, return probabilities accordingly
    if score1 > score2:
        return prob, round(1 - prob, 3)
    else:
        return round(1 - prob, 3), prob


def get_new_scores(score1, score2, caps1, caps2, matches1=0, matches2=0, c=1, number_of_players=50):
    """Calculates the new HeLO score based on a given game score.

    Args:
        score1 (int): HeLO score of the first team
        score2 (int): HeLO score of the second team
        caps1 (str): strong points captured by the first team at the end of the match
        caps2 (str): strong points captured by the second team at the end of the match
        matches1 (int, optional): number of games played (team 1). Defaults to 0.
        matches2 (int, optional): number of games played (team 2). Defaults to 0.
        c (int, optional): competitive factor, possible values = {0.5, 0.8, 1, 1.2}. Defaults to 1.
        number_of_players (int, optional): Number of players played in the game per team. Defaults to 50.

    Returns:
        int, int, str: new HeLO score for team 1 and team 2, possible error
    """
    try:
        # determine the "amount factor" by the number of games played
        a1 = 20 if matches1 is not None and matches1 > 30 else 40
        a2 = 20 if matches2 is not None and matches2 > 30 else 40
        # calculate the probabilities for the teams
        prob1, prob2 = get_win_prob(score1, score2)
        # check if points don't exceed maximum points, which are possible in HLL
        assert caps1 + caps2 <= 5
        # calulate the new HeLO scores
        score1_new = score1 + a1 * float(c) * (math.log(number_of_players/50, a1) + 1) * float(caps1 / 5 - prob1)
        score2_new = score2 + a2 * float(c) * (math.log(number_of_players/50, a2) + 1) * float(caps2 / 5 - prob2)
        return round(score1_new), round(score2_new), None
    except AssertionError:
        return None, None, "Sum of points in score must be less or equal to 5"


def get_coop_scores(clan_scores1: list, clan_scores2: list, caps1: int, caps2: int, c: int = 1,
                    player_dist1: list = None, player_dist2: list = None, num_players: int = 50):
    """Calculates the scores for games with more than one clan on one (or both) side(s).
    If a player distribution is given, the score will be calculated based on a weighted
    average. Otherwise a normal average will be calculated.

    Args:
        clan_scores1 (list): list of scores of the clans in the cooperation
        clan_scores2 (list): list of scores of the clans in the cooperation on the other side
        caps1 (int): strongpoints held by clans1 at the end of the game
        caps2 (int): strongpoints held by clans2 at the end of the game
        c (int, optional): competitive factor, possible values = {0.5, 0.8, 1, 1.2}. Defaults to 1.
        player_dist1 (list, optional): player distributions of the participating clans1.
                                        Defaults to None.
        player_dist2 (list, optional): player distributions of the participating clans2.
                                        Defaults to None.
        num_players (list, optional): total number of players, only necessary if no player
                                        distribution was given

    Returns:
        list, list: list of the new HeLO scores for every team (coop1, coop2)
    """
    # note: amount factor (a) will be ignored here, default is 40
    # otherwise, these kind of games won't generate a significant score
    a = 40

    # convert player distributions to numpy arrays and normalize
    try:
        # performs weighted average
        weights1 = np.array(player_dist1) / sum(player_dist1)
        weights2 = np.array(player_dist2) / sum(player_dist2)
        num_players = sum(player_dist1)
    except TypeError:
        # performs normal average
        weights1 = np.ones(len(clan_scores1)) / len(clan_scores1)
        weights2 = np.ones(len(clan_scores2)) / len(clan_scores2)

    # calculate the (weighted) average score of the cooperations
    avg1 = np.average(clan_scores1, weights=weights1)
    avg2 = np.average(clan_scores2, weights=weights2)

    score1, score2, err = get_new_scores(avg1, avg2, caps1, caps2,
                                        c=c, number_of_players=num_players)
    gain1, gain2 = score1 - avg1, score2 - avg2

    print(gain1, gain2)

    # share the gain depending on the player distribution
    # if there is no player distribution, share equally
    # cs = clan score, part = partial share according to the distribution
    clan_scores1 = [round(cs + part * gain1) for cs, part in zip(clan_scores1, weights1)]
    clan_scores2 = [round(cs + part * gain2) for cs, part in zip(clan_scores2, weights2)]

    return clan_scores1, clan_scores2



# deprecated
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


# deprecated
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
        return round(h1_new), round(h2_new), None
    except AssertionError:
        return None, None, "Sum of points in score must be less or equal to 5"


# deprecated
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


# deprecated
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
