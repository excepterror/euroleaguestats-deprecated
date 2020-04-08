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

    def __init__(self, _tree, his_name, **kwargs):
        super(GameStats, self).__init__(**kwargs)
        self.name = 'game_stats'

        self.add_widget(Image(source='Court.jpg', allow_stretch=True, keep_ratio=False))

        with self.canvas:
            Color(0, .2, .4, 1)
            self.vertical_l = Line(width=factor4, points=[0, 0, 0, scr_h])
            self.vertical_r = Line(width=factor4, points=[scr_w, 0, scr_w, scr_h])
            self.horizontal_top = Line(width=factor4, points=[0, scr_h, scr_w, scr_h])
            self.horizontal_bottom = Line(width=factor4, points=[0, 0, scr_w, 0])

        label = AnotherLabel(text='Games played by ' + str(his_name), font_size='17sp')
        recycle_viewer = RVMod(_tree, his_name)

        for w in [label, recycle_viewer]:
            self.add_widget(w)

    def on_enter(self, *args):
        check_in_names(screen_name='game_stats')


class Options(Screen):
    """
    Options & Player Info Screen Setup
    """

    def __init__(self, _tree, player_name, num, position, height, date, nationality, filename, **kwargs):
        super(Options, self).__init__(**kwargs)
        self.name = 'options'

        self.add_widget(Image(source='Court.jpg', allow_stretch=True, keep_ratio=False))

        with self.canvas:
            Color(0, .6, .6, 1)
            self.vertical_l = Line(width=factor4, points=[0, 0, 0, scr_h])
            self.vertical_r = Line(width=factor4, points=[scr_w, 0, scr_w, scr_h])
            self.horizontal_top = Line(width=factor4, points=[0, scr_h, scr_w, scr_h])
            self.horizontal_bottom = Line(width=factor4, points=[0, 0, scr_w, 0])

        ph = Image(source=filename, allow_stretch=True, keep_ratio=False, size_hint=[None, .18],
                   width='210dp',
                   pos_hint={'center_x': .5, 'y': .67})

        pl_name = MyOtherLabel(text=player_name, font_size='17sp')

        num_pos = Label(text=str(num) + " | " + str(position), color=[0, 0, 0, 1], font_size='17sp',
                        size_hint=[1, None], halign="center", valign="middle")
        num_pos.bind(width=lambda *x: num_pos.setter("text_size")(num_pos, (num_pos.width, None)),
                     texture_size=lambda *x: num_pos.setter("height")(num_pos, num_pos.texture_size[1]))

        bio = Label(text=str(height) + " | " + str(date) + " | " + str(nationality), color=[0, 0, 0, 1],
                    font_size='17sp', size_hint=[1, None], halign="center", valign="center")
        bio.bind(width=lambda *x: bio.setter("text_size")(bio, (bio.width, None)),
                 texture_size=lambda *x: bio.setter("height")(bio, bio.texture_size[1]))

        grid1 = GridLayout(size_hint=[1, .1], cols=1, rows=3, spacing=7, padding=10, pos_hint={'x': 0, 'y': .55})

        btn_for_all = MyLabel(text="Stats by game", size_hint=[.7, .1], pos_hint={'center_x': .5, 'y': .37})
        btn_for_all.bind(on_release=callback_to_sc4,
                         width=lambda *x: btn_for_all.setter("text_size")(btn_for_all, (btn_for_all.width, None)),
                         texture_size=lambda *x: btn_for_all.setter("height")(btn_for_all, btn_for_all.texture_size[1]))

        btn_for_av = MyLabel(text="Average Stats", size_hint=[.7, .1], pos_hint={'center_x': .5, 'y': .23})
        btn_for_av.bind(on_release=lambda *x: self.access_average_stats(player_name, tree),
                        width=lambda *x: btn_for_av.setter("text_size")(btn_for_av, (btn_for_av.width, None)),
                        texture_size=lambda *x: btn_for_av.setter("height")(btn_for_av, btn_for_av.texture_size[1]))

        btn_for_tot = MyLabel(text="Total Stats", size_hint=[.7, .1], pos_hint={'center_x': .5, 'y': .09})
        btn_for_tot.bind(on_release=lambda x: self.access_total_stats(player_name, tree),
                         width=lambda *x: btn_for_tot.setter("text_size")(btn_for_tot, (btn_for_tot.width, None)),
                         texture_size=lambda *x: btn_for_tot.setter("height")(btn_for_tot, btn_for_tot.texture_size[1]))

        for w in [num_pos, bio]:
            grid1.add_widget(w)

        for w in [pl_name, ph, btn_for_all, btn_for_av, btn_for_tot, grid1]:
            self.add_widget(w)

    @staticmethod
    def access_average_stats(player_name, _tree):
        av_stats_list = get_aver_stats(_tree)
        v = stability_check(av_stats_list)
        if v is None:
            pass
        else:
            average_stats_dict = dict_creator(v)
            rv_view = RV(average_stats_dict)
            display_data_popup = Popup(content=rv_view, size_hint=[.9, .9],
                                       separator_color=(1, .4, 0, 1),  # [255 / 255, 102 / 255, 0 / 255, 1.0],
                                       background="atlas://data/images/defaulttheme/textinput",
                                       title="Average Stats for " + player_name, title_align="center",
                                       title_size="16sp",
                                       title_font="Roboto-Regular", title_color=[.2, .6, .8, 1], auto_dismiss=True)
            display_data_popup.open()

    @staticmethod
    def access_total_stats(player_name, _tree):
        tot_stats_list = get_total_stats(_tree)
        v = stability_check(tot_stats_list)
        if v is None:
            pass
        else:
            total_stats_dict = dict_creator(v)
            rv_view = RV(total_stats_dict)
            display_data_popup = Popup(content=rv_view, size_hint=[.9, .9],
                                       separator_color=(1, .4, 0, 1),  # [255 / 255, 102 / 255, 0 / 255, 1.0],
                                       background="atlas://data/images/defaulttheme/textinput",
                                       title="Total Stats for " + player_name, title_align="center",
                                       title_size="16sp",
                                       title_font="Roboto-Regular", title_color=[.2, .6, .8, 1], auto_dismiss=True)
            display_data_popup.open()

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_enter(self, *args):
        check_in_names(screen_name='options')


