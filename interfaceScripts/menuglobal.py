import pygame as pg
from interfaceScripts import interfacesp as isp
from controlScripts import mapobject, mapobjtactic
import statessp
from interfaceScripts import interfacesp
import guidestorage


def set_level_production_deposit(resurses, input_field):
    if type(resurses) == mapobject.NaturalResources:
        resurses.production_size = input_field.text_displayed.strip()[:-1]
        new_text = str(resurses.production_size)
        input_field.text_displayed = input_field.text_original = new_text


def set_name_city(city, input_field):
    if type(city) == mapobject.City:
        city.name_city = input_field.text_displayed.strip()[:-1]
        input_field.text_original = input_field.text_displayed = city.name_city


def set_population_city(city, input_field):
    if type(city) == mapobject.City:
        city.population_size = str(input_field.text_displayed).strip()[:-1]
        new_text = str(city.population_size)
        input_field.text_displayed = input_field.text_original = new_text


class MapsInterfaceObjectGlobal:
    def __init__(self, map_manager):
        self.map_manager = map_manager

    def cell_menu_redactor_global(self):
        """ Создание кнопок меню ячейки, при выборе ячейки в режиме редактора глобальной карты """

        # Загрузка иконок
        icon_water_or_land_img = pg.image.load('Icons/icon_WaterOrLand.jpg')
        icon_resurses_img = pg.image.load('Icons/icon_Resurses.jpg')
        icon_city_img = pg.image.load('Icons/icon_City.jpg')
        icon_enterprises_img = pg.image.load('Icons/icon_enterprises.jpg')
        icon_road_img = pg.image.load('Icons/icon_Road.jpg')
        icon_fort_img = pg.image.load('Icons/icon_Fort.jpg')
        icon_army_img = pg.image.load('Icons/icon_Army.jpg')
        icon_states_img = pg.image.load('Icons/icon_States.jpg')

        Y = self.map_manager.size_window[1] - 100
        X = self.map_manager.size_window[0] / 2
        coord_buttons = [X - 22, X + 62, X - 106, X + 146, X - 190, X + 230, X - 277, X + 314]

        button_water_or_land = isp.Button(self.map_manager.screen, coord_buttons[0], Y, 44, 44,
                                          '', icon=icon_water_or_land_img,
                                          on_click=lambda: MenuGlobalRedactor(
                                              self.map_manager.screen, self.map_manager.chief_manager, self.map_manager,
                                              300, 200, 600, 400, 'Ячейка',
                                              MenuGlobalRedactor.MenuWaterOrLand, type_panel='transparent panel'))
        self.map_manager.chief_manager.button_list.append(button_water_or_land)
        self.map_manager.button_cell_list.append(button_water_or_land)

        button_resurses = isp.Button(self.map_manager.screen, coord_buttons[1], Y, 44,
                                     44, '', icon=icon_resurses_img, on_click=lambda: MenuGlobalRedactor(
                self.map_manager.screen, self.map_manager.chief_manager, self.map_manager, 300, 200, 600, 400,
                'Месторождение', MenuGlobalRedactor.ResursesRedactorMenu, type_panel='transparent panel'))
        self.map_manager.chief_manager.button_list.append(button_resurses)
        self.map_manager.button_cell_list.append(button_resurses)

        button_city = isp.Button(self.map_manager.screen, coord_buttons[2], Y, 44,
                                 44, '', icon=icon_city_img,
                                 on_click=lambda: MenuGlobalRedactorWithTabs(
                                     self.map_manager.screen, self.map_manager.chief_manager, self.map_manager,
                                     150, 100, 900, 600, 'Город',
                                     MenuGlobalRedactorWithTabs.CityRedactorMenu,
                                     MenuGlobalRedactorWithTabs.ButtonTabsCity))
        self.map_manager.chief_manager.button_list.append(button_city)
        self.map_manager.button_cell_list.append(button_city)

        button_enterprises = isp.Button(self.map_manager.screen, coord_buttons[3], Y, 44,
                                        44, '', icon=icon_enterprises_img, on_click=lambda: MenuGlobalRedactor(
                self.map_manager.screen, self.map_manager.chief_manager, self.map_manager, 300, 200, 600, 400,
                'Добывающее предприятие',
                MenuGlobalRedactor.MiningCompanyRedactorMenu, type_panel='transparent panel'))
        self.map_manager.chief_manager.button_list.append(button_enterprises)
        self.map_manager.button_cell_list.append(button_enterprises)

        button_road = isp.Button(self.map_manager.screen, coord_buttons[4], Y, 44,
                                 44, '', icon=icon_road_img, on_click=lambda: MenuGlobalRedactor(
                self.map_manager.screen, self.map_manager.chief_manager, self.map_manager, 300, 200, 600, 400, 'Дороги',
                MenuGlobalRedactor.road_redactor_menu, type_panel='transparent panel'))
        self.map_manager.chief_manager.button_list.append(button_road)
        self.map_manager.button_cell_list.append(button_road)

        button_fort = isp.Button(self.map_manager.screen, coord_buttons[5], Y, 44,
                                 44, '', icon=icon_fort_img, on_click=lambda: MenuGlobalRedactor(
                self.map_manager.screen, self.map_manager.chief_manager, self.map_manager, 300, 200, 600, 400,
                'Оборонительные сооружения',
                MenuGlobalRedactor.fortification_redactor_menu, type_panel='transparent panel'))
        self.map_manager.chief_manager.button_list.append(button_fort)
        self.map_manager.button_cell_list.append(button_fort)

        button_army = isp.Button(self.map_manager.screen, coord_buttons[6], Y, 44,
                                 44, '', icon=icon_army_img, on_click=self.map_manager.chief_manager.menu_enable)
        self.map_manager.chief_manager.button_list.append(button_army)
        self.map_manager.button_cell_list.append(button_army)

        button_states = isp.Button(self.map_manager.screen, coord_buttons[7], Y, 44, 44, '', icon=icon_states_img,
                                   on_click=lambda: MenuGlobalRedactor(
                                       self.map_manager.screen, self.map_manager.chief_manager, self.map_manager,
                                       150, 100, 900, 600, 'Государства',
                                       MenuGlobalRedactor.states_redactor_menu, type_panel='transparent panel',
                                       size_panel=3))
        self.map_manager.chief_manager.button_list.append(button_states)
        self.map_manager.button_cell_list.append(button_states)


