import pygame as pg
from interfaceScripts import interfacesp as ois
import guidestorage as gs
import statessp


class BaseMapObject:
    """  Базовый игровой объект """
    # Последний id, присвоенный объекту класса
    last_id = 1

    def __init__(self, screen, cell):
        self.id_object = 0
        self.screen = screen
        self.cell = cell
        BaseMapObject.last_id += 1

    def Draw(self):
        """ Базовый метод отрисовки """
        pass

    def get_game_object_dict(self):
        """ Извлекает словарь объекта для последующей сериализации """
        pass


def check_point_water_or_land(point_check, map_world, type_surface='water'):
    """ Определяет точка с прилегающими пикселями вода 'water' или суша 'land'
    для постройки дорог и городов"""
    point_check_list = (point_check, (point_check[0] - 1, point_check[1] - 1),
                        (point_check[0], point_check[1] - 1), (point_check[0] + 1, point_check[1] - 1),
                        (point_check[0] + 1, point_check[1]), (point_check[0] + 1, point_check[1] + 1),
                        (point_check[0], point_check[1] + 1), (point_check[0] - 1, point_check[1] + 1),
                        (point_check[0] - 1, point_check[1]))

    for point in point_check_list:
        if type_surface == 'water':
            if map_world.get_at(point)[2] < 200:
                return False
        elif type_surface == 'land':
            if map_world.get_at(point)[2] >= 200:
                return False

    return True


class Road(BaseMapObject):
    def __init__(self, screen, cell, type_road=gs.TypeRoad.dirt_road, side_road=1, wear_and_tear=0, object_dict=None):
        """ Инициализация экземпляра объекта дороги
         :param screen: ссылка на экземпляр окна
         :param cell: сслылка на эеземпляр ячейки, на которой находится дорога
         :param type_road: тип дороги
         :param side_road: направление дороги
         :param wear_and_tear: износ дороги 0 - новая, 100 - полностью разбита"""

        super().__init__(screen, cell)
        if object_dict:
            self.id_object = object_dict.get('id_object')
        self.type_road = type_road if not object_dict else gs.TypeRoad.get_instance(object_dict.get('type_road'))
        self.side_road = side_road if not object_dict else int(object_dict.get('side_road'))
        self.side_road = side_road if not object_dict else object_dict.get('point_bound')
        self.side_road = side_road if not object_dict else object_dict.get('side_road')

        self.point_center = (self.cell.centrX + 43, self.cell.centrY + 49) if not object_dict else\
            tuple(object_dict.get('point_center'))
        # todo Надо доработать на случай 2-х сухопутных ячеек
        self.point_bound = self.get_points_road() if not object_dict else tuple(object_dict.get('point_bound'))

        self.wear_and_tear = wear_and_tear if not object_dict else int(object_dict.get('wear_and_tear'))

    def Draw(self):
        """ Отрисовка, объекта дороги / Перегруженый метод базового класса  """
        color = ()
        color_list = ((139, 119, 101), (131, 139, 139), (54, 54, 54), (139, 0, 139))

        if self.type_road == gs.TypeRoad.dirt_road:
            color = color_list[0]
        elif self.type_road == gs.TypeRoad.asphalt_road:
            color = color_list[1]
        elif self.type_road == gs.TypeRoad.highway:
            color = color_list[2]
        elif self.type_road == gs.TypeRoad.railway:
            color = color_list[3]

        point_center = (self.point_center[0] + self.cell.map_manager.map_coordinates[0],
                        self.point_center[1] + self.cell.map_manager.map_coordinates[1])
        point_bound = (self.point_bound[0] + self.cell.map_manager.map_coordinates[0],
                       self.point_bound[1] + self.cell.map_manager.map_coordinates[1])

        if self.type_road != gs.TypeRoad.railway:
            pg.draw.line(self.screen, color, point_center, point_bound, width=4)
        else:
            pg.draw.line(self.screen, color, (point_center[0], point_center[1] + 2),
                         (point_bound[0], point_bound[1] + 2), width=2)

    def get_game_object_dict(self):
        """ Извлекает словарь объекта для последующей сериализации """

        game_object_dict = {
            'id_object': self.id_object, 'cell': self.cell.cell_id, 'type_road': self.type_road.value,
            'side_road': self.side_road, 'point_center': self.point_center, 'point_bound': self.point_bound,
            'wear_and_tear': self.wear_and_tear}

        return game_object_dict

    def get_points_road(self):
        """ Извлекаем ближайшую к границе ячейки граничную точку дороги, на которой находится суша
        или ближайшую к центру точку """
        point_check_list = ()

        # Выбираем список точек для кажлого из направлений
        if self.side_road == 1:
            point_check_list = ((self.cell.centrX + 63, self.cell.centrY + 12),
                                (self.cell.centrX + 61, self.cell.centrY + 16),
                                (self.cell.centrX + 59, self.cell.centrY + 20),
                                (self.cell.centrX + 56, self.cell.centrY + 24),
                                (self.cell.centrX + 54, self.cell.centrY + 28))

        elif self.side_road == 2:
            point_check_list = ((self.cell.centrX + 85, self.cell.centrY + 49),
                                (self.cell.centrX + 80, self.cell.centrY + 49),
                                (self.cell.centrX + 75, self.cell.centrY + 49),
                                (self.cell.centrX + 70, self.cell.centrY + 49),
                                (self.cell.centrX + 65, self.cell.centrY + 49))

        elif self.side_road == 3:
            point_check_list = ((self.cell.centrX + 62, self.cell.centrY + 85),
                                (self.cell.centrX + 60, self.cell.centrY + 81),
                                (self.cell.centrX + 58, self.cell.centrY + 77),
                                (self.cell.centrX + 56, self.cell.centrY + 74),
                                (self.cell.centrX + 54, self.cell.centrY + 70))

        elif self.side_road == 4:
            point_check_list = ((self.cell.centrX + 20, self.cell.centrY + 85),
                                (self.cell.centrX + 22, self.cell.centrY + 81),
                                (self.cell.centrX + 25, self.cell.centrY + 77),
                                (self.cell.centrX + 27, self.cell.centrY + 74),
                                (self.cell.centrX + 30, self.cell.centrY + 70))

        elif self.side_road == 5:
            point_check_list = ((self.cell.centrX + 1, self.cell.centrY + 49),
                                (self.cell.centrX + 6, self.cell.centrY + 49),
                                (self.cell.centrX + 11, self.cell.centrY + 49),
                                (self.cell.centrX + 16, self.cell.centrY + 49),
                                (self.cell.centrX + 21, self.cell.centrY + 49))

        elif self.side_road == 6:
            point_check_list = ((self.cell.centrX + 19, self.cell.centrY + 12),
                                (self.cell.centrX + 25, self.cell.centrY + 16),
                                (self.cell.centrX + 25, self.cell.centrY + 20),
                                (self.cell.centrX + 27, self.cell.centrY + 24),
                                (self.cell.centrX + 30, self.cell.centrY + 28))

        # Проверяем точки от границы к краю ячеек на сушу
        for point in point_check_list:
            if check_point_water_or_land(point, self.cell.map_manager.mapWorld_img, type_surface='land'):
                return point

        # Если последняя точка все равно вода - возвращаем её
        return point_check_list[4]


