"""The __main__ module controls the application's UI."""

import os
import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.core.window import Window
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import Metrics, dp
from kivy.uix.textinput import TextInput

from Widgets.popups import ConnWarnPopup, MessagePopup
from Widgets.any_colour_widgets import AnyColorLabel, AnyColorButton
from Widgets.tooltips import ToolTipTextUp, ToolTipTextDown
from Widgets.display_widgets import OptionsButtonLabel, DisplayLabel, DisplayButton
from Widgets.rv import RV
from Widgets.rv_mod import RVMod
from Widgets.rv_standings import RVSt
from Widgets.cube3d import Cube3D

from connectivity import resolve_connectivity
from participants import teams_codes, fetch_players, fetch_teams, url_for_players
from stability import access_bio, stability_check
from stats import dict_creator, fetch_aver_stats, fetch_total_stats
from standings import fetch_standings
from supplement import pos_init_dict, factor1, bind_instance

CURRENT_SEASON = ''

scr_w = Window.system_size[0]
scr_h = Window.system_size[1]

tree = None
athletes_name = None
my_home = None
my_teams = None
my_options = None
my_roster = None
menu = None
past_seasons = None
past_season_teams = None
past_roster = None
past_options = None
roster = {}


class PastSeasons(Screen):

    def __init__(self):
        super().__init__()

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size)
        self.bind(size=self.update_rect)

        self.text_input = TextInput(multiline=False, allow_copy=True,
                                    size_hint=[None, None],
                                    pos_hint={'center_x': .5, 'center_y': .5},
                                    hint_text='Any year from 2000 to 2019',
                                    input_filter='int',
                                    on_touch_down=self.clear_text,
                                    halign='center', width='220dp',
                                    height='35dp', font_size='16sp',
                                    hint_text_color=(1, .2, 0, .5),
                                    cursor_color=(1, .2, 0, .9), cursor_width='2sp',
                                    padding=[6, 6, 6, 6])
        self.text_input.bind(text=self.on_text)
        self.add_widget(self.text_input)

        ''' ------> btn2 and btn3 form one widget!'''
        btn1 = AnyColorButton(text=' ', r=1, g=.2, b=0, a=.9, font_size='21sp',
                              size_hint=[.45, .087],
                              pos_hint={'center_x': .5, 'center_y': .15})
        btn1.bind(on_press=self.fetch_past_teams)

        btn2 = AnyColorLabel(text='Go !', r=0, g=0, b=0, a=1,
                             size_hint=[.447, .084],
                             pos_hint={'center_x': .5, 'center_y': .15})

        for btn in [btn1, btn2]:
            self.add_widget(btn)

    def on_text(self, *args):
        if self.text_input.cursor_index() == 3:
            self.text_input.focus = False

    def clear_text(self, *args):
        self.text_input.text = ''

    def fetch_past_teams(self, *args):
        year = self.text_input.text
        allowed_period = [y for y in range(2000, 2020)]

        if year == '' or int(year) not in allowed_period:
            self.clear_text()
        else:
            teams_for_year = fetch_teams(year)

            global past_season_teams
            past_season_teams = PastSeasonTeams(teams_for_year[0], teams_for_year[1])
            past_season_teams.title.text = 'Season ' + teams_for_year[2] + ' - ' + str(int(teams_for_year[2]) + 1)

            sm.transition = FadeTransition(duration=.5)
            sm.switch_to(past_season_teams)

    def update_rect(self, *args):
        self.rect.size = Window.size

    @staticmethod
    def on_enter(*args):
        sm.check_in_names('past_seasons')


class GameStats(Screen):
    """
    Stats by Game Screen Setup
    """

    def __init__(self, _tree, his_name):
        super().__init__()

        with self.canvas.before:
            Color(1, 1, 1, .9)
            self.rect = Rectangle(size=self.size)
        self.bind(size=self.update_rect)

        label = DisplayLabel(text='Games played by ' + '[color=FF6600]' + str(his_name) + '[/color]',
                             font_size='17sp', r=0, g=0, b=0, a=1)
        recycle_viewer = RVMod(_tree, his_name)

        for w in [label, recycle_viewer]:
            self.add_widget(w)

    def update_rect(self, *args):
        self.rect.size = Window.size

    @staticmethod
    def on_enter(*args):
        sm.check_in_names('game_stats')


