import pygame as pg
from interfaceScripts import interfacesp as isp
import guidestorage as gs
from controlScripts import mapobjtactic
import statessp as ssp
from logging import Logging


class MapManager:
    """ Класс компоновки и отрисовки карты """

    def __init__(self, chief_manager, map_path: str, map_coordinates: tuple,
                 operating_mode=gs.OperatingMode.redactor_mode_global, saves=None):
        """ Инизиилизация объекта класса  MapManager
        :param chief_manager: ссылка на экземпляр класса главного менеджера ChiefManager
        :param map_path: путь к файлу карты
        :param map_coordinates: координаты начала отрисовки карты
        :param operating_mode: экземпляр тип режима работы guidestorage.OperatingMode
        :param saves: объект класса SaveAndLoadObject для загрузки сохраненного проекта"""
        # Ссылка на экземпляр окна игры
        self.screen = chief_manager.screen
        # Ссылка главного менеджера
        self.chief_manager = chief_manager
        # Размер окна игры
        self.size_window = chief_manager.size_window

        # Загрузка гексагонов
        self.hex_img = pg.image.load('Hexagon/hex1.png')
        self.hex_black_img = pg.image.load('Hexagon/hex_black.png')
        self.hex_red_img = pg.image.load('Hexagon/hex_red.png')
        self.hex_yellow_img = pg.image.load('Hexagon/hex_yellow2.png')
        self.hex_blue = pg.image.load('Hexagon/hex_blue2.png')
        self.hex_green = pg.image.load('Hexagon/hex_green.png')
        self.hex_fire = pg.image.load('Icons/aim2.png')

        # Загрузка карты
        self.map_path = map_path
        self.mapWorld_img = pg.image.load(map_path)

        # Определение размера карты
        self.sizeMap = self.mapWorld_img.get_size()

        # Список ячеек на карте
        self.Cells = list()
        self.dict_ind_cells = dict()

        # Ссылка на объект выбранной ячейки
        self.CellSelected = None

        # Список ячеек, доступных юниту для передвижения
        self.cells_for_movement = list()
        # Список ячеек, доступных юниту для нанесения удара
        self.cells_for_fire = list()

        # Режим скролла карты
        self.doMove = False

        # Координаты угла карты при загрузке
        self.map_coordinates = map_coordinates

        # Координаты угла карты в процессе игры
        self.coordinates_fix = map_coordinates

        # Создание объектов режима игры
        self.operating_mode = operating_mode

        # todo поля из удаляемых объектов
        # Список альянсов
        list_alliances = saves.get_list_alliances() if saves else list()
        self.list_alliance = list() if not list_alliances else list_alliances
        # Список стран, доступных для добавления
        list_states = saves.get_list_states() if saves else list()
        self.list_states = ssp.create_standard_list_of_states() if not list_states else list_states
        # Страна, делающая ход
        self.state_making_the_move = None if not self.list_states else self.list_states[0]

        # Расставляем и инициилизируем объекты ячеек, заполняем список ячеек на карте (Cells)
        self.arrange_and_create_cells((self.sizeMap[0], self.sizeMap[1]), saves)

        # Список отображаемых  кнопок на карте
        self.button_cell_list = list()

        # Список текстовых объектов и картинок, отображаемых на карте
        self.text_and_image_menu_list = list()

        # Список текстовых объектов и картинок, отображаемых на карте в анимациях
        self.text_and_image_animations_list = list()

        # Объект меню (если self.menu_object != None, карта блокируется)
        self.menu_object = None

        # Создание кнопки меню (возможно чего-то еще)
        self.buttons_and_objects_create()

        self.animations = None

    # Отрисовка страницы карты
    def Draw(self):
        """ Отрисовка страницы карты (Слой 1)"""
        self.screen.blit(self.mapWorld_img, self.map_coordinates)
        # Отрисовываем гексагоны
        self.draw_cells_in_visible_area()

        # Отрисовываем черный гексагон под указателем мыши (Слой 6)
        if not self.menu_object:
            self.black_cell_mouse_position()

        # Отрисовываем красный гексагон над выбранной ячейкой (Слой 7)
        self.red_selected_cell()

        # Отрисовываем Анимации
        if self.animations:
            # Чистим реестр отрисованных кадров анимации
            self.text_and_image_animations_list.clear()
            # Меняем кадры для всех анимаций
            self.animations.frame_switching_animations()
            # Отрисовываем по одному кадру для каждой анимации
            for frame in self.text_and_image_animations_list:
                frame.Draw()

        # Отрисовывем панель меню при наличии
        if self.menu_object:
            self.menu_object.Draw()

        # Отрисовываем кнопки (Верхний слой)
        for button in self.chief_manager.button_list:
            button.Draw()

        # Отрисовываем текстовые объекты и картинки (Верхний слой)
        for obj in self.chief_manager.text_and_image_list:
            obj.Draw()

    def draw_cells_in_visible_area(self):
        """ Отрисовка ячеек и расположенных на ней объектов на видимой части карты (слой 2) """
        # Отбор ячеек попадающих в видимую область
        for cell in self.Cells:
            if (((cell.centrX >= (abs(self.map_coordinates[0]) - 100)) and
                 (cell.centrX < (abs(self.map_coordinates[0]) + self.size_window[0] + 100))) and
                    ((cell.centrY >= (abs(self.map_coordinates[1]) - 100)) and
                     (cell.centrY < (abs(self.map_coordinates[1]) + self.size_window[1] + 100)))):
                # Отрисовка полупрозрачного объекта государственной принадлежности ячейки
                if cell.state and cell.state.object_color_territory:
                    self.screen.blit(cell.state.object_color_territory, (cell.centrX + self.map_coordinates[0],
                                                                         cell.centrY + self.map_coordinates[1]))
                if cell.move:
                    cell_hex = self.hex_green
                elif cell.fire:
                    cell_hex = self.hex_fire
                elif cell.Water == 1:
                    cell_hex = self.hex_blue
                elif cell.Water == 0:
                    cell_hex = self.hex_yellow_img
                else:
                    cell_hex = self.hex_img

                # Отрисовка гексагонов ячеек
                self.screen.blit(cell_hex, (cell.centrX + self.map_coordinates[0], cell.centrY +
                                            self.map_coordinates[1]))
                # todo Отладочное отображение индексов ячеек
                text_surface = pg.font.SysFont('arial', 12).render(str(cell.cell_id), False, (0, 0, 0))
                self.screen.blit(text_surface, (cell.centrX + self.map_coordinates[0] + 35, cell.centrY +
                                                self.map_coordinates[1] + 5))
                # todo Скорее всего объектом коллайдера не буду пользоваться
                Collider = pg.Rect(cell.centrX + 8, cell.centrY + 15, 90, 90)
                cell.Collider = Collider

                # Отрисовка объектов, расположенных на ячейке
                if cell.object_cell_list:
                    for obj in cell.object_cell_list:
                        obj.Draw()

    def adding_uploaded_game_objects(self, saves):
        """ Добавление игровых объектов при загрузке проекта
         :param saves: объект класса SaveAndLoadObject  (Анонимный метод) """
        pass

    def arrange_and_create_cells(self, size, saves):
        """ Извлечение списка координат  гексагонов для карты с полученными размерами
            Инициилизируем объекты ячеек, заполняем список ячеек на карте (Cells)
            :param size: кортеж длины и ширины карты в пикселях
            :param saves: объект класса SaveAndLoadObject для загрузки сохраненного проекта """

        # Новый проект
        if not saves:
            List = list()
            # Количество ячеек по длине и ширине
            countX = size[0] // 84
            countY = size[1] // 74

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
                new_cell = Cell(cell, ind, self)
                # Добавляем ячейки в список и словарь ячеек
                self.Cells.append(new_cell)
                self.dict_ind_cells[ind] = new_cell
                ind += 1
            Logging.logging_event(f'Количество ячеек на карте: {str(len(self.Cells))}')
        # Сохраненный проект
        else:
            list_dict_cells = saves.get_dict_cells()
            for cell_dict in list_dict_cells:
                coord = cell_dict.get('centrX'), cell_dict.get('centrY')
                state_cell = None
                if cell_dict.get('state') != 0:
                    for state in self.list_states:
                        if state.id_state == cell_dict.get('state'):
                            state_cell = state
                            break

                new_cell = Cell(coord, cell_dict.get('cell_id'), self, water=cell_dict.get('Water'), state=state_cell)
                self.Cells.append(new_cell)
                self.dict_ind_cells[cell_dict.get('cell_id')] = new_cell

    def mouse_click(self):
        """ Выбор ячейки при клике левой кнопкой мыши """

        mouse = pg.mouse.get_pos()

        for cell in self.Cells:
            x = cell.centrX + 44 + self.map_coordinates[0]
            y = cell.centrY + 50 + self.map_coordinates[1]
            if abs(mouse[0] - x) < 40 and abs(mouse[1] - y) < 40:
                if cell != self.CellSelected:
                    # Ячейка для передвижения
                    if cell in self.cells_for_movement:
                        self.do_if_cells_for_movement(cell)
                    # Ячейка для нанесения удара
                    elif cell in self.cells_for_fire:
                        self.do_if_cells_for_fire(cell)
                    else:
                        # Чистим ячейки для огня при выборе ячейки
                        self.clear_fire_list()
                        # Чистим ячейки для движения при выборе ячейки
                        self.clear_move_list()
                        self.CellSelected = cell
                        self.cell_menu()
                else:
                    # Чистим ячейки для огня при выборе ячейки
                    self.clear_fire_list()
                    # Чистим ячейки для движения при выборе ячейки
                    self.clear_move_list()
                    self.CellSelected = None
                    self.map_manager_button_clear()

                # Чистим ячейки для движения при выборе ячейки
                self.clear_move_list()

                return

    def move_map_with_right_down_mouse_button(self):
        """ Перетаскивание карты при перемещении мыши с зажатой правой клавишей """
        mouse = pg.mouse.get_pos()

        XX = mouse[0] - self.coordinates_fix[0]
        YY = mouse[1] - self.coordinates_fix[1]

        if 20 >= (self.map_coordinates[0] + XX) > (self.size_window[0] - self.sizeMap[0] - 20) and \
                20 >= (self.map_coordinates[1] + YY) > (self.size_window[1] - self.sizeMap[1] - 20):
            self.map_coordinates = (self.map_coordinates[0] + XX, self.map_coordinates[1] + YY)
        elif 20 >= (self.map_coordinates[0] + XX) > (self.size_window[0] - self.sizeMap[0] - 20) and \
                20 <= (self.map_coordinates[1] + YY) < (self.size_window[1] - self.sizeMap[1] - 20):
            self.map_coordinates = (self.map_coordinates[0] + XX, self.map_coordinates[1])
        elif 20 <= (self.map_coordinates[0] + XX) < (self.size_window[0] - self.sizeMap[0] - 20) and \
                20 >= (self.map_coordinates[1] + YY) > (self.size_window[1] - self.sizeMap[1] - 20):
            self.map_coordinates = (self.map_coordinates[0], self.map_coordinates[1] + YY)
        self.coordinates_fix = mouse

    def black_cell_mouse_position(self):
        """ Установка черного гексагона у ячейки, на которую наведена мышь  (6 слой) """
        mouse = pg.mouse.get_pos()

        for cell in self.Cells:
            x = cell.centrX + 44 + self.map_coordinates[0]
            y = cell.centrY + 50 + self.map_coordinates[1]
            if abs(mouse[0] - x) < 40 and abs(mouse[1] - y) < 40:
                if cell != self.CellSelected:
                    self.screen.blit(self.hex_black_img, (cell.centrX + self.map_coordinates[0],
                                                          cell.centrY + self.map_coordinates[1]))
                return

    def red_selected_cell(self):
        """ Установка красного гексагона на выбранную ячейку """
        if self.CellSelected is not None:
            x_pos = self.CellSelected.centrX + self.map_coordinates[0]
            y_pos = self.CellSelected.centrY + self.map_coordinates[1]
            self.screen.blit(self.hex_red_img, (x_pos, y_pos))

        self.additional_actions_with_red_selected_cell()

    def additional_actions_with_red_selected_cell(self):
        """ Дополнительные действия при выделении ячейки красным """
        pass

    def do_automatic_running(self):
        """ Сделать автоматический ход юнитом - ботом """
        pass

    def switch_motion_next_state(self):
        """ Переключение хода на следующую страну (Анонимный метод) """
        pass

    def find_unit(self):
        """ Извлекает объект юнита с выделенной ячейки """
        pass

    def do_if_cells_for_movement(self, cell):
        """ Действия, если выбрали ячейку для передвижения """
        pass

    def do_if_cells_for_fire(self, cell):
        """ Действия, если выбрали ячейку для огня
        :param cell: ссылка на экземпляр класса Cell (Ячейка)"""
        pass

    def clear_move_list(self):
        """ Чистим ячейки для движения при выборе ячейки """
        for cell_ in self.cells_for_movement:
            cell_.move = False
        self.cells_for_movement.clear()

    def clear_fire_list(self):
        """ Чистим ячейки для огня при выборе ячейки """
        for cell in self.cells_for_fire:
            cell.fire = False
        self.cells_for_fire.clear()

    def map_manager_button_clear(self):
        """" Удаление кнопок из массивов """

        for button in self.button_cell_list:
            if button in self.chief_manager.button_list:
                self.chief_manager.button_list.remove(button)
        for obj in self.text_and_image_menu_list:
            if obj in self.chief_manager.text_and_image_list:
                self.chief_manager.text_and_image_list.remove(obj)
        self.button_cell_list.clear()
        self.text_and_image_menu_list.clear()

    def buttons_and_objects_create(self):
        """ Кнопка меню и другие объекты интерфейса """
        button_menu = isp.Button(self.screen, 10, 10, 50, 30, 'Menu', on_click=self.chief_manager.menu_enable,
                                 font_size=16)
        self.chief_manager.button_list.append(button_menu)

        if self.operating_mode == gs.OperatingMode.game_mode_tactic:
            icon_forward = pg.image.load('Icons/forward_step.png')
            button_forward = isp.Button(self.screen, self.size_window[0] - 45, self.size_window[1] - 45, 44, 44,
                                        '', icon=icon_forward,
                                        on_click=self.switch_motion_next_state)
            self.chief_manager.button_list.append(button_forward)

            # Создание картинки с флагом страны, делающей ход
            self.update_flag()

    def additional_buttons_and_objects_create(self):
        """ Другие объекты интерфейса """
        pass

    def update_flag(self):
        """ Создание картинки с флагом страны, делающей ход """

        if self.state_making_the_move:
            icon_flag = pg.image.load(self.state_making_the_move.flag)
        else:
            icon_flag = pg.image.load('Icons/Nothing.png')
        flag_active_state = isp.ImageObject(self.screen, self.size_window[0] - 110, self.size_window[1] - 44,
                                            icon_flag, name='flag_of_state_making_move')
        self.chief_manager.text_and_image_list.append(flag_active_state)

    def cell_menu(self):
        """ Создание кнопок меню ячейки, при выборе ячейки """
        pass

    def find_adjacent_cells_new(self, ind_selected_cell, move_count):
        """ Поиск реестра индексов соседних ячеек на количество ходов move_count
            :param ind_selected_cell: индекс выбранной ячейки
            :param move_count: длина возможного хода (залпа) в ячейках """

        list_ind_move = list()

        # Ищем количество ячеек в вержнем ряду: count_one_row
        count_one_row = 0
        y_one = self.Cells[0].centrY
        for cell in self.Cells:
            if cell.centrY == y_one:
                count_one_row += 1
            else:
                break

        # Ищем номер ряда, на который кликнули
        number_row = 0
        index_first_cell = 0
        index_last_cell = 0

        while index_last_cell < ind_selected_cell:
            number_row += 1
            index_first_cell = index_last_cell + 1
            if number_row % 2 != 0:
                index_last_cell += count_one_row
            else:
                index_last_cell += count_one_row - 1

        # Добавляем ячейки выбранного ряда в массив ячеек движения
        list_ind_move.append(ind_selected_cell)
        for i in range(1, move_count + 1):
            # Добавляем ячейки слева
            if ind_selected_cell - i >= index_first_cell and 0 < ind_selected_cell - i <= len(self.Cells):
                list_ind_move.append(ind_selected_cell - i)
            # Добавляем ячейки справа
            if ind_selected_cell + i <= index_last_cell and 0 < ind_selected_cell + i <= len(self.Cells):
                list_ind_move.append(ind_selected_cell + i)

        # Присваиваем значение четности строки, в которой выбрана ячейка
        string_parity = True if number_row % 2 == 0 else False

        # Создаем переменные значений индексов первой и последней ячеек для строки ниже и выше выбранной
        ind_current_first_row = index_first_cell
        ind_current_last_row = index_last_cell
        ind_current_first_row2 = index_first_cell
        ind_current_last_row2 = index_last_cell

        # Добавляем ячейки сверху и снизу
        for n_move in range(1, move_count + 1):
            # Вычисляем первый и последний индекс строки, с которой добавляем ячейки
            string_parity = not string_parity
            if not string_parity:
                ind_current_first_row = ind_current_first_row - count_one_row
                ind_current_last_row = ind_current_last_row - count_one_row + 1
                ind_current_first_row2 = ind_current_first_row2 + count_one_row - 1
                ind_current_last_row2 = ind_current_last_row2 + count_one_row
            else:
                ind_current_first_row = ind_current_first_row - count_one_row + 1
                ind_current_last_row = ind_current_last_row - count_one_row
                ind_current_first_row2 = ind_current_first_row2 + count_one_row
                ind_current_last_row2 = ind_current_last_row2 + count_one_row - 1

            # Индекс первой ячейки верхней строки
            ind_first_cell = ind_selected_cell - count_one_row * n_move - (move_count - 1) + (n_move - 1)
            # Индекс первой ячейки нижней строки
            ind_first_cell2 = ind_selected_cell + count_one_row * n_move - move_count
            for i in range(move_count * 2 + (1 - n_move)):
                if ind_current_first_row <= ind_first_cell + i <= ind_current_last_row and \
                        0 < ind_first_cell + i <= len(self.Cells):
                    list_ind_move.append(ind_first_cell + i)
                if ind_current_first_row2 <= ind_first_cell2 + i <= ind_current_last_row2 and \
                        0 < ind_first_cell2 + i <= len(self.Cells):
                    list_ind_move.append(ind_first_cell2 + i)

        # Logging.logging_event(f"Метод find_adjacent_cells_new извлек список индексов ячеек {list_ind_move}")

        return list_ind_move

    def get_list_cells_for_move(self, move_count):
        """ Установка свойств ячеек для передвижения юнитов на количество ходов move_count
            :param move_count: дальность прередвижения в ячейках """
        pass

    def get_list_cells_for_fire(self, fire_count):
        """ Установка свойств ячеек для огня юнитов на дальность fire_count
            :param fire_count: дальность огня в ячейках """
        pass

    def highlighting_cells_for_unit(self, unit: mapobjtactic.MilitaryTacticUnit):
        """ Подсветка ячеек юниту для перемещения и огня
         :param unit:  объект класса mapobjtactic.MilitaryTacticUnit (Боевой юнит)"""
        pass

    def get_auto_water_or_land(self):
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
            len_color = len(color_list)
            percent = blue / len_color
            if percent > 0.8:
                cell.Water = 1
            elif percent < 0.2:
                cell.Water = 0
            else:
                cell.Water = 2


