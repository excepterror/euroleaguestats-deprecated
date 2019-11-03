import os
import requests
import kivy
from collections import OrderedDict

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import Metrics

from library import urls_teams, get_players
from library2 import access_bio, stability_check
from library3 import dict_creator, get_aver_stats, get_total_stats
from library4 import RV
from library5 import RVMod
from library6 import MyLabel, ExitPopup, ToolTipTextUp, ToolTipTextDown, MyOtherLabel
from library7 import AnotherSpecialButton, PlayerButton, ASpecialButton
from library8 import get_standings, AnotherLabel
from library9 import RVSt
from library10 import resolve_connectivity, GotItButton, ConnWarnPopup

scr_w = Window.system_size[0]
scr_h = Window.system_size[1]

'''
factor1: for logo images, is 38 for my laptop screen, dpi=99.8892
factor2: for rim.png, is 67 for my laptop screen, dpi=99.8892
factor3: for middle circle in 'teams' screen, is 29 for my laptop screen, dpi=99.8892
factor4: for border lines etc., is 3 for my laptop screen, dpi=99.8892
factor5: for bar width, is 2 for my laptop screen, dpi=99.8892
factor6: for bar margin in :cls: Roster, is 2 for my laptop screen, dpi=99.8892
a: 67.5 for my laptop screen, dpi=99.8892
c: 22.5 for my laptop screen, dpi=99.8892
'''

factor1 = round(Metrics.dpi * .40044, 0)
# factor2 = round(Metrics.dpi * .70077, 0)
factor3 = round(Metrics.dpi * .30033, 0)
factor4 = round(Metrics.dpi * .03003, 0)
factor5 = round(Metrics.dpi * .02002, 0)
factor6 = round(Metrics.dpi * .0, 0)

offset = (scr_w / 2 - 2 * factor1) / 3

a = factor1 + factor1 / 2
c = factor1 / 2


class GameStats(Screen):
    """
    Stats by Game Screen Setup
    """

    def __init__(self, **kwargs):
        super(GameStats, self).__init__(**kwargs)
        self.name = 'game_stats'

        self.add_widget(Image(source='Court.jpg', allow_stretch=True, keep_ratio=False))

        with self.canvas:
            Color(0, .2, .4, 1)
            self.vertical_l = Line(width=factor4, points=[0, 0, 0, scr_h])
            self.vertical_r = Line(width=factor4, points=[scr_w, 0, scr_w, scr_h])
            self.horizontal_top = Line(width=factor4, points=[0, scr_h, scr_w, scr_h])
            self.horizontal_bottom = Line(width=factor4, points=[0, 0, scr_w, 0])

        label = AnotherLabel(text='Games played by ' + self.player_name, font_size='17sp')
        recycle_viewer = RVMod()

        self.add_widget(label)
        self.add_widget(recycle_viewer)

    def on_enter(self, *args):
        if 'GameStats()' in screens_used:
            pass
        else:
            screens_used.append('GameStats()')