class Options(Screen):
    """
    Options & Player Info Screen Setup
    """

    def __init__(self, _tree, player_name, num, position, height, date, nationality, filename):
        super().__init__()

        with self.canvas.before:
            Color(1, 1, 1, .9)
            self.rect = Rectangle(size=self.size)
        self.bind(size=self.update_rect)

        ph = Image(source=filename, allow_stretch=True, keep_ratio=False, size_hint=[None, .18],
                   width='210dp',
                   pos_hint={'center_x': .5, 'y': .67})

        pl_name = DisplayLabel(text=player_name, font_size='17sp', r=0, g=.6, b=.6, a=1)

        num_pos = Label(text=str(num) + " | " + str(position), color=[0, 0, 0, 1], font_size='17sp',
                        size_hint=[1, None], halign="center", valign="middle")
        bind_instance(num_pos)

        bio = Label(text=str(height) + " | " + str(date) + " | " + str(nationality), color=[0, 0, 0, 1],
                    font_size='17sp', size_hint=[1, None], halign="center", valign="center")
        bind_instance(bio)

        grid1 = GridLayout(size_hint=[1, .1], cols=1, rows=3, spacing=7, padding=10, pos_hint={'x': 0, 'y': .55})

        btn_for_all = OptionsButtonLabel(text="Stats by game", size_hint=[.7, .1], pos_hint={'center_x': .5, 'y': .09})
        btn_for_all.bind(on_release=self.call_stats)

        btn_for_av = OptionsButtonLabel(text="Average Stats", size_hint=[.7, .1], pos_hint={'center_x': .5, 'y': .37})
        btn_for_av.bind(on_release=lambda *x: self.access_average_stats(player_name, tree))

        btn_for_tot = OptionsButtonLabel(text="Total Stats", size_hint=[.7, .1], pos_hint={'center_x': .5, 'y': .23})
        btn_for_tot.bind(on_release=lambda x: self.access_total_stats(player_name, tree))

        for w in [num_pos, bio]:
            grid1.add_widget(w)

        if sm.screens_visited[-1] == 'past_roster':
            btn_for_av.pos_hint = {'center_x': .5, 'y': .34}
            btn_for_tot.pos_hint = {'center_x': .5, 'y': .16}
            for w in [pl_name, ph, btn_for_av, btn_for_tot, grid1]:
                self.add_widget(w)
        else:
            for w in [pl_name, ph, btn_for_all, btn_for_av, btn_for_tot, grid1]:
                self.add_widget(w)

    @staticmethod
    def access_average_stats(player_name, _tree):

        av_stats_list = fetch_aver_stats(_tree)
        v = stability_check(av_stats_list)

        if v is None:
            pass

        else:
            average_stats_dict = dict_creator(v)
            rv_view = RV(average_stats_dict)
            display_data_popup = Popup(content=rv_view, size_hint=[.9, .9],
                                       separator_color=(1, .4, 0, 1),
                                       background="atlas://data/images/defaulttheme/textinput",
                                       title="Average Stats for " + player_name, title_align="center",
                                       title_size="16sp",
                                       title_font="Roboto-Regular", title_color=[.2, .6, .8, 1], auto_dismiss=True)
            display_data_popup.open()

    @staticmethod
    def access_total_stats(player_name, _tree):

        tot_stats_list = fetch_total_stats(_tree)
        v = stability_check(tot_stats_list)

        if v is None:
            pass

        else:
            total_stats_dict = dict_creator(v)
            rv_view = RV(total_stats_dict)
            display_data_popup = Popup(content=rv_view, size_hint=[.9, .9],
                                       separator_color=(1, .4, 0, 1),
                                       background="atlas://data/images/defaulttheme/textinput",
                                       title="Total Stats for " + player_name, title_align="center",
                                       title_size="16sp",
                                       title_font="Roboto-Regular", title_color=[.2, .6, .8, 1], auto_dismiss=True)
            display_data_popup.open()

    @staticmethod
    def call_stats(instance):

        """
        The following two lines perform a pre-check on the availability of statistics for the selected player. If no data
        are available, the code will not proceed to the next screen but will open the 'No data' popup, instead.
        """

        av_stats_list = fetch_aver_stats(tree)
        v = stability_check(av_stats_list)

        if v is None:
            pass

        else:
            game_stats = GameStats(_tree=tree, his_name=athletes_name)

            sm.transition = SlideTransition(direction='left')
            sm.switch_to(game_stats)

    def update_rect(self, *args):
        self.rect.size = Window.size

    @staticmethod
    def on_enter(*args):
        sm.check_in_names('options')