class City(BaseMapObject):
    def __init__(self, screen, cell, name_city, level_city, population_size, icon_city=None, state=None,
                 object_dict=None):
        """ Инициализация экземпляра объекта города
          :param screen: ссылка на экземпляр окна
          :param cell: сслылка на эеземпляр ячейки, на которой находится дорога
          :param name_city: название города
          :param level_city: уровень города
          :param population_size: население города
          :param icon_city: путь к файлу иконки города
          :param state: ссылка на объект государства, которому принадлежит город"""

        super().__init__(screen, cell)
        if object_dict:
            self.id_object = object_dict.get('id_object')
        self.__name_city = name_city if not object_dict else str(object_dict.get('name_city'))
        self.__level_city = level_city if not object_dict else int(object_dict.get('level_city'))
        self.__population_size = population_size if not object_dict else int(object_dict.get('population_size'))
        coord = self.get_coord_city_of_map()

        if object_dict:
            self.icon_city = object_dict.get('icon_city')
        elif icon_city:
            self.icon_city = icon_city
        elif not icon_city:
            self.icon_city = self.GetIconCity()

        self.icon_city_object = ois.ImageMapObject(self.screen, coord[0], coord[1], icon_city, cell=self.cell)
        self.text_name_city = ois.TextMapObject(self.screen, coord[2], coord[3], lambda: self.name_city, color='white',
                                                font_name='Arial', font_size=10, cell=self.cell)
        # Принадлежность к стороне конфликта
        self.state = state if not object_dict else statessp.States.dict_states.get(object_dict.get('state'))
        # Список предприятий, расположенных в городе
        self.company_list = list()

    @property
    def name_city(self):
        return self.__name_city

    @name_city.setter
    def name_city(self, name_city):
        self.__name_city = name_city

    @property
    def level_city(self):
        return self.__level_city

    @level_city.setter
    def level_city(self, level_city):
        try:
            level_city = int(level_city)

            if level_city < 1:
                level_city = 1
            elif level_city > 5:
                level_city = 5

            self.__level_city = level_city
        except ValueError:
            print('WARNING: Уровень города должен быть целым числом от 1 до 5')

    @property
    def population_size(self):
        return self.__population_size

    @population_size.setter
    def population_size(self, population_size):
        try:
            population_size = int(population_size)
            self.__population_size = population_size
        except ValueError:
            print('WARNING: Население города должно быть целым числом')

    def Draw(self):
        self.icon_city_object.Draw()
        self.text_name_city.Draw(centralized=True)

    def get_game_object_dict(self):
        """ Извлекает словарь объекта для последующей сериализации """

        game_object_dict = {
            'id_object': self.id_object, 'cell': self.cell.cell_id, 'name_city': self.name_city(),
            'level_city': self.level_city(), 'population_size': self.population_size(), 'icon_city': self.icon_city,
            'state': self.state.id_state}

        return game_object_dict

    def GetIconCity(self):
        """ Извлекает иконку города в зависимости от его уровня """
        icon_city = None
        if self.level_city == 1:
            icon_city = pg.image.load('MapObject/City1.png')
        elif self.level_city == 2:
            icon_city = pg.image.load('MapObject/City2.png')
        elif self.level_city == 3:
            icon_city = pg.image.load('MapObject/City3.png')
        elif self.level_city == 4:
            icon_city = pg.image.load('MapObject/City4.png')
        elif self.level_city == 5:
            icon_city = pg.image.load('MapObject/City5.png')

        return icon_city

    def get_coord_city_of_map(self):
        """  """

        x1, x2, y1, y2 = 0, 0, 0, 0
        if self.level_city == 1:
            x1 = 86/2 - 12
            y1 = 100/2 - 12
            y2 = y1 + 25 + 5
        elif self.level_city == 2:
            x1 = 86/2 - 13
            y1 = 100/2 - 13
            y2 = y1 + 27 + 5
        elif self.level_city == 3:
            x1 = 86/2 - 15
            y1 = 100/2 - 15
            y2 = y1 + 30 + 5
        elif self.level_city == 4:
            x1 = 86/2 - 17
            y1 = 100/2 - 17
            y2 = y1 + 35 + 5
        elif self.level_city == 5:
            x1 = 86/2 - 20
            y1 = 100/2 - 20
            y2 = y1 + 40 + 5

        x2 = 86/2

        return x1, y1, x2, y2

    def get_production_potential_city(self):
        """ Извлекает производственный потенциал города: количество слотов и максималиный уровень предприяития """
        count_slot, level_slot = 0, 0
        if self.level_city == 1:
            count_slot = 2
            level_slot = 2
        elif self.level_city == 2:
            count_slot = 4
            level_slot = 3
        elif self.level_city == 3:
            count_slot = 6
            level_slot = 4
        elif self.level_city == 4:
            count_slot = 8
            level_slot = 5
        elif self.level_city == 5:
            count_slot = 12
            level_slot = 5

        return count_slot, level_slot

    def get_min_populations(self):
        min_populations = 0
        if self.level_city == 1:
            min_populations = 20000

        elif self.level_city == 2:
            min_populations = 200001

        elif self.level_city == 3:
            min_populations = 500001

        elif self.level_city == 4:
            min_populations = 1000001

        elif self.level_city == 5:
            min_populations = 2500001

        return min_populations


