import pygame as pg
from interfaceScripts import interfacesp as isp
from controlScripts import mapobject, mapobjtactic
import statessp
from interfaceScripts import interfacesp
import guidestorage


class MapsInterfaceObjectTactic:
    def __init__(self, map_manager):
        self.map_manager = map_manager

    def cell_menu_redactor_tactic(self):
        """ Создание кнопок меню ячейки, при выборе ячейки в режиме редактора тактической карты """
        # Загрузка иконок\
        Y = self.map_manager.size_window[1] - 100
        X = self.map_manager.size_window[0] / 2
        coord_buttons = [X - 22, X + 62, X - 106, X + 146, X - 190, X + 230, X - 277, X + 314]

        icon_unit = pg.image.load('Icons/icon_Army.jpg')
        icon_states_img = pg.image.load('Icons/icon_States.jpg')
        icon_fort_img = pg.image.load('Icons/icon_Fort.jpg')
        icon_water_or_land_img = pg.image.load('Icons/icon_WaterOrLand.jpg')

        button_unit = isp.Button(self.map_manager.screen, coord_buttons[0], Y, 44, 44, '', icon=icon_unit,
                                 on_click=lambda: MenuTacticRedactor(
                                     self.map_manager.screen, self.map_manager.chief_manager, self.map_manager,
                                     150, 100, 900, 600, 'Подразделения',
                                     MenuTacticRedactor.unit_add_menu, type_panel='transparent panel',
                                     size_panel=3))
        self.map_manager.chief_manager.button_list.append(button_unit)
        self.map_manager.button_cell_list.append(button_unit)

        button_states = isp.Button(self.map_manager.screen, coord_buttons[1], Y, 44, 44, '', icon=icon_states_img,
                                   on_click=lambda: MenuTacticRedactor(
                                       self.map_manager.screen, self.map_manager.chief_manager, self.map_manager,
                                       150, 100, 900, 600, 'Государства',
                                       MenuTacticRedactor.states_redactor_menu, type_panel='transparent panel',
                                       size_panel=3))
        self.map_manager.chief_manager.button_list.append(button_states)
        self.map_manager.button_cell_list.append(button_states)

        button_fort = isp.Button(self.map_manager.screen, coord_buttons[2], Y, 44,
                                 44, '', icon=icon_fort_img, on_click=lambda: MenuTacticGame(
                self.map_manager.screen, self.map_manager.chief_manager, self.map_manager, 300, 200, 600, 400,
                'Оборонительные сооружения',
                MenuTacticRedactor.fortification_redactor_menu, type_panel='transparent panel'))
        self.map_manager.chief_manager.button_list.append(button_fort)
        self.map_manager.button_cell_list.append(button_fort)

        button_water_or_land = isp.Button(self.map_manager.screen, coord_buttons[3], Y, 44, 44,
                                          '', icon=icon_water_or_land_img,
                                          on_click=lambda: MenuTacticRedactor(
                                              self.map_manager.screen, self.map_manager.chief_manager,
                                              self.map_manager, 300, 200, 600, 400, 'Ячейка',
                                              MenuTacticRedactor.menu_water_or_land, type_panel='transparent panel'))
        self.map_manager.chief_manager.button_list.append(button_water_or_land)
        self.map_manager.button_cell_list.append(button_water_or_land)

    def cell_menu_game_tactic(self):
        """ Создание кнопок меню ячейки, при выборе ячейки в режиме игры на тактической карты """
        # Загрузка иконок\
        Y = self.map_manager.size_window[1] - 100
        X = self.map_manager.size_window[0] / 2
        coord_buttons = [X - 22, X + 62, X - 106, X + 146, X - 190, X + 230, X - 277, X + 314]

        icon_info_img = pg.image.load('Icons/info.png')
        icon_shield_img = pg.image.load('Icons/shield.png')
        icon_start_img = pg.image.load('Icons/start.jpg')
        icon_shovel_img = pg.image.load('Icons/shovel.jpg')

        button_unit = isp.Button(self.map_manager.screen, coord_buttons[0], Y, 44, 44, '', icon=icon_info_img,
                                 on_click=lambda: MenuTacticRedactor(
                                     self.map_manager.screen, self.map_manager.chief_manager, self.map_manager,
                                     150, 100, 900, 600, 'Подразделения',
                                     MenuTacticRedactor.unit_add_menu, type_panel='transparent panel',
                                     size_panel=3))
        self.map_manager.chief_manager.button_list.append(button_unit)
        self.map_manager.button_cell_list.append(button_unit)

        button_states = isp.Button(self.map_manager.screen, coord_buttons[1], Y, 44, 44, '', icon=icon_shield_img,
                                   on_click=lambda: MenuTacticRedactor(
                                       self.map_manager.screen, self.map_manager.chief_manager, self.map_manager,
                                       150, 100, 900, 600, 'Государства',
                                       MenuTacticRedactor.states_redactor_menu, type_panel='transparent panel',
                                       size_panel=3))
        self.map_manager.chief_manager.button_list.append(button_states)
        self.map_manager.button_cell_list.append(button_states)

        button_fort = isp.Button(self.map_manager.screen, coord_buttons[2], Y, 44,
                                 44, '', icon=icon_start_img, on_click=lambda: MenuTacticRedactor(
                self.map_manager.screen, self.map_manager.chief_manager, self.map_manager, 300, 200, 600, 400,
                'Оборонительные сооружения',
                MenuTacticRedactor.fortification_redactor_menu, type_panel='transparent panel'))
        self.map_manager.chief_manager.button_list.append(button_fort)
        self.map_manager.button_cell_list.append(button_fort)

        button_water_or_land = isp.Button(self.map_manager.screen, coord_buttons[3], Y, 44, 44,
                                          '', icon=icon_shovel_img,
                                          on_click=lambda: MenuTacticRedactor(
                                              self.map_manager.screen, self.map_manager.chief_manager, self.map_manager,
                                              300, 200, 600, 400, 'Ячейка',
                                              MenuTacticRedactor.menu_water_or_land, type_panel='transparent panel'))
        self.map_manager.chief_manager.button_list.append(button_water_or_land)
        self.map_manager.button_cell_list.append(button_water_or_land)