class Roster(Screen):
    """
    Roster Screen Setup
    """

    def __init__(self, team_roster, teams_name, **kwargs):
        super(Roster, self).__init__(**kwargs)
        self.name = 'roster'

        self.size_hint = [1, 1]
        self.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(Image(source='Court.jpg', allow_stretch=True, keep_ratio=False))

        title = MyOtherLabel(text=teams_name + ' Roster', font_size='17sp')
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

        # self.text and self.roster_n: from :meth: on_touch_up in :class: Draggable Logo
        grid = GridLayout(rows=len(team_roster), cols=1,
                          padding=10,
                          size_hint=[1, 1.8],
                          spacing=6)

        scrollable_roster.add_widget(grid)
        self.add_widget(scrollable_roster)

        # Widgets.
        for pl_name, url in team_roster.items():
            btn_player = PlayerButton(text=str(pl_name))
            btn_player.bind(on_release=callback_to_sc3)
            grid.add_widget(btn_player)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_enter(self, *args):
        check_in_names(screen_name='roster')


class DraggableLogo(DragBehavior, Widget):
    """
     This is a draggable widget (Ellipse, Rectangle or Image) with potentially multiple uses. It currently makes a
     few images draggable and adds a few effects too!
    """

    def __init__(self, emblem, **kwargs):
        super(DraggableLogo, self).__init__(**kwargs)

        self.logo = Image(source=emblem, allow_stretch=True, keep_ratio=False, size_hint=[None, None],
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

            image_name_ = image_name.rpartition('.')[0]
            teams_codes = urls_teams()[1]
            for team, data in teams_codes.items():
                # data[0] is a number from 1 - 18
                if team == image_name_:
                    roster = get_players(data[0])
                    global roster_n
                    roster_n = OrderedDict(sorted(roster.items(), key=lambda t: t[0]))

            callback_to_sc2(image_name_)
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

            self.vertical_l = Line(width=factor4, points=[0, 0, 0, scr_h])
            self.vertical_r = Line(width=factor4, points=[scr_w, 0, scr_w, scr_h])
            self.horizontal_top = Line(width=factor4, points=[0, scr_h, scr_w, scr_h])
            self.horizontal_bottom = Line(width=factor4, points=[0, 0, scr_w, 0])

        drag1 = DraggableLogo(pos=[offset, scr_h - a], emblem='Alba Berlin.png')

        drag2 = DraggableLogo(pos=[factor1 + 2 * offset, scr_h - a], emblem='Anadolu Efes Istanbul.png')

        drag3 = DraggableLogo(pos=[scr_w - 2 * factor1 - 2 * offset, scr_h - a],
                              emblem='AX Armani Exchange Olimpia Milan.png')

        drag4 = DraggableLogo(pos=[scr_w - offset - factor1, scr_h - a], emblem='Crvena Zvezda MTS Belgrade.png')
        drag5 = DraggableLogo(pos=[offset, scr_h - 2.5 * a], emblem='CSKA Moscow.png')

        drag6 = DraggableLogo(pos=[factor1 + 2 * offset, scr_h - 2.5 * a], emblem='FC Barcelona Lassa.png')

        drag7 = DraggableLogo(pos=[scr_w - 2 * factor1 - 2 * offset, scr_h - 2.5 * a], emblem='FC Bayern Munich.png')

        drag8 = DraggableLogo(pos=[scr_w - offset - factor1, scr_h - 2.5 * a], emblem='Fenerbahce Beko Istanbul.png')

        drag9 = DraggableLogo(pos=[offset, scr_h / 2 - factor1 / 2], emblem='Khimki Moscow Region.png')

        drag10 = DraggableLogo(pos=[scr_w - offset - factor1, scr_h / 2 - factor1 / 2],
                               emblem='KIROLBET Baskonia Vitoria Gasteiz.png')

        drag11 = DraggableLogo(pos=[offset, 1.5 * a + factor1 / 2], emblem='LDLC ASVEL Villeurbanne.png')

        drag12 = DraggableLogo(pos=[factor1 + 2 * offset, 1.5 * a + factor1 / 2], emblem='Maccabi FOX Tel Aviv.png')

        drag13 = DraggableLogo(pos=[scr_w - 2 * factor1 - 2 * offset, 1.5 * a + factor1 / 2],
                               emblem='Olympiacos Piraeus.png')

        drag14 = DraggableLogo(pos=[scr_w - offset - factor1, 1.5 * a + factor1 / 2],
                               emblem='Panathinaikos OPAP Athens.png')

        drag15 = DraggableLogo(pos=[offset, c], emblem='Real Madrid.png')

        drag16 = DraggableLogo(pos=[factor1 + 2 * offset, c], emblem='Valencia Basket.png')

        drag17 = DraggableLogo(pos=[scr_w - 2 * factor1 - 2 * offset, c], emblem='Zalgiris Kaunas.png')

        drag18 = DraggableLogo(pos=[scr_w - offset - factor1, c], emblem='Zenit St Petersburg.png')

        drags = [drag1, drag2, drag3, drag4, drag5, drag6, drag7, drag8, drag9, drag10, drag11, drag12, drag13, drag14,
                 drag15, drag16, drag17, drag18]
        for drag in drags:
            self.add_widget(drag)

    def on_enter(self, *args):
        check_in_names(screen_name='teams')


class Standings(Screen):
    """
    Standings Screen Setup.
    """

    def __init__(self, all_current_teams_standings, info, **kwargs):
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
                                  text='[b]' + info[0] + '\n' + '[color=FFFFFF]' + info[
                                      1] + '[/color]' + '[/b]')
        self.add_widget(round_info)

        rv_view = RVSt(all_current_teams_standings)
        self.add_widget(rv_view)

    def update_rect(self, *args):
        self.rect.size = Window.size
        # self.rect.pos = self.pos

    def on_enter(self, *args):
        check_in_names(screen_name='standings')


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
        self.name = 'change_log'

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
        check_in_names(screen_name='change_log')