class Options(Screen):
    """
    Options & Player Info Screen Setup
    """

    def __init__(self, **kwargs):
        super(Options, self).__init__(**kwargs)
        self.name = 'options'

        self.add_widget(Image(source='Court.jpg', allow_stretch=True, keep_ratio=False))

        with self.canvas:
            Color(0, .6, .6, 1)
            self.vertical_l = Line(width=factor4, points=[0, 0, 0, scr_h])
            self.vertical_r = Line(width=factor4, points=[scr_w, 0, scr_w, scr_h])
            self.horizontal_top = Line(width=factor4, points=[0, scr_h, scr_w, scr_h])
            self.horizontal_bottom = Line(width=factor4, points=[0, 0, scr_w, 0])

        ph = Image(source=self.filename, allow_stretch=True, keep_ratio=False, size_hint=[None, .18],
                   width='210dp',
                   pos_hint={'center_x': .5, 'y': .67})

        pl_name = MyOtherLabel(text=self.player_name, font_size='17sp')

        num_pos = Label(text=str(self.num) + " | " + str(self.position), color=[0, 0, 0, 1], font_size='17sp',
                        size_hint=[1, None], halign="center", valign="middle")
        num_pos.bind(width=lambda *x: num_pos.setter("text_size")(num_pos, (num_pos.width, None)),
                     texture_size=lambda *x: num_pos.setter("height")(num_pos, num_pos.texture_size[1]))

        bio = Label(text=str(self.height_) + " | " + str(self.date) + " | " + str(self.nationality), color=[0, 0, 0, 1],
                    font_size='17sp', size_hint=[1, None], halign="center", valign="center")
        bio.bind(width=lambda *x: bio.setter("text_size")(bio, (bio.width, None)),
                 texture_size=lambda *x: bio.setter("height")(bio, bio.texture_size[1]))

        grid1 = GridLayout(size_hint=[1, .1], cols=1, rows=3, spacing=7, padding=10, pos_hint={'x': 0, 'y': .55})

        btn_for_all = MyLabel(text="Stats by game", size_hint=[.7, .1], pos_hint={'center_x': .5, 'y': .37})
        btn_for_all.bind(on_release=callback_to_sc4,
                         width=lambda *x: btn_for_all.setter("text_size")(btn_for_all, (btn_for_all.width, None)),
                         texture_size=lambda *x: btn_for_all.setter("height")(btn_for_all, btn_for_all.texture_size[1]))

        btn_for_av = MyLabel(text="Average Stats", size_hint=[.7, .1], pos_hint={'center_x': .5, 'y': .23})
        btn_for_av.bind(on_release=lambda *x: self.access_average_stats(),
                        width=lambda *x: btn_for_av.setter("text_size")(btn_for_av, (btn_for_av.width, None)),
                        texture_size=lambda *x: btn_for_av.setter("height")(btn_for_av, btn_for_av.texture_size[1]))

        btn_for_tot = MyLabel(text="Total Stats", size_hint=[.7, .1], pos_hint={'center_x': .5, 'y': .09})
        btn_for_tot.bind(on_release=lambda x: self.access_total_stats(),
                         width=lambda *x: btn_for_tot.setter("text_size")(btn_for_tot, (btn_for_tot.width, None)),
                         texture_size=lambda *x: btn_for_tot.setter("height")(btn_for_tot, btn_for_tot.texture_size[1]))

        for w in [num_pos, bio]:
            grid1.add_widget(w)

        for w in [pl_name, ph, btn_for_all, btn_for_av, btn_for_tot, grid1]:
            self.add_widget(w)

    def access_average_stats(self):
        av_stats_list = get_aver_stats(self.t)
        v = stability_check(av_stats_list)
        if v is None:
            pass
        else:
            average_stats_dict = dict_creator(v)
            rv_view = RV(average_stats_dict)
            display_data_popup = Popup(content=rv_view, size_hint=[.9, .9],
                                       separator_color=(1, .4, 0, 1),  # [255 / 255, 102 / 255, 0 / 255, 1.0],
                                       background="atlas://data/images/defaulttheme/textinput",
                                       title="Average Stats for " + self.player_name, title_align="center",
                                       title_size="16sp",
                                       title_font="Roboto-Regular", title_color=[.2, .6, .8, 1], auto_dismiss=True)
            display_data_popup.open()

    def access_total_stats(self):
        tot_stats_list = get_total_stats(self.t)
        v = stability_check(tot_stats_list)
        if v is None:
            pass
        else:
            total_stats_dict = dict_creator(v)
            rv_view = RV(total_stats_dict)
            display_data_popup = Popup(content=rv_view, size_hint=[.9, .9],
                                       separator_color=(1, .4, 0, 1),  # [255 / 255, 102 / 255, 0 / 255, 1.0],
                                       background="atlas://data/images/defaulttheme/textinput",
                                       title="Total Stats for " + self.player_name, title_align="center",
                                       title_size="16sp",
                                       title_font="Roboto-Regular", title_color=[.2, .6, .8, 1], auto_dismiss=True)
            display_data_popup.open()

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_enter(self, *args):
        if 'Options()' in screens_used:
            pass
        else:
            screens_used.append('Options()')