class PastOptions(Options):
    def __init__(self, _tree, player_name, num, position, height, date, nationality, filename):
        super().__init__(_tree, player_name, num, position, height, date, nationality, filename)

    @staticmethod
    def on_enter(*args):
        sm.check_in_names('past_options')


class Roster(Screen):
    """
    Roster Screen Setup
    """

    def __init__(self, _roster_, teams_name):
        super().__init__()

        self.size_hint = [1, 1]
        self.pos_hint = {'x': 0, 'y': 0}

        self.roster = _roster_

        self.title = DisplayLabel(text=str(teams_name), font_size='17sp', r=0, g=.6, b=.6, a=1)
        self.add_widget(self.title)

        with self.canvas.before:
            Color(1, 1, 1, .9)
            self.rect = Rectangle(size=self.size)
        self.bind(size=self.update_rect)

        if self.roster == {}:

            message = Label(text='To be announced..... Almost there now!', font_size='25sp',
                            color=(0, 0, 0, 1),
                            size_hint=[1, .2],
                            pos_hint={'center_x': .5, 'center_y': .55},
                            halign='center',
                            valign='middle')

            message.bind(width=lambda *x: message.setter('text_size')(message, (message.width, None)),
                         texture_size=lambda *x: message.setter('height')(message, message.texture_size[1]))

            self.add_widget(message)

        else:

            '''Layouts.'''
            scrollable_roster = ScrollView(do_scroll_x=False, bar_color=[.2, .6, .8, 1],
                                           bar_pos_y="right", bar_width=dp(2), bar_margin=dp(2),
                                           scroll_type=["bars", "content"],
                                           size_hint=[.95, .84],
                                           pos_hint={'center_x': .5, 'y': .03})

            '''self.text and self.roster_n: from :meth: on_touch_up in :class: Draggable Logo'''
            grid = GridLayout(rows=len(self.roster), cols=1,
                              padding=10,
                              size_hint=[1, 2.45],
                              spacing=6)

            scrollable_roster.add_widget(grid)
            self.add_widget(scrollable_roster)

            for _name, url in self.roster.items():
                self.btn = DisplayButton(text=str(_name))
                self.btn.bind(on_release=self.call_options)
                grid.add_widget(self.btn)

    def update_rect(self, *args):
        self.rect.size = Window.size

    def call_options(self, instance):
        conn = resolve_connectivity()

        if conn is True:
            b = access_bio(self.roster, instance.text)

            global tree, athletes_name
            tree = b[2]
            athletes_name = b[0]

            global my_options
            my_options = Options(_tree=b[2], player_name=b[0], num=b[1][3], position=b[1][4], height=b[1][0],
                                 date=b[1][1], nationality=b[1][2], filename=b[1][5])
            sm.transition = SlideTransition(direction='left')
            sm.switch_to(my_options)

        else:
            ConnWarnPopup(message=conn).open()

    @staticmethod
    def on_enter(*args):
        sm.check_in_names('roster')


class PastRoster(Roster):
    def __init__(self, _roster_, name):
        super().__init__(_roster_, name)

        self.past_roster = _roster_

    def call_options(self, instance, *args):
        conn = resolve_connectivity()

        if conn is True:
            b = access_bio(self.past_roster, instance.text)

            global tree, athletes_name
            tree = b[2]
            athletes_name = b[0]

            global past_options
            past_options = PastOptions(_tree=b[2], player_name=b[0], num=b[1][3], position=b[1][4], height=b[1][0],
                                       date=b[1][1], nationality=b[1][2], filename=b[1][5])

            sm.transition = FadeTransition(duration=.5)
            sm.switch_to(past_options)

        else:
            ConnWarnPopup(message=conn).open()

    @staticmethod
    def on_enter(*args):
        sm.check_in_names('past_roster')


