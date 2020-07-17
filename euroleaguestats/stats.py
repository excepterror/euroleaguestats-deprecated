from collections import OrderedDict

dict_template = {'Minutes:': [1], 'Points:': [2], '2-Point Field Goals:': [3], '3-Point Field Goals:': [4],
                 'Free Throws:': [5], 'Offensive Rebounds:': [6], 'Defensive Rebounds:': [7],
                 'Total Rebounds:': [8], 'Assists:': [9], 'Steals:': [10], 'Turnovers:': [11],
                 'Blocks in Favour:': [12], 'Blocks Against:': [13], 'Fouls Committed:': [14], 'Fouls Drawn:': [15],
                 'Point Index Rating:': [16]}


def fetch_total_stats(tree):

    """Fetches total stats. Called by :cls: 'Options' - main.py
    """

    tot_av_stats = tree.xpath('//table[@id="tblPlayerPhaseStatistics"]/tbody/tr/td/text()')
    total_stats = tot_av_stats[-35:-19]

    if not total_stats:
        return None
    else:
        return total_stats


def fetch_aver_stats(tree):

    """Fetches average stats. Called by :cls: 'Options' - main.py
    """

    tot_av_stats = tree.xpath('//table[@id="tblPlayerPhaseStatistics"]/tbody/tr/td/text()')
    average_stats = tot_av_stats[-16:]

    if not average_stats:
        return None
    else:
        return average_stats


def fetch_opponents(tree, rivals_rs, rivals_po, rivals_ff):

    """Creates 3 dicts with opponents for every game of each phase: RS, PO & FF. A number corresponding to the 'round'
    played is also assigned. Called by :meth: 'access_per_game_stats' -library5.py
    """

    opponents_dict_rs = {}
    opponents_dict_po = {}
    opponents_dict_ff = {}
    round_num_rs = tree.xpath('//div[@class="PlayerPhasesStatisticsMainContainer"]//div[@id="E2019_RS"]//'
                              'table[@id="tblPlayerPhaseStatistics"]/tr/td[@class="PlayerGameNumberContainer"]'
                              '/text()')
    round_num_po = tree.xpath('//div[@class="PlayerPhasesStatisticsMainContainer"]//div[@id="E2019_PO"]//'
                              'table[@id="tblPlayerPhaseStatistics"]/tr/td[@class="PlayerGameNumberContainer"]'
                              '/text()')
    round_num_ff = tree.xpath('//div[@class="PlayerPhasesStatisticsMainContainer"]//div[@id="E2019_FF"]//'
                              'table[@id="tblPlayerPhaseStatistics"]/tr/td[@class="PlayerGameNumberContainer"]'
                              '/text()')
    round_num_rs_n = []
    round_num_po_n = []
    round_num_ff_n = []

    for data in round_num_rs:
        round_num_rs_n.append(data.partition('\r')[0])
    for data in round_num_po:
        round_num_po_n.append(data.partition('\r')[0])
    for data in round_num_ff:
        round_num_ff_n.append(data.partition('\r')[0])

    for i, rival in enumerate(rivals_rs):
        opponents_dict_rs.update({rival: int(round_num_rs_n[i])})

    for i, rival in enumerate(rivals_po):
        playoff_game = int(round_num_po_n[i]) - 30
        opponents_dict_po.update(
            {'PlayOffs - Game ' + str(playoff_game) + ':' + ' ' + rival: int(round_num_po_n[i])})

    for i, rival in enumerate(rivals_ff):
        final_four_game = int(round_num_ff_n[i]) - int(max(round_num_po_n))
        opponents_dict_po.update(
            {'FinalFour - Game ' + str(final_four_game) + ':' + ' ' + rival: int(round_num_ff_n[i])})

    opponents_dict_rs_n = OrderedDict(sorted(opponents_dict_rs.items(), key=lambda t: t[1]))
    opponents_dict_po_n = OrderedDict(sorted(opponents_dict_po.items(), key=lambda t: t[1]))
    opponents_dict_ff_n = OrderedDict(sorted(opponents_dict_ff.items(), key=lambda t: t[1]))

    del round_num_rs, round_num_rs_n, opponents_dict_rs, round_num_po_n, opponents_dict_po

    return [opponents_dict_rs_n, opponents_dict_po_n, opponents_dict_ff_n]


def per_game_stats(tree):

    """PURPOSE: Fetching game stats. Stats for each round played in RS.
    """

    games_stats_rs = tree.xpath(
        '//div[@class="PlayerPhasesStatisticsMainContainer"]//div[@id="E2019_RS"]//'
        'table[@id="tblPlayerPhaseStatistics"]/tr/td/text()')
    games_played_rs = len(games_stats_rs) / 17

    for i in range(int(games_played_rs)):
        del games_stats_rs[16 * i]

    '''Stats for each round played in POs.'''
    games_stats_po = tree.xpath(
        '//div[@class="PlayerPhasesStatisticsMainContainer"]//div[@id="E2019_PO"]//'
        'table[@id="tblPlayerPhaseStatistics"]/tr/td/text()')
    games_played_po = len(games_stats_po) / 17

    for i in range(int(games_played_po)):
        del games_stats_po[16 * i]

    '''Stats for each round played in FF.'''
    games_stats_ff = tree.xpath(
        '//div[@class="PlayerPhasesStatisticsMainContainer"]//div[@id="E2019_FF"]//'
        'table[@id="tblPlayerPhaseStatistics"]/tr/td/text()')
    games_played_ff = len(games_stats_ff) / 17

    for i in range(int(games_played_ff)):
        del games_stats_ff[16 * i]

    return [games_stats_rs, games_stats_po, games_stats_ff]


def per_game_statistics(games_stats_rs, games_stats_po, games_stats_ff, g, p=0):

    """PURPOSE: Dict with game stats for a single game. Called by :meth: 'apply_selection' in :cls: 'SelectableLabel' -
    library5.py
    """
    i = 16 * (g - 1)
    j = 16 * g

    per_game_stats_dict = OrderedDict(sorted(dict_template.items(), key=lambda t: t[1]))
    games_stats = games_stats_rs + games_stats_po + games_stats_ff
    game_stats = games_stats[i:j]

    for i, stat in enumerate(game_stats):
        if stat == '\xa0':
            game_stats[i] = '---'

    for k, v in per_game_stats_dict.items():
        per_game_stats_dict[k] = game_stats[p]
        p += 1
    del games_stats

    return per_game_stats_dict


def dict_creator(kind_of_stats, j=0):

    """PURPOSE: Creates dictionary. Used for dictionaries total_statistics and average_statistics.
    'kind of stats' can be average_stats or total_stats. Both objects are lists.
    """

    stats_dict = OrderedDict(sorted(dict_template.items(), key=lambda t: t[1]))
    stats = [kind_of_stats[stat] for stat in range(len(kind_of_stats))]

    for k, v in stats_dict.items():
        stats_dict[k] = stats[j]
        j += 1
    del stats

    return stats_dict
