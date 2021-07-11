import pygame as pg
import MapObjectScript as mos
import StatesScript as ss
import ObjectInterfaceScript as ois


def SetLevelProductionDeposit(resurses, input_field):
    if type(resurses) == mos.NaturalResources:
        resurses.production_size = input_field.text_displayed.strip()[:-1]
        new_text = str(resurses.production_size)
        input_field.text_displayed = input_field.text_original = new_text


def SetNameCity(city, input_field):
    if type(city) == mos.City:
        city.name_city = input_field.text_displayed.strip()[:-1]
        input_field.text_original = input_field.text_displayed = city.name_city


def SetPopulationCity(city, input_field):
    if type(city) == mos.City:
        city.population_size = input_field.text_displayed.strip()[:-1]
        new_text = str(city.population_size)
        input_field.text_displayed = input_field.text_original = new_text


class MenuMMRedactor(ois.MenuMapManager):
    def __init__(self, screen, map_manager, x, y, w, h, name, func, type_panel='fill_color', size_panel=1):
        super().__init__(screen, map_manager, x, y, w, h, name, func, type_panel=type_panel, size_panel=size_panel)

    # Кнопки меню установки типа ячейки: Вода(1), Суша(0), Побережье(2)
    def MenuWaterOrLand(self):
        """ Кнопки меню установки типа ячейки: Вода(1), Суша(0), Побережье(2) """
        # Устанавливаем воду
        button_water = ois.Button(self.screen, self.menu_panel.bounds.x + 20, self.menu_panel.bounds.y + 50, 150, 50,
                                  'Вода', on_click=lambda: self.map_manager.CellSelected.GetWaterOrLand(1))
        self.map_manager.button_cell_list.append(button_water)
        self.map_manager.chief_manager.button_list.append(button_water)

        # Устанавливаем сушу
        button_field = ois.Button(self.screen, self.menu_panel.bounds.x + 190, self.menu_panel.bounds.y + 50, 150, 50,
                                  'Суша', on_click=lambda: self.map_manager.CellSelected.GetWaterOrLand(0))
        self.map_manager.button_cell_list.append(button_field)
        self.map_manager.chief_manager.button_list.append(button_field)

        # Устанавливаем побережье
        button_coast = ois.Button(self.screen, self.menu_panel.bounds.x + 360, self.menu_panel.bounds.y + 50, 150, 50,
                                  'Побережье', on_click=lambda: self.map_manager.CellSelected.GetWaterOrLand(2))
        self.map_manager.button_cell_list.append(button_coast)
        self.map_manager.chief_manager.button_list.append(button_coast)

        # Запускаем автоматическое определение принадлежности участков
        auto_water_or_land = ois.Button(self.screen, self.menu_panel.bounds.x + 20, self.menu_panel.bounds.y + 120, 200,
                                        50, 'Автоопределение', on_click=self.map_manager.GetAutoWaterOrLand)
        self.map_manager.button_cell_list.append(auto_water_or_land)
        self.map_manager.chief_manager.button_list.append(auto_water_or_land)

        # Очищаем ячейку от всех объектов
        auto_water_or_land = ois.Button(self.screen, self.menu_panel.bounds.x + 250, self.menu_panel.bounds.y + 120,
                                        200, 50, 'Удалить объекты', on_click=self.map_manager.CellSelected.ClearObjects)
        self.map_manager.button_cell_list.append(auto_water_or_land)
        self.map_manager.chief_manager.button_list.append(auto_water_or_land)

        description_states = ois.TextObject(self.screen, self.menu_panel.bounds.x + 50,
                                            self.menu_panel.bounds.y + 190,
                                            lambda: 'Установка принадлежности ячейки государствам:',
                                            color='white', font_name='Arial', font_size=20)
        self.map_manager.text_and_image_menu_list.append(description_states)
        self.map_manager.chief_manager.text_and_image_list.append(description_states)
        ind = 0
        x = 50
        y = 240
        for state in self.map_manager.object_operating_mode.list_states:
            if state.status_states == ss.StatusState.state_in_the_game:
                self.ButtonStateForSelect(state, x, y)
                x += 70
                ind += 1
                if ind == 7:
                    x = 50
                    y = 300

        # Удаляем ссылку на государство, делая ячейку ничейной
        none_button = ois.Button(self.screen, self.menu_panel.bounds.x + x, self.menu_panel.bounds.y + y,
                                 64, 44, 'None', button_color=(112, 128, 144),
                                 on_click=self.SetNoneState)
        self.map_manager.button_cell_list.append(none_button)
        self.map_manager.chief_manager.button_list.append(none_button)

    def ButtonStateForSelect(self, state: ss.States, x, y):
        """ Кнопка - флаг для установки принадлежности ячейки государству """
        # Очищаем ячейку от всех объектов
        # image_flag = pg.image.load(state.flag)

        button_state_for_select = ois.Button(self.screen, self.menu_panel.bounds.x + x,
                                             self.menu_panel.bounds.y + y,
                                             64, 44, '', icon=pg.image.load(state.flag),
                                             on_click=lambda: self.SetStateForCell(state))
        self.map_manager.button_cell_list.append(button_state_for_select)
        self.map_manager.chief_manager.button_list.append(button_state_for_select)

    def SetStateForCell(self, state):
        """ Устанавливает у ячейки принадлежность государству """
        self.map_manager.CellSelected.state = state
        state.cell_territory_list.append(self.map_manager.CellSelected)

    def SetNoneState(self):
        """ Убирает у ячейки принадлежность государству """
        self.map_manager.CellSelected.state.cell_territory_list.remove(self.map_manager.CellSelected)
        self.map_manager.CellSelected.state = None

    # Кнопки и элементы меню расстановки месторождений
    def ResursesRedactorMenu(self):
        """ Отображение кнопок и элементов меню расстановки месторождений """
        resurses = None
        for obj in self.map_manager.CellSelected.object_cell_list:
            if type(obj) == mos.NaturalResources:
                resurses = obj
                break

        if self.map_manager.CellSelected and resurses is None:
            # Кнопка создания города
            button_new_resurses = ois.Button(self.screen, self.menu_panel.bounds.x + 115, self.menu_panel.bounds.y + 50,
                                             300, 50, 'Добавить месторождение',
                                             on_click=lambda: self.ADD_Resurses())
            self.map_manager.button_cell_list.append(button_new_resurses)
            self.map_manager.chief_manager.button_list.append(button_new_resurses)

        elif self.map_manager.CellSelected and resurses:
            resurses = None
            for obj in self.map_manager.CellSelected.object_cell_list:
                if type(obj) == mos.NaturalResources:
                    resurses = obj
                    break

            # Кнопка удаления месторождения
            button_delete_resurses = ois.Button(self.screen, self.menu_panel.bounds.x + 115,
                                                self.menu_panel.bounds.y + 50,
                                                300, 50, 'Удалить месторождение',
                                                on_click=lambda: self.DeleteNaturalResources(resurses))
            self.map_manager.button_cell_list.append(button_delete_resurses)
            self.map_manager.chief_manager.button_list.append(button_delete_resurses)

            # Описание типа месторождения
            description_type_resurses = ois.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                       self.menu_panel.bounds.y + 120,
                                                       lambda: mos.GetInfoDeposit(
                                                           resurses.type_resources_deposit)['name_deposit'],
                                                       color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_type_resurses)
            self.map_manager.chief_manager.text_and_image_list.append(description_type_resurses)

            # Описание уровня добычи месторождения
            description_level_production = ois.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                          self.menu_panel.bounds.y + 230, lambda: 'Уровень добычи: ',
                                                          color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_level_production)
            self.map_manager.chief_manager.text_and_image_list.append(description_level_production)

            level_production_input = ois.InputField(self.screen, self.menu_panel.bounds.x + 250,
                                                    self.menu_panel.bounds.y +
                                                    220, 250, 50, text=str(resurses.production_size),
                                                    name='level_production_input', type_content='Int',
                                                    on_click=lambda: SetLevelProductionDeposit(
                                                        resurses, level_production_input))
            self.map_manager.button_cell_list.append(level_production_input)
            self.map_manager.chief_manager.button_list.append(level_production_input)

            i = 0
            for type_deposit in mos.TypeResursesDeposit:
                self.ADD_ButtonResurses(resurses, type_deposit, i)
                i += 1

    def ADD_ButtonResurses(self, resurses, type_deposit, i):
        """ Отрисовка кнопки-иконки с типом ресурсов """
        button_deposit = ois.Button(self.screen, self.menu_panel.bounds.x + 10 + 40 * i + 2 * i,
                                    self.menu_panel.bounds.y + 150,
                                    29, 29, '', icon=mos.GetInfoDeposit(type_deposit)['icon_deposit'],
                                    on_click=lambda: self.ChangeTypeDeposit(resurses, type_deposit))
        self.map_manager.button_cell_list.append(button_deposit)
        self.map_manager.chief_manager.button_list.append(button_deposit)

    def ADD_Resurses(self):
        """ Добавление месторождения на карту"""
        resurses = mos.NaturalResources(self.screen, self.map_manager.CellSelected, mos.TypeResursesDeposit.forest)
        self.map_manager.CellSelected.object_cell_list.append(resurses)
        self.map_manager.MapManagerButtonClear()
        self.ResursesRedactorMenu()

        icon_close_img = pg.image.load('Icons/delete_icon_25.gif')
        button_close = ois.Button(self.screen, self.menu_panel.bounds.x + self.menu_panel.bounds.w - 31,
                                  self.menu_panel.bounds.y + 2, 29, 29, '', icon=icon_close_img, on_click=self.Close)
        self.map_manager.chief_manager.button_list.append(button_close)
        self.map_manager.button_cell_list.append(button_close)

    def DeleteNaturalResources(self, resurses):
        """ Удление месторождения с карты и закрытие меню расстановки месторождений """
        self.map_manager.CellSelected.object_cell_list.remove(resurses)
        self.Close()

    def ChangeTypeDeposit(self, deposit, type_deposit):
        """ Изменение типа месторождения """
        if type(deposit) == mos.NaturalResources:
            deposit.type_resources_deposit = type_deposit
            print('ChangeTypeDeposit', type_deposit)
            deposit.type_product = mos.GetInfoDeposit(deposit.type_resources_deposit)['type_production']
            deposit.production_size = 1000
            # *** добавить функцию определения дефолтного уровня добычи для каждого
            # типа месторождний ***

            for obj in self.map_manager.chief_manager.button_list:
                if type(obj) == ois.InputField and obj.name == 'populations_city_input':
                    pass
                    # obj.text_original = obj.text_displayed = str(city.population_size)

            deposit.icon_resources.image = mos.GetInfoDeposit(deposit.type_resources_deposit)['icon_deposit']

    def MiningCompanyRedactorMenu(self):
        """ Отображение кнопок и элементов меню расстановки городов """
        resurses = None
        mining_company = None
        for obj in self.map_manager.CellSelected.object_cell_list:
            if type(obj) == mos.NaturalResources:
                resurses = obj
                break

        if not resurses:
            return
        else:
            mining_company = resurses.mining_company

        if self.map_manager.CellSelected and mining_company is None:
            # Кнопка создания добывающего предпиятия
            button_new_mining_company = ois.Button(self.screen, self.menu_panel.bounds.x + 190,
                                                   self.menu_panel.bounds.y + 50, 250, 50, 'Добавить предприятие',
                                                   on_click=lambda: self.ADD_Mining_Company(resurses))
            self.map_manager.button_cell_list.append(button_new_mining_company)
            self.map_manager.chief_manager.button_list.append(button_new_mining_company)

        elif self.map_manager.CellSelected and mining_company:
            # Кнопка удаления добывающего предприятия
            button_delete_mining_company = ois.Button(self.screen, self.menu_panel.bounds.x + 190,
                                                      self.menu_panel.bounds.y + 50, 250, 50, 'Удалить предприятие',
                                                      on_click=lambda: self.Delete_Mining_Company(resurses))
            self.map_manager.button_cell_list.append(button_delete_mining_company)
            self.map_manager.chief_manager.button_list.append(button_delete_mining_company)

            # Описание уровня города
            description_level = ois.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                               self.menu_panel.bounds.y + 120,
                                               lambda: 'Уровень добывающего предприятия: ' + str(mining_company.level),
                                               color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_level)
            self.map_manager.chief_manager.text_and_image_list.append(description_level)

            # Кнопки изменения уровня города
            button_level1 = ois.Button(self.screen, self.menu_panel.bounds.x + 15, self.menu_panel.bounds.y + 150,
                                       100, 50, 'LEVEL1',
                                       on_click=lambda: self.Change_Level_Mining_Company(mining_company, 1))
            self.map_manager.button_cell_list.append(button_level1)
            self.map_manager.chief_manager.button_list.append(button_level1)

            button_level2 = ois.Button(self.screen, self.menu_panel.bounds.x + 130, self.menu_panel.bounds.y + 150,
                                       100, 50, 'LEVEL2',
                                       on_click=lambda: self.Change_Level_Mining_Company(mining_company, 2))
            self.map_manager.button_cell_list.append(button_level2)
            self.map_manager.chief_manager.button_list.append(button_level2)

            button_level3 = ois.Button(self.screen, self.menu_panel.bounds.x + 245, self.menu_panel.bounds.y + 150,
                                       100, 50, 'LEVEL3',
                                       on_click=lambda: self.Change_Level_Mining_Company(mining_company, 3))
            self.map_manager.button_cell_list.append(button_level3)
            self.map_manager.chief_manager.button_list.append(button_level3)

            button_level4 = ois.Button(self.screen, self.menu_panel.bounds.x + 360, self.menu_panel.bounds.y + 150,
                                       100, 50, 'LEVEL4',
                                       on_click=lambda: self.Change_Level_Mining_Company(mining_company, 4))
            self.map_manager.button_cell_list.append(button_level4)
            self.map_manager.chief_manager.button_list.append(button_level4)

            button_level5 = ois.Button(self.screen, self.menu_panel.bounds.x + 475, self.menu_panel.bounds.y + 150,
                                       100, 50, 'LEVEL5',
                                       on_click=lambda: self.Change_Level_Mining_Company(mining_company, 5))
            self.map_manager.button_cell_list.append(button_level5)
            self.map_manager.chief_manager.button_list.append(button_level5)

            # Описание уровня добычи предприятия
            description_production_size = ois.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                         self.menu_panel.bounds.y + 215,
                                                         lambda: f'Уровень добычи предприятия: '
                                                                 f'{mining_company.production_size} из'
                                                                 f' {mining_company.resources_deposit.production_size}',
                                                         color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_production_size)
            self.map_manager.chief_manager.text_and_image_list.append(description_production_size)

            # Описание численности персонала предприятия
            description_staff = ois.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                               self.menu_panel.bounds.y + 250,
                                               lambda: f'Численность персонала предприятия: {mining_company.staff}',
                                               color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_staff)
            self.map_manager.chief_manager.text_and_image_list.append(description_staff)

    def ADD_Mining_Company(self, deposit):
        """ Добавление добывающего предприятия """
        mining_company = mos.MiningCompany(self.screen, self.map_manager.CellSelected, resources_deposit=deposit)
        self.map_manager.CellSelected.object_cell_list.append(mining_company)
        self.map_manager.MapManagerButtonClear()
        self.MiningCompanyRedactorMenu()

        icon_close_img = pg.image.load('Icons/delete_icon_25.gif')
        button_close = ois.Button(self.screen, self.menu_panel.bounds.x + self.menu_panel.bounds.w - 31,
                                  self.menu_panel.bounds.y + 2, 29, 29, '', icon=icon_close_img, on_click=self.Close)
        self.map_manager.chief_manager.button_list.append(button_close)
        self.map_manager.button_cell_list.append(button_close)

    def Delete_Mining_Company(self, deposit):
        """ Удаление добывающего предприятия """
        self.map_manager.CellSelected.object_cell_list.remove(deposit.mining_company)
        deposit.mining_company = None

        icon_resources = mos.GetInfoDeposit(deposit.type_resources_deposit)['icon_deposit']
        deposit.icon_resources = ois.ImageMapObject(deposit.screen, 86 / 2 - 12, 100 / 2 - 12, icon_resources,
                                                    cell=deposit.cell)
        deposit.title_productions_deposit = ois.TextMapObject(deposit.screen, 86 / 2, 100 / 2 + 18,
                                                              lambda: 'Max: ' + str(deposit.production_size),
                                                              color='white', font_name='Arial', font_size=10,
                                                              cell=deposit.cell)
        self.Close()

    def Change_Level_Mining_Company(self, mining_company, level):
        """ Изменение уровня добывающего предприятия """
        print('mining_company, level', mining_company, level, type(mining_company))
        if type(mining_company) == mos.MiningCompany:
            mining_company.level = level
            mining_company.production_size = (mining_company.resources_deposit.production_size / 5) * level
            mining_company.staff = 1000 * level
            print('mining_company.staff', mining_company.staff)

    def RoadRedactorMenu(self):
        """ Отображение кнопок и элементов меню расстановки дорог """
        hexagon_image = ois.ImageObject(self.screen, self.menu_panel.bounds.x + 120, self.menu_panel.bounds.y + 80,
                                        pg.image.load('Other/big_hex.png'))
        self.map_manager.text_and_image_menu_list.append(hexagon_image)
        self.map_manager.chief_manager.text_and_image_list.append(hexagon_image)

        self.ButtonsRoad((self.menu_panel.bounds.x + 260, self.menu_panel.bounds.y + 50), 1)
        self.ButtonsRoad((self.menu_panel.bounds.x + 310, self.menu_panel.bounds.y + 155), 2)
        self.ButtonsRoad((self.menu_panel.bounds.x + 260, self.menu_panel.bounds.y + 270), 3)
        self.ButtonsRoad((self.menu_panel.bounds.x + 100, self.menu_panel.bounds.y + 270), 4)
        self.ButtonsRoad((self.menu_panel.bounds.x + 50, self.menu_panel.bounds.y + 155), 5)
        self.ButtonsRoad((self.menu_panel.bounds.x + 100, self.menu_panel.bounds.y + 50), 6)

    def ButtonsRoad(self, pos, side_road):
        """ Отображение блока кнопок для выбора покрытия дороги одной из сторон """
        button_dirt_road = ois.Button(self.screen, pos[0], pos[1], 25, 25, '', button_color=(139, 119, 101),
                                      on_click=lambda: self.ADD_Delete_Road(mos.TypeRoad.dirt_road, side_road))
        self.map_manager.button_cell_list.append(button_dirt_road)
        self.map_manager.chief_manager.button_list.append(button_dirt_road)

        button_asphalt_road = ois.Button(self.screen, pos[0] + 25, pos[1], 25, 25, '', button_color=(131, 139, 139),
                                         on_click=lambda: self.ADD_Delete_Road(mos.TypeRoad.asphalt_road, side_road))
        self.map_manager.button_cell_list.append(button_asphalt_road)
        self.map_manager.chief_manager.button_list.append(button_asphalt_road)

        button_highway = ois.Button(self.screen, pos[0], pos[1] + 25, 25, 25, '', button_color=(54, 54, 54),
                                    on_click=lambda: self.ADD_Delete_Road(mos.TypeRoad.highway, side_road))
        self.map_manager.button_cell_list.append(button_highway)
        self.map_manager.chief_manager.button_list.append(button_highway)

        button_railway = ois.Button(self.screen, pos[0] + 25, pos[1] + 25, 25, 25, '', button_color=(139, 0, 139),
                                    on_click=lambda: self.ADD_Delete_Road(mos.TypeRoad.railway, side_road))
        self.map_manager.button_cell_list.append(button_railway)
        self.map_manager.chief_manager.button_list.append(button_railway)

    def ADD_Delete_Road(self, type_road, side_road):
        """ Добавляем-удаляем дороги в режиме редактора """
        road_railway = road_other = None
        for obj in self.map_manager.CellSelected.object_cell_list:
            if type(obj) == mos.Road and obj.side_road == side_road:
                if obj.type_road == mos.TypeRoad.railway:
                    road_railway = obj
                else:
                    road_other = obj

        if type_road == mos.TypeRoad.railway and road_railway:
            # Удаляем железную дорогу
            self.map_manager.CellSelected.object_cell_list.remove(road_railway)

        elif type_road == mos.TypeRoad.railway and not road_railway:
            # Создаем железную дорогу
            new_road = mos.Road(self.screen, self.map_manager.CellSelected, type_road=type_road, side_road=side_road)
            self.map_manager.CellSelected.object_cell_list.append(new_road)

        elif type_road != mos.TypeRoad.railway and road_other and road_other.type_road != type_road:
            # Меняем тип автомобильной дороги
            road_other.type_road = type_road

        elif type_road != mos.TypeRoad.railway and road_other and road_other.type_road == type_road:
            # Удаляем автомобильную дорогу
            self.map_manager.CellSelected.object_cell_list.remove(road_other)

        elif type_road != mos.TypeRoad.railway and not road_other:
            # Создаём автомобильную дорогу
            new_road = mos.Road(self.screen, self.map_manager.CellSelected, type_road=type_road, side_road=side_road)
            self.map_manager.CellSelected.object_cell_list.append(new_road)

    def FortificationRedactorMenu(self):
        """ Отображение кнопок и элементов меню расстановки оборонительных сооружений """

        hexagon_image = ois.ImageObject(self.screen, self.menu_panel.bounds.x + 120, self.menu_panel.bounds.y + 80,
                                        pg.image.load('Other/big_hex.png'))
        self.map_manager.text_and_image_menu_list.append(hexagon_image)
        self.map_manager.chief_manager.text_and_image_list.append(hexagon_image)

        self.ButtonFortification((self.menu_panel.bounds.x + 260, self.menu_panel.bounds.y + 50), 1)
        self.ButtonFortification((self.menu_panel.bounds.x + 310, self.menu_panel.bounds.y + 155), 2)
        self.ButtonFortification((self.menu_panel.bounds.x + 260, self.menu_panel.bounds.y + 270), 3)
        self.ButtonFortification((self.menu_panel.bounds.x + 75, self.menu_panel.bounds.y + 270), 4)
        self.ButtonFortification((self.menu_panel.bounds.x + 25, self.menu_panel.bounds.y + 155), 5)
        self.ButtonFortification((self.menu_panel.bounds.x + 75, self.menu_panel.bounds.y + 50), 6)
        self.ButtonFortification((self.menu_panel.bounds.x + 160, self.menu_panel.bounds.y + 155), 7)

    def ButtonFortification(self, pos, side):
        """ Отображение блока кнопок для выбора типа фортификационного сооружения с одной из сторон """
        button_pillbox = ois.Button(self.screen, pos[0], pos[1], 25, 25, '',
                                    icon=pg.image.load('MapObject/Fortification/DZOT.png'),
                                    on_click=lambda: self.ADD_Delete_Fortification(mos.TypeFortification.pillbox, side))
        self.map_manager.button_cell_list.append(button_pillbox)
        self.map_manager.chief_manager.button_list.append(button_pillbox)

        button_steel_pillbox = ois.Button(self.screen, pos[0] + 27, pos[1], 25, 25, '',
                                          icon=pg.image.load('MapObject/Fortification/DZOT2.png'), on_click=lambda:
            self.ADD_Delete_Fortification(mos.TypeFortification.steel_pillbox, side))
        self.map_manager.button_cell_list.append(button_steel_pillbox)
        self.map_manager.chief_manager.button_list.append(button_steel_pillbox)

        button_artillery_pillbox = ois.Button(self.screen, pos[0] + 54, pos[1], 25, 25, '',
                                              icon=pg.image.load('MapObject/Fortification/ArtDZOTr.png'),
                                              on_click=lambda: self.ADD_Delete_Fortification(
                                                  mos.TypeFortification.artillery_pillbox, side))
        self.map_manager.button_cell_list.append(button_artillery_pillbox)
        self.map_manager.chief_manager.button_list.append(button_artillery_pillbox)

        button_artillery_tower = ois.Button(self.screen, pos[0], pos[1] + 27, 25, 25, '',
                                            icon=pg.image.load('MapObject/Fortification/ArtTowerl.png'),
                                            on_click=lambda: self.ADD_Delete_Fortification(
                                                mos.TypeFortification.artillery_tower, side))
        self.map_manager.button_cell_list.append(button_artillery_tower)
        self.map_manager.chief_manager.button_list.append(button_artillery_tower)

        if side == 7:
            button_air_defense_installations = ois.Button(self.screen, pos[0] + 27, pos[1] + 27, 25, 25, '',
                                                          icon=pg.image.load('MapObject/Fortification/PVOart.png'),
                                                          on_click=lambda: self.ADD_Delete_Fortification(
                                                              mos.TypeFortification.air_defense_installations, side))
            self.map_manager.button_cell_list.append(button_air_defense_installations)
            self.map_manager.chief_manager.button_list.append(button_air_defense_installations)
        else:
            button_naval_guns = ois.Button(self.screen, pos[0] + 27, pos[1] + 27, 25, 25, '',
                                           icon=pg.image.load('MapObject/Fortification/ArtNaval.png'),
                                           on_click=lambda: self.ADD_Delete_Fortification(
                                               mos.TypeFortification.naval_guns, side))
            self.map_manager.button_cell_list.append(button_naval_guns)
            self.map_manager.chief_manager.button_list.append(button_naval_guns)

        button_fortified_fort = ois.Button(self.screen, pos[0] + 54, pos[1] + 27, 25, 25, '',
                                           icon=pg.image.load('MapObject/Fortification/FortR.png'),
                                           on_click=lambda: self.ADD_Delete_Fortification(
                                               mos.TypeFortification.fortified_fort, side))
        self.map_manager.button_cell_list.append(button_fortified_fort)
        self.map_manager.chief_manager.button_list.append(button_fortified_fort)

    def ADD_Delete_Fortification(self, type_fortification: mos.TypeFortification, side: int):
        """ Добавляем-удаляем фортификационные сооружения в режиме редактора """
        print('ADD_Delete_Fortification', type_fortification, side)
        fort = air_fort = None
        for obj in self.map_manager.CellSelected.object_cell_list:
            if type(obj) == mos.Fortification and obj.side == side:
                if obj.type_fortification == mos.TypeFortification.air_defense_installations:
                    air_fort = obj
                else:
                    fort = obj

        if type_fortification != mos.TypeFortification.air_defense_installations:
            if not fort:
                if mos.GetPointFortification(self.map_manager.CellSelected, side, type_fortification):
                    pos = mos.GetPointFortification(self.map_manager.CellSelected, side, type_fortification)
                    pos = ((pos[0] - self.map_manager.CellSelected.centrX), (pos[1] -
                                                                             self.map_manager.CellSelected.centrY))
                    new_fortification = mos.Fortification(self.screen, self.map_manager.CellSelected, pos, side,
                                                          type_fortification)
                    self.map_manager.CellSelected.object_cell_list.append(new_fortification)

            elif fort and fort.type_fortification != type_fortification:
                fort.type_fortification = type_fortification
                fort.regular_combat_crew = mos.GetInfoFortification(type_fortification, side)['regular_combat_crew']
                fort.combat_crew = fort.regular_combat_crew
                fort.icon_fortification = ois.ImageMapObject(self.screen, fort.pos[0], fort.pos[1],
                                                             mos.GetInfoFortification(type_fortification,
                                                                                      side)['icon_fortification'],
                                                             cell=self.map_manager.CellSelected)

            elif fort and fort.type_fortification == type_fortification:
                self.map_manager.CellSelected.object_cell_list.remove(fort)

        elif type_fortification == mos.TypeFortification.air_defense_installations:
            if not air_fort:
                if mos.GetPointFortification(self.map_manager.CellSelected, side, type_fortification):
                    pos = mos.GetPointFortification(self.map_manager.CellSelected, side, type_fortification)
                    pos = ((pos[0] - self.map_manager.CellSelected.centrX), (pos[1] -
                                                                             self.map_manager.CellSelected.centrY))
                    new_fortification = mos.Fortification(self.screen, self.map_manager.CellSelected, pos, side,
                                                          type_fortification)
                    self.map_manager.CellSelected.object_cell_list.append(new_fortification)

            elif air_fort:
                self.map_manager.CellSelected.object_cell_list.remove(air_fort)

    def StatesRedactorMenu(self):
        """ Отображение блока кнопок для выбора государств, расположенных на карте """
        y = self.menu_panel.bounds.y + 50
        for state in self.map_manager.object_operating_mode.list_states:
            self.StringState(y, state)
            y += 44

    def StringState(self, y, state: ss.States):
        """ Отображение строки страны для отметки чекбоксом """
        print(state.name_state)
        # Чекбокс добавления страны в проект редактора
        checkbox_state = None
        if state.status_states == ss.StatusState.state_in_the_game:
            func = lambda: self.Delete_State(state, checkbox_state)
            condition = True
        else:
            func = lambda: self.ADD_State(state, checkbox_state)
            condition = False

        checkbox_state = ois.CheckBox(self.screen, self.menu_panel.bounds.x + 50, y + 12, 25, 25,
                                      condition=condition, on_click=func)
        self.map_manager.button_cell_list.append(checkbox_state)
        self.map_manager.chief_manager.button_list.append(checkbox_state)

        # Отображение флага страны
        image_flag = pg.image.load(state.flag)
        flag_state = ois.ImageObject(self.screen, self.menu_panel.bounds.x + 90, y, image_flag)
        self.map_manager.text_and_image_menu_list.append(flag_state)
        self.map_manager.chief_manager.text_and_image_list.append(flag_state)

        # Наименование страны
        name_state = ois.TextObject(self.screen, self.menu_panel.bounds.x + 170, y + 10, lambda: state.name_state,
                                    color='white', font_name='Arial', font_size=20)
        self.map_manager.text_and_image_menu_list.append(name_state)
        self.map_manager.chief_manager.text_and_image_list.append(name_state)

    def ADD_State(self, state: ss.States, check_box: ois.CheckBox):
        state.status_states = ss.StatusState.state_in_the_game
        # self.map_manager.object_operating_mode.list_current_states.append(state)
        check_box.on_click = lambda: self.Delete_State(state, check_box)
        state.object_color_territory = pg.image.load(state.color_territory)

    def Delete_State(self, state: ss.States, check_box: ois.CheckBox):
        state.status_states = ss.StatusState.state_for_select
        # self.map_manager.object_operating_mode.list_current_states.remove(state)
        check_box.on_click = lambda: self.ADD_State(state, check_box)
        state.object_color_territory = None

        # Удаляем ссылки на государство у принадлежащих ему ячеек
        for cell in state.cell_territory_list:
            cell.state = None

        # Очищаем реестр ячееек, принадлежащих стране
        state.cell_territory_list.clear()