class PastSeasonTeams(Roster):
    """
    Participant teams of past seasons.
    """

    def __init__(self, _roster_, name):
        super().__init__(_roster_, name)

        self.roster_of_teams = _roster_

    def call_options(self, instance, *args):
        conn = resolve_connectivity()
        global past_roster

        if conn is True:
            for name_of_team, data in self.roster_of_teams.items():

                if instance.text == name_of_team:
                    players_for_past_team = fetch_players(data[1])

                    past_roster = PastRoster(players_for_past_team, name_of_team)
                    past_roster.title.text = name_of_team + ' Roster'
                    sm.transition = FadeTransition(duration=.5)
                    sm.switch_to(past_roster)
        else:
            ConnWarnPopup(message=conn).open()

    @staticmethod
    def on_enter(*args):
        sm.check_in_names('past_season_teams')


class DraggableLogo(DragBehavior, Widget):
    """
     This is a draggable widget (Ellipse, Rectangle or Image) with potentially multiple uses. It currently makes a
     few images draggable and adds a few effects too!
    """

    offset_im = kivy.metrics.dp(35)

    def __init__(self, emblem, **kwargs):
        super().__init__(**kwargs)

        self.message_popup = MessagePopup(on_open=self.fetch_roster)

        self.logo = Image(source=emblem, allow_stretch=True, keep_ratio=False, size_hint=[None, None],
                          width=dp(50), height=dp(50), pos=self.pos)
        self.add_widget(self.logo)

        '''To set pos subtract from Window.width (and Window.height) offset_im.
        Convert width/2 (or height/2) from density-independent px to pixels.
        '''
        offset_im = self.offset_im

        self.im = Image(source='Images/rim.png', pos=(scr_w / 2 - offset_im, scr_h / 2 - offset_im),
                        size_hint=[None, None], allow_stretch=True, keep_ratio=False,
                        width='70dp', height='70dp', opacity=0)
        self.add_widget(self.im)

        self.bind(pos=self.update_logo)

        self.drag_rectangle = [self.x, self.y, factor1, factor1]
        self.drag_timeout = 10000000
        self.drag_distance = 0

        self.tooltip_up = ToolTipTextUp()
        self.tooltip_down = ToolTipTextDown()

    def update_logo(self, *args):
        self.logo.pos = self.pos

    def on_touch_down(self, touch):

        tx, ty = touch.pos
        sx, sy = self.pos

        if self.collide_point(*touch.pos) and (sx + factor1 >= tx > sx and sy + factor1 >= ty > sy):
            '''The two extra conditions must be met otherwise the opacity will be changed for all children!'''
            self.im.opacity = 1
            self.logo.opacity = .5

            '''Code to show tooltip text with chosen team's name on touch down event.'''
            teams_up = teams_codes()[0][:9]
            teams_down = teams_codes()[0][9:18]

            image_name = self.logo.source.rpartition('.')[0].split('Images/')[1]

            if image_name in teams_up:
                '''Checks to see if tooltip is already activated.'''

                if self.tooltip_up not in self.children:
                    self.tooltip_up.text = image_name
                    self.add_widget(self.tooltip_up)
                    Clock.schedule_once(self.remove_info_1, 1.5)

            elif image_name in teams_down:
                '''Checks to see if tooltip is already activated.'''

                if self.tooltip_down not in self.children:
                    self.tooltip_down.text = image_name
                    self.add_widget(self.tooltip_down)
                    Clock.schedule_once(self.remove_info_2, 1.5)

            else:
                pass

        return super().on_touch_down(touch)

    def remove_info_1(self, *args):
        self.remove_widget(self.tooltip_up)

    def remove_info_2(self, *args):
        self.remove_widget(self.tooltip_down)

    def on_touch_up(self, touch):

        self.logo.opacity = 1
        self.im.opacity = 0
        Animation.stop_all(self)

        if self.collide_point(*touch.pos):

            '''Code to get the image back to its original position.'''

            image_name = self.logo.source.partition('Images/')[-1]

            for k, v in pos_init_dict.items():
                if k == image_name:
                    anim = Animation(x=v[0], y=v[1], duration=1, t='out_elastic', opacity=1)
                    anim.start(self)

        if scr_w / 2. > self.x > scr_w / 2. - dp(35) and scr_h / 2. - dp(35) < self.y < scr_h / 2.:

            self.message_popup.message.text = 'Getting there...'
            self.message_popup.open()

        return super().on_touch_up(touch)

    def fetch_roster(self, *args):

        """Checking first if the position of the widget (image) is within the bounding circle, then..."""
        image_name = self.logo.source.partition('Images/')[-1].split('.')[0]
        codes = teams_codes()[1]

        for team, data in codes.items():
            if team == image_name:
                '''data[0] is a number from 1 - 18'''
                url = url_for_players(data[1], CURRENT_SEASON)
                global roster
                roster = fetch_players(url)
                self.call_roster(image_name)

    def call_roster(self, image_name):
        global my_roster
        my_roster = Roster(_roster_=roster, teams_name=image_name)
        my_roster.title.text = image_name + ' Roster'

        self.message_popup.dismiss()
        sm.transition = SlideTransition(direction='left')
        sm.switch_to(my_roster)