class Cell:
    """ Класс ячейки """

    def __init__(self, coord, cell_id, map_manager, water=0, state=None):
        """ Инициализация экземпляра объекта ячейка
         :param coord:  кортеж координат X и Y ячейки в пикселях
         :param cell_id: id ячейки
         :param map_manager: ссылка на объект класса MapManager
         :param water: код типа ячейки: Вода(1), Суша(0), Побережье(2)
         :param state: ссвлка на экземпляр класса States """

        self.cell_id = cell_id  # id ячейки
        self.centrX = coord[0]  # координата X ячейки
        self.centrY = coord[1]  # координата Y ячейки
        self.map_manager = map_manager  # ссылка на объект класса MapManager
        self.Collider = None  # удалить надо
        # todo переделать в guidestorage
        self.Water = water  # тип ячейки: Вода(1), Суша(0), Побережье(2)
        self.state = state  # ссылка на объект государства statessp.States, которому принадлежит ячейка
        self.move = False  # На ячейку могут переместиться выбранный юнит
        self.fire = False  # на ячейке расположен объект, который может атаковать выбранный юнит
        self.object_cell_list = list()  # список объектов, расположенных на ячейке
        # self.animation1 = None

    # Установка типа ячейки: Вода(1), Суша(0), Побережье(2)
    def get_water_or_land(self, type_terrain):
        """ Установка типа ячейки: Вода(1), Суша(0), Побережье(2)
        :param type_terrain: код типа ячейки: Вода(1), Суша(0), Побережье(2)"""
        if type_terrain == 1:
            self.Water = 1
        elif type_terrain == 2:
            self.Water = 2
        elif type_terrain == 0:
            self.Water = 0

    def clear_objects_from_cell(self):
        """ Очищает объекты с ячейки """

        self.object_cell_list.clear()
