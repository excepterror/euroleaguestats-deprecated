"""RecycleView Widget. Called in Class 'Standings' - library8.py. Used for the presentation of standings."""

from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.metrics import dp

Builder.load_string('''
<DataLabel>:
    canvas.before:
        Color:
            rgba: (0, 0, 0, .75)
        RoundedRectangle:
            segments: 40
            radius: 7,0
            pos: self.pos
            size: self.size
<RVSt>:
    viewclass: 'DataLabel'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        size_hint_x: None
        width: root.width
        spacing: dp(5)
        orientation: 'vertical'
''')


class DataLabel(Label):
    """Customized Label for the RecycleView Widget #1."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = [0, 0]
        self.halign = 'center'
        self.valign = 'middle'
        self.font_size = '16sp'
        self.markup = True
        self.bind(width=lambda *x: self.setter('text_size')(self, (self.width, None)),
                  texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))


class RVSt(RecycleView):
    """The RecycleView Widget. Used for presenting the standings."""

    def __init__(self, current_teams_standings):
        super().__init__()
        self.size_hint = [.9, .85]
        self.pos_hint = {'center_x': .5, 'top': .86}
        self.bar_pos_y = 'right'
        self.bar_color = (0, 0, 0, 1)
        self.bar_margin = -dp(6)
        self.bar_width = dp(2)

        self.data = [{'text': '[b][color=FF6600]' + str(team) + '[/color][/b]'
                              + '\n' + '[color=FFFFFF] W  L  PTS+  PTS-  +/-[/color]' + '\n'
                              + '[i][color=FF6600]' + str(items[1]) + '[/color][/i]'}

                     if list(current_teams_standings.keys()).index(team) <= 7 else

                     {'text': '[b][color=0099CC]' + str(team) + '[/color][/b]'
                              + '\n' + '[color=FFFFFF] W  L  PTS+  PTS-  +/-[/color]' + '\n'
                              + '[i][color=0099CC]' + str(items[1]) + '[/color][/i]'}

                     for team, items in current_teams_standings.items()
                     ]