def get_info_deposit(type_deposit, water=0):
    info_deposit = dict()
    """ Извлекает данные в зависимости от типа месторождения:
     - тип продукции
     - наименование объекта месторождения на русском языке
     - иконку месторождения
     - тип добывающего предприятия   """
    if type_deposit == gs.TypeResursesDeposit.forest:
        info_deposit = {'type_production': gs.TypeProduct.wood, 'name_deposit': 'Лесной массив',
                        'icon_deposit': pg.image.load('MapObject/Forest2.png'),
                        'mining_company': gs.TypeMiningCompany.sawmills}
    elif type_deposit == gs.TypeResursesDeposit.fertile_soil:
        info_deposit = {'type_production': gs.TypeProduct.vegetable_food, 'name_deposit': 'Плодородные земли',
                        'icon_deposit': pg.image.load('MapObject/field.png'),
                        'mining_company': gs.TypeMiningCompany.farm}
    elif type_deposit == gs.TypeResursesDeposit.pasture:
        info_deposit = {'type_production': gs.TypeProduct.animal_food, 'name_deposit': 'Пастбища',
                        'icon_deposit': pg.image.load('MapObject/Pasture2.png'),
                        'mining_company': gs.TypeMiningCompany.meat_farm}
    elif type_deposit == gs.TypeResursesDeposit.fish_area:
        info_deposit = {'type_production': gs.TypeProduct.fish_food, 'name_deposit': 'Рыболовные участки',
                        'icon_deposit': pg.image.load('MapObject/fish.png'),
                        'mining_company': gs.TypeMiningCompany.trawler}
    elif type_deposit == gs.TypeResursesDeposit.coal_deposit:
        info_deposit = {'type_production': gs.TypeProduct.coal, 'name_deposit': 'Месторождение угля',
                        'icon_deposit': pg.image.load('MapObject/Coal.png'),
                        'mining_company': gs.TypeMiningCompany.coal_mine}
    elif type_deposit == gs.TypeResursesDeposit.oil_field and water == 0:
        info_deposit = {'type_production': gs.TypeProduct.oil, 'name_deposit': 'Месторождение нефти',
                        'icon_deposit': pg.image.load('MapObject/Oil.png'),
                        'mining_company': gs.TypeMiningCompany.oil_company}
    elif type_deposit == gs.TypeResursesDeposit.oil_field and water == 1:
        info_deposit = {'type_production': gs.TypeProduct.oil, 'name_deposit': 'Месторождение нефти',
                        'icon_deposit': pg.image.load('MapObject/Oil.png'),
                        'mining_company': gs.TypeMiningCompany.oil_platform}
    elif type_deposit == gs.TypeResursesDeposit.gas_field:
        info_deposit = {'type_production': gs.TypeProduct.gas, 'name_deposit': 'Месторождение газа',
                        'icon_deposit': pg.image.load('MapObject/gas.png'),
                        'mining_company': gs.TypeMiningCompany.gas_tower}
    elif type_deposit == gs.TypeResursesDeposit.iron_deposit:
        info_deposit = {'type_production': gs.TypeProduct.iron_ore, 'name_deposit': 'Месторождение железной руды',
                        'icon_deposit': pg.image.load('MapObject/iron_ore.png'),
                        'mining_company': gs.TypeMiningCompany.iron_mine}
    elif type_deposit == gs.TypeResursesDeposit.copper_deposit:
        info_deposit = {'type_production': gs.TypeProduct.copper_ore, 'name_deposit': 'Месторождение меди',
                        'icon_deposit': pg.image.load('MapObject/copper_ore.png'),
                        'mining_company': gs.TypeMiningCompany.copper_mine}
    elif type_deposit == gs.TypeResursesDeposit.polymetal_deposit:
        info_deposit = {'type_production': gs.TypeProduct.polymetal_ore,
                        'name_deposit': 'Месторождение полиметаллических руд',
                        'icon_deposit': pg.image.load('MapObject/Polymetal.png'),
                        'mining_company': gs.TypeMiningCompany.polymetal_mine}
    elif type_deposit == gs.TypeResursesDeposit.uranium_deposit:
        info_deposit = {'type_production': gs.TypeProduct.uranium_ore, 'name_deposit': 'Месторождение урана',
                        'icon_deposit': pg.image.load('MapObject/uran.png'),
                        'mining_company': gs.TypeMiningCompany.uranium_mine}
    elif type_deposit == gs.TypeResursesDeposit.apatite_deposit:
        info_deposit = {'type_production': gs.TypeProduct.apatite, 'name_deposit': 'Месторождение аппатитов',
                        'icon_deposit': pg.image.load('MapObject/appatit.png'),
                        'mining_company': gs.TypeMiningCompany.apatite_mine}
    elif type_deposit == gs.TypeResursesDeposit.limestone_deposit:
        info_deposit = {'type_production': gs.TypeProduct.limestone, 'name_deposit': 'Месторождение известняка',
                        'icon_deposit': pg.image.load('MapObject/limestone.png'),
                        'mining_company': gs.TypeMiningCompany.limestone_mine}
    elif type_deposit == gs.TypeResursesDeposit.place_for_dam:
        info_deposit = {'type_production': gs.TypeProduct.electricity, 'name_deposit': 'Место для ГЭС',
                        'icon_deposit': pg.image.load('MapObject/Hidro_point.png'),
                        'mining_company': gs.TypeMiningCompany.hydroelectric_power_stations}

    return info_deposit


