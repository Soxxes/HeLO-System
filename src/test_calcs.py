from calcs import get_coop_scores

# some scores
clan1 = 513
clan2 = 683
clan3 = 711
clan4 = 578
clan5 = 604

coop1 = [clan2, clan3]          # in Germany we say: "Die guten ins Töpfchen ..."
coop2 = [clan1, clan4, clan5]   # " ... die schlechten ins Kröpfchen"

player_distribution1 = [30, 20]
player_distribution2 = [5, 25, 20]

num_matches1 = [17, 35]
num_matches2 = [4, 3]

# game result
caps1 = 5
caps2 = 0

# test a: with distributions
new1a, new2a, err = get_coop_scores(coop1, coop2, caps1, caps2,
                                player_dist1=player_distribution1,
                                player_dist2=player_distribution2,
                                num_matches1=num_matches1, num_matches2=num_matches2)

# test b: without distributions
new1b, new2b, err = get_coop_scores(coop1, coop2, caps1, caps2)

# test c: with distribution, but without num_matches
new1c, new2c, err = get_coop_scores(coop1, coop2, caps1, caps2,
                                player_dist1=player_distribution1,
                                player_dist2=player_distribution2)

print("------------------------------------")
print(f"test a: {new1a}, {new2a}")
print(f"test b: {new1b}, {new2b}")
print(f"test c: {new1c}, {new2c}")
