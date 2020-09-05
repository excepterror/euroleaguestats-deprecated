from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout


class ConnWarnPopup(Popup):

    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        self.content = layout
        self.title = 'Connection Error'
        self.title_size = '17sp'
        self.title_color = [.2, .6, .8, 1]
        self.title_font = 'Roboto-Regular'
        self.separator_color = [.2, .6, .8, 1]
        self.size_hint = [.9, .35]
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.auto_dismiss = True

        message = Label(text=message, font_size='17sp',
                        color=(1, .4, 0, 1),
                        size_hint=[1, .2],
                        pos_hint={'center_x': .5, 'center_y': .55},
                        halign='center',
                        valign='middle')
        message.bind(width=lambda *x: message.setter('text_size')(message, (message.width, None)),
                     texture_size=lambda *x: message.setter('height')(message, message.texture_size[1]))

        for w in [message]:
            layout.add_widget(w)


class MessagePopup(Popup):
    """PURPOSE: Exit options Popup. Called by :cls: 'MyScreenManager' - main.py.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        self.content = layout
        self.size_hint = [.9, .35]
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.title = 'Message'
        self.title_size = '17sp'
        self.title_font = 'Roboto-Regular'
        self.title_color = (.2, .6, .8, 1)
        self.separator_color = (.2, .6, .8, 1)
        self.auto_dismiss = False

        self.message = Label(text='', font_size='17sp',
                             color=(1, .4, 0, 1),
                             size_hint=[1, .2],
                             pos_hint={'center_x': .5, 'center_y': .55},
                             halign='center',
                             valign='middle')

        self.message.bind(width=lambda *x: self.message.setter('text_size')(self.message, (self.message.width, None)),
                          texture_size=lambda *x: self.message.setter('height')(self.message,
                                                                                self.message.texture_size[1]))

        for w in [self.message]:
            layout.add_widget(w)
