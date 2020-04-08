import socket

from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.button import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout


from jnius import autoclass


def resolve_connectivity():
    available_net = check_network_availability()
    if available_net:
        available_site = is_connected('www.euroleague.net')
        if available_site:
            return True
        else:
            message = "euroleague.net could not be reached. Please, check your network connection."
            return message
    else:
        message = 'Could not detect any network. Please, connect to a network first.'
        return message


def check_network_availability():
    Context = autoclass('android.content.Context')
    NetworkCapabilities = autoclass('android.net.NetworkCapabilities')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity

    # Create an instance of :cls: ConnectivityManager
    con_mgr = activity.getSystemService(Context.CONNECTIVITY_SERVICE)
    # Return the Network object corresponding to the currently active default data network.
    network = con_mgr.getActiveNetwork()
    # Call the NetworkCapabilities java class for our current Network object.
    capabilities = con_mgr.getNetworkCapabilities(network)
    # Check if the Network object is not null and verify the type of available network.
    if capabilities is not None and (
            capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) or capabilities.hasTransport(
        NetworkCapabilities.TRANSPORT_CELLULAR)):
        return True
    else:
        return False


def is_connected(hostname):
    # Called by :cls: 'Standings' - main.py.
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 10)
        s.shutdown(2) 
        s.close()
        return True
    except OSError:
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


class ConnWarnPopup(Popup):
    def __init__(self, message, **kwargs):
        super(ConnWarnPopup, self).__init__(**kwargs)

        layout = FloatLayout()

        self.content = layout
        self.title = "Connection Error"
        self.title_size = "17sp"
        self.title_color = [.2, .6, .8, 1]
        self.title_font = "Roboto-Regular"
        self.separator_color = [.2, .6, .8, 1]
        self.size_hint = [.9, .35]
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.auto_dismiss = True

        message = Label(text=message, font_size="17sp",
                        color=(1, .4, 0, 1),
                        size_hint=[1, .2],
                        pos_hint={'center_x': .5, 'center_y': .55},
                        halign="center",
                        valign="middle")
        message.bind(width=lambda *x: message.setter("text_size")(message, (message.width, None)),
                     texture_size=lambda *x: message.setter("height")(message, message.texture_size[1]))

        for w in [message]:
            layout.add_widget(w)