def get_info_mining_company(type_mining_company):
    """ Извлекает данные в зависимости от типа месторождения:
         - тип продукции
         - наименование объекта добывающего предприятия на русском языке
         - иконку добывающего предприятия
         - тип месторождения   """
    info_mining_company = None
    print('type_mining_company', type_mining_company)

    if type_mining_company == gs.TypeMiningCompany.sawmills:
        info_mining_company = {'type_production': gs.TypeProduct.wood, 'name_mining_company': 'Пиларама',
                               'icon_mining_company': pg.image.load('MapObject/Pilorama.png'),
                               'type_deposit': gs.TypeResursesDeposit.forest}
    elif type_mining_company == gs.TypeMiningCompany.farm:
        info_mining_company = {'type_production': gs.TypeProduct.vegetable_food, 'name_mining_company': 'Ферма',
                               'icon_mining_company': pg.image.load('MapObject/Farm.png'),
                               'type_deposit': gs.TypeResursesDeposit.fertile_soil}
    elif type_mining_company == gs.TypeMiningCompany.meat_farm:
        info_mining_company = {'type_production': gs.TypeProduct.animal_food,
                               'name_mining_company': 'Животноводческий комплекс',
                               'icon_mining_company': pg.image.load('MapObject/Meat_farm.png'),
                               'type_deposit': gs.TypeResursesDeposit.pasture}
    elif type_mining_company == gs.TypeMiningCompany.trawler:
        info_mining_company = {'type_production': gs.TypeProduct.fish_food, 'name_mining_company': 'Траулер',
                               'icon_mining_company': pg.image.load('MapObject/Trawler.png'),
                               'type_deposit': gs.TypeResursesDeposit.fish_area}
    elif type_mining_company == gs.TypeMiningCompany.coal_mine:
        info_mining_company = {'type_production': gs.TypeProduct.wood, 'name_mining_company': 'Угольная шахта',
                               'icon_mining_company': pg.image.load('MapObject/Coal_mine.png'),
                               'type_deposit': gs.TypeResursesDeposit.coal_deposit}
    elif type_mining_company == gs.TypeMiningCompany.oil_company:
        info_mining_company = {'type_production': gs.TypeProduct.oil, 'name_mining_company': 'Нефтедобывающая компания',
                               'icon_mining_company': pg.image.load('MapObject/Oil_pump.png'),
                               'type_deposit': gs.TypeResursesDeposit.oil_field}
    elif type_mining_company == gs.TypeMiningCompany.oil_platform:
        info_mining_company = {'type_production': gs.TypeProduct.oil, 'name_mining_company': 'Нефтяная платформа',
                               'icon_mining_company': pg.image.load('MapObject/Oil_platform.png'),
                               'type_deposit': gs.TypeResursesDeposit.oil_field}
    elif type_mining_company == gs.TypeMiningCompany.gas_tower:
        info_mining_company = {'type_production': gs.TypeProduct.gas, 'name_mining_company': 'Газодобывающая компания',
                               'icon_mining_company': pg.image.load('MapObject/Gas_tower.png'),
                               'type_deposit': gs.TypeResursesDeposit.gas_field}
    elif type_mining_company == gs.TypeMiningCompany.iron_mine:
        info_mining_company = {'type_production': gs.TypeProduct.iron_ore, 'name_mining_company': 'Железный рудник',
                               'icon_mining_company': pg.image.load('MapObject/Iron_mine.png'),
                               'type_deposit': gs.TypeResursesDeposit.iron_deposit}
    elif type_mining_company == gs.TypeMiningCompany.copper_mine:
        info_mining_company = {'type_production': gs.TypeProduct.copper_ore, 'name_mining_company': 'Медный рудник',
                               'icon_mining_company': pg.image.load('MapObject/Copper_mine.png'),
                               'type_deposit': gs.TypeResursesDeposit.copper_deposit}
    elif type_mining_company == gs.TypeMiningCompany.polymetal_mine:
        info_mining_company = {'type_production': gs.TypeProduct.wood, 'name_mining_company': 'Рудник полиметаллов',
                               'icon_mining_company': pg.image.load('MapObject/Polimetal_mine.png'),
                               'type_deposit': gs.TypeResursesDeposit.polymetal_deposit}
    elif type_mining_company == gs.TypeMiningCompany.uranium_mine:
        info_mining_company = {'type_production': gs.TypeProduct.uranium_ore, 'name_mining_company': 'Урановый рудник',
                               'icon_mining_company': pg.image.load('MapObject/Uran_mine.png'),
                               'type_deposit': gs.TypeResursesDeposit.uranium_deposit}
    elif type_mining_company == gs.TypeMiningCompany.apatite_mine:
        info_mining_company = {'type_production': gs.TypeProduct.apatite, 'name_mining_company': 'Апатитовая шахта',
                               'icon_mining_company': pg.image.load('MapObject/Apatit_mine.png'),
                               'type_deposit': gs.TypeResursesDeposit.apatite_deposit}
    elif type_mining_company == gs.TypeMiningCompany.limestone_mine:
        info_mining_company = {'type_production': gs.TypeProduct.limestone, 'name_mining_company':
                               'Известняковый карьер',
                               'icon_mining_company': pg.image.load('MapObject/Limestoun_mine.png'),
                               'type_deposit': gs.TypeResursesDeposit.limestone_deposit}
    elif type_mining_company == gs.TypeMiningCompany.sawmills:
        info_mining_company = {'type_production': gs.TypeProduct.electricity, 'name_mining_company':
                               'Гидроэлектростанция',
                               'icon_mining_company': pg.image.load('MapObject/HES.png'),
                               'type_deposit': gs.TypeResursesDeposit.place_for_dam}

    print('info_mining_company', info_mining_company)
    return info_mining_company