class MenuGlobalRedactor(interfacesp.MenuMapManager):
    """ Окна меню редактора карты без вкладок """
    def __init__(self, screen, chief_manager, map_manager, x, y, w, h, name, func, type_panel='fill_color',
                 size_panel=1, count_page=0, up_pos=0, scroll=False, length_registry=0):
        super().__init__(screen, chief_manager, map_manager, x, y, w, h, name, func, type_panel=type_panel,
                         count_page=count_page, size_panel=size_panel,
                         up_pos=up_pos, scroll=scroll, length_registry=length_registry)
        self.name = 'Меню редактора карты'

    # Кнопки меню установки типа ячейки: Вода(1), Суша(0), Побережье(2)
    def MenuWaterOrLand(self):
        """ Кнопки меню установки типа ячейки: Вода(1), Суша(0), Побережье(2) """
        # Устанавливаем воду
        button_water = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 20,
                                          self.menu_panel.bounds.y + 50, 150, 50, 'Вода',
                                          on_click=lambda: self.map_manager.CellSelected.get_water_or_land(1))
        self.map_manager.button_cell_list.append(button_water)
        self.map_manager.chief_manager.button_list.append(button_water)

        # Устанавливаем сушу
        button_field = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 190,
                                          self.menu_panel.bounds.y + 50, 150, 50, 'Суша',
                                          on_click=lambda: self.map_manager.CellSelected.get_water_or_land(0))
        self.map_manager.button_cell_list.append(button_field)
        self.map_manager.chief_manager.button_list.append(button_field)

        # Устанавливаем побережье
        button_coast = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 360,
                                          self.menu_panel.bounds.y + 50, 150, 50, 'Побережье',
                                          on_click=lambda: self.map_manager.CellSelected.get_water_or_land(2))
        self.map_manager.button_cell_list.append(button_coast)
        self.map_manager.chief_manager.button_list.append(button_coast)

        # Запускаем автоматическое определение принадлежности участков
        auto_water_or_land = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 20,
                                                self.menu_panel.bounds.y + 120, 200, 50, 'Автоопределение',
                                                on_click=self.map_manager.get_auto_water_or_land)
        self.map_manager.button_cell_list.append(auto_water_or_land)
        self.map_manager.chief_manager.button_list.append(auto_water_or_land)

        # Очищаем ячейку от всех объектов
        auto_water_or_land = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 250,
                                                self.menu_panel.bounds.y + 120, 200, 50, 'Удалить объекты',
                                                on_click=self.map_manager.CellSelected.clear_objects_from_cell)
        self.map_manager.button_cell_list.append(auto_water_or_land)
        self.map_manager.chief_manager.button_list.append(auto_water_or_land)

        description_states = interfacesp.TextObject(self.screen, self.menu_panel.bounds.x + 50,
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
                self.ButtonStateForSelect(state, x, y)
                x += 70
                ind += 1
                if ind == 7:
                    x = 50
                    y = 300

        # Удаляем ссылку на государство, делая ячейку ничейной
        none_button = interfacesp.Button(self.screen, self.menu_panel.bounds.x + x, self.menu_panel.bounds.y + y,
                                         64, 44, 'None', button_color=(112, 128, 144),
                                         on_click=self.SetNoneState)
        self.map_manager.button_cell_list.append(none_button)
        self.map_manager.chief_manager.button_list.append(none_button)

    def ButtonStateForSelect(self, state: statessp.States, x, y):
        """ Кнопка - флаг для установки принадлежности ячейки государству """
        # Очищаем ячейку от всех объектов
        # image_flag = pg.image.load(state.flag)

        button_state_for_select = interfacesp.Button(self.screen, self.menu_panel.bounds.x + x,
                                                     self.menu_panel.bounds.y + y,
                                                     64, 44, '', icon=pg.image.load(state.flag),
                                                     on_click=lambda: self.SetStateForCell(state))
        self.map_manager.button_cell_list.append(button_state_for_select)
        self.map_manager.chief_manager.button_list.append(button_state_for_select)

    def SetStateForCell(self, state):
        """ Устанавливает у ячейки принадлежность государству """
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

    def SetNoneState(self):
        """ Убирает у ячейки принадлежность государству """
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

    # Кнопки и элементы меню расстановки месторождений
    def ResursesRedactorMenu(self):
        """ Отображение кнопок и элементов меню расстановки месторождений """
        resurses = None
        for obj in self.map_manager.CellSelected.object_cell_list:
            if type(obj) == mapobject.NaturalResources:
                resurses = obj
                break

        if self.map_manager.CellSelected and resurses is None:
            # Кнопка создания города
            button_new_resurses = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 115,
                                                     self.menu_panel.bounds.y + 50, 300, 50, 'Добавить месторождение',
                                                     on_click=lambda: self.ADD_Resurses())
            self.map_manager.button_cell_list.append(button_new_resurses)
            self.map_manager.chief_manager.button_list.append(button_new_resurses)

        elif self.map_manager.CellSelected and resurses:
            resurses = None
            for obj in self.map_manager.CellSelected.object_cell_list:
                if type(obj) == mapobject.NaturalResources:
                    resurses = obj
                    break

            # Кнопка удаления месторождения
            button_delete_resurses = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 115,
                                                        self.menu_panel.bounds.y + 50,
                                                        300, 50, 'Удалить месторождение',
                                                        on_click=lambda: self.DeleteNaturalResources(resurses))
            self.map_manager.button_cell_list.append(button_delete_resurses)
            self.map_manager.chief_manager.button_list.append(button_delete_resurses)

            # Описание типа месторождения
            description_type_resurses = interfacesp.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                               self.menu_panel.bounds.y + 120,
                                                               lambda: mapobject.get_info_deposit(
                                                                   resurses.type_resources_deposit)['name_deposit'],
                                                               color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_type_resurses)
            self.map_manager.chief_manager.text_and_image_list.append(description_type_resurses)

            # Описание уровня добычи месторождения
            description_level_production = interfacesp.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                                  self.menu_panel.bounds.y + 230,
                                                                  lambda: 'Уровень добычи: ',
                                                                  color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_level_production)
            self.map_manager.chief_manager.text_and_image_list.append(description_level_production)

            level_production_input = interfacesp.InputField(self.screen, self.menu_panel.bounds.x + 250,
                                                            self.menu_panel.bounds.y +
                                                            220, 250, 50, text=str(resurses.production_size),
                                                            name='level_production_input', type_content='Int',
                                                            on_click=lambda: set_level_production_deposit(
                                                                resurses, level_production_input))
            self.map_manager.button_cell_list.append(level_production_input)
            self.map_manager.chief_manager.button_list.append(level_production_input)

            i = 0
            for type_deposit in guidestorage.TypeResursesDeposit:
                self.ADD_ButtonResurses(resurses, type_deposit, i)
                i += 1

    def ADD_ButtonResurses(self, resurses, type_deposit, i):
        """ Отрисовка кнопки-иконки с типом ресурсов """
        button_deposit = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 10 + 40 * i + 2 * i,
                                            self.menu_panel.bounds.y + 150,
                                            29, 29, '', icon=mapobject.get_info_deposit(type_deposit)['icon_deposit'],
                                            on_click=lambda: self.ChangeTypeDeposit(resurses, type_deposit))
        self.map_manager.button_cell_list.append(button_deposit)
        self.map_manager.chief_manager.button_list.append(button_deposit)

    def ADD_Resurses(self):
        """ Добавление месторождения на карту"""
        resurses = mapobject.NaturalResources(self.screen, self.map_manager.CellSelected,
                                              guidestorage.TypeResursesDeposit.forest)
        self.map_manager.CellSelected.object_cell_list.append(resurses)
        self.map_manager.map_manager_button_clear()
        self.ResursesRedactorMenu()

        icon_close_img = pg.image.load('Icons/delete_icon_25.gif')
        button_close = interfacesp.Button(self.screen, self.menu_panel.bounds.x + self.menu_panel.bounds.w - 31,
                                          self.menu_panel.bounds.y + 2, 29, 29, '', icon=icon_close_img,
                                          on_click=self.Close)
        self.map_manager.chief_manager.button_list.append(button_close)
        self.map_manager.button_cell_list.append(button_close)

    def DeleteNaturalResources(self, resurses):
        """ Удление месторождения с карты и закрытие меню расстановки месторождений """
        self.map_manager.CellSelected.object_cell_list.remove(resurses)
        self.Close()

    def ChangeTypeDeposit(self, deposit, type_deposit):
        """ Изменение типа месторождения """
        if type(deposit) == mapobject.NaturalResources:
            deposit.type_resources_deposit = type_deposit
            deposit.type_product = mapobject.get_info_deposit(deposit.type_resources_deposit)['type_production']
            deposit.production_size = 1000
            # *** добавить функцию определения дефолтного уровня добычи для каждого
            # типа месторождний ***

            for obj in self.map_manager.chief_manager.button_list:
                if type(obj) == interfacesp.InputField and obj.name == 'populations_city_input':
                    pass
                    # obj.text_original = obj.text_displayed = str(city.population_size)

            deposit.icon_resources.image = mapobject.get_info_deposit(deposit.type_resources_deposit)['icon_deposit']

    def MiningCompanyRedactorMenu(self):
        """ Отображение кнопок и элементов меню расстановки городов """
        resurses = None
        mining_company = None
        for obj in self.map_manager.CellSelected.object_cell_list:
            if type(obj) == mapobject.NaturalResources:
                resurses = obj
                break

        if not resurses:
            return
        else:
            mining_company = resurses.mining_company

        if self.map_manager.CellSelected and mining_company is None:
            # Кнопка создания добывающего предпиятия
            button_new_mining_company = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 190,
                                                           self.menu_panel.bounds.y + 50, 250, 50,
                                                           'Добавить предприятие',
                                                           on_click=lambda: self.ADD_Mining_Company(resurses))
            self.map_manager.button_cell_list.append(button_new_mining_company)
            self.map_manager.chief_manager.button_list.append(button_new_mining_company)

        elif self.map_manager.CellSelected and mining_company:
            # Кнопка удаления добывающего предприятия
            button_delete_mining_company = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 190,
                                                              self.menu_panel.bounds.y + 50, 250, 50,
                                                              'Удалить предприятие',
                                                              on_click=lambda: self.Delete_Mining_Company(resurses))
            self.map_manager.button_cell_list.append(button_delete_mining_company)
            self.map_manager.chief_manager.button_list.append(button_delete_mining_company)

            # Описание уровня города
            description_level = interfacesp.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                       self.menu_panel.bounds.y + 120,
                                                       lambda: 'Уровень добывающего предприятия: ' +
                                                               str(mining_company.level),
                                                       color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_level)
            self.map_manager.chief_manager.text_and_image_list.append(description_level)

            # Кнопки изменения уровня города
            button_level1 = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 15,
                                               self.menu_panel.bounds.y + 150, 100, 50, 'LEVEL1',
                                               on_click=lambda: self.change_level_mining_company(mining_company, 1))
            self.map_manager.button_cell_list.append(button_level1)
            self.map_manager.chief_manager.button_list.append(button_level1)

            button_level2 = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 130,
                                               self.menu_panel.bounds.y + 150, 100, 50, 'LEVEL2',
                                               on_click=lambda: self.change_level_mining_company(mining_company, 2))
            self.map_manager.button_cell_list.append(button_level2)
            self.map_manager.chief_manager.button_list.append(button_level2)

            button_level3 = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 245,
                                               self.menu_panel.bounds.y + 150, 100, 50, 'LEVEL3',
                                               on_click=lambda: self.change_level_mining_company(mining_company, 3))
            self.map_manager.button_cell_list.append(button_level3)
            self.map_manager.chief_manager.button_list.append(button_level3)

            button_level4 = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 360,
                                               self.menu_panel.bounds.y + 150, 100, 50, 'LEVEL4',
                                               on_click=lambda: self.change_level_mining_company(mining_company, 4))
            self.map_manager.button_cell_list.append(button_level4)
            self.map_manager.chief_manager.button_list.append(button_level4)

            button_level5 = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 475,
                                               self.menu_panel.bounds.y + 150, 100, 50, 'LEVEL5',
                                               on_click=lambda: self.change_level_mining_company(mining_company, 5))
            self.map_manager.button_cell_list.append(button_level5)
            self.map_manager.chief_manager.button_list.append(button_level5)

            # Описание уровня добычи предприятия
            description_production_size = interfacesp.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                                 self.menu_panel.bounds.y + 215,
                                                                 lambda: f'Уровень добычи предприятия: '
                                                                 f'{mining_company.production_size} из'
                                                                 f' {mining_company.resources_deposit.production_size}',
                                                                 color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_production_size)
            self.map_manager.chief_manager.text_and_image_list.append(description_production_size)

            # Описание численности персонала предприятия
            description_staff = interfacesp.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                       self.menu_panel.bounds.y + 250,
                                                       lambda: f'Численность персонала предприятия:'
                                                               f' {mining_company.staff}',
                                                       color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_staff)
            self.map_manager.chief_manager.text_and_image_list.append(description_staff)

    def ADD_Mining_Company(self, deposit):
        """ Добавление добывающего предприятия """
        mining_company = mapobject.MiningCompany(self.screen, self.map_manager.CellSelected, resources_deposit=deposit)
        self.map_manager.CellSelected.object_cell_list.append(mining_company)
        self.map_manager.map_manager_button_clear()
        self.MiningCompanyRedactorMenu()

        icon_close_img = pg.image.load('Icons/delete_icon_25.gif')
        button_close = interfacesp.Button(self.screen, self.menu_panel.bounds.x + self.menu_panel.bounds.w - 31,
                                          self.menu_panel.bounds.y + 2, 29, 29, '', icon=icon_close_img,
                                          on_click=self.Close)
        self.map_manager.chief_manager.button_list.append(button_close)
        self.map_manager.button_cell_list.append(button_close)

    def Delete_Mining_Company(self, deposit):
        """ Удаление добывающего предприятия """
        self.map_manager.CellSelected.object_cell_list.remove(deposit.mining_company)
        deposit.mining_company = None

        icon_resources = mapobject.get_info_deposit(deposit.type_resources_deposit)['icon_deposit']
        deposit.icon_resources = interfacesp.ImageMapObject(deposit.screen, 86 / 2 - 12, 100 / 2 - 12, icon_resources,
                                                            cell=deposit.cell)
        deposit.title_productions_deposit = interfacesp.TextMapObject(deposit.screen, 86 / 2, 100 / 2 + 18,
                                                                      lambda: 'Max: ' + str(deposit.production_size),
                                                                      color='white', font_name='Arial', font_size=10,
                                                                      cell=deposit.cell)
        self.Close()

    @staticmethod
    def change_level_mining_company(mining_company, level):
        """ Изменение уровня добывающего предприятия """

        if type(mining_company) == mapobject.MiningCompany:
            mining_company.level = level
            mining_company.production_size = (mining_company.resources_deposit.production_size / 5) * level
            mining_company.staff = 1000 * level

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
        y = self.menu_panel.bounds.y + 50
        for state in self.map_manager.list_states:
            self.StringState(y, state)
            y += 44

    def StringState(self, y, state: statessp.States):
        """ Отображение строки страны для отметки чекбоксом """
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
        state.status_states = guidestorage.StatusState.state_for_game
        check_box.on_click = lambda: self.delete_state(state, check_box)
        state.object_color_territory = pg.image.load(state.color_territory)

    def delete_state(self, state: statessp.States, check_box: interfacesp.CheckBox):
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
                                         icon=pg.image.load(mapobjtactic.get_path_icon_unit(type_unit)),
                                         on_click=lambda: self.add_unit(type_unit))
        self.map_manager.button_cell_list.append(button_unit)
        self.map_manager.chief_manager.button_list.append(button_unit)

        # Наименование юнита
        name_unit = interfacesp.TextObject(self.screen, x + 40, y + 5, lambda: mapobjtactic.get_text_unit(type_unit)[0],
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


class MenuGlobalRedactorWithTabs(interfacesp.MenuMapManagerWithTabs):
    """ Окна меню редактора карты с вкладками """
    def __init__(self, screen, chief_manager, map_manager, x, y, w, h, name, func, func_tabs, size_panel=3,
                 count_page=0, up_pos=0, scroll=False, length_registry=0):
        super().__init__(screen, chief_manager, map_manager, x, y, w, h, name, func, func_tabs, size_panel=size_panel,
                         count_page=count_page, up_pos=up_pos, scroll=scroll, length_registry=length_registry)

    def ButtonTabsCity(self):
        button_icon_img = pg.image.load('Other/tab.png')
        button_city = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 10, self.menu_panel.bounds.y + 10,
                                         154, 44, 'Город', button_color=None, icon=button_icon_img, on_click=self.Close)
        self.map_manager.chief_manager.button_list.append(button_city)
        self.map_manager.button_cell_list.append(button_city)

        button_company = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 170,
                                            self.menu_panel.bounds.y + 10, 154, 44,
                                            'Предприятия', button_color=None, icon=button_icon_img, on_click=self.Close)
        self.map_manager.chief_manager.button_list.append(button_company)
        self.map_manager.button_cell_list.append(button_company)

        line_tabs = interfacesp.ImageObject(self.screen, self.menu_panel.bounds.x + 10, self.menu_panel.bounds.y + 59,
                                            pg.image.load('Other/line_880.png'))
        self.map_manager.text_and_image_menu_list.append(line_tabs)
        self.map_manager.chief_manager.text_and_image_list.append(line_tabs)

    # Кнопки и элементы меню расстановки городов
    def CityRedactorMenu(self):
        """ Отображение кнопок и элементов меню расстановки городов """
        city = None
        for obj in self.map_manager.CellSelected.object_cell_list:
            if type(obj) == mapobject.City:
                city = obj
                break
        if self.map_manager.CellSelected and city is None:
            # Кнопка создания города
            button_new_city = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 190,
                                                 self.menu_panel.bounds.y + 150,
                                                 150, 50, 'Добавить город', on_click=lambda: self.ADD_City())
            self.map_manager.button_cell_list.append(button_new_city)
            self.map_manager.chief_manager.button_list.append(button_new_city)

        elif self.map_manager.CellSelected and city:
            city = None
            for obj in self.map_manager.CellSelected.object_cell_list:
                if type(obj) == mapobject.City:
                    city = obj
                    break

            # Кнопка удаления города
            button_delete_city = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 190,
                                                    self.menu_panel.bounds.y + 150,
                                                    150, 50, 'Удалить город',
                                                    on_click=lambda: self.DeleteCity(city))
            self.map_manager.button_cell_list.append(button_delete_city)
            self.map_manager.chief_manager.button_list.append(button_delete_city)

            # Описание уровня города
            description_level = interfacesp.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                       self.menu_panel.bounds.y + 220,
                                                       lambda: 'Уровень города: ' + str(city.level_city), color='white',
                                                       font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_level)
            self.map_manager.chief_manager.text_and_image_list.append(description_level)

            # Кнопки изменения уровня города
            button_level1_city = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 15,
                                                    self.menu_panel.bounds.y + 250, 100, 50, 'LEVEL1',
                                                    on_click=lambda: self.ChangeLevelCity(city, 1))
            self.map_manager.button_cell_list.append(button_level1_city)
            self.map_manager.chief_manager.button_list.append(button_level1_city)

            button_level2_city = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 130,
                                                    self.menu_panel.bounds.y + 250, 100, 50, 'LEVEL2',
                                                    on_click=lambda: self.ChangeLevelCity(city, 2))
            self.map_manager.button_cell_list.append(button_level2_city)
            self.map_manager.chief_manager.button_list.append(button_level2_city)

            button_level3_city = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 245,
                                                    self.menu_panel.bounds.y + 250, 100, 50, 'LEVEL3',
                                                    on_click=lambda: self.ChangeLevelCity(city, 3))
            self.map_manager.button_cell_list.append(button_level3_city)
            self.map_manager.chief_manager.button_list.append(button_level3_city)

            button_level4_city = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 360,
                                                    self.menu_panel.bounds.y + 250, 100, 50, 'LEVEL4',
                                                    on_click=lambda: self.ChangeLevelCity(city, 4))
            self.map_manager.button_cell_list.append(button_level4_city)
            self.map_manager.chief_manager.button_list.append(button_level4_city)

            button_level5_city = interfacesp.Button(self.screen, self.menu_panel.bounds.x + 475,
                                                    self.menu_panel.bounds.y + 250, 100, 50, 'LEVEL5',
                                                    on_click=lambda: self.ChangeLevelCity(city, 5))
            self.map_manager.button_cell_list.append(button_level5_city)
            self.map_manager.chief_manager.button_list.append(button_level5_city)

            # Описание уровня города
            description_name = interfacesp.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                      self.menu_panel.bounds.y + 330, lambda: 'Наименование города: ',
                                                      color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_name)
            self.map_manager.chief_manager.text_and_image_list.append(description_name)

            name_city_input = interfacesp.InputField(self.screen, self.menu_panel.bounds.x + 250,
                                                     self.menu_panel.bounds.y + 320,
                                                     250, 50, text=city.name_city, name='name_city_input',
                                                     on_click=lambda: set_name_city(city, name_city_input))
            self.map_manager.button_cell_list.append(name_city_input)
            self.map_manager.chief_manager.button_list.append(name_city_input)

            # Описание численности населения города
            description_populations = interfacesp.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                             self.menu_panel.bounds.y + 400,
                                                             lambda: 'Количество жителей: ',
                                                             color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_populations)
            self.map_manager.chief_manager.text_and_image_list.append(description_populations)

            populations_city_input = interfacesp.InputField(self.screen, self.menu_panel.bounds.x + 250,
                                                            self.menu_panel.bounds.y + 390, 250, 50,
                                                            text=str(city.population_size),
                                                            name='populations_city_input', type_content='Int',
                                                            on_click=lambda: set_population_city(
                                                                city, populations_city_input))
            self.map_manager.button_cell_list.append(populations_city_input)
            self.map_manager.chief_manager.button_list.append(populations_city_input)

            # Описание промышленного потенциала города
            description_potential = interfacesp.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                           self.menu_panel.bounds.y + 470,
                                                           lambda: 'Количество слотов: ' +
                                                           str(city.GetProductionPotentialCity()[0]) +
                                                           ', макс. уровень слотов: ' +
                                                           str(city.GetProductionPotentialCity()[1]),
                                                           color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_potential)
            self.map_manager.chief_manager.text_and_image_list.append(description_potential)

    def ADD_City(self):
        """ Добавление города """
        city = mapobject.City(self.screen, self.map_manager.CellSelected, 'Новый город', 1, 20000)
        self.map_manager.CellSelected.object_cell_list.append(city)
        self.map_manager.map_manager_button_clear()
        self.CityRedactorMenu()

        icon_close_img = pg.image.load('Icons/delete_icon_25.gif')
        button_close = interfacesp.Button(self.screen, self.menu_panel.bounds.x + self.menu_panel.bounds.w - 31,
                                          self.menu_panel.bounds.y + 2, 29, 29, '', icon=icon_close_img,
                                          on_click=self.Close)
        self.map_manager.chief_manager.button_list.append(button_close)
        self.map_manager.button_cell_list.append(button_close)
        self.func_tabs(self)

    def ChangeLevelCity(self, city, level):
        """ Изменение уровня города """
        if type(city) == mapobject.City:
            city.level_city = level
            city.population_size = city.get_min_populations()

            for obj in self.map_manager.chief_manager.button_list:
                if type(obj) == interfacesp.InputField and obj.name == 'populations_city_input':
                    obj.text_original = obj.text_displayed = str(city.population_size)

            coord = city.get_coord_city_of_map()
            city.icon_city = interfacesp.ImageMapObject(self.screen, coord[0], coord[1], city.GetIconCity(),
                                                        cell=city.cell)

    def DeleteCity(self, city):
        """ Удаление города и закрытие меню расстановки городов """
        self.map_manager.CellSelected.object_cell_list.remove(city)
        self.Close()

    def CompanyRedactorMenu(self):
        pass
