from interfaceScripts import interfacesp as isp, menutactic as mmm
from controlScripts import mapobjtactic
import animations
import guidestorage as gs
from interfaceScripts.menutactic import MapsInterfaceObjectTactic
import pygame as pg
from controlScripts.mapmanager import MapManager
from logging import Logging
import random


class RedactorManagerTactic(MapManager):
    def __init__(self, chief_manager, map_path: str, map_coordinates: tuple,
                 operating_mode=gs.OperatingMode.redactor_mode_global, saves=None):
        """ Инизиализация объекта класса  MapManager
        :param chief_manager: ссылка на экземпляр класса главного менеджера ChiefManager
        :param map_path: путь к файлу карты
        :param map_coordinates: координаты начала отрисовки карты
        :param operating_mode: экземпляр тип режима работы guidestorage.OperatingMode
        :param saves: объект класса SaveAndLoadObject для загрузки сохраненного проекта"""

        super(RedactorManagerTactic, self).__init__(chief_manager, map_path, map_coordinates, operating_mode, saves)
        self.additional_buttons_and_objects_create()

    def cell_menu(self):
        """ Создание кнопок меню ячейки, при выборе ячейки """
        MapsInterfaceObjectTactic(self).cell_menu_redactor_tactic()

    def mouse_click(self):
        """ Выбор ячейки при клике левой кнопкой мыши """

        tr = ''
        for sd in self.list_states:
            tr += (sd.name_state + ' ' + sd.status_states.name + '||||')

        print(tr)

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