class Roster(Screen):
    """
    Roster Screen Setup
    """

    def __init__(self, **kwargs):
        super(Roster, self).__init__(**kwargs)
        self.name = 'roster'

        self.size_hint = [1, 1]
        self.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(Image(source='Court.jpg', allow_stretch=True, keep_ratio=False))

        title = MyOtherLabel(text=self.text + ' Roster', font_size='17sp')
        self.add_widget(title)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect)

        with self.canvas:
            Color(0, .6, .6, 1)
            self.vertical_l = Line(width=factor4, points=[0, 0, 0, scr_h])
            self.vertical_r = Line(width=factor4, points=[scr_w, 0, scr_w, scr_h])
            self.horizontal_top = Line(width=factor4, points=[0, scr_h, scr_w, scr_h])
            self.horizontal_bottom = Line(width=factor4, points=[0, 0, scr_w, 0])

        # Layouts.
        scrollable_roster = ScrollView(do_scroll_x=False, bar_color=[.2, .6, .8, 1],
                                       bar_pos_y="right", bar_width=factor5, bar_margin=factor6,
                                       scroll_type=["bars", "content"],
                                       size_hint=[.95, .84],
                                       pos_hint={'center_x': .5, 'y': .03})

        grid = GridLayout(rows=len(self.roster_n), cols=1,
                          padding=10,
                          size_hint=[1, 1.8],
                          spacing=6)

        scrollable_roster.add_widget(grid)
        self.add_widget(scrollable_roster)

        # Widgets.
        for pl_name, url in self.roster_n.items():
            btn_player = PlayerButton(text=str(pl_name))
            btn_player.bind(on_release=callback_to_sc3)
            grid.add_widget(btn_player)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_enter(self, *args):
        if 'Roster()' in screens_used:
            pass
        else:
            screens_used.append('Roster()')