class Teams(Screen):
    """
    Teams' Screen Setup
    """

    def __init__(self):
        super().__init__()

        with self.canvas.before:
            Color(1, 1, 1, .9)
            self.rect = Rectangle(size=self.size)
        self.bind(size=self.update_rect)

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.centered_circle = Line(width=dp(3) / 2.6).circle = (
                scr_w / 2., scr_h / 2., dp(35), 0, 360, 60)

        for k, v in pos_init_dict.items():
            drag = DraggableLogo(pos=v, emblem='Images/' + k)
            self.add_widget(drag)

    def update_rect(self, *args):
        self.rect.size = Window.size

    @staticmethod
    def on_enter(*args):
        sm.check_in_names('teams')


class Standings(Screen):
    """
    Standings Screen Setup.
    """

    def __init__(self, all_current_teams_standings, info):
        super().__init__()

        _info_ = info[1].split(' ')

        with self.canvas.before:
            Color(1, 1, 1, .9)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect)

        round_info = DisplayLabel(font_size='17sp',
                                  text='[b][color=FFFFFF]' + info[0] + '[/color]' + '\n'
                                       + '[color=FFFFFF]' + _info_[1] + '[/color]'
                                       + '[i][color=FF6600]' + ' ' + _info_[2] + '[/color][/i]' + '[/b]',
                                  r=0, g=0, b=0, a=1)
        self.add_widget(round_info)

        rv_view = RVSt(all_current_teams_standings)
        self.add_widget(rv_view)

    def update_rect(self, *args):
        self.rect.size = Window.size

    @staticmethod
    def on_enter(*args):
        sm.check_in_names('standings')


class ChangeLogScreen(Screen):
    """
    Changelog Screen Setup
    """

    log_text_1 = StringProperty(
        '\n[u]' + 'ELS `Monolith` v1.4.1' + '[/u]'
        + '\n\n> Update for Season 2020 - 21'
        + '\n\n\n [u]' + 'ELS `Monolith` v1.4.0' + '[/u]'
        + '\n\n> App engine upgrade'
        + '\n\n> Code improvements'
        + '\n\n> New Graphics'
        + '\n\n> New! Past Seasons Statistics (2000 - 2019)'
        + '\n\n> Optimised for Android 10')

    def __init__(self):
        super().__init__()

        with self.canvas.before:
            Color(1, 1, 1, .9)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect)

        got_it = AnyColorButton(text='GOT IT !', r=0, g=.6, b=.6, a=1,
                                size_hint=[.8, .097], font_size='19sp',
                                pos_hint={'center_x': .5, 'center_y': .1})
        got_it.bind(on_press=self.callback_home)
        self.add_widget(got_it)

        header = Label(text='C h a n g e l o g', font_size='30sp',
                       pos_hint={'center_x': .5, 'center_y': .93},
                       color=(0, 0, 0, 1), size_hint=[1, None],
                       halign='center', valign='middle',
                       font_name='Roboto-Regular')
        bind_instance(header)
        self.add_widget(header)

        log1 = Label(text=self.log_text_1, font_size='17sp',
                     pos_hint={'center_x': .5, 'center_y': .6},
                     size_hint=[.9, None],
                     color=(0, 0, 0, 1),
                     halign='center', valign='middle',
                     font_name='Roboto-Regular',
                     markup=True)
        bind_instance(log1)
        self.add_widget(log1)

    def update_rect(self, *args):
        self.rect.size = Window.size

    @staticmethod
    def callback_home(*args):
        del sm.screens_visited[-1]
        sm.switch_to(my_home)

    @staticmethod
    def on_enter(*args):
        sm.check_in_names('change_log')