class MenuTacticGame(isp.MenuMapManager):
    """ Окна меню игры без вклдадок """
    def __init__(self, screen, chief_manager, map_manager, x, y, w, h, name, func, type_panel='fill_color',
                 size_panel=1, count_page=0, up_pos=0, scroll=False, length_registry=0):
        super().__init__(screen, chief_manager, map_manager, x, y, w, h, name, func, type_panel=type_panel,
                         count_page=count_page, size_panel=size_panel,
                         up_pos=up_pos, scroll=scroll, length_registry=length_registry)
        self.name = 'Меню игры'

    def victory_menu(self):
        """ Отображение кнопок и элементов меню победы """

        image_victory = isp.ImageObject(self.screen, 315, 270, pg.image.load('Other/victory.png'))
        self.map_manager.text_and_image_menu_list.append(image_victory)
        self.map_manager.chief_manager.text_and_image_list.append(image_victory)


class MenuTacticRedactor(interfacesp.MenuMapManager):
    """ Окна меню редактора карты без вкладок """
    def __init__(self, screen, chief_manager, map_manager, x, y, w, h, name, func, type_panel='fill_color',
                 size_panel=1, count_page=0, up_pos=0, scroll=False, length_registry=0):
        super().__init__(screen, chief_manager, map_manager, x, y, w, h, name, func, type_panel=type_panel,
                         count_page=count_page, size_panel=size_panel,
                         up_pos=up_pos, scroll=scroll, length_registry=length_registry)
        self.name = 'Меню редактора карты'

    def menu_water_or_land(self):
        """ Кнопки меню установки типа ячейки: Вода(1), Суша(0), Побережье(2) """

        # Устанавливаем воду
        button_water = isp.Button(self.screen, self.menu_panel.bounds.x + 20,
                                  self.menu_panel.bounds.y + 50, 150, 50, 'Вода',
                                  on_click=lambda: self.map_manager.CellSelected.get_water_or_land(1))
        self.map_manager.button_cell_list.append(button_water)
        self.map_manager.chief_manager.button_list.append(button_water)

        # Устанавливаем сушу
        button_field = isp.Button(self.screen, self.menu_panel.bounds.x + 190,
                                  self.menu_panel.bounds.y + 50, 150, 50, 'Суша',
                                  on_click=lambda: self.map_manager.CellSelected.get_water_or_land(0))
        self.map_manager.button_cell_list.append(button_field)
        self.map_manager.chief_manager.button_list.append(button_field)

        # Устанавливаем побережье
        button_coast = isp.Button(self.screen, self.menu_panel.bounds.x + 360,
                                  self.menu_panel.bounds.y + 50, 150, 50, 'Побережье',
                                  on_click=lambda: self.map_manager.CellSelected.get_water_or_land(2))
        self.map_manager.button_cell_list.append(button_coast)
        self.map_manager.chief_manager.button_list.append(button_coast)

        # Запускаем автоматическое определение принадлежности участков
        auto_water_or_land = isp.Button(self.screen, self.menu_panel.bounds.x + 20,
                                        self.menu_panel.bounds.y + 120, 200, 50, 'Автоопределение',
                                        on_click=self.map_manager.get_auto_water_or_land)
        self.map_manager.button_cell_list.append(auto_water_or_land)
        self.map_manager.chief_manager.button_list.append(auto_water_or_land)

        # Очищаем ячейку от всех объектов
        auto_water_or_land = isp.Button(self.screen, self.menu_panel.bounds.x + 250,
                                        self.menu_panel.bounds.y + 120, 200, 50, 'Удалить объекты',
                                        on_click=self.map_manager.CellSelected.clear_objects_from_cell)
        self.map_manager.button_cell_list.append(auto_water_or_land)
        self.map_manager.chief_manager.button_list.append(auto_water_or_land)

        description_states = isp.TextObject(self.screen, self.menu_panel.bounds.x + 50,
                                            self.menu_panel.bounds.y + 190,
                                            lambda: 'Установка принадлежности ячейки государствам:',
                                            color='white', font_name='Arial', font_size=20)
        self.map_manager.text_and_image_menu_list.append(description_states)
        self.map_manager.chief_manager.text_and_image_list.append(description_states)
        ind = 0
        x = 50
        y = 240
        for state in self.map_manager.list_states:
            if state.status_states == guidestorage.StatusState.state_for_game:
                self.button_state_for_select(state, x, y)
                x += 70
                ind += 1
                if ind == 7:
                    x = 50
                    y = 300

        # Удаляем ссылку на государство, делая ячейку ничейной
        none_button = interfacesp.Button(self.screen, self.menu_panel.bounds.x + x, self.menu_panel.bounds.y + y,
                                         64, 44, 'None', button_color=(112, 128, 144),
                                         on_click=self.set_none_state)
        self.map_manager.button_cell_list.append(none_button)
        self.map_manager.chief_manager.button_list.append(none_button)

    def button_state_for_select(self, state: statessp.States, x, y):
        """ Кнопка - флаг для установки принадлежности ячейки государству
         :param state: ссылка на экземпляр объекта Государство
         :param x: координата x кнопки
         :param y: координата y кнопки """

        button_state_for_select = interfacesp.Button(self.screen, self.menu_panel.bounds.x + x,
                                                     self.menu_panel.bounds.y + y,
                                                     64, 44, '', icon=pg.image.load(state.flag),
                                                     on_click=lambda: self.set_state_for_cell(state))
        self.map_manager.button_cell_list.append(button_state_for_select)
        self.map_manager.chief_manager.button_list.append(button_state_for_select)

    def set_state_for_cell(self, state):
        """ Устанавливает у ячейки принадлежность государству
         :param state: ссылка на экземпляр объекта Государство """

        print('set_state_for_cell: ', state.name_state)
        self.map_manager.CellSelected.state = state
        state.cell_territory_list.append(self.map_manager.CellSelected)

        if self.map_manager.operating_mode == guidestorage.OperatingMode.redactor_mode_tactic:
            unit_was = False
            for unit in self.map_manager.CellSelected.object_cell_list:
                if type(unit) == mapobjtactic.MilitaryTacticUnit:
                    unit.state = state
                    unit.flag_unit = interfacesp.ImageMapObject(self.screen, 86 / 2 + 22, 100 / 2 - 20,
                                                                unit.get_icon_mini_flag(),
                                                                cell=self.map_manager.CellSelected)
                    unit_was = True
                    break
            if not unit_was:
                if self.map_manager.CellSelected.state:
                    self.map_manager.CellSelected.state.cell_territory_list.remove(self.map_manager.CellSelected)
                    self.map_manager.CellSelected.state = None

    def set_none_state(self):
        """ Убирает у ячейки (юнита) принадлежность к государству """

        print('set_none_state ', self.map_manager.list_states)
        for st in self.map_manager.list_states:
            pass
        if self.map_manager.CellSelected.state:
            self.map_manager.CellSelected.state.cell_territory_list.remove(self.map_manager.CellSelected)
            self.map_manager.CellSelected.state = None
            if self.map_manager.operating_mode == guidestorage.OperatingMode.redactor_mode_tactic:
                for unit in self.map_manager.CellSelected.object_cell_list:
                    if type(unit) == mapobjtactic.MilitaryTacticUnit:
                        unit.state = None
                        unit.flag_unit = interfacesp.ImageMapObject(self.screen, 86 / 2 + 22, 100 / 2 - 20,
                                                                    unit.get_icon_mini_flag(),
                                                                    cell=self.map_manager.CellSelected)
                        break

    def road_redactor_menu(self):
        """ Отображение кнопок и элементов меню расстановки дорог """
        hexagon_image = interfacesp.ImageObject(self.screen, self.menu_panel.bounds.x + 120,
                                                self.menu_panel.bounds.y + 80, pg.image.load('Other/big_hex.png'))
        self.map_manager.text_and_image_menu_list.append(hexagon_image)
        self.map_manager.chief_manager.text_and_image_list.append(hexagon_image)

        self.buttons_road((self.menu_panel.bounds.x + 260, self.menu_panel.bounds.y + 50), 1)
        self.buttons_road((self.menu_panel.bounds.x + 310, self.menu_panel.bounds.y + 155), 2)
        self.buttons_road((self.menu_panel.bounds.x + 260, self.menu_panel.bounds.y + 270), 3)
        self.buttons_road((self.menu_panel.bounds.x + 100, self.menu_panel.bounds.y + 270), 4)
        self.buttons_road((self.menu_panel.bounds.x + 50, self.menu_panel.bounds.y + 155), 5)
        self.buttons_road((self.menu_panel.bounds.x + 100, self.menu_panel.bounds.y + 50), 6)

    def buttons_road(self, pos, side_road):
        """ Отображение блока кнопок для выбора покрытия дороги одной из сторон """
        button_dirt_road = interfacesp.Button(self.screen, pos[0], pos[1], 25, 25, '', button_color=(139, 119, 101),
                                              on_click=lambda: self.add_delete_road(guidestorage.TypeRoad.dirt_road,
                                                                                    side_road))
        self.map_manager.button_cell_list.append(button_dirt_road)
        self.map_manager.chief_manager.button_list.append(button_dirt_road)

        button_asphalt_road = interfacesp.Button(self.screen, pos[0] + 25, pos[1], 25, 25, '',
                                                 button_color=(131, 139, 139), on_click=lambda: self.add_delete_road(
                                                     guidestorage.TypeRoad.asphalt_road, side_road))
        self.map_manager.button_cell_list.append(button_asphalt_road)
        self.map_manager.chief_manager.button_list.append(button_asphalt_road)

        button_highway = interfacesp.Button(self.screen, pos[0], pos[1] + 25, 25, 25, '', button_color=(54, 54, 54),
                                            on_click=lambda: self.add_delete_road(
                                                guidestorage.TypeRoad.highway, side_road))
        self.map_manager.button_cell_list.append(button_highway)
        self.map_manager.chief_manager.button_list.append(button_highway)

        button_railway = interfacesp.Button(self.screen, pos[0] + 25, pos[1] + 25, 25, 25, '',
                                            button_color=(139, 0, 139), on_click=lambda: self.add_delete_road(
                                                guidestorage.TypeRoad.railway, side_road))
        self.map_manager.button_cell_list.append(button_railway)
        self.map_manager.chief_manager.button_list.append(button_railway)

    def add_delete_road(self, type_road, side_road):
        """ Добавляем-удаляем дороги в режиме редактора """
        road_railway = road_other = None
        for obj in self.map_manager.CellSelected.object_cell_list:
            if type(obj) == mapobject.Road and obj.side_road == side_road:
                if obj.type_road == guidestorage.TypeRoad.railway:
                    road_railway = obj
                else:
                    road_other = obj

        if type_road == guidestorage.TypeRoad.railway and road_railway:
            # Удаляем железную дорогу
            self.map_manager.CellSelected.object_cell_list.remove(road_railway)

        elif type_road == guidestorage.TypeRoad.railway and not road_railway:
            # Создаем железную дорогу
            new_road = mapobject.Road(self.screen, self.map_manager.CellSelected, type_road=type_road,
                                      side_road=side_road)
            self.map_manager.CellSelected.object_cell_list.append(new_road)

        elif type_road != guidestorage.TypeRoad.railway and road_other and road_other.type_road != type_road:
            # Меняем тип автомобильной дороги
            road_other.type_road = type_road

        elif type_road != guidestorage.TypeRoad.railway and road_other and road_other.type_road == type_road:
            # Удаляем автомобильную дорогу
            self.map_manager.CellSelected.object_cell_list.remove(road_other)

        elif type_road != guidestorage.TypeRoad.railway and not road_other:
            # Создаём автомобильную дорогу
            new_road = mapobject.Road(self.screen, self.map_manager.CellSelected, type_road=type_road,
                                      side_road=side_road)
            self.map_manager.CellSelected.object_cell_list.append(new_road)

    def fortification_redactor_menu(self):
        """ Отображение кнопок и элементов меню расстановки оборонительных сооружений """

        hexagon_image = interfacesp.ImageObject(self.screen, self.menu_panel.bounds.x + 120,
                                                self.menu_panel.bounds.y + 80, pg.image.load('Other/big_hex.png'))
        self.map_manager.text_and_image_menu_list.append(hexagon_image)
        self.map_manager.chief_manager.text_and_image_list.append(hexagon_image)

        self.button_fortification((self.menu_panel.bounds.x + 260, self.menu_panel.bounds.y + 50), 1)
        self.button_fortification((self.menu_panel.bounds.x + 310, self.menu_panel.bounds.y + 155), 2)
        self.button_fortification((self.menu_panel.bounds.x + 260, self.menu_panel.bounds.y + 270), 3)
        self.button_fortification((self.menu_panel.bounds.x + 75, self.menu_panel.bounds.y + 270), 4)
        self.button_fortification((self.menu_panel.bounds.x + 25, self.menu_panel.bounds.y + 155), 5)
        self.button_fortification((self.menu_panel.bounds.x + 75, self.menu_panel.bounds.y + 50), 6)
        self.button_fortification((self.menu_panel.bounds.x + 160, self.menu_panel.bounds.y + 155), 7)

    def button_fortification(self, pos, side):
        """ Отображение блока кнопок для выбора типа фортификационного сооружения с одной из сторон """
        button_pillbox = interfacesp.Button(self.screen, pos[0], pos[1], 25, 25, '',
                                            icon=pg.image.load('MapObject/Fortification/DZOT.png'),
                                            on_click=lambda: self.add_delete_fortification(
                                                guidestorage.TypeFortification.pillbox, side))
        self.map_manager.button_cell_list.append(button_pillbox)
        self.map_manager.chief_manager.button_list.append(button_pillbox)

        button_steel_pillbox = interfacesp.Button(self.screen, pos[0] + 27, pos[1], 25, 25, '',
                                                  icon=pg.image.load('MapObject/Fortification/DZOT2.png'),
                                                  on_click=lambda: self.add_delete_fortification(
                                              guidestorage.TypeFortification.steel_pillbox, side))
        self.map_manager.button_cell_list.append(button_steel_pillbox)
        self.map_manager.chief_manager.button_list.append(button_steel_pillbox)

        button_artillery_pillbox = interfacesp.Button(self.screen, pos[0] + 54, pos[1], 25, 25, '',
                                                      icon=pg.image.load('MapObject/Fortification/ArtDZOTr.png'),
                                                      on_click=lambda: self.add_delete_fortification(
                                                  guidestorage.TypeFortification.artillery_pillbox, side))
        self.map_manager.button_cell_list.append(button_artillery_pillbox)
        self.map_manager.chief_manager.button_list.append(button_artillery_pillbox)

        button_artillery_tower = interfacesp.Button(self.screen, pos[0], pos[1] + 27, 25, 25, '',
                                                    icon=pg.image.load('MapObject/Fortification/ArtTowerl.png'),
                                                    on_click=lambda: self.add_delete_fortification(
                                                guidestorage.TypeFortification.artillery_tower, side))
        self.map_manager.button_cell_list.append(button_artillery_tower)
        self.map_manager.chief_manager.button_list.append(button_artillery_tower)

        if side == 7:
            button_air_defense_installations = interfacesp.Button(
                self.screen, pos[0] + 27, pos[1] + 27, 25, 25, '',
                icon=pg.image.load('MapObject/Fortification/PVOart.png'),
                on_click=lambda: self.add_delete_fortification(guidestorage.TypeFortification.air_defense_installations,
                                                               side))
            self.map_manager.button_cell_list.append(button_air_defense_installations)
            self.map_manager.chief_manager.button_list.append(button_air_defense_installations)
        else:
            button_naval_guns = interfacesp.Button(self.screen, pos[0] + 27, pos[1] + 27, 25, 25, '',
                                                   icon=pg.image.load('MapObject/Fortification/ArtNaval.png'),
                                                   on_click=lambda: self.add_delete_fortification(
                                               guidestorage.TypeFortification.naval_guns, side))
            self.map_manager.button_cell_list.append(button_naval_guns)
            self.map_manager.chief_manager.button_list.append(button_naval_guns)

        button_fortified_fort = interfacesp.Button(self.screen, pos[0] + 54, pos[1] + 27, 25, 25, '',
                                                   icon=pg.image.load('MapObject/Fortification/FortR.png'),
                                                   on_click=lambda: self.add_delete_fortification(
                                               guidestorage.TypeFortification.fortified_fort, side))
        self.map_manager.button_cell_list.append(button_fortified_fort)
        self.map_manager.chief_manager.button_list.append(button_fortified_fort)

    def add_delete_fortification(self, type_fortification: guidestorage.TypeFortification, side: int):
        """ Добавляем-удаляем фортификационные сооружения в режиме редактора """
        fort = air_fort = None
        for obj in self.map_manager.CellSelected.object_cell_list:
            if type(obj) == mapobject.Fortification and obj.side == side:
                if obj.type_fortification == guidestorage.TypeFortification.air_defense_installations:
                    air_fort = obj
                else:
                    fort = obj

        if type_fortification != guidestorage.TypeFortification.air_defense_installations:
            if not fort:
                if mapobject.get_point_fortification(self.map_manager.CellSelected, side, type_fortification):
                    pos = mapobject.get_point_fortification(self.map_manager.CellSelected, side, type_fortification)
                    pos = ((pos[0] - self.map_manager.CellSelected.centrX), (pos[1] -
                                                                             self.map_manager.CellSelected.centrY))
                    new_fortification = mapobject.Fortification(self.screen, self.map_manager.CellSelected, pos, side,
                                                                type_fortification)
                    self.map_manager.CellSelected.object_cell_list.append(new_fortification)

            elif fort and fort.type_fortification != type_fortification:
                fort.type_fortification = type_fortification
                fort.regular_combat_crew = mapobject.get_info_fortification(
                    type_fortification, side)['regular_combat_crew']
                fort.combat_crew = fort.regular_combat_crew
                fort.icon_fortification = interfacesp.ImageMapObject(self.screen, fort.pos[0], fort.pos[1],
                                                                     mapobject.get_info_fortification(type_fortification,
                                                                                                      side)['icon_fortification'],
                                                                     cell=self.map_manager.CellSelected)

            elif fort and fort.type_fortification == type_fortification:
                self.map_manager.CellSelected.object_cell_list.remove(fort)

        elif type_fortification == guidestorage.TypeFortification.air_defense_installations:
            if not air_fort:
                if mapobject.get_point_fortification(self.map_manager.CellSelected, side, type_fortification):
                    pos = mapobject.get_point_fortification(self.map_manager.CellSelected, side, type_fortification)
                    pos = ((pos[0] - self.map_manager.CellSelected.centrX), (pos[1] -
                                                                             self.map_manager.CellSelected.centrY))
                    new_fortification = mapobject.Fortification(self.screen, self.map_manager.CellSelected, pos, side,
                                                                type_fortification)
                    self.map_manager.CellSelected.object_cell_list.append(new_fortification)

            elif air_fort:
                self.map_manager.CellSelected.object_cell_list.remove(air_fort)

    def states_redactor_menu(self):
        """ Отображение блока кнопок для выбора государств, расположенных на карте """
        print('states_redactor_menu')
        y = self.menu_panel.bounds.y + 50
        for state in self.map_manager.list_states:
            self.string_state(y, state)
            y += 44

    def string_state(self, y, state: statessp.States):
        """ Отображение строки страны для отметки чекбоксом
         :param y: координата y строки
         :param state: ссылка на экземпляр объекта Государство """
        # todo Возможно надо вынести в суперкласс

        # Чекбокс добавления страны в проект редактора
        checkbox_state = None
        condition = True if state.status_states == guidestorage.StatusState.state_for_game else False

        if state.status_states == guidestorage.StatusState.state_for_game:
            on_click = lambda: self.delete_state(state, checkbox_state)
        else:
            on_click = lambda: self.add_state(state, checkbox_state)

        checkbox_state = interfacesp.CheckBox(self.screen, self.menu_panel.bounds.x + 50, y + 12, 25, 25,
                                              condition=condition, on_click=on_click)

        self.map_manager.button_cell_list.append(checkbox_state)
        self.map_manager.chief_manager.button_list.append(checkbox_state)
        print(checkbox_state.name + '44')

        # Отображение флага страны
        image_flag = pg.image.load(state.flag)
        flag_state = interfacesp.ImageObject(self.screen, self.menu_panel.bounds.x + 90, y, image_flag)
        self.map_manager.text_and_image_menu_list.append(flag_state)
        self.map_manager.chief_manager.text_and_image_list.append(flag_state)

        # Наименование страны
        name_state = interfacesp.TextObject(self.screen, self.menu_panel.bounds.x + 170, y + 10,
                                            lambda: state.name_state, color='white', font_name='Arial', font_size=20)
        self.map_manager.text_and_image_menu_list.append(name_state)
        self.map_manager.chief_manager.text_and_image_list.append(name_state)

    def add_state(self, state: statessp.States, check_box: interfacesp.CheckBox):
        """ Отображение строки страны для отметки чекбоксом
         :param state: ссылка на экземпляр объекта Государство
         :param check_box: ссылка на экземпляр объекта Чек-бокс """

        print("add_state: ", state.name_state)
        state.status_states = guidestorage.StatusState.state_for_game
        check_box.on_click = lambda: self.delete_state(state, check_box)
        state.object_color_territory = pg.image.load(state.color_territory)

    def delete_state(self, state: statessp.States, check_box: interfacesp.CheckBox):
        print("delete_state: ", state.name_state)
        state.status_states = guidestorage.StatusState.state_for_select
        check_box.on_click = lambda: self.add_state(state, check_box)
        state.object_color_territory = None

        # Удаляем ссылки на государство у принадлежащих ему ячеек
        for cell in state.cell_territory_list:
            cell.state = None

        # Очищаем реестр ячееек, принадлежащих стране
        state.cell_territory_list.clear()

    def unit_add_menu(self):
        """ Отображение блока кнопок для выбора юнитов, расположенных на карте """
        x = self.menu_panel.bounds.x + 50
        y = self.menu_panel.bounds.y + 50
        units_per_page = 13  # количество единиц, умещающихся на странице
        self.map_manager.chief_manager.menu_object.count_page = units_per_page

        length_registry = len(mapobjtactic.MilitaryTacticUnit.standard_unit)
        if length_registry > units_per_page:
            self.map_manager.chief_manager.menu_object.scroll = True
            self.map_manager.chief_manager.menu_object.length_registry = length_registry

            i = 0
            for unit in mapobjtactic.MilitaryTacticUnit.standard_unit:
                if self.map_manager.chief_manager.menu_object.up_pos <= i <\
                        (self.map_manager.chief_manager.menu_object.up_pos + units_per_page):
                    self.unit_string(x, y,
                                     mapobjtactic.MilitaryTacticUnit.standard_unit.get(unit).get('type_military_unit'))
                    y += 40
                i += 1
        else:

            for unit in mapobjtactic.MilitaryTacticUnit.standard_unit:
                self.unit_string(x, y,
                                 mapobjtactic.MilitaryTacticUnit.standard_unit.get(unit).get('type_military_unit'))
                y += 40

    def unit_string(self, x, y, type_unit: guidestorage.MilitaryUnits):
        """ Отображение строки юнита для выборки """

        # Кнопка с изображением юнита
        button_unit = interfacesp.Button(self.screen, x, y, 35, 35, '',
                                         icon=pg.image.load(mapobjtactic.MilitaryTacticUnit.get_path_icon_unit(
                                             type_unit)),
                                         on_click=lambda: self.add_unit(type_unit))
        self.map_manager.button_cell_list.append(button_unit)
        self.map_manager.chief_manager.button_list.append(button_unit)

        # Наименование юнита
        name_unit = interfacesp.TextObject(self.screen, x + 40, y + 5,
                                           lambda: mapobjtactic.MilitaryTacticUnit.get_text_unit(type_unit)[0],
                                           color='white', font_name='Arial', font_size=20)
        self.map_manager.text_and_image_menu_list.append(name_unit)
        self.map_manager.chief_manager.text_and_image_list.append(name_unit)

    def update_registry(self):
        """ Обновляем реестр после скролла """
        # Удаляем кнопки меню
        self.map_manager.map_manager_button_clear()
        icon_close_img = pg.image.load('Icons/delete_icon_25.gif')
        button_close = interfacesp.Button(self.screen, self.menu_panel.bounds.x + self.menu_panel.bounds.w - 31,
                                          self.menu_panel.bounds.y + 2, 29, 29, '', icon=icon_close_img,
                                          on_click=self.Close)
        self.map_manager.chief_manager.button_list.append(button_close)
        self.map_manager.button_cell_list.append(button_close)
        self.unit_add_menu()

    def add_unit(self, type_unit: guidestorage.MilitaryUnits):
        """ Добавление юнита на карту """
        unit_was = False
        for unit in self.map_manager.CellSelected.object_cell_list:
            if type(unit) == mapobjtactic.MilitaryTacticUnit:
                self.map_manager.CellSelected.object_cell_list.remove(unit)
                if unit.type_military_unit != type_unit:
                    unit_new = mapobjtactic.MilitaryTacticUnit(self.screen, self.map_manager.CellSelected,
                                                               type_unit, {})
                    self.map_manager.CellSelected.object_cell_list.append(unit_new)
                unit_was = True
                break
        if not unit_was:
            unit_new = mapobjtactic.MilitaryTacticUnit(self.screen, self.map_manager.CellSelected, type_unit, {})
            self.map_manager.CellSelected.object_cell_list.append(unit_new)

    def delete_unit(self, unit):
        """ Удаление юнита с карты """
        self.map_manager.CellSelected.object_cell_list.remove(unit)