class NaturalResources(BaseMapObject):
    """ Объект природных ресурсов """
    def __init__(self, screen, cell, type_resources_deposit, production_size=0, icon_resources=None):
        super().__init__(screen, cell)
        self.type_resources_deposit = type_resources_deposit
        self.type_product = get_info_deposit(self.type_resources_deposit)['type_production']
        if production_size == 0:
            # *** добавить функцию определения дефолтного уровня добычи для каждого типа месторождний ***
            production_size = 1000
        self.__production_size = production_size

        if icon_resources is None:
            icon_resources = get_info_deposit(self.type_resources_deposit)['icon_deposit']

        self.icon_resources = ois.ImageMapObject(self.screen, 86/2 - 12, 100/2 - 12, icon_resources, cell=self.cell)
        self.title_productions_deposit = ois.TextMapObject(self.screen, 86/2, 100/2+18,
                                                           lambda: 'Max: ' + str(self.production_size), color='white',
                                                           font_name='Arial', font_size=10, cell=self.cell)
        self.mining_company = None

    def Draw(self):
        """ Отрисовка объекта на карте """
        if self.icon_resources:
            self.icon_resources.Draw()
        if self.title_productions_deposit:
            self.title_productions_deposit.Draw(centralized=True)

    @property
    def production_size(self):
        return self.__production_size

    @production_size.setter
    def production_size(self, production_size):
        try:
            production_size = int(production_size)
            self.__production_size = production_size
        except ValueError:
            print('WARNING: Население города должно быть целым числом')


