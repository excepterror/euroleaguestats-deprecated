import requests

from lxml import etree
from collections import OrderedDict
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle


def get_standings():
    # Used in :meth: callback_to_sc1b - main.py.
    url = "http://www.euroleague.net/main/standings?seasoncode=E2018"
    response = requests.get(url)
    tree = etree.HTML(response.content)

    round_ = tree.xpath(
        "//div[@id='wrap']//div[@id='container']//div[@id='main-one']"
        "//div[@class='eu-show-games-topic-header']/span/text()")

    standings_teams = tree.xpath(
        "//div[@id='wrap']//div[@id='container']//div[@id='main-one']"
        "//div[@class='PhaseGroupStandingsMainContainer eu-RS-E2018 eu-RS-E']"
        "//table[@class='table responsive fixed-cols-1 table-left-cols-1 table-expand table-striped table-hover table-"
        "noborder table-centered table-condensed']/tbody/tr//td[@class='eu-game-info-grid-main-column']/a/text()")

    standings_data = tree.xpath(
        "//div[@id='wrap']//div[@id='container']//div[@id='main-one']"
        "//div[@class='PhaseGroupStandingsMainContainer eu-RS-E2018 eu-RS-E']"
        "//table[@class='table responsive fixed-cols-1 table-left-cols-1 table-expand table-striped table-hover table-"
        "noborder table-centered table-condensed']/tbody/tr/td/text()")

    round = round_[0].split(",")[:2]

    teams_standings = []
    for data in standings_teams:
        teams_standings.append(data.partition(" " * 33)[-1].rpartition("\r")[0])

    data_standings = []
    for data in standings_data:
        k = data.partition(" " * 28)[-1].rpartition("\r")[0]
        if k in ['     (qualified)', '']:
            pass
        else:
            data_standings.append(data.partition(" " * 28)[-1].rpartition("\r")[0])

    teams_performance_ = {}
    for i, team in enumerate(teams_standings):
        if team in teams_performance_:
            teams_performance_[team] = team
        else:
            special_str = ''
            for j in range(5 * i, 5 * i + 5):
                special_str += '  ' + data_standings[j]
            teams_performance_[team] = [i, special_str]
    teams_performance = OrderedDict(sorted(teams_performance_.items(), key=lambda t: t[1]))
    return [teams_performance, round]


class AnotherLabel(Label):
    # Used in Class 'Standings' & 'GameStats'- main.py.
    def __init__(self, **kwargs):
        super(AnotherLabel, self).__init__(**kwargs)
        # self.font_size = "14sp"
        self.size_hint = [.94, .065]
        self.pos_hint = {'center_x': .5, 'y': .90}
        self.color = (1, 1, 1, 1)  # (1, .4, 0, 1)
        self.halign = "center"
        self.valign = "middle"
        self.markup = True

        with self.canvas.before:
            Color(0, .2, .4, 1, mode='rgba')
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=40, radius=[17, ])
        self.bind(size=self.update_rect)

        self.bind(width=lambda *x: self.setter("text_size")(self, (self.width, None)),
                  texture_size=lambda *x: self.setter("height")(self, self.texture_size[1]))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
