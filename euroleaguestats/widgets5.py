
"""RecycleView Widget. Called by :cls: 'Options'. Used for the presentation of average & total stats.
"""

from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.metrics import dp


Builder.load_string('''
<RV>:
    viewclass: 'StatLabel'
    RecycleBoxLayout:
        default_size: None, dp(36)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        size_hint_x: None
        width: root.width
        orientation: 'vertical'
''')


class StatLabel(Label):

    """Customized Label for the RecycleView Widget.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '14sp'
        self.halign = 'center'
        self.valign = 'middle'
        self.color = [0, 0, 0, 1]
        self.bind(width=lambda *x: self.setter('text_size')(self, (self.width, None)))
        self.markup = True


class RV(RecycleView):

    """The RecycleView Widget. Used for presenting average and total stats.
    """

    def __init__(self, stat_dict, **kwargs):
        super().__init__(**kwargs)

        self.bar_pos_y = 'right'
        self.bar_color = (.2, .6, .8, 1)
        self.bar_margin = -dp(6)
        self.bar_width = dp(2)
        self.data = [{'text': '[b]' + str(stat_category.upper()) + '[/b]' + '   ' + str(data_element)} for
                     stat_category, data_element in
                     stat_dict.items()]