class Enterprises(BaseMapObject):
    def __init__(self, screen, cell, city=None, level=1, icon_enterprises=None):
        super().__init__(screen, cell)

        self.city = city
        self.__level = level
        self.icon_enterprises = icon_enterprises
        self.__production_size = None
        self.__staff = None
        self.type_product = None

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level):
        try:
            level = int(level)

            if level < 1:
                level = 1
            elif level > 5:
                level = 5

            self.__level = level
        except ValueError:
            print('WARNING: Уровень предприятия должен быть целым числом от 1 до 5')

    @property
    def production_size(self):
        return self.__production_size

    @production_size.setter
    def production_size(self, production_size):
        try:
            production_size = int(production_size)
            self.__production_size = production_size
        except ValueError:
            print('WARNING: Уровень производства предприятия должен быть целым числом')

    @property
    def staff(self):
        return self.__staff

    @staff.setter
    def staff(self, staff):
        try:
            staff = int(staff)
            self.__staff = staff
        except ValueError:
            print('WARNING: Численность персонала предприятия должна быть целым числом')


class MiningCompany(Enterprises):
    """ Объект добывающего предприятия """
    def __init__(self, screen, cell, city=None, level=1, icon_enterprises=None,
                 resources_deposit=gs.TypeResursesDeposit.forest):
        super().__init__(screen, cell, city=city, level=level, icon_enterprises=icon_enterprises)

        self.resources_deposit = resources_deposit
        self.type_mining_company = get_info_deposit(self.resources_deposit.type_resources_deposit,
                                                    cell.Water)['mining_company']
        self.level = level
        self.type_product = get_info_mining_company(self.type_mining_company)['type_production']
        self.production_size = int(self.resources_deposit.production_size/5 * self.level)
        # *** добавить функцию определения уровня добычи в зависимости от уровня добывающего предприятия ***
        self.staff = int(1000 * self.level)
        # *** добавить функцию определения численности персонала в зависимости от уровня
        # и типа добывающего предприятия ***

        if icon_enterprises is None:
            icon_enterprises = get_info_mining_company(self.type_mining_company)['icon_mining_company']

        self.icon_mining_company = ois.ImageMapObject(self.screen, 86/2 - 12, 100/2 - 12, icon_enterprises,
                                                      cell=self.cell)
        self.title_mining_company = ois.TextMapObject(self.screen, 86/2, 100/2+18,
                                                      lambda: f'Lv{self.level}: {self.production_size}',
                                                      color='white', font_name='Arial',
                                                      font_size=10, cell=self.cell)

        # Прекращаем отображать объект месторождения
        self.resources_deposit.icon_resources = None
        self.resources_deposit.title_productions_deposit = None

        # Устанавливаем в объекте месторождения ссылку на текущий объект добывающего предприяятия
        self.resources_deposit.mining_company = self

    def Draw(self):
        """" Отрисовка объекта добывающего предприятия на карте / перегружаем метод базового класса """
        self.icon_mining_company.Draw()
        self.title_mining_company.Draw(centralized=True)


