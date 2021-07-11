from enum import Enum


def CreateStandardListOfStates():
    """ Создание дефолтного списка стран для нового проекта в редакторе """
    list_states = list()
    list_states.append(States('Великобритания', 'Other/Flags/England_flag.png', 'Hexagon/hex_state_pink.png',
                              status_states=StatusState.state_for_select))
    list_states.append(States('Германия', 'Other/Flags/Germany_flag.png', 'Hexagon/hex_state_black.png',
                              status_states=StatusState.state_for_select))
    list_states.append(States('Индия', 'Other/Flags/India_flag.png', 'Hexagon/hex_state_yellow.png',
                              status_states=StatusState.state_for_select))
    list_states.append(States('Испания', 'Other/Flags/Spain_flag.png', 'Hexagon/hex_state_orange.png',
                              status_states=StatusState.state_for_select))
    list_states.append(States('Италия', 'Other/Flags/Italy_flag.png', 'Hexagon/hex_state_green.png',
                              status_states=StatusState.state_for_select))
    list_states.append(States('Китай', 'Other/Flags/China_flag.png', 'Hexagon/hex_state_dark_red.png',
                              status_states=StatusState.state_for_select))
    list_states.append(States('Румыния', 'Other/Flags/Romania_flag.jpg', 'Hexagon/hex_state_dark_brown.png',
                              status_states=StatusState.state_for_select))
    list_states.append(States('СССР', 'Other/Flags/USSR_flag.png', 'Hexagon/hex_state_dark_red.png',
                              status_states=StatusState.state_for_select))
    list_states.append(States('США', 'Other/Flags/USA_flag.png', 'Hexagon/hex_state_light_blue.png',
                              status_states=StatusState.state_for_select))
    list_states.append(States('Тайланд', 'Other/Flags/Thailand_flag.png', 'Hexagon/hex_state_dark_green.png',
                              status_states=StatusState.state_for_select))
    list_states.append(States('Франция', 'Other/Flags/France_flag.png', 'Hexagon/hex_state_dark_blue.png',
                              status_states=StatusState.state_for_select))
    list_states.append(States('Япония', 'Other/Flags/Japan_flag.png', 'Hexagon/hex_state_violent.png',
                              status_states=StatusState.state_for_select))

    return list_states


class TypeAlliance:
    """ тип альянса """
    trade_alliance = 1
    military_alliance = 2


class Alliance:
    """ Объект союза """
    def __init__(self, name_alliance, type_alliance=TypeAlliance.military_alliance):
        self.id_alliance = 0
        self.name_alliance = name_alliance
        self.type_alliance = type_alliance


class StatusState(Enum):
    """ Статус государства на карте """
    state_in_the_game = 1
    state_for_select = 2
    state_loser = 3


class States:
    """ Объект государства """
    def __init__(self, name_states, flag, color_territory, cell_territory_list=None,
                 status_states=StatusState.state_in_the_game, alliance=None):
        """ Объект государства """
        self.id_state = 0
        self.name_state = name_states

        # Флаг государства / путь к файлу картинки
        self.flag = flag

        # Подсветка территории, принадлежащей объекту государства / путь к файлу картинки
        self.color_territory = color_territory

        self.object_color_territory = None

        # Список ячеек, принадлежащих государству
        self.cell_territory_list = cell_territory_list if cell_territory_list else list()

        # Статус государства
        self.status_states = status_states

        # Ссылка на Альянс,  в который входит государство
        self.alliance = alliance
