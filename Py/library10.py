import socket

from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.button import ButtonBehavior


def is_connected(hostname):
    # Called by :cls: 'Standings' - main.py.
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.shutdown(2)
        s.close()
        return True
    except:
        pass
    return False


class GotItButton(ButtonBehavior, Label):
    """This widget is practically an overlay to the widget below."""

    def __init__(self, **kwargs):
        super(GotItButton, self).__init__(**kwargs)
        self.font_size = "19sp"
        self.color = [1, 1, 1, 1]
        self.halign = "center"
        self.valign = "middle"

        with self.canvas.before:
            Color(0, .6, .6, 1, mode='rgba')
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=40, radius=[22, ])
        self.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