class Menu(Screen):
    """Main menu
    """

    def __init__(self):
        super().__init__()

        with self.canvas.before:
            Color(1, 1, 1, .9)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect)

        with self.canvas.before:
            Color(1, .2, 0, .9)
            self.bottom_rect = Rectangle(size=(scr_w, scr_h / 6))

        with self.canvas.before:
            Color(1, .2, 0, .9)
            self.top_rect = Rectangle(size=(scr_w, scr_h), pos=(0, scr_h - scr_h / 36))
        self.bind(size=self.update_rect)

        with self.canvas.before:
            Color(1, 1, 1, .8)
            Line(points=(scr_w / 12, scr_h / 12, scr_w / 3.5, scr_h / 12))
            Line(points=(2.5 * scr_w / 3.5, scr_h / 12, 11 * scr_w / 12, scr_h / 12))

        els = Label(text='EuroLeagueStats 2020 - 2021',
                    font_size='13sp',
                    size_hint=[.3, None],
                    pos_hint={'center_x': .5, 'center_y': .085},
                    halign='center', valign='middle',
                    color=(1, 1, 1, .8))
        els.bind(width=lambda *x: els.setter('text_size')(els, (els.width, None)),
                 texture_size=lambda *x: els.setter('height')(els, els.texture_size[1]))

        btn1 = AnyColorButton(text='Current Season', r=1, g=.2, b=0, a=.9, font_size='21sp',
                              size_hint=[.7, .097], color=(1, 1, 1, .8),
                              pos_hint={'center_x': .5, 'center_y': .75})
        btn1.bind(on_press=self.call_teams)

        btn2 = AnyColorButton(text='Standings', r=1, g=.2, b=0, a=.9, font_size='21sp',
                              size_hint=[.7, .097], color=(1, 1, 1, .8),
                              pos_hint={'center_x': .5, 'center_y': .55})
        btn2.bind(on_press=self.call_standings)

        btn3 = AnyColorButton(text='2000 - 2019', r=1, g=.2, b=0, a=.9, font_size='21sp',
                              size_hint=[.7, .097], color=(1, 1, 1, .8),
                              pos_hint={'center_x': .5, 'center_y': .35})
        btn3.bind(on_press=self.call_past_seasons)

        for btn in [btn1, btn2, btn3, els]:
            self.add_widget(btn)

    def update_rect(self, *args):
        self.rect.size = Window.size

    @staticmethod
    def call_teams(*args):
        conn = resolve_connectivity()

        if conn is True:
            global my_teams
            my_teams = Teams()

            sm.transition = SlideTransition(direction='left')
            sm.switch_to(my_teams)
        else:
            ConnWarnPopup(message=conn).open()

    @staticmethod
    def call_standings(*args):
        conn = resolve_connectivity()

        if conn is True:
            current_teams_standings = fetch_standings()[0]
            info = fetch_standings()[1]
            my_standings = Standings(all_current_teams_standings=current_teams_standings, info=info)

            sm.transition = SlideTransition(direction='left')
            sm.switch_to(my_standings)
        else:
            ConnWarnPopup(message=conn).open()

    @staticmethod
    def call_past_seasons(*args):
        conn = resolve_connectivity()

        if conn is True:
            global past_seasons
            past_seasons = PastSeasons()
            sm.switch_to(past_seasons)
        else:
            ConnWarnPopup(message=conn).open()

    @staticmethod
    def on_enter(*args):
        sm.check_in_names('menu')


