from enum import Enum


class OperatingMode(Enum):
    """ Режим работы на карте """
    redactor_mode_global = 1
    redactor_mode_tactic = 2
    game_mode_global = 3
    game_mode_tactic = 4

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта OperatingMode по значению
          :param value: значение """
        return OperatingMode(value)


class CombatModifiers(Enum):
    """ Боевые модификаторы """
    trench_modifier = 1
    ready_to_defend = 2
    ready_to_advance = 3

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта CombatModifiers по значению
          :param value: значение """
        return CombatModifiers(value)


class TypeResursesDeposit(Enum):
    """ Справочник видов месторождений """
    forest = 1
    fertile_soil = 2
    pasture = 3
    coal_deposit = 4
    oil_field = 5
    gas_field = 6
    iron_deposit = 7
    copper_deposit = 8
    polymetal_deposit = 9
    apatite_deposit = 10
    uranium_deposit = 11
    limestone_deposit = 12
    fish_area = 13
    place_for_dam = 14

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта TypeResursesDeposit по значению
          :param value: значение """
        return TypeResursesDeposit(value)


class TypeProduct(Enum):
    """ Справочник номенклатуры продукции """
    wood = 1
    vegetable_food = 2
    animal_food = 3
    fish_food = 4
    coal = 5
    oil = 6
    gas = 7
    iron_ore = 8
    copper_ore = 9
    polymetal_ore = 10
    limestone = 11
    uranium_ore = 12
    apatite = 13

    electricity = 14
    iron = 15
    copper = 16
    polymetal = 17
    uranium = 18
    plutonium = 19

    fertilizer = 20
    fish = 21
    cement = 22

    machines_and_equipment = 23

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта TypeProduct по значению
          :param value: значение """
        return TypeProduct(value)


class TypeMiningCompany(Enum):
    """ Справочник добывющих и производственных предприятий, расположенных вне городов """
    sawmills = 1
    farm = 2
    meat_farm = 3
    trawler = 4
    coal_mine = 5
    oil_company = 6
    oil_platform = 7
    gas_tower = 8
    iron_mine = 9
    copper_mine = 10
    polymetal_mine = 11
    limestone_mine = 12
    uranium_mine = 13
    apatite_mine = 14
    hydroelectric_power_stations = 15

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта TypeMiningCompany по значению
          :param value: значение """
        return TypeMiningCompany(value)


class TypeCompany(Enum):
    """ Справочник типов производственных и сервиснх компаний, расположенных в городах """
    # Электроэнергетика
    heat_power_station = 1
    gas_power_station = 2
    solar_power_station = 3
    wind_power_station = 4
    nuclear_power_station = 5

    # Машиностроение
    car_tractor_factory = 6
    shipyard = 7
    machine_tool_factory = 8

    # Военная промышленость
    weapons_factory = 9
    ammunition_factory = 10
    tank_factory = 11
    military_shipyard = 12
    aircraft_factory = 13

    # Перерабатывающая промышленность
    oil_refinery = 14
    petrochemical_factory = 15
    building_materials_factory = 16
    chemical_factory = 17
    steel_factory = 18
    copper_smelter = 19
    enrichment_plant = 20

    # Пищевая промышленность
    fish_processing_factory = 21

    # Социальная сфера
    university = 22
    medical_clinic = 23
    residential_complex = 24
    social_service = 25

    # Инфраструктура
    building_company = 26
    trucking_company = 27
    railway_company = 28
    air_company = 29
    sea_company = 3
    airport = 31
    sea_port = 32
    warehouse_complex = 33
    scientific_research_center = 34

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта TypeCompany по значению
          :param value: значение """
        return TypeCompany(value)


class MilitaryUnits(Enum):
    """ Типы боевых юнитов """
    # Пехота
    militia = 1
    infantry = 2
    elite_infantry = 3
    motorized_infantry = 4
    mechanized_infantry = 5
    marines = 6
    airborne_troops = 7

    # Артиллерия
    light_antitank_cannon_50 = 8
    antitank_cannon_76 = 9
    heavy_antitank_cannon_100 = 10
    cannon_76 = 11
    cannon_120 = 12
    cannon_150 = 13
    howitzer_120 = 14
    howitzer_150 = 15
    howitzer_200 = 16
    howitzer_300 = 17
    mortar_50 = 18
    mortar_80 = 19
    mortar_120 = 20

    # САУ
    self_propelled_cannon_76 = 21
    self_propelled_cannon_120 = 22
    self_propelled_cannon_150 = 23
    self_propelled_cannon_200 = 24
    self_propelled_antitank_76 = 25
    self_propelled_antitank_100 = 26
    self_propelled_antitank_120 = 27

    # Танки
    light_tank_50 = 28
    middle_tank_76 = 29
    heavy_tank_100 = 30
    super_heavy_tank_120 = 31

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта MilitaryUnits по значению
          :param value: значение """
        return MilitaryUnits(value)


class TypeMilitaryObject(Enum):
    """ Типы военных объектов """
    military_base = 1
    defensive_construction = 2
    military_warehouse = 3
    military_seaport = 4
    military_airport = 5

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта TypeMilitaryObject по значению
          :param value: значение """
        return TypeMilitaryObject(value)


class TypeRoad(Enum):
    """ Типы дорог """
    dirt_road = 1
    asphalt_road = 2
    highway = 3
    railway = 4

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта TypeRoad по значению
          :param value: значение """
        return TypeRoad(value)


class TypeAlliance(Enum):
    """ тип альянса """
    trade_alliance = 1
    military_alliance = 2

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта TypeAlliance по значению
          :param value: значение """
        return TypeAlliance(value)


class StatusState(Enum):
    """ Статус государства на карте """
    state_in_the_game = 1  # Доступные государства (Редактор)
    state_for_select = 2  # Государства доступные для выбора (Редактор)
    state_loser = 3  # Проигравшие государства (Игра)
    state_for_game = 4  # Государства в Игре, имеющие ходы
    state_player = 5  # Государство под управлением игрока

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта StatusState по значению
          :param value: значение """
        return StatusState(value)


class TypeFortification(Enum):
    """ Типы фотрификационных сооружений """
    pillbox = 1
    steel_pillbox = 2
    artillery_pillbox = 3
    artillery_tower = 4
    naval_guns = 5
    fortified_fort = 6
    air_defense_installations = 7

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта TypeFortification по значению
          :param value: значение """
        return TypeFortification(value)


class MilitarySubdivision(Enum):
    """ Огранизационные воинские подраздеения """
    # Минимальное подразделение (до 1 000 чел)
    battalion = 1
    # 3-4 батальона == полк (до 4 000 чел)
    regiment = 2
    # 3-4 полка == дивизия (до 16 000 чел)
    division = 3
    # 3-4 дивизии == армейский корпус (до 64 000 чел)
    army_corps = 4
    # 3-4 армейских корпуса == армия (до 256 000 чел)
    army = 5

    @staticmethod
    def get_instance(value):
        """ Извлечение объекта MilitarySubdivision по значению
          :param value: значение """
        return MilitarySubdivision(value)
