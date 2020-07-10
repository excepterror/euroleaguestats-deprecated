import requests

from collections import OrderedDict
from lxml import etree
from urllib.parse import urljoin


def teams_codes():
    """PURPOSE: Returns the names of the teams and the dictionary. Called in 'Class' DraggableLogo - main.py."""

    codes = {'Alba Berlin': [1, 'BER'], 'Anadolu Efes Istanbul': [2, 'IST'],
             'AX Armani Exchange Olimpia Milan': [3, 'MIL'], 'Crvena Zvezda MTS Belgrade': [4, 'RED'],
             'CSKA Moscow': [5, 'CSK'],
             'FC Barcelona Lassa': [6, 'BAR'], 'FC Bayern Munich': [7, 'MUN'], 'Fenerbahce Beko Istanbul': [8, 'ULK'],
             'Khimki Moscow Region': [9, 'KHI'], 'KIROLBET Baskonia Vitoria Gasteiz': [10, 'BAS'],
             'LDLC ASVEL Villeurbanne': [11, 'ASV'], 'Maccabi FOX Tel Aviv': [12, 'TEL'],
             'Olympiacos Piraeus': [13, 'OLY'], 'Panathinaikos OPAP Athens': [14, 'PAN'], 'Real Madrid': [15, 'MAD'],
             'Valencia Basket': [16, 'PAM'], 'Zalgiris Kaunas': [17, 'ZAL'], 'Zenit St Petersburg': [18, 'DYR']}

    teams_codes_n = OrderedDict(sorted(codes.items(), key=lambda t: t[1]))
    teams = [k for k, v in teams_codes_n.items()]
    return [teams, teams_codes_n]


def url_for_players(team_code, season_code):
    base_url = 'https://www.euroleague.net/competition/teams/showteam?clubcode='
    url = base_url + team_code + '&seasoncode=' + season_code
    return url


def fetch_teams(year):

    """Fetch teams
    """

    teams_dict = {}
    url = 'https://www.euroleague.net/competition/teams?seasoncode=E' + str(year)
    response = requests.get(url)
    tree = etree.HTML(response.content)

    '''Gets urls and names from html source. Returns lists.'''
    urls = tree.xpath('//div[@class="teams"]/div[@class="item"]/div[@class="RoasterName"]/a[1]/@href')
    names = tree.xpath('//div[@class="teams"]/div[@class="item"]/div[@class="RoasterName"]/a[1]/text()')

    '''Fixes urls.'''
    fixed_urls = [urljoin('https://www.euroleague.net/', link) for link in urls]

    for i, name in enumerate(names):
        if name in teams_dict:
            teams_dict[name] = name
        else:
            teams_dict[name] = [i + 1, fixed_urls[i]]

    return [teams_dict, names, year]


def fetch_players(url):
    """PURPOSE: Create dict with players' names and urls: {"name": [i, url]}."""

    player_dict = {}
    response = requests.get(url)
    tree = etree.HTML(response.content)

    '''Gets urls and names from html source. Returns lists.'''
    urls = tree.xpath('//div[@class="wp-module"]/div[@class="item player"]/div[@class="img"]/a[1]/@href')
    names = tree.xpath('//div[@class="wp-module"]/div[@class="item player"]/div[@class="name"]/a[1]/text()')

    '''Fixes urls.'''
    fixed_urls = [urljoin('https://www.euroleague.net/', link) for link in urls]

    '''Creates dict with players names, urls and also assigns a num to each of them.'''
    for i, name in enumerate(names):
        if name in player_dict:
            player_dict[name] = name
        else:
            player_dict[name] = [i + 1, fixed_urls[i]]

    del names, urls, fixed_urls, tree

    return player_dict


def get_tree(link):
    """PURPOSE: HTML Scrapper."""

    response = requests.get(link)
    tree = etree.HTML(response.content)

    return tree


def check_opponents(t):
    """PURPOSE: Creates 3 dicts with all teams the player played against in Regular Season, Play-Offs & Finals.
    Called by :meth: 'access_per_game_stats' - library5.py."""

    rivals_rs = t.xpath(
        '//div[@class="PlayerPhasesStatisticsMainContainer"]//div[@id="E2019_RS"]//'
        'table[@id="tblPlayerPhaseStatistics"]/tr/td[@class="RivalContainer"]/a/text()')
    rivals_po = t.xpath(
        '//div[@class="PlayerPhasesStatisticsMainContainer"]//div[@id="E2019_PO"]//'
        'table[@id="tblPlayerPhaseStatistics"]/tr/td[@class="RivalContainer"]/a/text()')
    rivals_ff = t.xpath(
        '//div[@class="PlayerPhasesStatisticsMainContainer"]//div[@id="E2019_FF"]//'
        'table[@id="tblPlayerPhaseStatistics"]/tr/td[@class="RivalContainer"]/a/text()')

    return [rivals_rs, rivals_po, rivals_ff]


def get_opponents_dict_on_press(roster_n, player_name):
    """PURPOSE: Checks link for a chosen player. If valid, the player's name and tree are returned.
    Called by :meth: 'access_bio' - library2.py."""

    link = None
    for name, url in roster_n.items():
        if name == player_name:
            link = url[1]
    if link is not None:
        t = get_tree(link)
        y = [t, player_name]
        return y
    return