class Company(Enterprises):
    """ Объект производственного или сервисного предприятия """

    def __init__(self, screen, cell, city=None, level=1, icon_enterprises=None,
                 type_company=gs.TypeCompany.building_company):
        super().__init__(screen, cell, city=city, level=level, icon_enterprises=icon_enterprises)
        self.type_company = type_company
        self.level = level
        self.type_product = None
        self.production_size = 1000 * self.level
        # *** добавить функцию определения уровня добычи в зависимости от уровня добывающего предприятия ***
        self.staff = 1000 * self.level
        # *** добавить функцию определения численности персонала в зависимости от уровня
        # и типа добывающего предприятия ***
        self.city.company_list.append(self)


class MilitaryObject(BaseMapObject):
    """ Базовый класс военного объекта """
    def __init__(self, screen, cell):
        super().__init__(screen, cell)


def get_info_fortification(type_fortification: gs.TypeFortification, side: int):
    """ Извлекает данные в зависимости от типа оборонительного сооружения:
         - численность боевого расчета оборонительного соооружения
         - наименование объекта оборонительного сооружения на русском языке
         - иконку оборонительного сооружения """
    """ Извлекаем штатную численность боевого расчета оборонительного соооружения """
    info_fortification = dict()

    if type_fortification == gs.TypeFortification.pillbox:
        info_fortification = {'regular_combat_crew': 200, 'name_fortification': 'ДЗОТы',
                              'icon_fortification': pg.image.load('MapObject/Fortification/DZOT.png')}

    elif type_fortification == gs.TypeFortification.steel_pillbox:
        info_fortification = {'regular_combat_crew': 200, 'name_fortification': 'Стальные ДЗОТы',
                              'icon_fortification': pg.image.load('MapObject/Fortification/DZOT2.png')}

    elif type_fortification == gs.TypeFortification.artillery_pillbox:
        icon_fortification = pg.image.load('MapObject/Fortification/ArtDZOTr.png') if side in [1, 2, 3] else\
            pg.image.load('MapObject/Fortification/ArtDZOTl.png')
        info_fortification = {'regular_combat_crew': 200, 'name_fortification': 'Артиллерийские ДЗОТы',
                              'icon_fortification': icon_fortification}

    elif type_fortification == gs.TypeFortification.artillery_tower:
        icon_fortification = pg.image.load('MapObject/Fortification/ArtTowerr.png') if side in [1, 2, 3] else \
            pg.image.load('MapObject/Fortification/ArtTowerl.png')
        info_fortification = {'regular_combat_crew': 400, 'name_fortification': 'Башенные орудия',
                              'icon_fortification': icon_fortification}

    elif type_fortification == gs.TypeFortification.fortified_fort:
        icon_fortification = pg.image.load('MapObject/Fortification/FortR.png') if side in [1, 2, 3] else \
            pg.image.load('MapObject/Fortification/FortL.png')
        info_fortification = {'regular_combat_crew': 600, 'name_fortification': 'Укрепленный форт',
                              'icon_fortification': icon_fortification}

    elif type_fortification == gs.TypeFortification.naval_guns:
        info_fortification = {'regular_combat_crew': 400, 'name_fortification': 'Противокорабельная батарея',
                              'icon_fortification': pg.image.load('MapObject/Fortification/ArtNaval.png')}

    elif type_fortification == gs.TypeFortification.air_defense_installations:
        info_fortification = {'regular_combat_crew': 200, 'name_fortification': 'Установки ПВО',
                              'icon_fortification': pg.image.load('MapObject/Fortification/PVOart.png')}

    return info_fortification