class HomeScreen(Screen):
    """
    Landing Screen Setup
    """

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.name = 'home'

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

        for w in [btn1, btn2, btn3, btn4]:
            self.add_widget(w)

    def update_rect(self, *args):
        self.rect.size = Window.size

    def on_enter(self, *args):
        check_in_names(screen_name='home')


def check_in_names(screen_name):
    if screen_name in screens_used:
        pass
    else:
        screens_used.append(screen_name)


def callback_to_sc1a(*args):
    conn = resolve_connectivity()
    if conn is True:
        global my_teams
        my_teams = Teams()
        sm.switch_to(my_teams)
    else:
        ConnWarnPopup(message=conn).open()


def callback_to_sc1b(*args):
    conn = resolve_connectivity()
    if conn is True:
        current_teams_standings = get_standings()[0]
        inf = get_standings()[1]
        my_standings = Standings(all_current_teams_standings=current_teams_standings, info=inf)
        sm.switch_to(my_standings)
    else:
        ConnWarnPopup(message=conn).open()


def callback_to_sc1c(*args):
    change_log = ChangeLogScreen()
    sm.switch_to(change_log)


def callback_to_sc1d(*args):
    del screens_used[-1]
    sm.switch_to(my_home)


def callback_to_sc2(image_name):
    global my_roster
    my_roster = Roster(team_roster=roster_n, teams_name=image_name)
    sm.switch_to(my_roster)