class DraggableLogo(DragBehavior, Widget):
    """
     This is a draggable widget (Ellipse, Rectangle or Image) with potentially multiple uses. It currently makes a
     few images draggable and adds a few effects too!
    """

    def __init__(self, **kwargs):
        super(DraggableLogo, self).__init__(**kwargs)
        # self.size = (45, 45)
        # with self.canvas:
        # Color(1, 1, 1, 1)
        # self.my_circle = Ellipse(source=self.emblem, size=self.size, pos=self.pos)  # draggable circle
        # self.rect = Rectangle(pos=self.pos, size=self.size) # draggable rectangle

        self.logo = Image(source=self.emblem, allow_stretch=True, keep_ratio=False, size_hint=[None, None],
                          width=factor1, height=factor1, pos=self.pos)
        self.add_widget(self.logo)

        # To set pos subtract from Window.width (and Window.height) offset_im.
        # Convert width/2 (or height/2) from density-independent px to pixels.
        offset_im = kivy.metrics.dp(35)
        self.im = Image(source='rim.png', pos=(Window.width / 2 - offset_im, Window.height / 2 - offset_im),
                        size_hint=[None, None], allow_stretch=True, keep_ratio=False,
                        width='70dp', height='70dp', opacity=0)
        self.add_widget(self.im)

        self.bind(pos=self.update_rect)

        self.drag_rectangle = [self.x, self.y, factor1, factor1]
        self.drag_timeout = 10000000
        self.drag_distance = 0

        self.tooltip_up = ToolTipTextUp()  # ToolTip text feature, see on_touch_down below.
        self.tooltip_down = ToolTipTextDown()  # ToolTip text feature, see on_touch_down below.

    def update_rect(self, *args):
        # self.rect.size = self.size
        self.logo.pos = self.pos

    def on_touch_down(self, touch):

        tx, ty = touch.pos
        sx, sy = self.pos

        if self.collide_point(*touch.pos) and (sx + factor1 >= tx > sx and sy + factor1 >= ty > sy):
            # The two extra conditions must be met otherwise the opacity will be changed for all children!
            self.im.opacity = 1
            self.logo.opacity = .5

            # Code to show tooltip text with chosen team's name on touch down event.
            teams_up = urls_teams()[0][:9]
            teams_down = urls_teams()[0][9:18]

            image_name = self.logo.source.rpartition('.')[0]

            if image_name in teams_up:
                # Checks to see if tooltip is already activated.
                if self.tooltip_up not in self.children:
                    self.tooltip_up.text = image_name
                    self.add_widget(self.tooltip_up)
                    Clock.schedule_once(self.remove_info_1, 1.5)
            elif image_name in teams_down:
                # Checks to see if tooltip is already activated.
                if self.tooltip_down not in self.children:
                    self.tooltip_down.text = image_name
                    self.add_widget(self.tooltip_down)
                    Clock.schedule_once(self.remove_info_2, 1.5)
            else:
                pass
        return super(DraggableLogo, self).on_touch_down(touch)

    def remove_info_1(self, *args):
        self.remove_widget(self.tooltip_up)

    def remove_info_2(self, *args):
        self.remove_widget(self.tooltip_down)

    def on_touch_up(self, touch):

        self.logo.opacity = 1
        self.im.opacity = 0

        pos_init_dict = {'Alba Berlin.png': [offset, scr_h - a],
                         'Anadolu Efes Istanbul.png': [factor1 + 2 * offset, scr_h - a],
                         'AX Armani Exchange Olimpia Milan.png': [scr_w - 2 * factor1 - 2 * offset, scr_h - a],
                         'Crvena Zvezda MTS Belgrade.png': [scr_w - offset - factor1, scr_h - a],
                         'CSKA Moscow.png': [offset, scr_h - 2.5 * a],
                         'FC Barcelona Lassa.png': [factor1 + 2 * offset, scr_h - 2.5 * a],
                         'FC Bayern Munich.png': [scr_w - 2 * factor1 - 2 * offset, scr_h - 2.5 * a],
                         'Fenerbahce Beko Istanbul.png': [scr_w - offset - factor1, scr_h - 2.5 * a],
                         'Khimki Moscow Region.png': [offset, scr_h / 2 - factor1 / 2],
                         'KIROLBET Baskonia Vitoria Gasteiz.png': [scr_w - offset - factor1, scr_h / 2 - factor1 / 2],
                         'LDLC ASVEL Villeurbanne.png': [offset, 1.5 * a + factor1 / 2],
                         'Maccabi FOX Tel Aviv.png': [factor1 + 2 * offset, 1.5 * a + factor1 / 2],
                         'Olympiacos Piraeus.png': [scr_w - 2 * factor1 - 2 * offset,
                                                    1.5 * a + factor1 / 2],
                         'Panathinaikos OPAP Athens.png': [scr_w - offset - factor1, 1.5 * a + factor1 / 2],
                         'Real Madrid.png': [offset, c],
                         'Valencia Basket.png': [factor1 + 2 * offset, c],
                         'Zalgiris Kaunas.png': [scr_w - 2 * factor1 - 2 * offset, c],
                         'Zenit St Petersburg.png': [scr_w - offset - factor1, c]}

        Animation.stop_all(self)

        if self.collide_point(*touch.pos):
            # Code to get the image back to its original position.
            image_name = self.logo.source.rpartition('\\')[-1]
            for k, v in pos_init_dict.items():
                if k == image_name:
                    anim = Animation(x=v[0], y=v[1], duration=1, t='out_elastic', opacity=1)
                    anim.start(self)

        if scr_w / 2. > self.x > scr_w / 2. - factor3 and scr_h / 2. - factor3 < self.y < scr_h / 2.:
            # Checking first if the position of the widget (image) is within the bounding circle, then...

            image_name = self.logo.source.rpartition('\\')[-1]
            roster_n = {}

            image_name_ = image_name.rpartition('.')[0]
            teams_codes = urls_teams()[1]
            for team, data in teams_codes.items():
                if team == image_name_:
                    roster = get_players(data[0])
                    roster_n = OrderedDict(sorted(roster.items(), key=lambda t: t[1]))

            Roster.text = image_name_
            Roster.roster_n = roster_n
            callback_to_sc2()
        return super(DraggableLogo, self).on_touch_up(touch)