def get_point_fortification(cell, side: int, type_fortification: gs.TypeFortification):
    """ Извлекает точку в ячейке, на которую есть возможность установить оборонительное сооружение
     Если такой точки не обнаружено, то извлекает False"""
    if cell.Water != 1:
        # Выбираем список точек для кажлого из направлений
        point_check_list = ()
        if side == 1:
            point_check_list = ((cell.centrX + 59, cell.centrY + 20),
                                (cell.centrX + 56, cell.centrY + 24),
                                (cell.centrX + 54, cell.centrY + 28))

        elif side == 2:
            point_check_list = ((cell.centrX + 75, cell.centrY + 49),
                                (cell.centrX + 70, cell.centrY + 49),
                                (cell.centrX + 65, cell.centrY + 49))

        elif side == 3:
            point_check_list = ((cell.centrX + 58, cell.centrY + 77),
                                (cell.centrX + 56, cell.centrY + 74),
                                (cell.centrX + 54, cell.centrY + 70))

        elif side == 4:
            point_check_list = ((cell.centrX + 25, cell.centrY + 77),
                                (cell.centrX + 27, cell.centrY + 74),
                                (cell.centrX + 30, cell.centrY + 70))

        elif side == 5:
            point_check_list = ((cell.centrX + 11, cell.centrY + 49),
                                (cell.centrX + 16, cell.centrY + 49),
                                (cell.centrX + 21, cell.centrY + 49))

        elif side == 6:
            point_check_list = ((cell.centrX + 25, cell.centrY + 20),
                                (cell.centrX + 27, cell.centrY + 24),
                                (cell.centrX + 30, cell.centrY + 28))

        elif side == 7:
            if type_fortification == gs.TypeFortification.air_defense_installations:
                point_check_list = ((cell.centrX + 64, cell.centrY + 62),
                                    (cell.centrX + 64, cell.centrY + 37),
                                    (cell.centrX + 43, cell.centrY + 77))
            else:
                point_check_list = ((cell.centrX + 20, cell.centrY + 62),
                                    (cell.centrX + 20, cell.centrY + 37),
                                    (cell.centrX + 43, cell.centrY + 20))

        # Проверяем точки от границы к краю ячеек на сушу
        for point in point_check_list:
            if check_point_water_or_land(point, cell.map_manager.mapWorld_img, type_surface='land'):
                return point

        return False


class Fortification(MilitaryObject):
    """ Стационарные оборонительные сооружения """
    def __init__(self, screen, cell, pos, side, type_fortification):
        super().__init__(screen, cell)
        self.pos = pos
        self.side = side
        self.type_fortification = type_fortification
        self.regular_combat_crew = get_info_fortification(self.type_fortification, self.side)['regular_combat_crew']
        self.combat_crew = self.regular_combat_crew

        icon_fortification = get_info_fortification(self.type_fortification, self.side)['icon_fortification']
        size_icon = icon_fortification.get_size()
        x = pos[0] - size_icon[0]//2
        y = pos[1] - size_icon[1]//2
        self.icon_fortification = ois.ImageMapObject(self.screen, x, y, icon_fortification, cell=self.cell)

    def Draw(self):
        """" Отрисовка объекта оборонительного сооружения на карте / перегружаем метод базового класса """
        self.icon_fortification.Draw()
