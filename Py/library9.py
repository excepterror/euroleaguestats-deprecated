from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.metrics import Metrics

factor5 = round(Metrics.dpi * .02002, 0)  # factor for bar width, is 2 for my laptop screen, dpi=99.8892
factor6 = round(Metrics.dpi * .06006, 0)  # factor for bar margin, is 6 for my laptop screen, dpi=99.8892

########################################################################################################################
# RecycleView Widget. Called in Class 'Standings' - library8.py. Used for the presentation of standings.
########################################################################################################################


Builder.load_string('''
<DataLabel>:
    canvas.before:
        Color:
            rgba: (0, 0, 0, .8)
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
        spacing: 5
        orientation: 'vertical'
''')


class DataLabel(Label):
    # Customized Label for the RecycleView Widget.
    def __init__(self, **kwargs):
        super(DataLabel, self).__init__(**kwargs)
        self.padding = [0, 0]
        self.halign = "center"
        self.valign = "middle"
        self.font_size = '16sp'
        self.color = [1, .4, 0, 1]
        self.markup = True
        self.bind(width=lambda *x: self.setter("text_size")(self, (self.width, None)),
                  texture_size=lambda *x: self.setter("height")(self, self.texture_size[1]))


class RVSt(RecycleView):
    # The RecycleView Widget. Used for presenting the standings.
    def __init__(self, teams_performance, **kwargs):
        super(RVSt, self).__init__(**kwargs)

        self.size_hint = [.9, .85]
        self.pos_hint = {'center_x': .5, 'top': .86}
        self.bar_pos_y = 'right'
        self.bar_color = (.2, .6, .8, 1)
        self.bar_margin = -factor6
        self.bar_width = factor5

        self.data = [{'text': '[b]' + str(
            team) + '[/b]' + '\n' + '[b][color=0099CC] W   L   PTS+   PTS-   +/-[/color][/b]' + '\n' + '[i]' + str(
            items[1]) + '[/i]'} for team, items in
                     teams_performance.iteritems()]
