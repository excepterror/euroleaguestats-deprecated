"""Called by :cls: DraggableLogo in main.py"""

from kivy.metrics import dp
from kivy.core.window import Window

scr_w = Window.system_size[0]
scr_h = Window.system_size[1]

factor1 = dp(40)
offset_x = (scr_w / 2 - 2 * factor1) / 3
offset_y_1 = dp(67.5)
offset_y_2 = dp(22.5)

pos_init_dict = {'Alba Berlin.png': [offset_x, scr_h - offset_y_1],
                 'Anadolu Efes Istanbul.png': [factor1 + 2 * offset_x, scr_h - offset_y_1],
                 'AX Armani Exchange Olimpia Milan.png': [scr_w - 2 * factor1 - 2 * offset_x - dp(9),
                                                          scr_h - offset_y_1],
                 'Crvena Zvezda MTS Belgrade.png': [scr_w - offset_x - factor1 - dp(9), scr_h - offset_y_1],
                 'CSKA Moscow.png': [offset_x, scr_h - 2.5 * offset_y_1],
                 'FC Barcelona Lassa.png': [factor1 + 2 * offset_x, scr_h - 2.5 * offset_y_1],
                 'FC Bayern Munich.png': [scr_w - 2 * factor1 - 2 * offset_x - dp(9),
                                          scr_h - 2.5 * offset_y_1],
                 'Fenerbahce Beko Istanbul.png': [scr_w - offset_x - factor1 - dp(9),
                                                  scr_h - 2.5 * offset_y_1],
                 'Khimki Moscow Region.png': [offset_x, scr_h / 2 - offset_y_2],
                 'KIROLBET Baskonia Vitoria Gasteiz.png': [scr_w - offset_x - factor1 - dp(9),
                                                           scr_h / 2 - offset_y_2],
                 'LDLC ASVEL Villeurbanne.png': [offset_x, 1.5 * offset_y_1 + offset_y_2],
                 'Maccabi FOX Tel Aviv.png': [factor1 + 2 * offset_x, 1.5 * offset_y_1 + offset_y_2],
                 'Olympiacos Piraeus.png': [scr_w - 2 * factor1 - 2 * offset_x - dp(9),
                                            1.5 * offset_y_1 + offset_y_2],
                 'Panathinaikos OPAP Athens.png': [scr_w - offset_x - factor1 - dp(9),
                                                   1.5 * offset_y_1 + offset_y_2],
                 'Real Madrid.png': [offset_x, offset_y_2],
                 'Valencia Basket.png': [factor1 + 2 * offset_x, offset_y_2],
                 'Zalgiris Kaunas.png': [scr_w - 2 * factor1 - 2 * offset_x - dp(9), offset_y_2],
                 'Zenit St Petersburg.png': [scr_w - offset_x - factor1 - dp(9), offset_y_2]}


def bind_instance(instance):
    return instance.bind(width=lambda *x: instance.setter("text_size")(instance, (instance.width, None)),
                         texture_size=lambda *x: instance.setter("height")(instance, instance.texture_size[1]))