class Teams(Screen):
    """
    Teams' Screen Setup
    """

    def __init__(self, **kwargs):
        super(Teams, self).__init__(**kwargs)
        self.name = 'teams'

        ph = Image(source='Court.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(ph)

        with self.canvas:
            Color(0, 0, 0, 1)  # 1, .2, 0, .9
            self.centered_circle = Line(width=factor4 / 2.6).circle = (
                scr_w / 2., scr_h / 2., factor3, 0, 360, 60)

            # self.centered_line_l = Line(width=factor4 / 2.5, points=[0, scr_h / 2, scr_w / 2 - factor3, scr_h / 2])
            # self.centered_line_r = Line(width=factor4 / 2.5, points=[scr_w, scr_h / 2, scr_w / 2 + factor3, scr_h / 2])
            self.vertical_l = Line(width=factor4, points=[0, 0, 0, scr_h])
            self.vertical_r = Line(width=factor4, points=[scr_w, 0, scr_w, scr_h])
            self.horizontal_top = Line(width=factor4, points=[0, scr_h, scr_w, scr_h])
            self.horizontal_bottom = Line(width=factor4, points=[0, 0, scr_w, 0])

        DraggableLogo.emblem = 'Alba Berlin.png'
        self.add_widget(DraggableLogo(pos=[offset, scr_h - a]))

        DraggableLogo.emblem = 'Anadolu Efes Istanbul.png'
        self.add_widget(DraggableLogo(pos=[factor1 + 2 * offset, scr_h - a]))

        DraggableLogo.emblem = 'AX Armani Exchange Olimpia Milan.png'
        self.add_widget(DraggableLogo(pos=[scr_w - 2 * factor1 - 2 * offset, scr_h - a]))

        DraggableLogo.emblem = 'Crvena Zvezda MTS Belgrade.png'
        self.add_widget(DraggableLogo(pos=[scr_w - offset - factor1, scr_h - a]))

        DraggableLogo.emblem = 'CSKA Moscow.png'
        self.add_widget(DraggableLogo(pos=[offset, scr_h - 2.5 * a]))

        DraggableLogo.emblem = 'FC Barcelona Lassa.png'
        self.add_widget(DraggableLogo(pos=[factor1 + 2 * offset, scr_h - 2.5 * a]))

        DraggableLogo.emblem = 'FC Bayern Munich.png'
        self.add_widget(DraggableLogo(pos=[scr_w - 2 * factor1 - 2 * offset, scr_h - 2.5 * a]))

        DraggableLogo.emblem = 'Fenerbahce Beko Istanbul.png'
        self.add_widget(DraggableLogo(pos=[scr_w - offset - factor1, scr_h - 2.5 * a]))

        DraggableLogo.emblem = 'Khimki Moscow Region.png'
        self.add_widget(DraggableLogo(pos=[offset, scr_h / 2 - factor1 / 2]))

        DraggableLogo.emblem = 'KIROLBET Baskonia Vitoria Gasteiz.png'
        self.add_widget(DraggableLogo(pos=[scr_w - offset - factor1, scr_h / 2 - factor1 / 2]))

        DraggableLogo.emblem = 'LDLC ASVEL Villeurbanne.png'
        self.add_widget(DraggableLogo(pos=[offset, 1.5 * a + factor1 / 2]))

        DraggableLogo.emblem = 'Maccabi FOX Tel Aviv.png'
        self.add_widget(DraggableLogo(pos=[factor1 + 2 * offset, 1.5 * a + factor1 / 2]))

        DraggableLogo.emblem = 'Olympiacos Piraeus.png'
        self.add_widget(DraggableLogo(pos=[scr_w - 2 * factor1 - 2 * offset, 1.5 * a + factor1 / 2]))

        DraggableLogo.emblem = 'Panathinaikos OPAP Athens.png'
        self.add_widget(DraggableLogo(pos=[scr_w - offset - factor1, 1.5 * a + factor1 / 2]))

        DraggableLogo.emblem = 'Real Madrid.png'
        self.add_widget(DraggableLogo(pos=[offset, c]))

        DraggableLogo.emblem = 'Valencia Basket.png'
        self.add_widget(DraggableLogo(pos=[factor1 + 2 * offset, c]))

        DraggableLogo.emblem = 'Zalgiris Kaunas.png'
        self.add_widget(DraggableLogo(pos=[scr_w - 2 * factor1 - 2 * offset, c]))

        DraggableLogo.emblem = 'Zenit St Petersburg.png'
        self.add_widget(DraggableLogo(pos=[scr_w - offset - factor1, c]))

    def on_enter(self, *args):
        if 'Teams()' in screens_used:
            pass
        else:
            screens_used.append('Teams()')


class Standings(Screen):
    """
    Standings Screen Setup.
    """

    def __init__(self, **kwargs):
        super(Standings, self).__init__(**kwargs)
        self.name = 'standings'

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect)

        with self.canvas:
            Color(1, .2, 0, .9)
            self.vertical_l = Line(width=factor4, points=[0, 0, 0, scr_h])
            self.vertical_r = Line(width=factor4, points=[scr_w, 0, scr_w, scr_h])
            self.horizontal_top = Line(width=factor4, points=[0, scr_h, scr_w, scr_h])
            self.horizontal_bottom = Line(width=factor4, points=[0, 0, scr_w, 0])

        round_info = AnotherLabel(font_size='17sp',
                                  text='[b]' + self.info[0] + '\n' + '[color=FFFFFF]' + self.info[
                                      1] + '[/color]' + '[/b]')
        self.add_widget(round_info)

        rv_view = RVSt(self.current_teams_standings)
        self.add_widget(rv_view)

    def update_rect(self, *args):
        self.rect.size = Window.size
        # self.rect.pos = self.pos

    def on_enter(self, *args):
        if 'Standings()' in screens_used:
            pass
        else:
            screens_used.append('Standings()')