class MenuMMRedactorWithTabs(ois.MenuMapManagerWithTabs):
    def __init__(self, screen, map_manager, x, y, w, h, name, func, func_tabs):
        super().__init__(screen, map_manager, x, y, w, h, name, func, func_tabs)

    def ButtonTabsCity(self):
        button_icon_img = pg.image.load('Other/tab.png')
        button_city = ois.Button(self.screen, self.menu_panel.bounds.x + 10, self.menu_panel.bounds.y + 10, 154, 44,
                                 'Город', button_color=None, icon=button_icon_img, on_click=self.Close)
        self.map_manager.chief_manager.button_list.append(button_city)
        self.map_manager.button_cell_list.append(button_city)

        button_company = ois.Button(self.screen, self.menu_panel.bounds.x + 170, self.menu_panel.bounds.y + 10, 154, 44,
                                    'Предприятия', button_color=None, icon=button_icon_img, on_click=self.Close)
        self.map_manager.chief_manager.button_list.append(button_company)
        self.map_manager.button_cell_list.append(button_company)

        line_tabs = ois.ImageObject(self.screen, self.menu_panel.bounds.x + 10, self.menu_panel.bounds.y + 59,
                                    pg.image.load('Other/line_880.png'))
        self.map_manager.text_and_image_menu_list.append(line_tabs)
        self.map_manager.chief_manager.text_and_image_list.append(line_tabs)

        # Кнопки и элементы меню расстановки городов

    def CityRedactorMenu(self):
        """ Отображение кнопок и элементов меню расстановки городов """
        city = None
        for obj in self.map_manager.CellSelected.object_cell_list:
            if type(obj) == mos.City:
                city = obj
                break
        print(city)
        if self.map_manager.CellSelected and city is None:
            # Кнопка создания города
            button_new_city = ois.Button(self.screen, self.menu_panel.bounds.x + 190, self.menu_panel.bounds.y + 150,
                                         150, 50, 'Добавить город', on_click=lambda: self.ADD_City())
            self.map_manager.button_cell_list.append(button_new_city)
            self.map_manager.chief_manager.button_list.append(button_new_city)

        elif self.map_manager.CellSelected and city:
            city = None
            for obj in self.map_manager.CellSelected.object_cell_list:
                if type(obj) == mos.City:
                    city = obj
                    break

            # Кнопка удаления города
            button_delete_city = ois.Button(self.screen, self.menu_panel.bounds.x + 190, self.menu_panel.bounds.y + 150,
                                            150, 50, 'Удалить город',
                                            on_click=lambda: self.DeleteCity(city))
            self.map_manager.button_cell_list.append(button_delete_city)
            self.map_manager.chief_manager.button_list.append(button_delete_city)

            # Описание уровня города
            description_level = ois.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                               self.menu_panel.bounds.y + 220,
                                               lambda: 'Уровень города: ' + str(city.level_city), color='white',
                                               font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_level)
            self.map_manager.chief_manager.text_and_image_list.append(description_level)

            # Кнопки изменения уровня города
            button_level1_city = ois.Button(self.screen, self.menu_panel.bounds.x + 15, self.menu_panel.bounds.y + 250,
                                            100, 50, 'LEVEL1',
                                            on_click=lambda: self.ChangeLevelCity(city, 1))
            self.map_manager.button_cell_list.append(button_level1_city)
            self.map_manager.chief_manager.button_list.append(button_level1_city)

            button_level2_city = ois.Button(self.screen, self.menu_panel.bounds.x + 130, self.menu_panel.bounds.y + 250,
                                            100, 50, 'LEVEL2',
                                            on_click=lambda: self.ChangeLevelCity(city, 2))
            self.map_manager.button_cell_list.append(button_level2_city)
            self.map_manager.chief_manager.button_list.append(button_level2_city)

            button_level3_city = ois.Button(self.screen, self.menu_panel.bounds.x + 245, self.menu_panel.bounds.y + 250,
                                            100, 50, 'LEVEL3',
                                            on_click=lambda: self.ChangeLevelCity(city, 3))
            self.map_manager.button_cell_list.append(button_level3_city)
            self.map_manager.chief_manager.button_list.append(button_level3_city)

            button_level4_city = ois.Button(self.screen, self.menu_panel.bounds.x + 360, self.menu_panel.bounds.y + 250,
                                            100, 50, 'LEVEL4',
                                            on_click=lambda: self.ChangeLevelCity(city, 4))
            self.map_manager.button_cell_list.append(button_level4_city)
            self.map_manager.chief_manager.button_list.append(button_level4_city)

            button_level5_city = ois.Button(self.screen, self.menu_panel.bounds.x + 475, self.menu_panel.bounds.y + 250,
                                            100, 50, 'LEVEL5',
                                            on_click=lambda: self.ChangeLevelCity(city, 5))
            self.map_manager.button_cell_list.append(button_level5_city)
            self.map_manager.chief_manager.button_list.append(button_level5_city)

            # Описание уровня города
            description_name = ois.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                              self.menu_panel.bounds.y + 330,
                                              lambda: 'Наименование города: ', color='white',
                                              font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_name)
            self.map_manager.chief_manager.text_and_image_list.append(description_name)

            name_city_input = ois.InputField(self.screen, self.menu_panel.bounds.x + 250,
                                             self.menu_panel.bounds.y + 320,
                                             250, 50, text=city.name_city, name='name_city_input',
                                             on_click=lambda: SetNameCity(city, name_city_input))
            self.map_manager.button_cell_list.append(name_city_input)
            self.map_manager.chief_manager.button_list.append(name_city_input)

            # Описание численности населения города
            description_populations = ois.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                     self.menu_panel.bounds.y + 400, lambda: 'Количество жителей: ',
                                                     color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_populations)
            self.map_manager.chief_manager.text_and_image_list.append(description_populations)

            populations_city_input = ois.InputField(self.screen, self.menu_panel.bounds.x + 250,
                                                    self.menu_panel.bounds.y + 390, 250, 50,
                                                    text=str(city.population_size),
                                                    name='populations_city_input', type_content='Int',
                                                    on_click=lambda: SetPopulationCity(city, populations_city_input))
            self.map_manager.button_cell_list.append(populations_city_input)
            self.map_manager.chief_manager.button_list.append(populations_city_input)

            # Описание промышленного потенциала города
            description_potential = ois.TextObject(self.screen, self.menu_panel.bounds.x + 15,
                                                   self.menu_panel.bounds.y + 470, lambda: 'Количество слотов: ' +
                                                   str(city.GetProductionPotentialCity()[0]) +
                                                   ', макс. уровень слотов: ' +
                                                   str(city.GetProductionPotentialCity()[1]),
                                                   color='white', font_name='Arial', font_size=20)
            self.map_manager.text_and_image_menu_list.append(description_potential)
            self.map_manager.chief_manager.text_and_image_list.append(description_potential)

    def ADD_City(self):
        """ Добавление города """
        city = mos.City(self.screen, self.map_manager.CellSelected, 'Новый город', 1, 20000)
        self.map_manager.CellSelected.object_cell_list.append(city)
        self.map_manager.MapManagerButtonClear()
        self.CityRedactorMenu()

        icon_close_img = pg.image.load('Icons/delete_icon_25.gif')
        button_close = ois.Button(self.screen, self.menu_panel.bounds.x + self.menu_panel.bounds.w - 31,
                                  self.menu_panel.bounds.y + 2, 29, 29, '', icon=icon_close_img, on_click=self.Close)
        self.map_manager.chief_manager.button_list.append(button_close)
        self.map_manager.button_cell_list.append(button_close)
        self.func_tabs(self)

    def ChangeLevelCity(self, city, level):
        """ Изменение уровня города """
        if type(city) == mos.City:
            city.level_city = level
            city.population_size = city.GetMinPopulations()

            for obj in self.map_manager.chief_manager.button_list:
                if type(obj) == ois.InputField and obj.name == 'populations_city_input':
                    obj.text_original = obj.text_displayed = str(city.population_size)

            coord = city.CoordCityOfMap()
            city.icon_city = ois.ImageMapObject(self.screen, coord[0], coord[1], city.GetIconCity(), cell=city.cell)

    def DeleteCity(self, city):
        """ Удаление города и закрытие меню расстановки городов """
        self.map_manager.CellSelected.object_cell_list.remove(city)
        self.Close()

    def CompanyRedactorMenu(self):
        pass
