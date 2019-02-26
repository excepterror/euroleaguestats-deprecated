from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.metrics import Metrics

from library import check_opponents
from library3 import per_game_statistics, per_game_stats, get_opponents
from library4 import RV

factor5 = round(Metrics.dpi * .02002, 0)  # factor for bar width, is 2 for my laptop screen, dpi=99.8892
factor6 = round(Metrics.dpi * .01001, 0)  # factor for bar margin, is 1 for my laptop screen, dpi=99.8892


########################################################################################################################
# RecycleView Widget. Called by :cls:. Used for the presentation of per game stats.
########################################################################################################################


def access_per_game_stats(tree, name):
    k = per_game_stats(tree)  # Fetches stats for all games in each phase.
    y = check_opponents(tree)  # Creates dict with all opponents during each phase.
    q = get_opponents(tree, y[0], y[1], y[2])  # Creates 3 dicts, each, filled with the opponents of each phase, plus
    # the 'round' number.
    opponents_dict_rs = q[0]
    opponents_dict_po = q[1]
    opponents_dict_ff = q[2]
    games_stats_rs = k[0]
    games_stats_po = k[1]
    games_stats_ff = k[2]
    return \
        [opponents_dict_rs, opponents_dict_po, opponents_dict_ff, games_stats_rs, games_stats_po, games_stats_ff, name]


Builder.load_string('''
<SelectableLabel>:
    # Draw a background to indicate selection.
    canvas.before:
        Color:
            rgba: (1, 0.4, 0, .8) if self.selected else (0, 0, 0, .8)
        RoundedRectangle:
            segments: 40
            radius: 7,0
            pos: self.pos
            size: self.size
<RVMod>:
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        size_hint_x: None
        width: root.width
        orientation: 'vertical'
        spacing: 5
        multiselect: False
        touch_multiselect: False
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    # Adds selection and focus behaviour to the view.
    def __init__(self, **kwargs):
        super(SelectableRecycleBoxLayout, self).__init__(**kwargs)
        self.padding = 5


class SelectableLabel(RecycleDataViewBehavior, Label):
    # Add selection support to the Label.
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(SelectableLabel, self).__init__(**kwargs)
        self.halign = "center"
        self.valign = "middle"
        self.font_size = "16sp"
        self.color = (.2, .6, .8, 1)
        self.bind(width=lambda *x: self.setter("text_size")(self, (self.width, None)))

    def refresh_view_attrs(self, rv, index, data):
        # Catch and handle the view changes.
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        # Add selection on touch down.
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        # Respond to the selection of items in the view.
        self.selected = is_selected
        if is_selected:
            opponent = list(rv.data[index].values())
            g = index + 1
            games_stats_rs = rv.games_stats_rs
            games_stats_po = rv.games_stats_po
            games_stats_ff = rv.games_stats_ff
            z = per_game_statistics(games_stats_rs, games_stats_po, games_stats_ff, g)
            rv_view = RV(z)

            display_data_popup = Popup(content=rv_view, size_hint=[.9, .9],
                                       background="atlas://data/images/defaulttheme/textinput",
                                       separator_color=(1, .4, 0, 1),  # [255 / 255, 102 / 255, 0 / 255, 1.0]
                                       title=rv.pl_name + " " + opponent[0][9:], title_align="center",
                                       title_size="16sp",
                                       title_font="Roboto-Regular", title_color=[.2, .6, .8, 1], auto_dismiss=True)
            display_data_popup.open()
        else:
            return


class RVMod(RecycleView):
    # The RecycleView Widget. Used for presenting stats by game.
    def __init__(self, **kwargs):
        super(RVMod, self).__init__(**kwargs)
        self.viewclass = 'SelectableLabel'
        self.size_hint = [.95, .85]
        self.pos_hint = {'center_x': .5, 'y': .02}
        self.bar_pos_y = 'right'
        self.bar_width = factor5
        self.bar_margin = -factor6
        self.bar_color = (1, .4, 0, 1)

        a = access_per_game_stats(self.tree, self.name)
        self.data_rs = [{'text': "Round " + str(num) + ":" + " " + str(opp)} for opp, num in
                        a[0].items()]
        self.data_po = [{'text': str(opp)} for opp, num in a[1].items()]
        self.data_ff = [{'text': str(opp)} for opp, num in a[2].items()]
        self.data = self.data_rs + self.data_po + self.data_ff
        # self.opp = opponents_dict
        self.games_stats_rs = a[3]
        self.games_stats_po = a[4]
        self.games_stats_ff = a[5]
        self.pl_name = a[6]
