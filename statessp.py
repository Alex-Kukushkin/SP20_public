import guidestorage as es


def create_standard_list_of_states():
    """ Создание дефолтного списка стран для нового проекта в редакторе """
    list_states = list()
    list_states.append(States('Великобритания', 'Other/Flags/England_flag.png',
                              'Other/Flags_mini/England_flag_mini.png', 'Hexagon/hex_state_pink.png',
                              status_states=es.StatusState.state_for_select))
    list_states.append(States('Германия', 'Other/Flags/Germany_flag.png', 'Other/Flags_mini/Germany_flag_mini.png',
                              'Hexagon/hex_state_black.png',
                              status_states=es.StatusState.state_for_select))
    list_states.append(States('Индия', 'Other/Flags/India_flag.png', 'Other/Flags_mini/India_flag_mini.png',
                              'Hexagon/hex_state_yellow.png',
                              status_states=es.StatusState.state_for_select))
    list_states.append(States('Испания', 'Other/Flags/Spain_flag.png', 'Other/Flags_mini/Spain_flag_mini.png',
                              'Hexagon/hex_state_orange.png',
                              status_states=es.StatusState.state_for_select))
    list_states.append(States('Италия', 'Other/Flags/Italy_flag.png', 'Other/Flags_mini/Italy_flag_mini.png',
                              'Hexagon/hex_state_green.png',
                              status_states=es.StatusState.state_for_select))
    list_states.append(States('Китай', 'Other/Flags/China_flag.png', 'Other/Flags_mini/China_flag_mini.png',
                              'Hexagon/hex_state_dark_red.png',
                              status_states=es.StatusState.state_for_select))
    list_states.append(States('Румыния', 'Other/Flags/Romania_flag.jpg', 'Other/Flags_mini/Romania_flag_mini.jpg',
                              'Hexagon/hex_state_dark_brown.png',
                              status_states=es.StatusState.state_for_select))
    list_states.append(States('СССР', 'Other/Flags/USSR_flag.png', 'Other/Flags_mini/USSR_flag_mini.png',
                              'Hexagon/hex_state_dark_red.png',
                              status_states=es.StatusState.state_for_select))
    list_states.append(States('США', 'Other/Flags/USA_flag.png', 'Other/Flags_mini/USA_flag_mini.png',
                              'Hexagon/hex_state_light_blue.png',
                              status_states=es.StatusState.state_for_select))
    list_states.append(States('Тайланд', 'Other/Flags/Thailand_flag.png', 'Other/Flags_mini/Tailand_flag_mini.png',
                              'Hexagon/hex_state_dark_green.png',
                              status_states=es.StatusState.state_for_select))
    list_states.append(States('Франция', 'Other/Flags/France_flag.png', 'Other/Flags_mini/France_flag_mini.png',
                              'Hexagon/hex_state_dark_blue.png',
                              status_states=es.StatusState.state_for_select))
    list_states.append(States('Япония', 'Other/Flags/Japan_flag.png', 'Other/Flags_mini/Japan_flag_mini.png',
                              'Hexagon/hex_state_violent.png',
                              status_states=es.StatusState.state_for_select))

    return list_states


class Alliance:
    """ Объект союза """
    # Последний id, присвоенный объекту класса
    last_id = 0
    list_alliances = list()

    def __init__(self, name_alliance: str, type_alliance=es.TypeAlliance.military_alliance, id_alliance=0):
        self.id_alliance = Alliance.last_id if id_alliance == 0 else id_alliance
        self.name_alliance = name_alliance
        self.type_alliance = type_alliance
        Alliance.last_id += 1

        Alliance.list_alliances.append(self)
        print(Alliance.list_alliances)

    @staticmethod
    def get_object_alliance_by_id(id_alliance):
        """ Получает объект альянса по id
         :param id_alliance - id альянса """

        for obj in Alliance.list_alliances:
            if obj.id_alliance == id_alliance:
                return obj


class States:
    """ Объект государства """
    # Последний id, присвоенный объекту класса
    last_id = 1
    list_states = list()
    dict_states = dict()

    def __init__(self, name_states, flag, flag_mini, color_territory, cell_territory_list=None,
                 status_states=es.StatusState.state_in_the_game, alliance=None, state_player=False, id_state=None):
        """ Объект государства """
        if not id_state:
            self.id_state = States.last_id
            States.last_id += 1
        else:
            self.id_state = id_state
            if id_state > States.last_id:
                States.last_id = id_state

        self.name_state = name_states
        self.state_player = state_player

        # Флаг государства / путь к файлу картинки
        self.flag = flag
        self.flag_mini = flag_mini

        # Подсветка территории, принадлежащей объекту государства / путь к файлу картинки
        self.color_territory = color_territory

        self.object_color_territory = None

        # Список ячеек, принадлежащих государству
        self.cell_territory_list = cell_territory_list if cell_territory_list else list()

        # Статус государства
        self.status_states = status_states

        # Ссылка на Альянс,  в который входит государство
        self.alliance = alliance

        States.list_states.append(self)
        States.dict_states[self.id_state] = self