class ChangeLogScreen(Screen):
    """
    Changelog Screen Setup
    """
    log_text_1 = StringProperty(
        '\n[u]' + 'ELS v1.3.3 64-bit - Current Release' + '[/u]'
        + '\n\n> Update for Season 2019-20'
        + '\n\n> Other improvements')

    def __init__(self, **kwargs):
        super(ChangeLogScreen, self).__init__(**kwargs)
        self.name = 'changelog'

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect)

        got_it = GotItButton(text='OK, GOT IT !', size_hint=[.8, .097],
                             pos_hint={'center_x': .5, 'center_y': .1})
        got_it.bind(on_press=callback_to_sc1d,
                    width=lambda *x: got_it.setter("text_size")(got_it, (got_it.width, None)),
                    texture_size=lambda *x: got_it.setter("height")(got_it, got_it.texture_size[1]))
        self.add_widget(got_it)

        header = Label(text='C h a n g e l o g', font_size='30sp',
                       pos_hint={'center_x': .5, 'center_y': .93},
                       color=(0, 0, 0, 1),
                       halign='center', valign='middle',
                       font_name='Roboto-Regular')
        header.bind(width=lambda *x: header.setter("text_size")(header, (header.width, None)),
                    texture_size=lambda *x: header.setter("height")(header, header.texture_size[1]))
        self.add_widget(header)

        log1 = Label(text=self.log_text_1, font_size='17sp',
                     pos_hint={'center_x': .5, 'center_y': .6},
                     size_hint=[.9, 1],
                     color=(0, 0, 0, 1),
                     halign='center', valign='middle',
                     font_name='Roboto-Regular',
                     markup=True)
        log1.bind(width=lambda *x: log1.setter("text_size")(log1, (log1.width, None)),
                  texture_size=lambda *x: log1.setter("height")(log1, log1.texture_size[1]))
        self.add_widget(log1)

    def update_rect(self, *args):
        self.rect.size = Window.size
        # self.rect.pos = self.pos

    def on_enter(self, *args):
        if 'ChangeLogScreen()' in screens_used:
            pass
        else:
            screens_used.append('ChangeLogScreen()')


class HomeScreen(Screen):
    """
    Landing Screen Setup
    """

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.name = 'landing'

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect)

        im = Image(source='Logo.png', allow_stretch=True, keep_ratio=False, size_hint=[None, None],
                   pos_hint={'center_x': .5, 'center_y': .75},
                   width='250dp',
                   height='250dp')
        self.add_widget(im)

        btn1 = AnotherSpecialButton(text='Statistics', size_hint=[.7, .097],
                                    pos_hint={'center_x': .5, 'center_y': .4})
        btn1.bind(on_press=callback_to_sc1a,
                  width=lambda *x: btn1.setter("text_size")(btn1, (btn1.width, None)),
                  texture_size=lambda *x: btn1.setter("height")(btn1, btn1.texture_size[1]))

        btn2 = AnotherSpecialButton(text='Standings', size_hint=[.7, .097],
                                    pos_hint={'center_x': .5, 'center_y': .25})
        btn2.bind(on_press=callback_to_sc1b,
                  width=lambda *x: btn2.setter("text_size")(btn2, (btn2.width, None)),
                  texture_size=lambda *x: btn2.setter("height")(btn2, btn2.texture_size[1]))

        # ------> btn3 and btn4 form one widget!
        btn3 = AnotherSpecialButton(text='This text will not show', size_hint=[.6, .087],
                                    pos_hint={'center_x': .5, 'center_y': .1})
        btn3.bind(on_press=callback_to_sc1c,
                  width=lambda *x: btn3.setter("text_size")(btn3, (btn3.width, None)),
                  texture_size=lambda *x: btn3.setter("height")(btn3, btn3.texture_size[1]))

        btn4 = ASpecialButton(text='Changelog', size_hint=[.585, .084],
                              pos_hint={'center_x': .5, 'center_y': .1})
        btn1.bind(width=lambda *x: btn4.setter("text_size")(btn4, (btn4.width, None)),
                  texture_size=lambda *x: btn4.setter("height")(btn4, btn4.texture_size[1]))

        # version = Label(text='v1.2.9', font_size='10sp', color=(0, .6, .8, 1), size_hint=[.25, .05],
        # pos_hint={'x': .75, 'y': 0}, halign='right', valign='middle')
        # version.bind(width=lambda *x: version.setter("text_size")(version, (version.width, None)),
        # texture_size=lambda *x: version.setter("height")(version, version.texture_size[1]))

        for w in [btn1, btn2, btn3, btn4]:
            self.add_widget(w)

    def update_rect(self, *args):
        self.rect.size = Window.size
        # self.rect.pos = self.pos

    def on_enter(self, *args):
        if 'HomeScreen()' in screens_used:
            pass
        else:
            screens_used.append('HomeScreen()')


