episode_counts = [6, 22, 23, 14, 26, 24, 24, 24, 23]


def check_validity(season: int, episode: int):
    return (1 <= season <= 9) and (1 <= episode <= episode_counts[season])