class HomeScreen(Screen):
    """
    Home Screen Setup
    """

    def __init__(self):
        super().__init__()

        with self.canvas.before:
            Color(1, 1, 1, .9)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect)

        cube3d = Cube3D()
        self.add_widget(cube3d)

        btn1 = AnyColorButton(text='Statistics', r=1, g=.2, b=0, a=.9, font_size='21sp',
                              size_hint=[.7, .097], color=(1, 1, 1, .8),
                              pos_hint={'center_x': .5, 'center_y': .3})
        btn1.bind(on_press=self.call_menu)

        '''btn2 and btn3 form one widget!'''
        btn2 = AnyColorButton(text=' ', r=1, g=.2, b=0, a=.9, font_size='21sp',
                              size_hint=[.6, .087],
                              pos_hint={'center_x': .5, 'center_y': .15})
        btn2.bind(on_press=self.call_changelog)

        btn3 = AnyColorLabel(text='Changelog', r=1, g=1, b=1, a=1,
                             size_hint=[.597, .084],
                             pos_hint={'center_x': .5, 'center_y': .15})

        for w in [btn1, btn2, btn3]:
            self.add_widget(w)

    def update_rect(self, *args):
        self.rect.size = Window.size

    @staticmethod
    def call_menu(*args):
        conn = resolve_connectivity()

        if conn is True:
            global menu
            menu = Menu()

            sm.transition = FadeTransition(duration=.5)
            sm.switch_to(menu)

        else:
            ConnWarnPopup(message=conn).open()

    @staticmethod
    def call_changelog(*args):
        change_log = ChangeLogScreen()

        sm.transition = FadeTransition(duration=.5)
        sm.switch_to(change_log)

    @staticmethod
    def on_enter(*args):
        sm.check_in_names('home')


class MyScreenManager(ScreenManager):
    back = BooleanProperty(False)
    screens_visited = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.exit_popup = MessagePopup()

        '''Device's back button functionality.'''
        Window.bind(on_keyboard=self.android_back_click)

    def android_back_click(self, window, key, *largs):

        if key in [27, 1001]:

            screens_menu = (
                ('menu', my_home), ('teams', menu), ('standings', menu), ('past_seasons', menu), ('roster', my_teams),
                ('options', my_roster), ('game_stats', my_options), ('past_season_teams', past_seasons),
                ('past_roster', past_season_teams), ('past_options', past_roster))

            if self.screens_visited[-1] not in ('home', 'change_log'):

                for scr_name, instance in screens_menu:
                    if self.screens_visited[-1] == scr_name:
                        sm.switch_to(instance)
                        del self.screens_visited[-1]
                        return True

            else:

                if self.screens_visited[-1] == 'change_log':
                    sm.transition = FadeTransition(duration=.5)
                    ''' "ChangeLogScreen()" entry in :list: screens_visited is deleted, whenever the user presses
                    the OK button in ChangeLogScreen (see, :meth: callback_to_sc1d).'''
                    return True

                else:

                    self.exit_popup.message.text = 'See you later!'
                    self.exit_popup.open()
                    Clock.schedule_once(self.exit_app, 1)

                    return True

        return False

    def check_in_names(self, screen_name):
        if screen_name in self.screens_visited:
            pass
        else:
            self.screens_visited.append(screen_name)

    def exit_app(self, *args):
        self.exit_popup.dismiss()
        App.get_running_app().stop()


sm = MyScreenManager()


class EuroLeagueStatsApp(App):
    def build(self):
        global my_home
        my_home = HomeScreen()
        sm.switch_to(my_home)
        return sm

    def on_stop(self):

        """Cleaning up any residual non essential jpeg files."""

        for file_name in os.listdir(os.getcwd()):
            if file_name.endswith('.jpg') and file_name not in ('Court.jpg', 'NoImage.jpg'):
                try:
                    os.remove(file_name)
                except OSError:
                    pass


if __name__ == '__main__':
    EuroLeagueStatsApp().run()
