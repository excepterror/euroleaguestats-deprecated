import requests
import os
import kivy

from collections import OrderedDict

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition
from kivy.core.window import Window
from kivy.properties import BooleanProperty
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
from library7 import AnotherSpecialButton, PlayerButton  # ASpecialButton,
from library8 import get_standings, AnotherLabel
from library9 import RVSt
from library10 import is_connected

kivy.require('1.10.1')


########################################################################################################################
# Stats by game Screen Setup.
########################################################################################################################


class GameStats(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(GameStats, self).__init__(**kwargs)

        self.add_widget(Image(source='court.jpg', allow_stretch=True, keep_ratio=False))

        with self.canvas:
            Color(0, 0, 0, 1)
            self.vertical_l = Line(width=3, points=[0, 0, 0, y])
            self.vertical_r = Line(width=3, points=[x, 0, x, y])
            self.horizontal_top = Line(width=3, points=[0, y, x, y])
            self.horizontal_bottom = Line(width=3, points=[0, 0, x, 0])

        label = AnotherLabel(text='Games played by ' + self.player_name, font_size='14sp')
        recycle_viewer = RVMod()

        self.add_widget(label)
        self.add_widget(recycle_viewer)

    def on_enter(self, *args):
        if 'GameStats()' in screens_used:
            pass
        else:
            screens_used.append('GameStats()')


########################################################################################################################
# Options & Player Info Screen Setup.
########################################################################################################################


class Options(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(Options, self).__init__(**kwargs)

        self.add_widget(Image(source='court.jpg', allow_stretch=True, keep_ratio=False))

        with self.canvas:
            Color(0, .6, .6, 1)
            self.vertical_l = Line(width=6, points=[0, 0, 0, y])
            self.vertical_r = Line(width=6, points=[x, 0, x, y])
            self.horizontal_top = Line(width=6, points=[0, y, x, y])
            self.horizontal_bottom = Line(width=6, points=[0, 0, x, 0])

        # D/L player's photo.
        if self.photo != 'NoImage.jpg':
            response = requests.get(self.photo)

            filename = self.player_name + ".jpg"
            with open(filename, "wb") as file_:
                file_.write(response.content)
        else:
            filename = 'NoImage.jpg'

        ph = Image(source=filename, allow_stretch=True, keep_ratio=False, size_hint=[None, .18],
                   width='210dp',
                   pos_hint={'center_x': .5, 'y': .67})

        name = MyOtherLabel(text=self.player_name, font_size='16sp')

        num_pos = Label(text=str(self.num) + " | " + str(self.position), color=[0, 0, 0, 1], font_size='16sp',
                        size_hint=[1, None], halign="center", valign="middle")
        num_pos.bind(width=lambda *x: num_pos.setter("text_size")(num_pos, (num_pos.width, None)),
                     texture_size=lambda *x: num_pos.setter("height")(num_pos, num_pos.texture_size[1]))

        bio = Label(text=str(self.height_) + " | " + str(self.date) + " | " + str(self.nationality), color=[0, 0, 0, 1],
                    font_size='16sp', size_hint=[1, None], halign="center", valign="center")
        bio.bind(width=lambda *x: bio.setter("text_size")(bio, (bio.width, None)),
                 texture_size=lambda *x: bio.setter("height")(bio, bio.texture_size[1]))

        grid1 = GridLayout(size_hint=[1, .1], cols=1, rows=3, spacing=7, padding=10, pos_hint={'x': 0, 'y': .55})

        btn_for_all = MyLabel(text="Stats by game!", size_hint=[.7, .1], pos_hint={'center_x': .5, 'y': .37})
        btn_for_all.bind(on_release=callback_to_sc4,
                         width=lambda *x: btn_for_all.setter("text_size")(btn_for_all, (btn_for_all.width, None)),
                         texture_size=lambda *x: btn_for_all.setter("height")(btn_for_all, btn_for_all.texture_size[1]))

        btn_for_av = MyLabel(text="Average Stats!", size_hint=[.7, .1], pos_hint={'center_x': .5, 'y': .23})
        btn_for_av.bind(on_release=lambda *x: self.access_average_stats(),
                        width=lambda *x: btn_for_av.setter("text_size")(btn_for_av, (btn_for_av.width, None)),
                        texture_size=lambda *x: btn_for_av.setter("height")(btn_for_av, btn_for_av.texture_size[1]))

        btn_for_tot = MyLabel(text="Total Stats!", size_hint=[.7, .1], pos_hint={'center_x': .5, 'y': .09})
        btn_for_tot.bind(on_release=lambda x: self.access_total_stats(),
                         width=lambda *x: btn_for_tot.setter("text_size")(btn_for_tot, (btn_for_tot.width, None)),
                         texture_size=lambda *x: btn_for_tot.setter("height")(btn_for_tot, btn_for_tot.texture_size[1]))

        for w in [num_pos, bio]:
            grid1.add_widget(w)

        for w in [name, ph, btn_for_all, btn_for_av, btn_for_tot, grid1]:
            self.add_widget(w)

        if filename != 'NoImage.jpg':
            try:
                os.remove(filename)
            except OSError:
                pass
        else:
            pass

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


########################################################################################################################
# Roster Screen Setup.
########################################################################################################################


class Roster(Screen, FocusBehavior, FloatLayout):
    def __init__(self, **kwargs):
        super(Roster, self).__init__(**kwargs)

        self.size_hint = [1, 1]
        self.pos_hint = {'x': 0, 'y': 0}
        self.add_widget(Image(source='court.jpg', allow_stretch=True, keep_ratio=False))

        title = MyOtherLabel(text=self.text + ' Roster', font_size='15sp')
        self.add_widget(title)

        with self.canvas:
            Color(0, .6, .6, 1)
            self.vertical_l = Line(width=6, points=[0, 0, 0, y])
            self.vertical_r = Line(width=6, points=[x, 0, x, y])
            self.horizontal_top = Line(width=6, points=[0, y, x, y])
            self.horizontal_bottom = Line(width=6, points=[0, 0, x, 0])

        # Layouts.
        scrollable_roster = ScrollView(do_scroll_x=False, bar_color=[.2, .6, .8, 1],
                                       bar_pos_y="left", bar_width=3, bar_margin=2, scroll_type=["bars", "content"],
                                       size_hint=[.95, .84],
                                       pos_hint={'center_x': .5, 'y': .03})

        grid = GridLayout(rows=len(self.roster_n), cols=1,
                          padding=10,
                          size_hint=[1, 1.8],
                          spacing=5)

        scrollable_roster.add_widget(grid)
        self.add_widget(scrollable_roster)

        # Widgets.
        for name, url in self.roster_n.items():
            btn_player = PlayerButton(text=str(name))
            btn_player.bind(on_release=callback_to_sc3)
            grid.add_widget(btn_player)

    def on_enter(self, *args):
        if 'Roster()' in screens_used:
            pass
        else:
            screens_used.append('Roster()')


########################################################################################################################
# Teams' Screen Setup.
########################################################################################################################


class DraggableLogo(DragBehavior, Widget):
    """This is a draggable widget (Ellipse, Rectangle or Image) that can be used anywhere you want. It currently makes a
     bunch of images draggable and adds a few effects too!"""

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

        # To set pos subtract from Window.width (or Window.height) factor2 * width (or height) / 2
        self.im = Image(source='rim.png', pos=(Window.width / 2 - factor2, Window.height / 2 - factor2),
                        size_hint=[None, None],
                        width=factor2 * 2, height=factor2 * 2, opacity=0)
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

        if self.collide_point(*touch.pos) and sx + factor1 >= tx > sx and sy + factor1 >= ty > sy:
            # The two extra conditions must be met otherwise the opacity will be changed for all widget's children!
            self.im.opacity = 1
            self.logo.opacity = .5

            # Code to show tooltip text with chosen team's name on touch down event.
            teams_up = urls_teams()[0][:8]
            teams_down = urls_teams()[0][8:16]

            image_name = self.logo.source.rpartition('.')[0]

            if image_name in teams_up:
                for child in self.children:
                    # Checks to see if tooltip is already added & avoids subsequent crash.
                    if self.tooltip_up not in self.children:
                        self.tooltip_up.text = image_name
                        self.add_widget(self.tooltip_up)
                        Clock.schedule_once(self.remove_info_1, 1.5)
            elif image_name in teams_down:
                for child in self.children:
                    # Checks to see if tooltip is already added & avoids subsequent crash.
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

        tx, ty = touch.pos
        sx, sy = self.pos

        self.logo.opacity = 1
        self.im.opacity = 0

        pos_init_dict = {'Anadolu Efes Istanbul.png': [offset, y - a],
                         'AX Armani Exchange Olimpia Milan.png': [factor1 + 2 * offset, y - a],
                         'Buducnost VOLI Podgorica.png': [x - 2 * factor1 - 2 * offset, y - a],
                         'CSKA Moscow.png': [x - offset - factor1, y - a],
                         'Darussafaka Tefken Istanbul.png': [offset, y - 2.5 * a],
                         'FC Barcelona Lassa.png': [factor1 + 2 * offset, y - 2.5 * a],
                         'FC Bayern Munich.png': [x - 2 * factor1 - 2 * offset, y - 2.5 * a],
                         'Fenerbahce Istanbul.png': [x - offset - factor1, y - 2.5 * a],
                         'Herbalife Gran Canaria.png': [offset, 1.5 * a + factor1 / 2],
                         'Khimki Moscow Region.png': [factor1 + 2 * offset, 1.5 * a + factor1 / 2],
                         'KIROLBET Baskonia Vitoria Gasteiz.png': [x - 2 * factor1 - 2 * offset, 1.5 * a + factor1 / 2],
                         'Maccabi FOX Tel Aviv.png': [x - offset - factor1, 1.5 * a + factor1 / 2],
                         'Olympiacos Piraeus.png': [offset, c],
                         'Panathinaikos OPAP Athens.png': [factor1 + 2 * offset, c],
                         'Real Madrid.png': [x - 2 * factor1 - 2 * offset, c],
                         'Zalgiris Kaunas.png': [x - offset - factor1, c]}

        Animation.stop_all(self)

        if self.collide_point(*touch.pos) and sx + factor1 >= tx > sx and sy + factor1 >= ty > sy:
            # Code to get the image back to its original position.
            image_name = self.logo.source.rpartition('\\')[-1]
            for k, v in pos_init_dict.items():
                if k == image_name:
                    anim = Animation(x=v[0], y=v[1], duration=1, t='out_elastic', opacity=1)
                    anim.start(self)

        if x / 2. > self.x > x / 2. - factor3 and y / 2. - factor3 < self.y < y / 2. and (
                self.collide_point(*touch.pos) and sx + factor1 >= tx > sx and sy + factor1 >= ty > sy):
            # Checking first if the position of the widget (image) is within the bounding circle, then...

            image_name = self.logo.source.rpartition('\\')[-1]
            roster_n = {}

            image_name_ = image_name.rpartition('.')[0]
            teams_codes = urls_teams()[1]
            for team, data in teams_codes.items():
                if team == image_name_:
                    roster = get_players(data[0])
                    roster_n = OrderedDict(sorted(roster.iteritems(), key=lambda t: t[1]))

            Roster.text = image_name_
            Roster.roster_n = roster_n
            callback_to_sc2()

        return super(DraggableLogo, self).on_touch_up(touch)


class Teams(Screen, FloatLayout):
    # Menu screen.
    def __init__(self, **kwargs):
        super(Teams, self).__init__(**kwargs)

        ph = Image(source='court.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(ph)

        with self.canvas:
            Color(1, .2, 0, .9)  # 1, .4, 0, 1
            self.centered_circle = Line(width=3).circle = (
                x / 2., y / 2., factor3, 0, 360, 60)

            self.centered_line_l = Line(width=3, points=[0, y / 2, x / 2 - factor3, y / 2])
            self.centered_line_r = Line(width=3, points=[x, y / 2, x / 2 + factor3, y / 2])
            self.vertical_l = Line(width=6, points=[0, 0, 0, y])
            self.vertical_r = Line(width=6, points=[x, 0, x, y])
            self.horizontal_top = Line(width=6, points=[0, y, x, y])
            self.horizontal_bottom = Line(width=6, points=[0, 0, x, 0])

            # self.test_line = Line(width=1, points=[0, y / 2 - 112.5, x, y / 2 - 112.5])

        DraggableLogo.emblem = 'Anadolu Efes Istanbul.png'
        self.add_widget(DraggableLogo(pos=[offset, y - a]))

        DraggableLogo.emblem = 'AX Armani Exchange Olimpia Milan.png'
        self.add_widget(DraggableLogo(pos=[factor1 + 2 * offset, y - a]))

        DraggableLogo.emblem = 'Buducnost VOLI Podgorica.png'
        self.add_widget(DraggableLogo(pos=[x - 2 * factor1 - 2 * offset, y - a]))

        DraggableLogo.emblem = 'CSKA Moscow.png'
        self.add_widget(DraggableLogo(pos=[x - offset - factor1, y - a]))

        DraggableLogo.emblem = 'Darussafaka Tefken Istanbul.png'
        self.add_widget(DraggableLogo(pos=[offset, y - 2.5 * a]))

        DraggableLogo.emblem = 'FC Barcelona Lassa.png'
        self.add_widget(DraggableLogo(pos=[factor1 + 2 * offset, y - 2.5 * a]))

        DraggableLogo.emblem = 'FC Bayern Munich.png'
        self.add_widget(DraggableLogo(pos=[x - 2 * factor1 - 2 * offset, y - 2.5 * a]))

        DraggableLogo.emblem = 'Fenerbahce Istanbul.png'
        self.add_widget(DraggableLogo(pos=[x - offset - factor1, y - 2.5 * a]))

        DraggableLogo.emblem = 'Herbalife Gran Canaria.png'
        self.add_widget(DraggableLogo(pos=[offset, 1.5 * a + factor1 / 2]))

        DraggableLogo.emblem = 'Khimki Moscow Region.png'
        self.add_widget(DraggableLogo(pos=[factor1 + 2 * offset, 1.5 * a + factor1 / 2]))

        DraggableLogo.emblem = 'KIROLBET Baskonia Vitoria Gasteiz.png'
        self.add_widget(DraggableLogo(pos=[x - 2 * factor1 - 2 * offset, 1.5 * a + factor1 / 2]))

        DraggableLogo.emblem = 'Maccabi FOX Tel Aviv.png'
        self.add_widget(DraggableLogo(pos=[x - offset - factor1, 1.5 * a + factor1 / 2]))

        DraggableLogo.emblem = 'Olympiacos Piraeus.png'
        self.add_widget(DraggableLogo(pos=[offset, c]))

        DraggableLogo.emblem = 'Panathinaikos OPAP Athens.png'
        self.add_widget(DraggableLogo(pos=[factor1 + 2 * offset, c]))

        DraggableLogo.emblem = 'Real Madrid.png'
        self.add_widget(DraggableLogo(pos=[x - 2 * factor1 - 2 * offset, c]))

        DraggableLogo.emblem = 'Zalgiris Kaunas.png'
        self.add_widget(DraggableLogo(pos=[x - offset - factor1, c]))

    def on_enter(self, *args):
        if 'Teams()' in screens_used:
            pass
        else:
            screens_used.append('Teams()')


########################################################################################################################
# Standings' Screen Setup.
########################################################################################################################


class Standings(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(Standings, self).__init__(**kwargs)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect)

        with self.canvas:
            Color(1, .2, 0, .9)
            self.vertical_l = Line(width=6, points=[0, 0, 0, y])
            self.vertical_r = Line(width=6, points=[x, 0, x, y])
            self.horizontal_top = Line(width=6, points=[0, y, x, y])
            self.horizontal_bottom = Line(width=6, points=[0, 0, x, 0])

        round_info = AnotherLabel(font_size='14sp',
                                  text='[b]' + self.info[0] + '\n' + '[color=FFFFFF]' + self.info[
                                      1] + '[/color]' + '[/b]')
        self.add_widget(round_info)

        rv_view = RVSt(self.teams_performance)
        self.add_widget(rv_view)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_enter(self, *args):
        if 'Standings()' in screens_used:
            pass
        else:
            screens_used.append('Standings()')


########################################################################################################################
# Landing Screen Setup.
########################################################################################################################


class LandingScreen(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(LandingScreen, self).__init__(**kwargs)

        c = is_connected("www.euroleague.net")
        if c is False:
            with self.canvas.before:
                Color(1, 1, 1, .1)
                self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_rect)

            message = Label(
                text="Could not connect to www.euroleague.net. Please, close the app and check you network connection.",
                font_size="13sp", color=[0, 0, 0, 1], size_hint_y=None, pos_hint={"x": .5, "y": .35},
                halign="center", valign="center")
            message.bind(width=lambda *x: message.setter("text_size")(message, (message.width, None)),
                         texture_size=lambda *x: message.setter("height")(message, message.texture_size[1]))

            warning_popup = Popup(content=message, size_hint=[.8, .4], title="Connection Error",
                                  title_size="15sp", title_color=[0, 0, 0, 1], separator_color=[1, .4, 0, 1],
                                  title_font="Roboto-Regular", background="atlas://data/images/defaulttheme/textinput",
                                  pos_hint={'center_x': .5, 'center_y': .5}, auto_dismiss=False)
            warning_popup.open()

        else:

            with self.canvas.before:
                Color(1, 1, 1, 1)
                self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_rect)

            im = Image(source='Logo.png', size_hint=[1, .5], pos_hint={'center_x': .5, 'center_y': .7})
            self.add_widget(im)

            '''btn1 = ASpecialButton(text='This text will not show!', size_hint=[.497, .097],
                                  pos_hint={'center_x': .5, 'center_y': .3})
            btn1.bind(width=lambda *x: btn1.setter("text_size")(btn1, (btn1.width, None)),
                      texture_size=lambda *x: btn1.setter("height")(btn1, btn1.texture_size[1]))'''

            btn1_ = AnotherSpecialButton(text='Enter', size_hint=[.6, .097],
                                         pos_hint={'center_x': .5, 'center_y': .3})
            btn1_.bind(on_press=callback_to_sc1a,
                       width=lambda *x: btn1_.setter("text_size")(btn1_, (btn1_.width, None)),
                       texture_size=lambda *x: btn1_.setter("height")(btn1_, btn1_.texture_size[1]))

            '''btn2 = ASpecialButton(text='This text will not show!', size_hint=[.497, .097],
                                  pos_hint={'center_x': .5, 'center_y': .15})
            btn2.bind(width=lambda *x: btn2.setter("text_size")(btn2, (btn2.width, None)),
                      texture_size=lambda *x: btn2.setter("height")(btn2, btn2.texture_size[1]))'''

            btn2_ = AnotherSpecialButton(text='Standings', size_hint=[.6, .097],
                                         pos_hint={'center_x': .5, 'center_y': .15})
            btn2_.bind(on_press=callback_to_sc1b,
                       width=lambda *x: btn2_.setter("text_size")(btn2_, (btn2_.width, None)),
                       texture_size=lambda *x: btn2_.setter("height")(btn2_, btn2_.texture_size[1]))

            version = Label(text='v1.2.2', font_size='10', color=(0, .6, .8, 1), size_hint=[.25, .05],
                            pos_hint={'x': .75, 'y': 0}, halign='right', valign='middle')
            version.bind(width=lambda *x: version.setter("text_size")(version, (version.width, None)),
                         texture_size=lambda *x: version.setter("height")(version, version.texture_size[1]))

            for w in [btn1_, btn2_, version]:
                self.add_widget(w)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_enter(self, *args):
        if 'LandingScreen()' in screens_used:
            pass
        else:
            screens_used.append('LandingScreen()')


########################################################################################################################
########################################################################################################################


def callback_to_sc1a(*args):
    sm.switch_to(Teams())


def callback_to_sc1b(*args):
    Standings.teams_performance = get_standings()[0]
    Standings.info = get_standings()[1]
    sm.switch_to(Standings())


def callback_to_sc2():
    sm.switch_to(Roster())


def callback_to_sc3(instance):
    b = access_bio(Roster.roster_n, instance.text)

    Options.t = b[2]
    Options.photo = b[1][5]
    Options.player_name = b[0]
    Options.num = b[1][3]
    Options.position = b[1][4]
    Options.height_ = b[1][0]
    Options.date = b[1][1]
    Options.nationality = b[1][2]

    sm.switch_to(Options())


def callback_to_sc4(instance):
    # The following two lines perform a pre-check on the availability of statistics for the selected player. If no data
    # are available, the code will not proceed to the next screen but will open the 'No data' popup.
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

        self.transition = FallOutTransition(duration=.2)

        # Device's back button functionality.
        Window.bind(on_keyboard=self.android_back_click)

    def android_back_click(self, window, key, *largs):
        if key in [27, 1001]:
            if screens_used[-1] != 'LandingScreen()':
                del screens_used[-1]
                self.back = True
                return True
            else:
                ExitPopup().open()
                return True
        return False

    def on_back(self, instance, back, *args):
        self.switch_to(eval(screens_used[-1]))
        self.back = False


sm = MyScreenManager()
screens_used = []

x = Window.system_size[0]
y = Window.system_size[1]

factor1 = Metrics.dpi * .40044  # factor for logo images, is 40 for my laptop screen, dpi=99.8892
factor2 = Metrics.dpi * .70077  # factor for rim.png, is 70 for my laptop screen, dpi=99.8892
factor3 = Metrics.dpi * .30033  # factor for middle circle in 'teams' screen, is 30 for my laptop screen, dpi=99.8892

offset = (x / 2 - 2 * factor1) / 3
a = factor1 + factor1 / 2  # 67.5 for my laptop screen, dpi=99.8892
c = factor1 / 2  # 22.5 for my laptop screen, dpi=99.8892


class EuroLeagueStatsApp(App):
    def build(self):
        sm.add_widget(LandingScreen())
        return sm


if __name__ == '__main__':
    EuroLeagueStatsApp().run()