class GameManagerTactic(MapManager):
    def __init__(self, chief_manager, map_path: str, map_coordinates: tuple,
                 operating_mode=gs.OperatingMode.redactor_mode_global, saves=None):
        """ Инизиализация объекта класса  MapManager
        :param chief_manager: ссылка на экземпляр класса главного менеджера ChiefManager
        :param map_path: путь к файлу карты
        :param map_coordinates: координаты начала отрисовки карты
        :param operating_mode: экземпляр тип режима работы guidestorage.OperatingMode
        :param saves: объект класса SaveAndLoadObject для загрузки сохраненного проекта"""

        super(GameManagerTactic, self).__init__(chief_manager, map_path, map_coordinates, operating_mode, saves)

        self.dict_list_unit_in_states = self.get_dict_list_unit_in_states()
        # Расставляем игровые объекты на карте
        if saves:
            self.adding_uploaded_game_objects(saves)

        # Очередь ходящих юнитов страны: state_making_the_move
        self.queue_of_walking_units = self.dict_list_unit_in_states.get(self.state_making_the_move.name_state).copy()
        # Инициализируем класс аниматора
        self.animations = animations.Animations(self.screen, self)
        # Количество сделанных ходов
        self.cycle = 1
        self.start_active_unit_animation()
        # Закидываем всех юнитов ходящей страны в очередь
        self.queue_of_walking_units = self.dict_list_unit_in_states.get(
            self.state_making_the_move.name_state).copy()
        # todo self.object_operating_mode.do_automatic_running(None)
        self.additional_buttons_and_objects_create()
        # Запускаем автоходы
        self.chief_manager.method_AI = lambda: self.do_automatic_running()

    def do_automatic_running(self):
        """ Сделать автоматический ход юнитом - ботом """
        unit = self.get_unit_from_queue()
        if unit:
            Logging.logging_event(f" Автоматический ход для юнита {unit.type_military_unit.name} страны  "
                                  f"{self.state_making_the_move.name_state} с ячейки {unit.cell.cell_id}.")
            # активизируем ячейку юнита
            self.CellSelected = unit.cell
            self.red_selected_cell()
            # Если есть вражеский юнит, по которому можно открыть огонь, открываем огонь и не двигаемся
            if self.cells_for_fire:
                self.do_if_cells_for_fire(random.choice(self.cells_for_fire))
            # Если нет возможности открыть огонь, двигаемся в сторону цели (врага)
            elif self.cells_for_movement:
                cell_move = self.get_object_cell_for_move(unit)
                if cell_move:
                    self.do_if_cells_for_movement(cell_move)
                else:
                    self.queue_of_walking_units.remove(unit)
        else:
            Logging.logging_event(f" Нет доступных для хода юнитов у страны  "
                                  f"{self.state_making_the_move.name_state}, переключаем на следующую")
            self.switch_motion_next_state()

    def get_object_cell_for_move(self, unit):
        """ Получаем ячейку, доступную для хода юниту
        :param unit: юнит, собравшийся совершить перемещение """

        # Ищем индекс ячейки для перемещения
        # todo Нужен метод для определения целей: уничтожение врага, защита объекта, разведка территории,
        # todo выживание(дезертирство), отступление, занятие позиций и т.д.
        # todo Пока целью юнита в тактическом режиме является уничтожение ближайшего врага
        # Ищем индекс ячейки ближайшего врага и расстояние в ячейках до него
        nearest_enemy = self.find_nearest_ind_cell_enemy_unit_and_range()
        # Если не нашли врага, извлекаем None и выходим из метода
        if not nearest_enemy:
            return None
        ind_enemy_cell = nearest_enemy[0]
        distance_to_enemy = nearest_enemy[1]

        # Юнит не способен нанести удар, совершив ход
        range_strike = unit.motion + unit.range_fire
        if range_strike <= distance_to_enemy:
            # Передвигаемся на максимально-возможную дистанцию
            count_move = unit.motion
        else:
            # Передвигаемся на минимальное расстояние, с которого можно нанести удар
            count_move = distance_to_enemy - unit.range_fire

        remaining_distance = distance_to_enemy - count_move

        # Получаем объект ячейки для передвижения
        cell_move = self.get_cell_object_for_automatic_move(unit, ind_enemy_cell, count_move, remaining_distance)

        return cell_move

    def get_unit_from_queue(self):
        """ Извлекает юнита готового к ходу из очереди, если очередь пуста - извлекает None
            Гоняем список queue_of_walking_units по кругу, удаляем из него только юнитов, не имеющих ни хода, ни огня
            как только список пройдет до конца, не найдя ни одного доступного действия - чистим список
            переключаем ход на другую страну """

        for unit in self.queue_of_walking_units.copy():
            # Удаляем из очереди уничтоженного юнита
            if unit.overall_health <= 0:
                self.queue_of_walking_units.remove(unit)

            if unit.remains_move != 0 and unit.remains_salvo != 0:
                Logging.logging_event(f" Готов ходить юнит {unit.type_military_unit.name} страны "
                                      f"{self.state_making_the_move.name_state}  с ячейки {unit.cell.cell_id}. "
                                      f"Есть ходы и залпы ")
                return unit
            elif unit.remains_move == 0 and unit.remains_salvo != 0:
                if self.get_list_ind_cells_for_fire(unit.range_fire, unit):
                    Logging.logging_event(f" Готов открыть огонь юнит {unit.type_military_unit.name} страны "
                                          f"{self.state_making_the_move.name_state}  с ячейки {unit.cell.cell_id}. "
                                          f"Нет ходов, есть залпы ")
                    return unit
            elif unit.remains_move != 0 and unit.remains_salvo == 0:
                if not self.get_list_ind_cells_for_fire(unit.range_fire, unit):
                    Logging.logging_event(f" Готов ходить юнит {unit.type_military_unit.name} страны "
                                          f"{self.state_making_the_move.name_state}  с ячейки {unit.cell.cell_id}. "
                                          f"Есть ходы, нет залпов,"
                                          f" нет врагов в зоне поражения ")
                    return unit
            elif unit.remains_move == 0 and unit.remains_salvo == 0:
                ''' Logging.logging_event(f" Удаляем из реестра юнит {unit.type_military_unit.name} страны "
                                      f"{self.state_making_the_move.name_state}  с ячейки {unit.cell.cell_id}. "
                                      f"Нет ходов и залпов ") '''
                if unit in self.queue_of_walking_units:
                    self.queue_of_walking_units.remove(unit)
        else:
            ''' Logging.logging_event(f" Чистим реестр queue_of_walking_units страны "
                                  f"{self.state_making_the_move.name_state}. Нет ни одного доступного действия"
                                  f" у оставшихся юнитов ") '''
            self.queue_of_walking_units.clear()

    def switch_motion_next_state(self):
        """ Переключение хода на следующую страну """
        # Удаляем ссылку на объект выбранной ячейки
        self.CellSelected = None
        # Чистим ячейки для движения  огня при переключении хода
        self.clear_move_list()
        self.clear_fire_list()
        # Устанавливаем индекс сходившего государства в реестре государств карты
        ind_state_making_the_move = self.list_states.index(self.state_making_the_move)
        if self.state_making_the_move in self.list_states:
            if self.dict_list_unit_in_states.get(self.state_making_the_move.name_state):

                for unit in self.dict_list_unit_in_states.get(self.state_making_the_move.name_state):
                    # Восстанавливаем у сходившей страны ходы и залпы
                    unit.remains_move = unit.move_per_turn
                    unit.remains_salvo = unit.salvo_per_turn
                    # Очищаем реестр ячеек для передвижения и огня
                    self.clear_fire_list()
                    self.clear_move_list()
            else:
                # Удаляем страну
                self.destruction_of_state_without_units(self.state_making_the_move)

        # Выключаем анимацию активности
        self.animations.stop_playing_animations_for_name(name_animation='action')

        # Установка новой ходящей страны
        if len(self.list_states) <= ind_state_making_the_move + 1:
            self.state_making_the_move = self.list_states[0]
            # Прибавляем 1 ход, когда сходили все страны из реестра стран
            self.cycle += 1
            # Обновляем текст с количеством сделанных ходов
            for obj in self.chief_manager.text_and_image_list:
                if obj.name == 'cycle_text':
                    self.chief_manager.text_and_image_list.remove(obj)
                    self.update_cycle()
        else:
            self.state_making_the_move = self.list_states[ind_state_making_the_move + 1]

        Logging.logging_event(f" Ходит страна {self.state_making_the_move.name_state}")
        # Закидываем всех юнитов в очередь скопировав список
        self.queue_of_walking_units = self.dict_list_unit_in_states.get(self.state_making_the_move.name_state).copy()

        # Выводим в логи тип юнитов и ячейку расположения
        units_info = list()
        for unit_in_queue in self.queue_of_walking_units:
            units_info.append((unit_in_queue.type_military_unit.name, f'cell_id: {unit_in_queue.cell.cell_id}',
                               f'overall_health: {unit_in_queue.overall_health}'))
        Logging.logging_event(f" Юниты страны {self.state_making_the_move.name_state} == "
                              f"{str(len(self.queue_of_walking_units))}: {units_info}")

        # Запускаем анимацию действия у юнитов новой ходящей страны, если у неё есть юниты
        if self.dict_list_unit_in_states.get(self.state_making_the_move.name_state):
            #  Запуск анимации активности у юнита, имеющего доступные ходы
            self.start_active_unit_animation()

            # Замена иконки флага около кнопки хода
            for obj in self.chief_manager.text_and_image_list:
                if obj.name == 'flag_of_state_making_move':
                    self.chief_manager.text_and_image_list.remove(obj)
                    self.update_flag()
                    break
            # Делаем автоматический ход страной - ботом
            if not self.state_making_the_move.state_player:
                self.do_automatic_running()
        # Если у новой ходящей страны нет юнитов, рекурсивно перезапускаем метод
        else:
            self.switch_motion_next_state()

    def get_dict_list_unit_in_states(self):
        """ Извлекает заготовку словаря для заполнения """
        # todo вроде как лишний метод, тоже самое сделает метод adding_uploaded_game_objects
        dict_list_unit_in_states = dict()
        for state in self.list_states:
            dict_list_unit_in_states[state.name_state] = list()

        return dict_list_unit_in_states

    def adding_uploaded_game_objects(self, saves):
        """ Добавление игровых объектов при загрузке проекта
         :param saves: объект класса SaveAndLoadObject """
        list_dict_unit = saves.get_dict_unit()
        for unit in list_dict_unit:
            cell_obj = self.dict_ind_cells.get(unit.get('cell'))

            type_unit = gs.MilitaryUnits.get_instance(unit.get('type_military_unit'))
            unit = mapobjtactic.MilitaryTacticUnit(self.screen, cell_obj, type_unit, unit)
            if cell_obj:
                cell_obj.object_cell_list.append(unit)
                # Добавляем юнита в реестр словаря dict_list_unit_in_states
                self.dict_list_unit_in_states.get(unit.state.name_state).append(unit)

    def check_of_state_without_units(self, state):
        """ Проверка потери государством последнего юнита на карте """
        if not self.dict_list_unit_in_states.get(state.name_state):
            if state == self.state_making_the_move:
                self.switch_motion_next_state()
            else:
                # Удаляем страну
                self.destruction_of_state_without_units(state)

    def destruction_of_state_without_units(self, state):
        """ Удаление государства с уничтоженными юнитами из реестра ходящих государств """

        self.list_states.remove(state)
        Logging.logging_event(f' УДАЛЯЕМ страну: {state.name_state} у которой не осталось юнитов на карте')
        self.check_the_victory()

    def check_the_victory(self):
        """ Проверка факта победы-поражения при уничтожении каждого государства """
        # todo победа пока определяется тем, что на карте остались государства одного альянса
        alliance = self.list_states[0].alliance
        for state in self.list_states:
            if state.alliance != alliance:
                # Еще есть силы вражеского альянса, игра продолжается
                return
        else:
            # остались государства одного альянса - запускаем окно победы или поражения
            # todo сделать в будущем развилку, если в битве участвовали силы игрока
            Logging.logging_event(f' В ТАКТИЧЕСКОМ СРАЖЕНИИ ПОБЕДИЛ АЛЬЯНС: {alliance.name_alliance} ')
            # Удаляем ссылку на метод AI
            self.chief_manager.method_AI = None
            # Отрисовываем окно с сообщением об победе
            mmm.MenuTacticGame(self.screen, self.chief_manager, self,
                               300, 200, 600, 400, f'Альянс {alliance.name_alliance} победил',
                               mmm.MenuTacticGame.victory_menu, type_panel='transparent panel')

    def start_active_unit_animation(self):
        """ Запуск анимации активности у юнита, имеющего доступные ходы """
        for unit in self.queue_of_walking_units:
            # Включаем анимацию юнита, имеющего ходы
            animations.Animation(self.animations, self.animations.action_set, unit.cell, 0, 7, animation_finite=False,
                                 name_animation='action')

    def get_cell_object_for_automatic_move(self, unit, ind_cell_target, count_move, remaining_distance,
                                           deep_extract_set=1):
        """ Извлекает ссылку на объект доступной для передвидения ячейки увеличивая глубину совпадения сфер,
        если совпадение в одну ячейку не дало результата
        Если нет доступной ячейки для передвижения в сторону целевой ячейки - извлекаем None
         :param unit: ссылка на объект двигающегося юнита
         :param ind_cell_target: индекс ячеки объекта, к которому осуществляется перемещение
         :param count_move: расстояние, на которое будет сделан ход
         :param remaining_distance: оставшееся расстояние до пересечения
         :param deep_extract_set: глубина пересечения сфер для извлечения списка ячеек"""

        # Ищем список индексов ячеек пересечения сфер
        ind_cell_set = self.get_set_ind_cell_for_move(unit.cell.cell_id, ind_cell_target, count_move,
                                                      remaining_distance, deep_extract_set)

        # Собираем список пересечения ячеек, доступных для передвижения и  ячеек пересечения сфер
        cell_set = list()
        for cell in self.cells_for_movement:
            if cell.cell_id in ind_cell_set:
                cell_set.append(cell)

        # Если есть доспупные ячейки для передвижения в ячеках пересечения сфер, извлекаем одну их них рандомно
        if cell_set:
            return random.choice(cell_set)

        # Если Нет доспупных ячеек для передвижения в ячеках пересечения сфер, рекурсивно перезапускаем метод,
        # пока глубина пересечения сфер не достигнет количества доступных ходов
        else:
            if unit.motion == count_move:
                if count_move != deep_extract_set + 1:
                    self.get_cell_object_for_automatic_move(unit, ind_cell_target, count_move, remaining_distance,
                                                            deep_extract_set + 1)
                else:
                    return None
            else:
                self.get_cell_object_for_automatic_move(unit, ind_cell_target, count_move + 1, remaining_distance - 1,
                                                        deep_extract_set + 1)

    def find_nearest_ind_cell_enemy_unit_and_range(self):
        """ Извлекает кортеж: индекс ближайшего вражеского юнита и количество ходов до него от выделенной ячейки """
        list_ind_enemy_cell = list()
        # Перебираем список стран, ищем вражеские
        for state in self.list_states:
            if state.alliance != self.state_making_the_move.alliance:

                # Перебираем юнитов, скидываем в список индексы ячеек, на которых они находятся
                for enemy_unit in self.dict_list_unit_in_states.get(state.name_state):
                    list_ind_enemy_cell.append(enemy_unit.cell.cell_id)

        count_move = 1
        while count_move < 200:
            list_ind_cell = self.find_adjacent_cells_new(self.CellSelected.cell_id, count_move)
            for ind_cell in list_ind_enemy_cell:
                if ind_cell in list_ind_cell:
                    return ind_cell, count_move

            count_move += 1

    def get_set_ind_cell_for_move(self, ind_cell_moved_unit, ind_cell_target, count_move, remaining_distance,
                                  deep_extract_set=1):
        """ Извлекает список индексов ячеек для совершения хода или индекс одной ячейки:
        ищет пересечения во множестве индексов ячеек перемещения от ячейки с индексом ind_cell_moved_unit на
        количество ходов count_move и множестве индексов индексов ячеек перемещения от ячейки
        с индексом ind_cell_target на количество ходов remaining_distance,
        совпадающие индексы добавляются в извлекаемый сет

         :param ind_cell_moved_unit: индекс ячейки нахождения юнита
         :param ind_cell_target: индекс ячеки объекта, к которому осуществляется перемещение
         :param count_move: расстояние, на которое будет сделан ход
         :param remaining_distance: оставшееся расстояние до пересечения
         :param deep_extract_set: глубина пересечения сфер для извлечения списка ячеек """

        ind_cell_set = list()
        # Список индексов ячеек возможного передвижения юнита
        list_ind_cell1 = self.find_adjacent_cells_new(ind_cell_moved_unit, count_move)
        # Дистанция от врага с учетом глубины пересечения
        distance_into_deep_of_intersection = remaining_distance + deep_extract_set - 1
        # Список индексов ячеек на расстояние от ячейки цели до пересечения с ячейками передвижения
        # юнита с учетом глубины
        list_ind_cell2 = self.find_adjacent_cells_new(ind_cell_target, distance_into_deep_of_intersection)
        for ind_cell in list_ind_cell1:
            if ind_cell in list_ind_cell2:
                ind_cell_set.append(ind_cell)

        return ind_cell_set

    def additional_actions_with_red_selected_cell(self):
        """ Дополнительные действия при выделении ячейки красным """

        if self.CellSelected is not None and self.CellSelected.object_cell_list:
            for obj in self.CellSelected.object_cell_list:
                if type(obj) == mapobjtactic.MilitaryTacticUnit:
                    self.highlighting_cells_for_unit(obj)

    def find_unit(self):
        """ Извлекает объект юнита с выделенной ячейки """
        unit = None
        if self.CellSelected.object_cell_list:
            for obj in self.CellSelected.object_cell_list:
                if type(obj) == mapobjtactic.MilitaryTacticUnit:
                    unit = obj
        return unit

    def do_if_cells_for_movement(self, cell):
        """ Действия, если выбрали ячейку для передвижения """

        if self.CellSelected.object_cell_list:
            for obj in self.CellSelected.object_cell_list:
                if type(obj) == mapobjtactic.MilitaryTacticUnit:
                    # Чистим ячейки для огня при выборе ячейки
                    self.clear_fire_list()
                    # Чистим ячейки для движения при выборе ячейки
                    self.clear_move_list()

                    obj.change_cell(self.CellSelected, cell)
                    Logging.logging_event(f" Переместился юнит {obj.type_military_unit.name} страны  "
                                          f"{self.state_making_the_move.name_state} с ячейки "
                                          f"{self.CellSelected.cell_id} на ячейку {cell.cell_id}")
        self.CellSelected = cell
        self.cell_menu()

    def do_if_cells_for_fire(self, cell):
        """ Действия, если выбрали ячейку для огня
        :param cell: ссылка на экземпляр класса Cell (Ячейка)"""
        if self.CellSelected.object_cell_list:
            enemy_unit = None
            if cell.object_cell_list:
                for obj in cell.object_cell_list:
                    if type(obj) == mapobjtactic.MilitaryTacticUnit:
                        enemy_unit = obj
            for obj in self.CellSelected.object_cell_list:
                if type(obj) == mapobjtactic.MilitaryTacticUnit:
                    # Открываем огонь по вражескому юниту
                    damage = obj.open_fire(enemy_unit)
                    Logging.logging_event(f" Открыл огонь юнит {obj.type_military_unit.name} страны  "
                                          f"{self.state_making_the_move.name_state} с ячейки {obj.cell.cell_id}"
                                          f" по вражескому юниту {enemy_unit.type_military_unit.name}"
                                          f" на ячейке {enemy_unit.cell.cell_id}, нанесен ущерб: {damage}, "
                                          f"оставшееся здоровье вражеского юнита {enemy_unit.overall_health}")
                    # Отображение нанесенного ущерба
                    if self.animations:
                        animations.MovingInscription(self.animations, self.screen,
                                                     80, 20, text_func=lambda: '- ' + str(damage),
                                                     color='red', font_name='Arial', font_size=10,
                                                     cell=cell)
                    # Запускаем анимацию взрыва
                    if self.animations:
                        animations.Animation(self.animations, self.animations.explosion_set, cell, 10, 10,
                                             animation_finite=True, event=lambda: self.return_fire(enemy_unit, obj))

                    if obj.remains_salvo == 0:
                        # Чистим ячейки для огня при выборе ячейки
                        self.clear_fire_list()
                    else:
                        if enemy_unit not in self.dict_list_unit_in_states.get(
                                enemy_unit.state.name_state):
                            # Если вражеский юнит уничтожен,
                            # обновляем подсветку ячеек передвижения и огня
                            self.clear_fire_list()
                            self.clear_move_list()
                            self.highlighting_cells_for_unit(obj)

                    if obj.remains_move == 0:
                        # Чистим ячейки для движения при выборе ячейки
                        self.clear_move_list()

    def return_fire(self, enemy_unit, attacker_unit):
        """ Ответный огонь атакованного юнита
        :param enemy_unit: вражеский юнит, наносящий ответный огонь
        :param attacker_unit: юнит, наносивший первоначальную атаку """
        if enemy_unit and enemy_unit in self.dict_list_unit_in_states.get(
                enemy_unit.state.name_state):
            # Ответный огонь, если вражеский юнит не уничтожен
            # Вычисляем массив индексов ячеек для огня
            list_ind_fire = self.find_adjacent_cells_new(enemy_unit.cell.cell_id, enemy_unit.range_fire)
            # Проверяем, входит ли в него атаковавший юнит
            if attacker_unit.cell.cell_id in list_ind_fire:
                # Наносим ответный удар
                damage = enemy_unit.open_fire(attacker_unit)
                Logging.logging_event(f" Открыл ОТВЕТНЫЙ огонь юнит {enemy_unit.type_military_unit.name} "
                                      f"с ячейки {enemy_unit.cell.cell_id}"
                                      f" по атаковавшему юниту {attacker_unit.type_military_unit.name}"
                                      f" на ячейке {attacker_unit.cell.cell_id}, нанесен ущерб: {damage},"
                                      f" оставшееся здоровье атаковавшего юнита {attacker_unit.overall_health}")
                # Отображение нанесенного ущерба
                if self.animations:
                    animations.MovingInscription(self.animations, self.screen,
                                                 80, 20, text_func=lambda: '- ' + str(damage),
                                                 color='red', font_name='Arial', font_size=10,
                                                 cell=attacker_unit.cell)
                # Запускаем анимацию взрыва
                if self.animations:
                    animations.Animation(self.animations, self.animations.explosion_set,
                                         attacker_unit.cell, 10, 10, animation_finite=True)

    def additional_buttons_and_objects_create(self):
        """ Другие объекты интерфейса """

        # Создание надписи о количестве ходов
        self.update_cycle()

    def update_cycle(self):
        """ Создание надписи о количестве ходов """

        cycle_text = isp.TextObject(self.screen, self.size_window[0] - 250, self.size_window[1] - 40,
                                    lambda: 'Ход ' + str(self.cycle), name='cycle_text',
                                    color='white', font_name='Arial', font_size=30)
        self.chief_manager.text_and_image_list.append(cycle_text)

    def cell_menu(self):
        """ Создание кнопок меню ячейки, при выборе ячейки """
        MapsInterfaceObjectTactic(self).cell_menu_game_tactic()

    def get_list_cells_for_move(self, move_count):
        """ Установка свойств ячеек для передвижения юнитов на количество ходов move_count
            :param move_count: дальность прередвижения в ячейках """

        list_ind_move = self.find_adjacent_cells_new(self.CellSelected.cell_id, move_count)
        list_ind_move.remove(self.CellSelected.cell_id)

        for cell_ind in list_ind_move:
            # todo пока проверяется наличие объектов в ячейке, если есть, сходить туда не даём
            cell = self.dict_ind_cells.get(cell_ind)

            if not cell.object_cell_list:
                cell.move = True
                self.cells_for_movement.append(cell)

    def get_list_ind_cells_for_move(self, move_count, unit):
        """ Установка свойств ячеек для передвижения юнитов на количество ходов move_count
            :param move_count: дальность прередвижения в ячейках
            :param unit: Юнит, для которого ищем доступные для передвижения ячейки """

        list_ind_for_move = list()
        # Ищем соседние ячейки вокруг ячейки расположения юнита
        list_ind_move = self.find_adjacent_cells_new(unit.cell.cell_id, move_count)
        list_ind_move.remove(self.CellSelected.cell_id)

        for cell_ind in list_ind_move:
            # todo пока проверяется наличие объектов в ячейке, если есть, сходить туда не даём
            if not self.dict_ind_cells.get(cell_ind).object_cell_list:
                list_ind_for_move.append(cell_ind)
        return list_ind_for_move

    def get_list_cells_for_fire(self, fire_count):
        """ Установка свойств ячеек для огня юнитов на дальность fire_count
            :param fire_count: дальность огня в ячейках """

        list_ind_fire = self.find_adjacent_cells_new(self.CellSelected.cell_id, fire_count)
        list_ind_fire.remove(self.CellSelected.cell_id)

        for cell_ind in list_ind_fire:
            cell = self.dict_ind_cells.get(cell_ind)
            if cell.object_cell_list and cell.state:
                # todo пока реализовано, что врагом считается юнит, состоящий в другом альянсе
                if cell.state and self.CellSelected.state and cell.state.alliance != self.CellSelected.state.alliance:
                    cell.fire = True
                    self.cells_for_fire.append(cell)

    def get_list_ind_cells_for_fire(self, fire_count, unit):
        """ Установка свойств ячеек для огня юнитов на дальность fire_count
            :param fire_count: дальность огня в ячейках
            :param unit: Юнит, для которого ищем доступные для открытия огня ячейки """

        list_ind_for_fire = list()
        # Ищем соседние ячейки вокруг ячейки расположения юнита
        list_ind_fire = self.find_adjacent_cells_new(unit.cell.cell_id, fire_count)
        list_ind_fire.remove(unit.cell.cell_id)

        for cell_ind in list_ind_fire:
            # todo пока реализовано, что врагом считается юнит, состоящий в другом альянсе
            cell = self.dict_ind_cells.get(cell_ind)
            if cell and cell.object_cell_list:
                enemy_unit = self.find_unit2(cell)
                if enemy_unit and enemy_unit.state.alliance != unit.state.alliance:
                    list_ind_for_fire.append(cell_ind)
        return list_ind_for_fire

    @staticmethod
    def find_unit2(cell):
        """ Извлекает объект юнита с выделенной ячейки """
        unit = None
        if cell.object_cell_list:
            for obj in cell.object_cell_list:
                if type(obj) == mapobjtactic.MilitaryTacticUnit:
                    unit = obj
        return unit

    def highlighting_cells_for_unit(self, unit: mapobjtactic.MilitaryTacticUnit):
        """ Подсветка ячеек юниту для перемещения и огня
         :param unit:  объект класса mapobjtactic.MilitaryTacticUnit (Боевой юнит)"""

        if unit.state == self.state_making_the_move:

            if unit.remains_move != 0:
                self.get_list_cells_for_move(unit.motion)

            if unit.remains_salvo != 0:
                self.get_list_cells_for_fire(unit.range_fire)

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
