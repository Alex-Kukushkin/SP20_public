import pygame as pg
import ObjectInterfaceScript as ois
import MenuMMScript as mmm
import StatesScript as ss
from enum import Enum


class OperatingMode(Enum):
    """ Режим работы на карте """
    redactor_mode = 1
    game_mode = 2


class MapManager:
    """ Класс компоновки и отрисовки карты """
    def __init__(self, screen, chief_manager, size_window, map_path, map_coordinates,
                 operating_mode=OperatingMode.redactor_mode):
        # Ссылка на экземпляр окна игры
        self.screen = screen

        # Ссылка главного менеджера
        self.chief_manager = chief_manager

        # Размер окна игры
        self.size_window = size_window

        # Загрузка гексагонов
        self.hex_img = pg.image.load('Hexagon/hex1.png')
        self.hex_black_img = pg.image.load('Hexagon/hex_black.png')
        self.hex_red_img = pg.image.load('Hexagon/hex_red.png')
        self.hex_yellow_img = pg.image.load('Hexagon/hex_yellow2.png')
        self.hex_blue = pg.image.load('Hexagon/hex_blue2.png')

        # Загрузка карты
        self.map_path = map_path
        self.mapWorld_img = pg.image.load(map_path)

        # Определение размера карты
        self.sizeMap = self.mapWorld_img.get_size()

        # Список ячеек на карте
        self.Cells = list()

        # Ссылка на объект выбранной ячейки
        self.CellSelected = None

        # Режим скролла карты
        self.doMove = False

        # Координаты угла карты при загрузке
        self.map_coordinates = map_coordinates

        # Координаты угла карты в процессе игры
        self.coordinates_fix = map_coordinates

        # Расставляем и инициилизируем объекты ячеек, заполняем список ячеек на карте (Cells)
        self.HexagonCoord((self.sizeMap[0], self.sizeMap[1]))

        # Список отображаемых  кнопок на карте
        self.button_cell_list = list()

        # Список текстовых объектов и картинок, отображаемых на карте
        self.text_and_image_menu_list = list()

        # Объект меню (если self.menu_object != None, карта блокируется)
        self.menu_object = None

        # Создание объектов режима игры
        self.object_operating_mode = None

        self.operating_mode = operating_mode
        if operating_mode == OperatingMode.redactor_mode:
            self.object_operating_mode = RedactorManager()
        elif operating_mode == OperatingMode.game_mode:
            self.object_operating_mode = GameManager()

        # Создание кнопки меню (возможно чего-то еще)
        self.ButtonsAndObjectsCreate()

    # Отрисовка страницы карты
    def Draw(self):
        """ Отрисовка страницы карты (Слой 1)"""
        self.screen.blit(self.mapWorld_img, self.map_coordinates)
        # Отрисовываем гексагоны
        self.HexagonCreate()

        # Отрисовываем черный гексагон под указателем мыши (Слой 6)
        if not self.menu_object:
            self.MousePos()

        # Отрисовываем красный гексагон над выбранной ячейкой (Слой 7)
        self.RedSelectedCell()

        # Отрисовывем панель меню при наличии
        if self.menu_object:
            self.menu_object.Draw()

        # Отрисовываем кнопки (Верхний слой)
        for button in self.chief_manager.button_list:
            button.Draw()

        # Отрисовываем текстовые объекты и картинки (Верхний слой)
        for obj in self.chief_manager.text_and_image_list:
            obj.Draw()

    # Извлечение списка координат гексагонов для карты с полученными размерами
    # Инициилизируем объекты ячеек, заполняем список ячеек на карте (Cells)
    def HexagonCoord(self, Size):
        """ Извлечение списка координат  гексагонов для карты с полученными размерами
            Инициилизируем объекты ячеек, заполняем список ячеек на карте (Cells)  """
        print('Определение координат гексагонов')
        List = list()

        # Количество ячеек по длине и ширине
        countX = Size[0] // 84
        countY = Size[1] // 74

        yy = 0
        for i in range(countY):
            if i % 2 == 0:
                countXX = countX
                xx = 0
            else:
                countXX = countX - 1
                xx = 43

            for j in range(countXX):
                xxx = xx + j * 85
                List.append((xxx, yy))
            yy += 75

        # Инициилизация объектов ячеек
        ind = 1
        for cell in List:
            self.Cells.append(Cell(cell, ind, self))
            ind += 1
        print('Количество ячеек на карте:', len(self.Cells))

    # Выбор ячейки при клике левой кнопкой мыши
    def MouseClick(self):
        """ Выбор ячейки при клике левой кнопкой мыши """
        mouse = pg.mouse.get_pos()

        for cell in self.Cells:
            x = cell.centrX + 44 + self.map_coordinates[0]
            y = cell.centrY + 50 + + self.map_coordinates[1]
            if abs(mouse[0] - x) < 40 and abs(mouse[1] - y) < 40:
                if cell != self.CellSelected:
                    self.CellSelected = cell
                    self.CellMenu()
                else:
                    self.CellSelected = None
                    self.MapManagerButtonClear()

                print('Центр ячейки:', cell.centrX, cell.centrY)
                return

    # Удаление кнопок из массивов
    def MapManagerButtonClear(self):
        """" Удаление кнопок из массивов """
        for button in self.button_cell_list:
            if button in self.chief_manager.button_list:
                self.chief_manager.button_list.remove(button)
        for obj in self.text_and_image_menu_list:
            if obj in self.chief_manager.text_and_image_list:
                self.chief_manager.text_and_image_list.remove(obj)
        self.button_cell_list.clear()
        self.text_and_image_menu_list.clear()

    # Перетаскивание карты при перемещении мыши с зажатой правой клавишей
    def MouseRightDown(self):
        """ Перетаскивание карты при перемещении мыши с зажатой правой клавишей """
        mouse = pg.mouse.get_pos()

        XX = mouse[0] - self.coordinates_fix[0]
        YY = mouse[1] - self.coordinates_fix[1]

        if(((self.map_coordinates[0] + XX) <= 0 and (self.map_coordinates[1] + YY) <= 0) and
                (self.map_coordinates[0] + XX) > (self.size_window[0] - self.sizeMap[0]) and
                (self.map_coordinates[1] + YY) > (self.size_window[1] - self.sizeMap[1])):
            self.map_coordinates = (self.map_coordinates[0] + XX, self.map_coordinates[1] + YY)
            self.coordinates_fix = mouse

    # Расстановка гексагонов(слой 2)
    def HexagonCreate(self):
        """ # Расстановка гексагонов по карте(слой 2) """
        for cell in self.Cells:
            if (((cell.centrX >= (abs(self.map_coordinates[0]) - 100)) and
                 (cell.centrX < (abs(self.map_coordinates[0]) + self.size_window[0] + 100))) and
                    ((cell.centrY >= (abs(self.map_coordinates[1]) - 100)) and
                     (cell.centrY < (abs(self.map_coordinates[1]) + self.size_window[1] + 100)))):
                if cell.state and cell.state.object_color_territory:
                    self.screen.blit(cell.state.object_color_territory, (cell.centrX + self.map_coordinates[0],
                                                                         cell.centrY + self.map_coordinates[1]))

                if cell.Water == 1:
                    cell_hex = self.hex_blue
                elif cell.Water == 0:
                    cell_hex = self.hex_yellow_img
                else:
                    cell_hex = self.hex_img

                self.screen.blit(cell_hex, (cell.centrX + self.map_coordinates[0], cell.centrY +
                                            self.map_coordinates[1]))

                Collider = pg.Rect(cell.centrX + 8, cell.centrY + 15, 90, 90)
                cell.Collider = Collider
                if cell.object_cell_list:
                    for obj in cell.object_cell_list:
                        obj.Draw()

    # Установка черного гексагона у ячейки, на которую наведена мышь (6 слой)
    def MousePos(self):
        """ Установка черного гексагона у ячейки, на которую наведена мышь """
        mouse = pg.mouse.get_pos()

        for cell in self.Cells:
            x = cell.centrX + 44 + self.map_coordinates[0]
            y = cell.centrY + 50 + self.map_coordinates[1]
            if abs(mouse[0] - x) < 40 and abs(mouse[1] - y) < 40:
                if cell != self.CellSelected:
                    self.screen.blit(self.hex_black_img, (cell.centrX + self.map_coordinates[0],
                                                          cell.centrY + self.map_coordinates[1]))
                return

    # Установка красного гексагона при клике левой кнопкой мыши (7 слой)
    def RedSelectedCell(self):
        """ Установка красного гексагона на выбранную ячейку """
        if self.CellSelected is not None:
            x_pos = self.CellSelected.centrX + self.map_coordinates[0]
            y_pos = self.CellSelected.centrY + self.map_coordinates[1]
            self.screen.blit(self.hex_red_img, (x_pos, y_pos))

    def ButtonsAndObjectsCreate(self):
        """ Кнопка меню и другие объекты интерфейса """
        button_menu = ois.Button(self.screen, 10, 10, 50, 30, 'Menu', on_click=self.chief_manager.MenuEnable,
                                 font_size=16)
        self.chief_manager.button_list.append(button_menu)

    # Создание кнопок меню ячейки
    def CellMenu(self):
        """ Создание кнопок меню ячейки, при выборе ячейки """
        # Загрузка иконок
        icon_water_or_land_img = pg.image.load('Icons/icon_WaterOrLand.jpg')
        icon_resurses_img = pg.image.load('Icons/icon_Resurses.jpg')
        icon_city_img = pg.image.load('Icons/icon_City.jpg')
        icon_enterprises_img = pg.image.load('Icons/icon_enterprises.jpg')
        icon_road_img = pg.image.load('Icons/icon_Road.jpg')
        icon_fort_img = pg.image.load('Icons/icon_Fort.jpg')
        icon_army_img = pg.image.load('Icons/icon_Army.jpg')
        icon_states_img = pg.image.load('Icons/icon_States.jpg')

        Y = self.size_window[1] - 100
        X = self.size_window[0]/2
        coord_buttons = [X - 22, X + 62, X - 106, X + 146, X - 190, X + 230, X - 277, X + 314]

        button_water_or_land = ois.Button(self.screen, coord_buttons[0], Y, 44, 44,
                                          '', icon=icon_water_or_land_img,
                                          on_click=lambda: mmm.MenuMMRedactor(
                                          self.screen, self, 300, 200, 600, 400, 'Ячейка',
                                          mmm.MenuMMRedactor.MenuWaterOrLand, type_panel='transparent panel'))
        self.chief_manager.button_list.append(button_water_or_land)
        self.button_cell_list.append(button_water_or_land)

        button_resurses = ois.Button(self.screen, coord_buttons[1], Y, 44,
                                     44, '', icon=icon_resurses_img, on_click=lambda: mmm.MenuMMRedactor(
                                     self.screen, self, 300, 200, 600,  400, 'Месторождение',
                                     mmm.MenuMMRedactor.ResursesRedactorMenu, type_panel='transparent panel'))
        self.chief_manager.button_list.append(button_resurses)
        self.button_cell_list.append(button_resurses)

        button_city = ois.Button(self.screen, coord_buttons[2], Y, 44,
                                 44, '', icon=icon_city_img,
                                 on_click=lambda: mmm.MenuMMRedactorWithTabs(
                                 self.screen, self, 150, 100, 900,  600, 'Город',
                                 mmm.MenuMMRedactorWithTabs.CityRedactorMenu,
                                     mmm.MenuMMRedactorWithTabs.ButtonTabsCity))
        self.chief_manager.button_list.append(button_city)
        self.button_cell_list.append(button_city)

        button_enterprises = ois.Button(self.screen, coord_buttons[3], Y, 44,
                                        44, '', icon=icon_enterprises_img, on_click=lambda: mmm.MenuMMRedactor(
                                        self.screen, self, 300, 200, 600,  400, 'Добывающее предприятие',
                                        mmm.MenuMMRedactor.MiningCompanyRedactorMenu, type_panel='transparent panel'))
        self.chief_manager.button_list.append(button_enterprises)
        self.button_cell_list.append(button_enterprises)

        button_road = ois.Button(self.screen, coord_buttons[4], Y, 44,
                                 44, '', icon=icon_road_img, on_click=lambda: mmm.MenuMMRedactor(
                                 self.screen, self, 300, 200, 600,  400, 'Дороги',
                                 mmm.MenuMMRedactor.RoadRedactorMenu, type_panel='transparent panel'))
        self.chief_manager.button_list.append(button_road)
        self.button_cell_list.append(button_road)

        button_fort = ois.Button(self.screen, coord_buttons[5], Y, 44,
                                 44, '', icon=icon_fort_img, on_click=lambda: mmm.MenuMMRedactor(
                                 self.screen, self, 300, 200, 600,  400, 'Оборонительные сооружения',
                                 mmm.MenuMMRedactor.FortificationRedactorMenu, type_panel='transparent panel'))
        self.chief_manager.button_list.append(button_fort)
        self.button_cell_list.append(button_fort)

        button_army = ois.Button(self.screen, coord_buttons[6], Y, 44,
                                 44, '', icon=icon_army_img, on_click=self.chief_manager.MenuEnable)
        self.chief_manager.button_list.append(button_army)
        self.button_cell_list.append(button_army)

        button_states = ois.Button(self.screen, coord_buttons[7], Y, 44, 44, '', icon=icon_states_img,
                                   on_click=lambda: mmm.MenuMMRedactor(
                                   self.screen, self, 150, 100, 900,  600, 'Государства',
                                   mmm.MenuMMRedactor.StatesRedactorMenu, type_panel='transparent panel', size_panel=3))
        self.chief_manager.button_list.append(button_states)
        self.button_cell_list.append(button_states)

    # Автоматическая установка типа ячейки: Вода(1), Суша(0), Побережье(2) по доле синих пикселей
    def GetAutoWaterOrLand(self):
        """ Автоматическая установка типа ячейки: Вода(1), Суша(0), Побережье(2) по доле синих пикселей  """
        for cell in self.Cells:
            color_list = list()
            for xx in range(cell.centrX + 1, cell.centrX + 85):
                for yy in range(cell.centrY + 1, cell.centrY + 98):
                    if xx < self.sizeMap[0] and yy < self.sizeMap[1]:
                        color_list.append(self.mapWorld_img.get_at((xx, yy)))

            blue = 0
            for col in color_list:
                if col[2] >= 200:
                    blue += 1
            print('44')
            len_color = len(color_list)
            percent = blue/len_color
            if percent > 0.8:
                cell.Water = 1
            elif percent < 0.2:
                cell.Water = 0
            else:
                cell.Water = 2