def callback_to_sc3(instance, *args):
    conn = resolve_connectivity()
    if conn is True:

        roster = roster_n
        b = access_bio(roster, instance.text)

        global tree, athletes_name
        tree = b[2]
        athletes_name = b[0]

        # D/L player's photo.
        photo_link = b[1][5]
        if photo_link != 'NoImage.jpg':
            response = requests.get(photo_link)
            file_name = b[0] + ".jpg"
            with open(file_name, "wb") as f:
                f.write(response.content)
        else:
            file_name = 'NoImage.jpg'

        global my_options
        my_options = Options(_tree=b[2], player_name=b[0], num=b[1][3], position=b[1][4], height=b[1][0], date=b[1][1],
                             nationality=b[1][2], filename=file_name)
        sm.switch_to(my_options)

    else:
        ConnWarnPopup(message=conn).open()


def callback_to_sc4(instance):
    """
    The following two lines perform a pre-check on the availability of statistics for the selected player. If no data
    are available, the code will not proceed to the next screen but will open the 'No data' popup, instead.
    """
    av_stats_list = get_aver_stats(tree)
    v = stability_check(av_stats_list)
    if v is None:
        pass
    else:
        g_s = GameStats(_tree=tree, his_name=athletes_name)
        sm.switch_to(g_s)


class MyScreenManager(ScreenManager):
    back = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

        self.transition = FadeTransition(duration=.2)

        # Device's back button functionality.
        Window.bind(on_keyboard=self.android_back_click)

    def android_back_click(self, window, key, *largs):
        if key in [27, 1001]:
            x = screens_used[-1]
            screens_menu = (
            ('teams', my_home), ('roster', my_teams), ('options', my_roster), ('game_stats', my_options),
            ('standings', my_home))
            if x not in ['home', 'change_log']:
                for n, cl in screens_menu:
                    if x == n:
                        sm.switch_to(cl)
                        del screens_used[-1]
                        return True
            else:
                if screens_used[-1] in ['change_log']:
                    return True
                else:
                    ExitPopup().open()
                    Clock.schedule_once(self.exit_app, 1.5)
                    return True
        return False

    @staticmethod
    def exit_app(*args):
        ExitPopup().dismiss()
        App.get_running_app().stop()


tree = None
athletes_name = None
my_home = None
my_teams = None
my_options = None
my_roster = None

sm = MyScreenManager()
screens_used = []


class EuroLeagueStatsApp(App):
    def build(self):
        global my_home
        my_home = HomeScreen()
        sm.add_widget(my_home)
        return sm

    def on_stop(self):
        for file_name in os.listdir(os.getcwd()):
            if file_name.endswith('.jpg') and file_name not in ['Court.jpg', 'NoImage.jpg']:
                try:
                    os.remove(file_name)
                except OSError:
                    pass


if __name__ == '__main__':
    EuroLeagueStatsApp().run()
