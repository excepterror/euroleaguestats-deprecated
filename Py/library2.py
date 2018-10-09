from kivy.uix.label import Label
from kivy.uix.popup import Popup

from library import get_opponents_dict_on_press


def stability_check(list_of_stats):
    # PURPOSE: Pre-check to find if statistical data are available. Called by :meth: access_average_stats,
    #  access_total_stats and callback_to_sc4 in Class 'Options' - main.py.
    if list_of_stats is None:
        # m = None
        warning_popup = Popup(title="Message", title_color=[0, 0, 0, 1], title_size="17sp",
                              separator_color=[1, .4, 0, 1], title_font="Roboto-Regular",
                              background="atlas://data/images/defaulttheme/textinput",
                              size_hint=[.8, .4], auto_dismiss=True)
        message = Label(text="No data for this player yet.", font_size="16sp", color=[0, 0, 0, 1], size_hint_y=None,
                        pos_hint={"x": .5, "y": .5}, halign="center", valign="center")
        message.bind(width=lambda *x: message.setter("text_size")(message, (message.width, None)),
                     texture_size=lambda *x: message.setter("height")(message, message.texture_size[1]))
        warning_popup.add_widget(message)
        warning_popup.open()
    else:
        return list_of_stats


def access_bio(roster_n, player_name):
    # PURPOSE: Called by :cls: 'Options' - main.py
    v = get_opponents_dict_on_press(roster_n, player_name)
    # team_logo = tree.xpath("//div[@class='team-logo']/a/img/@src")
    player_info = v[0].xpath("//div[@class='summary-second']/span/text()")
    player_pos = v[0].xpath("//div[@class='summary-first']/span/span/text()")
    player_photo = v[0].xpath("//div[@class='player-img']/img/@src")
    if not player_photo:
        player_photo = ['NoImage.jpg']
    else:
        pass
    bio = player_info + player_pos + player_photo  # + team_logo
    name = v[1]
    tree = v[0]
    return [name, bio, tree]