def callback_to_sc1a(*args):
    conn = resolve_connectivity()
    if conn is True:
        sm.switch_to(Teams())
    else:
        ConnWarnPopup(message=conn).open()


def callback_to_sc1b(*args):
    conn = resolve_connectivity()
    if conn is True:
        Standings.current_teams_standings = get_standings()[0]
        Standings.info = get_standings()[1]
        sm.switch_to(Standings())
    else:
        ConnWarnPopup(message=conn).open()


def callback_to_sc1c(*args):
    sm.switch_to(ChangeLogScreen())


def callback_to_sc1d(*args):
    del screens_used[-1]
    sm.switch_to(HomeScreen())


def callback_to_sc2():
    sm.switch_to(Roster())


def callback_to_sc3(instance):
    conn = resolve_connectivity()
    if conn is True:
        b = access_bio(Roster.roster_n, instance.text)

        Options.t = b[2]
        Options.player_name = b[0]
        Options.num = b[1][3]
        Options.position = b[1][4]
        Options.height_ = b[1][0]
        Options.date = b[1][1]
        Options.nationality = b[1][2]

        # D/L player's photo.
        photo_link = b[1][5]
        if photo_link != 'NoImage.jpg':
            response = requests.get(photo_link)
            filename = b[0] + ".jpg"
            with open(filename, "wb") as f:
                f.write(response.content)
        else:
            filename = 'NoImage.jpg'
        Options.filename = filename

        sm.switch_to(Options())

    else:
        ConnWarnPopup(message=conn).open()


def callback_to_sc4(instance):
    """
    The following two lines perform a pre-check on the availability of statistics for the selected player. If no data
    are available, the code will not proceed to the next screen but will open the 'No data' popup, instead.
    """
    av_stats_list = get_aver_stats(Options.t)  # Or: get_total_stats(Options.t)
    v = stability_check(av_stats_list)
    if v is None:
        pass
    else:
        RVMod.tree = Options.t
        RVMod.name = GameStats.player_name = Options.player_name
        sm.switch_to(GameStats())


class MyScreenManager(ScreenManager):
    back = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

        self.transition = FadeTransition(duration=.2)

        # Device's back button functionality.
        Window.bind(on_keyboard=self.android_back_click)

    def android_back_click(self, window, key, *largs):
        if key in [27, 1001]:
            if screens_used[-1] not in ['HomeScreen()', 'ChangeLogScreen()']:
                del screens_used[-1]
                self.back = True
                return True
            else:
                if screens_used[-1] in ['ChangeLogScreen()']:
                    ''' "ChangeLogScreen()" entry in :list: screens_used is deleted, when the user presses
                    the OK button in ChangeLogScreen (see, :meth: callback_to_sc1d).'''
                    return True
                else:
                    ExitPopup().open()
                    Clock.schedule_once(self.exit_app, 2)
                    return True
        return False

    def on_back(self, instance, back, *args):
        self.switch_to(eval(screens_used[-1]))
        self.back = False

    @staticmethod
    def exit_app(*args):
        ExitPopup().dismiss()
        App.get_running_app().stop()


sm = MyScreenManager()
screens_used = []


class EuroLeagueStatsApp(App):
    def build(self):
        sm.add_widget(HomeScreen())
        return sm

    def on_stop(self):
        for filename in os.listdir(os.getcwd()):
            if filename.endswith('.jpg') and filename not in ['Court.jpg', 'NoImage.jpg']:
                try:
                    os.remove(filename)
                except OSError:
                    pass


if __name__ == '__main__':
    EuroLeagueStatsApp().run()
