from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.core.window import Window
from kivy.app import App
from kivy.metrics import Metrics

x = Window.system_size[0]
y = Window.system_size[1]

factor1 = Metrics.dpi * .40004
offset = (x / 2 - 2 * factor1) / 3
a = factor1 + factor1 / 2


class MyLabel(ButtonBehavior, Label):
    # Used in Class 'Options' for button customisation - main.py.
    def __init__(self, **kwargs):
        super(MyLabel, self).__init__(**kwargs)
        self.font_size = "17sp"
        self.color = [0, .6, .6, .8]
        self.halign = "center"
        self.valign = "middle"

        with self.canvas.before:
            Color(1, 1, 1, .6, mode='rgba')
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=20, radius=[5, ])
        self.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ExitPopup(Popup):
    # PURPOSE: Exit options Popup. Called by :cls: 'MyScreenManager' - main.py.
    def __init__(self, **kwargs):
        super(ExitPopup, self).__init__(**kwargs)

        layout = FloatLayout()

        self.content = layout
        self.size_hint = [.8, .4]
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.title = 'Message'
        self.background = "atlas://data/images/defaulttheme/textinput"
        self.title_size = "15sp"
        self.title_font = "Roboto-Regular"
        self.title_color = (.2, .6, .8, 1)
        self.separator_color = (.2, .6, .8, 1)  # [51 / 255, 153 / 255, 204 / 255, 1.0]
        self.auto_dismiss = False

        message = Label(text='Exit EuroLeagueStats?', font_size="15sp",
                        color=(1, .4, 0, 1),
                        size_hint=[1, .2],
                        pos_hint={'x': 0, 'y': .58},
                        halign="center",
                        valign="middle")

        message.bind(width=lambda *x: message.setter("text_size")(message, (message.width, None)),
                     texture_size=lambda *x: message.setter("height")(message, message.texture_size[1]))

        btn_exit = Button(text='Exit', size_hint=[.4, .25], pos_hint={'x': 0, 'y': .1}, font_size="14sp",
                          halign="center",
                          valign="middle",
                          background_color=(1, 0, 0, 1))

        btn_exit.bind(on_press=self.exit_app,
                      width=lambda *x: btn_exit.setter("text_size")(btn_exit, (btn_exit.width, None)))

        btn_cancel_exit = Button(on_press=self.cancel_exit, text='Cancel', size_hint=[.4, .25],
                                 pos_hint={'x': .6, 'y': .1},
                                 font_size="14sp", halign="center", valign="middle", background_color=(1, 1, 1, 1))

        btn_cancel_exit.bind(
            width=lambda *x: btn_cancel_exit.setter("text_size")(btn_cancel_exit, (btn_cancel_exit.width, None)))

        for w in [message, btn_exit, btn_cancel_exit]:
            layout.add_widget(w)

    @staticmethod
    def exit_app(*args):
        App.get_running_app().stop()
        Window.close()

    def cancel_exit(self, *args):
        self.dismiss()


class ToolTipTextUp(Label):
    # PURPOSE: Called by :meth: __init__ & on_touch_down in Class 'DraggableLogo' - main.py.
    def __init__(self, **kwargs):
        super(ToolTipTextUp, self).__init__(**kwargs)

        self.font_size = "14sp"
        self.color = (1, .4, 0, .9)
        self.width = x - 2 * offset
        self.height = '30dp'
        self.pos = (offset, y - a - .75 * a / 1.2)  # y - 2.5 * a - factor1 - (factor1 / 3)
        # self.halign = "center"
        # self.valign = "middle"

        '''self.bind(
            width=lambda *x: self.setter("text_size")(self, (self.width, None)),
            texture_size=lambda *x: self.setter("height")(self, self.texture_size[1]))'''

        with self.canvas.before:
            Color(1, 1, 1, .6, mode='rgba')
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=40, radius=[10, ])
        self.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ToolTipTextDown(Label):
    # PURPOSE: Called by :meth: __init__ & on_touch_down in Class 'DraggableLogo' - main.py.
    def __init__(self, **kwargs):
        super(ToolTipTextDown, self).__init__(**kwargs)

        self.font_size = "14sp"
        self.color = (1, .4, 0, .9)
        self.width = x - 2 * offset
        self.height = '30dp'
        self.pos = (offset, .75 * a / 3.5 + a)
        # self.halign = "center"
        # self.valign = "middle"

        '''self.bind(
            width=lambda *x: self.setter("text_size")(self, (self.width, None)),
            texture_size=lambda *x: self.setter("height")(self, self.texture_size[1]))'''

        with self.canvas.before:
            Color(1, 1, 1, .6, mode='rgba')
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=40, radius=[10, ])
        self.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MyOtherLabel(Label):
    # Used in Class 'Roster' & 'Options' - main.py.
    def __init__(self, **kwargs):
        super(MyOtherLabel, self).__init__(**kwargs)
        # self.font_size = "14sp"
        self.size_hint = [.94, .066]
        self.pos_hint = {'center_x': .5, 'y': .90}
        self.color = (1, 1, 1, 1)
        self.halign = "center"
        self.valign = "middle"
        # self.markup = True

        with self.canvas.before:
            Color(0, .6, .6, 1, mode='rgba')
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=40, radius=[17, ])
        self.bind(size=self.update_rect)

        self.bind(width=lambda *x: self.setter("text_size")(self, (self.width, None)),
                  texture_size=lambda *x: self.setter("height")(self, self.texture_size[1]))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
