import requests

from collections import OrderedDict
from lxml import etree
from urllib.parse import urljoin


def urls_teams():
    # PURPOSE: Returns the names of the teams and the dictionary. Called in 'Class' DraggableLogo - main.py.
    teams_codes = {'Alba Berlin': [1], 'Anadolu Efes Istanbul': [2],
                   'AX Armani Exchange Olimpia Milan': [3], 'Crvena Zvezda MTS Belgrade': [4], 'CSKA Moscow': [5],
                   'FC Barcelona Lassa': [6], 'FC Bayern Munich': [7], 'Fenerbahce Beko Istanbul': [8],
                   'Khimki Moscow Region': [9], 'KIROLBET Baskonia Vitoria Gasteiz': [10],
                   'LDLC ASVEL Villeurbanne': [11], 'Maccabi FOX Tel Aviv': [12],
                   'Olympiacos Piraeus': [13], 'Panathinaikos OPAP Athens': [14], 'Real Madrid': [15],
                   'Valencia Basket': [16], 'Zalgiris Kaunas': [17], 'Zenit St Petersburg': [18]}
    teams = []
    teams_codes_n = OrderedDict(sorted(teams_codes.items(), key=lambda t: t[1]))
    for k, v in teams_codes_n.items():
        teams.append(k)
    return [teams, teams_codes_n]


def get_players(suffix):
    # PURPOSE: Create dict with players' names and urls: {"name": [i, url]}.
    players_names = []
    players_urls = []
    player_dict = {}
    base_url = "https://www.euroleague.net/competition/players?team="
    url = base_url + str(suffix)
    response = requests.get(url)
    tree = etree.HTML(response.content)
    # Gets urls and names from html source. Returns lists.
    urls = tree.xpath("//div[@class='items-list']/div[@class='item']/a[1]/@href")
    names = tree.xpath("//div[@class='items-list']/div[@class='item']/a[1]/text()")
    # Fixes names.
    for data in names:
        players_names.append(data.partition(" " * 24)[-1].rpartition("\r")[0])
    # Fixes urls.
    for link in urls:
        players_urls.append(urljoin("https://www.euroleague.net/", link))
    # Creates dict with players names, urls and also assigns a num to each of them.
    for i, name in enumerate(players_names):
        if name in player_dict:
            player_dict[name] = name
        else:
            player_dict[name] = [i + 1, players_urls[i]]
    del names, players_names, urls, players_urls
    return player_dict


def get_tree(link):
    # PURPOSE: HTML Scrapper.
    response = requests.get(link)
    tree = etree.HTML(response.content)
    return tree


def check_opponents(t):
    # PURPOSE: Creates 3 dicts with all teams the player played against in Regular Season, Play-Offs & Finals.
    rivals_rs = t.xpath(
        "//div[@class='PlayerPhasesStatisticsMainContainer']//div[@id='E2019_RS']//"
        "table[@id='tblPlayerPhaseStatistics']/tr/td[@class='RivalContainer']/a/text()")
    rivals_po = t.xpath(
        "//div[@class='PlayerPhasesStatisticsMainContainer']//div[@id='E2019_PO']//"
        "table[@id='tblPlayerPhaseStatistics']/tr/td[@class='RivalContainer']/a/text()")
    rivals_ff = t.xpath(
        "//div[@class='PlayerPhasesStatisticsMainContainer']//div[@id='E2019_FF']//"
        "table[@id='tblPlayerPhaseStatistics']/tr/td[@class='RivalContainer']/a/text()")
    return [rivals_rs, rivals_po, rivals_ff]


def get_opponents_dict_on_press(roster_n, player_name):
    # PURPOSE: Checks link for a chosen player. If valid, the player's name and tree are returned.
    link = None
    for name, url in roster_n.items():
        if name == player_name:
            link = url[1]
    if link is not None:
        t = get_tree(link)
        y = [t, player_name]
        return y
    return
