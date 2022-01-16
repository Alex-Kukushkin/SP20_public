import guidestorage as gs
import animations
from interfaceScripts.menuglobal import MapsInterfaceObjectGlobal
from controlScripts.mapmanager import MapManager


class RedactorManagerGlobal(MapManager):
    def __init__(self, chief_manager, map_path: str, map_coordinates: tuple,
                 operating_mode=gs.OperatingMode.redactor_mode_global, saves=None):
        """ Инизиализация объекта класса  MapManager
        :param chief_manager: ссылка на экземпляр класса главного менеджера ChiefManager
        :param map_path: путь к файлу карты
        :param map_coordinates: координаты начала отрисовки карты
        :param operating_mode: экземпляр тип режима работы guidestorage.OperatingMode
        :param saves: объект класса SaveAndLoadObject для загрузки сохраненного проекта"""

        super(RedactorManagerGlobal, self).__init__(chief_manager, map_path, map_coordinates, operating_mode, saves)
        self.additional_buttons_and_objects_create()

    def cell_menu(self):
        """ Создание кнопок меню ячейки, при выборе ячейки в режиме редактора глобальной карты """

        MapsInterfaceObjectGlobal(self).cell_menu_redactor_global()


class GameManagerGlobal(MapManager):
    def __init__(self, chief_manager, map_path: str, map_coordinates: tuple,
                 operating_mode=gs.OperatingMode.redactor_mode_global, saves=None):
        """ Инизиализация объекта класса  MapManager
        :param chief_manager: ссылка на экземпляр класса главного менеджера ChiefManager
        :param map_path: путь к файлу карты
        :param map_coordinates: координаты начала отрисовки карты
        :param operating_mode: экземпляр тип режима работы guidestorage.OperatingMode
        :param saves: объект класса SaveAndLoadObject для загрузки сохраненного проекта"""

        super(GameManagerGlobal, self).__init__(chief_manager, map_path, map_coordinates, operating_mode, saves)

        self.additional_buttons_and_objects_create()

        # Очередь ходящих юнитов страны: state_making_the_move
        self.queue_of_walking_units = list()
        # Инициализируем класс аниматора
        self.animations = animations.Animations(self.screen, self)
        # Количество сделанных ходов
        self.cycle = 1
        # Запускаем автоходы
        self.chief_manager.method_AI = lambda: self.do_automatic_running()

    def do_automatic_running(self):
        """ Сделать автоматический ход юнитом - ботом """
        pass

    def cell_menu(self):
        """ Создание кнопок меню ячейки, при выборе ячейки """
        pass