class Cell:
    """ Класс содержимого ячейки """
    def __init__(self, coord, cell_id, map_manager, state=None):
        self.cell_id = cell_id
        self.centrX = coord[0]
        self.centrY = coord[1]
        self.map_manager = map_manager
        self.Collider = None
        self.Water = 1
        self.state = state
        self.object_cell_list = list()

    # Установка типа ячейки: Вода(1), Суша(0), Побережье(2)
    def GetWaterOrLand(self, type_terrain):
        """ Установка типа ячейки: Вода(1), Суша(0), Побережье(2) """
        if type_terrain == 1:
            self.Water = 1
        elif type_terrain == 2:
            self.Water = 2
        elif type_terrain == 0:
            self.Water = 0

    def ClearObjects(self):
        """ Очищает объекты с ячейки """
        self.object_cell_list.clear()


class BaseManager:
    """ Суперкласс для менеджера """
    def __init__(self, list_alliance=None, list_states=None):
        # Список альянсов
        self.list_alliance = list() if not  list_alliance else list_alliance

        # Список стран
        self.list_states = list() if not list_states else list_states


class GameManager(BaseManager):
    """ Класс управляющий игрой """
    def __init__(self, list_alliance=None, list_states=None):
        super(GameManager, self).__init__(list_alliance, list_states)


class RedactorManager(BaseManager):
    """ Класс, управляющий режимом редактора """
    def __init__(self, list_alliance=None, list_states=None):
        super(RedactorManager, self).__init__(list_alliance, list_states)

        # Список стран, доступных для добавления
        self.list_states = ss.CreateStandardListOfStates() if not list_states else list_states





