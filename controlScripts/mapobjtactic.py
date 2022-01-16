import pygame as pg
from controlScripts import mapobject
import guidestorage
from interfaceScripts import interfacesp
import math
import animations
from logging import Logging


class MilitaryTacticUnit(mapobject.BaseMapObject):
    """ Юниты на тактической карте """
    # Список словарей со стандартными значениями параметров юнитов
    standard_unit = {
        # Пехота
        guidestorage.MilitaryUnits.militia.name: {
            'type_military_unit': guidestorage.MilitaryUnits.militia, 'moral': 1,
            'max_count': 1000, 'health_unit': 10, 'overall_health': 10000, 'armor': 2, 'motion': 2, 'range_fire': 2,
            'fire_on_infantry': 1, 'fire_on_armor': 1, 'fire_on_aviation': 0, 'fire_on_fortification': 0,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},
        guidestorage.MilitaryUnits.infantry.name: {
            'type_military_unit': guidestorage.MilitaryUnits.infantry, 'moral': 2,
            'max_count': 1000, 'health_unit': 12, 'overall_health': 12000, 'armor': 0, 'motion': 3, 'range_fire': 2,
            'fire_on_infantry': 2, 'fire_on_armor': 2, 'fire_on_aviation': 1, 'fire_on_fortification': 1,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},
        guidestorage.MilitaryUnits.elite_infantry.name: {
            'type_military_unit': guidestorage.MilitaryUnits.elite_infantry, 'moral': 3,
            'max_count': 1000, 'health_unit': 15, 'overall_health': 15000, 'armor': 1, 'motion': 3, 'range_fire': 2,
            'fire_on_infantry': 3, 'fire_on_armor': 3, 'fire_on_aviation': 2, 'fire_on_fortification': 2,
            'salvo_per_turn': 2, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 2},

        # Мотопехота
        guidestorage.MilitaryUnits.motorized_infantry.name: {
            'type_military_unit': guidestorage.MilitaryUnits.motorized_infantry, 'moral': 2,
            'max_count': 900, 'health_unit': 12, 'overall_health': 10800, 'armor': 0, 'motion': 6, 'range_fire': 2,
            'fire_on_infantry': 2, 'fire_on_armor': 2, 'fire_on_aviation': 1, 'fire_on_fortification': 1,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},
        guidestorage.MilitaryUnits.mechanized_infantry.name: {
            'type_military_unit': guidestorage.MilitaryUnits.mechanized_infantry, 'moral': 3,
            'max_count': 600, 'health_unit': 20, 'overall_health': 12000, 'armor': 2, 'motion': 5, 'range_fire': 3,
            'fire_on_infantry': 3, 'fire_on_armor': 3, 'fire_on_aviation': 3, 'fire_on_fortification': 3,
            'salvo_per_turn': 2, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 2},

        # Противотанковые орудия
        guidestorage.MilitaryUnits.light_antitank_cannon_50.name: {
            'type_military_unit': guidestorage.MilitaryUnits.light_antitank_cannon_50, 'moral': 2,
            'max_count': 30, 'health_unit': 50, 'overall_health': 1500, 'armor': 2, 'motion': 2, 'range_fire': 4,
            'fire_on_infantry': 10, 'fire_on_armor': 30, 'fire_on_aviation': 0, 'fire_on_fortification': 5,
            'salvo_per_turn': 2, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 2},
        guidestorage.MilitaryUnits.antitank_cannon_76.name: {
            'type_military_unit': guidestorage.MilitaryUnits.antitank_cannon_76, 'moral': 2,
            'max_count': 24, 'health_unit': 60, 'overall_health': 1440, 'armor': 3, 'motion': 2, 'range_fire': 5,
            'fire_on_infantry': 15, 'fire_on_armor': 50, 'fire_on_aviation': 0, 'fire_on_fortification': 15,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},
        guidestorage.MilitaryUnits.heavy_antitank_cannon_100.name: {
            'type_military_unit': guidestorage.MilitaryUnits.heavy_antitank_cannon_100, 'moral': 3,
            'max_count': 18, 'health_unit': 70, 'overall_health': 1260, 'armor': 4, 'motion': 1, 'range_fire': 5,
            'fire_on_infantry': 20, 'fire_on_armor': 80, 'fire_on_aviation': 0, 'fire_on_fortification': 35,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},

        # Полевая артиллерия
        guidestorage.MilitaryUnits.cannon_76.name: {
            'type_military_unit': guidestorage.MilitaryUnits.cannon_76, 'moral': 2,
            'max_count': 27, 'health_unit': 60, 'overall_health': 1620, 'armor': 2, 'motion': 2, 'range_fire': 4,
            'fire_on_infantry': 40, 'fire_on_armor': 10, 'fire_on_aviation': 0, 'fire_on_fortification': 10,
            'salvo_per_turn': 2, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 2},
        guidestorage.MilitaryUnits.cannon_120.name: {
            'type_military_unit': guidestorage.MilitaryUnits.cannon_120, 'moral': 2,
            'max_count': 24, 'health_unit': 70, 'overall_health': 1680, 'armor': 3, 'motion': 1, 'range_fire': 4,
            'fire_on_infantry': 60, 'fire_on_armor': 20, 'fire_on_aviation': 0, 'fire_on_fortification': 30,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},
        guidestorage.MilitaryUnits.cannon_150.name: {
            'type_military_unit': guidestorage.MilitaryUnits.cannon_150, 'moral': 3,
            'max_count': 18, 'health_unit': 80, 'overall_health': 1440, 'armor': 3, 'motion': 1, 'range_fire': 5,
            'fire_on_infantry': 80, 'fire_on_armor': 30, 'fire_on_aviation': 0, 'fire_on_fortification': 70,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},

        # Гаубицы
        guidestorage.MilitaryUnits.howitzer_120.name: {
            'type_military_unit': guidestorage.MilitaryUnits.howitzer_120, 'moral': 2,
            'max_count': 21, 'health_unit': 60, 'overall_health': 1260, 'armor': 2, 'motion': 1, 'range_fire': 5,
            'fire_on_infantry': 60, 'fire_on_armor': 20, 'fire_on_aviation': 0, 'fire_on_fortification': 20,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},
        guidestorage.MilitaryUnits.howitzer_150.name: {
            'type_military_unit': guidestorage.MilitaryUnits.howitzer_150, 'moral': 2,
            'max_count': 18, 'health_unit': 70, 'overall_health': 1260, 'armor': 2, 'motion': 1, 'range_fire': 6,
            'fire_on_infantry': 90, 'fire_on_armor': 25, 'fire_on_aviation': 0, 'fire_on_fortification': 40,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},
        guidestorage.MilitaryUnits.howitzer_200.name: {
            'type_military_unit': guidestorage.MilitaryUnits.howitzer_200, 'moral': 3,
            'max_count': 12, 'health_unit': 90, 'overall_health': 1080, 'armor': 2, 'motion': 1, 'range_fire': 7,
            'fire_on_infantry': 120, 'fire_on_armor': 30, 'fire_on_aviation': 0, 'fire_on_fortification': 70,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},
        guidestorage.MilitaryUnits.howitzer_300.name: {
            'type_military_unit': guidestorage.MilitaryUnits.howitzer_300, 'moral': 4,
            'max_count': 9, 'health_unit': 120, 'overall_health': 1080, 'armor': 2, 'motion': 1, 'range_fire': 6,
            'fire_on_infantry': 200, 'fire_on_armor': 50, 'fire_on_aviation': 0, 'fire_on_fortification': 150,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},

        # Минометы
        guidestorage.MilitaryUnits.mortar_50.name: {
            'type_military_unit': guidestorage.MilitaryUnits.mortar_50, 'moral': 2,
            'max_count': 39, 'health_unit': 30, 'overall_health': 1080, 'armor': 0, 'motion': 3, 'range_fire': 3,
            'fire_on_infantry': 30, 'fire_on_armor': 5, 'fire_on_aviation': 0, 'fire_on_fortification': 4,
            'salvo_per_turn': 3, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 3},
        guidestorage.MilitaryUnits.mortar_80.name: {
            'type_military_unit': guidestorage.MilitaryUnits.mortar_80, 'moral': 2,
            'max_count': 33, 'health_unit': 40, 'overall_health': 1080, 'armor': 0, 'motion': 2, 'range_fire': 3,
            'fire_on_infantry': 50, 'fire_on_armor': 10, 'fire_on_aviation': 0, 'fire_on_fortification': 7,
            'salvo_per_turn': 2, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 2},
        guidestorage.MilitaryUnits.mortar_120.name: {
            'type_military_unit': guidestorage.MilitaryUnits.mortar_120, 'moral': 3,
            'max_count': 27, 'health_unit': 50, 'overall_health': 1080, 'armor': 0, 'motion': 2, 'range_fire': 4,
            'fire_on_infantry': 80, 'fire_on_armor': 15, 'fire_on_aviation': 0, 'fire_on_fortification': 12,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},

        # САУ - штурмовые орудия
        guidestorage.MilitaryUnits.self_propelled_cannon_76.name: {
            'type_military_unit': guidestorage.MilitaryUnits.self_propelled_cannon_76, 'moral': 2,
            'max_count': 30, 'health_unit': 120, 'overall_health': 1080, 'armor': 10, 'motion': 5, 'range_fire': 4,
            'fire_on_infantry': 40, 'fire_on_armor': 10, 'fire_on_aviation': 0, 'fire_on_fortification': 10,
            'salvo_per_turn': 2, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 2},
        guidestorage.MilitaryUnits.self_propelled_cannon_120.name: {
            'type_military_unit': guidestorage.MilitaryUnits.self_propelled_cannon_120, 'moral': 3,
            'max_count': 24, 'health_unit': 150, 'overall_health': 1080, 'armor': 20, 'motion': 4, 'range_fire': 5,
            'fire_on_infantry': 60, 'fire_on_armor': 20, 'fire_on_aviation': 0, 'fire_on_fortification': 30,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},
        guidestorage.MilitaryUnits.self_propelled_cannon_150.name: {
            'type_military_unit': guidestorage.MilitaryUnits.self_propelled_cannon_150, 'moral': 4,
            'max_count': 18, 'health_unit': 200, 'overall_health': 1080, 'armor': 30, 'motion': 3, 'range_fire': 6,
            'fire_on_infantry': 100, 'fire_on_armor': 30, 'fire_on_aviation': 1, 'fire_on_fortification': 70,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},
        guidestorage.MilitaryUnits.self_propelled_cannon_200.name: {
            'type_military_unit': guidestorage.MilitaryUnits.self_propelled_cannon_200, 'moral': 4,
            'max_count': 12, 'health_unit': 250, 'overall_health': 1080, 'armor': 20, 'motion': 2, 'range_fire': 6,
            'fire_on_infantry': 150, 'fire_on_armor': 50, 'fire_on_aviation': 2, 'fire_on_fortification': 120,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},

        # САУ - истребители танков
        guidestorage.MilitaryUnits.self_propelled_antitank_76.name: {
            'type_military_unit': guidestorage.MilitaryUnits.self_propelled_antitank_76, 'moral': 2,
            'max_count': 27, 'health_unit': 120, 'overall_health': 1080, 'armor': 20, 'motion': 4, 'range_fire': 4,
            'fire_on_infantry': 15, 'fire_on_armor': 50, 'fire_on_aviation': 0, 'fire_on_fortification': 15,
            'salvo_per_turn': 2, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 2},
        guidestorage.MilitaryUnits.self_propelled_antitank_100.name: {
            'type_military_unit': guidestorage.MilitaryUnits.self_propelled_antitank_100, 'moral': 3,
            'max_count': 21, 'health_unit': 150, 'overall_health': 1080, 'armor': 30, 'motion': 3, 'range_fire': 5,
            'fire_on_infantry': 20, 'fire_on_armor': 80, 'fire_on_aviation': 1, 'fire_on_fortification': 35,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},
        guidestorage.MilitaryUnits.self_propelled_antitank_120.name: {
            'type_military_unit': guidestorage.MilitaryUnits.self_propelled_antitank_120, 'moral': 4,
            'max_count': 18, 'health_unit': 250, 'overall_health': 1080, 'armor': 40, 'motion': 2, 'range_fire': 6,
            'fire_on_infantry': 30, 'fire_on_armor': 120, 'fire_on_aviation': 2, 'fire_on_fortification': 50,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},

        # Танки
        guidestorage.MilitaryUnits.light_tank_50.name: {
            'type_military_unit': guidestorage.MilitaryUnits.light_tank_50, 'moral': 2,
            'max_count': 45, 'health_unit': 80, 'overall_health': 1080, 'armor': 10, 'motion': 6, 'range_fire': 3,
            'fire_on_infantry': 30, 'fire_on_armor': 20, 'fire_on_aviation': 0, 'fire_on_fortification': 5,
            'salvo_per_turn': 2, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 2},
        guidestorage.MilitaryUnits.middle_tank_76.name: {
            'type_military_unit': guidestorage.MilitaryUnits.middle_tank_76, 'moral': 3,
            'max_count': 39, 'health_unit': 150, 'overall_health': 1080, 'armor': 25, 'motion': 5, 'range_fire': 4,
            'fire_on_infantry': 40, 'fire_on_armor': 40, 'fire_on_aviation': 0, 'fire_on_fortification': 10,
            'salvo_per_turn': 2, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 2},
        guidestorage.MilitaryUnits.heavy_tank_100.name: {
            'type_military_unit': guidestorage.MilitaryUnits.heavy_tank_100, 'moral': 4,
            'max_count': 30, 'health_unit': 250, 'overall_health': 1080, 'armor': 40, 'motion': 4, 'range_fire': 5,
            'fire_on_infantry': 50, 'fire_on_armor': 60, 'fire_on_aviation': 2, 'fire_on_fortification': 20,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1},
        guidestorage.MilitaryUnits.super_heavy_tank_120.name: {
            'type_military_unit': guidestorage.MilitaryUnits.super_heavy_tank_120, 'moral': 5,
            'max_count': 21, 'health_unit': 350, 'overall_health': 1080, 'armor': 50, 'motion': 3, 'range_fire': 5,
            'fire_on_infantry': 60, 'fire_on_armor': 80, 'fire_on_aviation': 3, 'fire_on_fortification': 30,
            'salvo_per_turn': 1, 'move_per_turn': 1, 'remains_move': 1, 'remains_salvo': 1}
    }

    def __init__(self,   screen, cell, type_unit: guidestorage.MilitaryUnits, unit_dict: dict):
        super().__init__(screen, cell)
        # id юнита в БД
        if not unit_dict:
            self.id_unit = self.id_object
        else:
            unit_dict.get('id_unit')
            if unit_dict.get('id_unit') > mapobject.BaseMapObject.last_id:
                mapobject.BaseMapObject.last_id = unit_dict.get('id_unit')

        # Ячейка, на которой располагается юнит
        self.cell = cell
        # Тип из перечисления MilitaryUnits
        self.type_military_unit = type_unit if not unit_dict else guidestorage.MilitaryUnits.get_instance(
            unit_dict.get('type_military_unit'))
        # Наименование подразделения (Юнита)
        self.name_unit = '' if not unit_dict else unit_dict.get('name_unit')

        # Максимальная численность единиц в подразделении
        self.max_count = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('max_count') if not unit_dict \
            else unit_dict.get('max_count')
        # Текущая численность единиц в подразделении
        self.current_count = self.max_count if not unit_dict else unit_dict.get('current_count')
        # Максимальное здоровье единицы
        self.health_unit = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('health_unit') if not unit_dict \
            else unit_dict.get('health_unit')
        # Общее здоровье подразделения
        self.overall_health = self.max_count * self.health_unit if not unit_dict else unit_dict.get('overall_health')

        # Броня единицы
        self.armor = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('armor') if not unit_dict else\
            unit_dict.get('armor')
        # Огонь единицы по пехоте
        self.fire_on_infantry = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('fire_on_infantry') if not\
            unit_dict else unit_dict.get('fire_on_infantry')
        # Огонь единицы по бронированным целям
        self.fire_on_armor = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('fire_on_armor') if not \
            unit_dict else unit_dict.get('fire_on_armor')
        # Огонь по воздушным целям
        self.fire_on_aviation = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('fire_on_aviation') if not \
            unit_dict else unit_dict.get('fire_on_aviation')
        # Огонь по воздушным целям
        self.fire_on_fortification = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('fire_on_fortification')\
            if not unit_dict else unit_dict.get('fire_on_fortification')

        # Дальность хода
        self.motion = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('motion') if not unit_dict else \
            unit_dict.get('motion')
        # Дальность огня
        self.range_fire = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('range_fire') if not unit_dict \
            else unit_dict.get('range_fire')
        # Базовая мораль
        self.moral = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('moral') if not unit_dict else \
            unit_dict.get('moral')

        # Скорострельность: количество выстрелов за ход
        self.salvo_per_turn = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('salvo_per_turn')\
            if not unit_dict else unit_dict.get('salvo_per_turn')
        # Количество передвижений за один ход
        self.move_per_turn = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('move_per_turn')\
            if not unit_dict else unit_dict.get('move_per_turn')
        # Количество оставшихся ходов (Для режима игры), не может ходить, если == 0
        self.remains_move = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('remains_move') \
            if not unit_dict else unit_dict.get('remains_move')
        # Количество оставшихся залпов (Для режима игры), не может стреллять, если == 0
        self.remains_salvo = MilitaryTacticUnit.standard_unit.get(type_unit.name).get('remains_salvo')\
            if not unit_dict else unit_dict.get('remains_salvo')
        # Модификаторы во время боя: объекты класса guidestorage.CombatModifiers
        self.modifiers = None

        # Принадлежность к стороне конфликта
        if not unit_dict or (unit_dict and unit_dict.get('state') == 0):
            self.state = None
        else:
            state = None
            for st in self.cell.map_manager.list_states:
                if st.id_state == unit_dict.get('state'):
                    state = st
                    break
            self.state = state

        # Иконка юнита на карте
        self.icon_unit = interfacesp.ImageMapObject(self.screen, 86 / 2 - 17, 100 / 2 - 17,
                                                    self.get_icon_unit(type_unit), cell=self.cell)
        # Краткая подпись у юнита
        self.text_unit = interfacesp.TextMapObject(self.screen, 86 / 2, 100 / 2 + 13,
                                                   lambda: self.get_text_unit(type_unit)[1],
                                                   color='white', font_name='Arial', font_size=10, cell=self.cell)
        # Надпись о здоровье юнита
        self.text_health = interfacesp.TextMapObject(self.screen, 86 / 2, 100 / 2 - 30,
                                                     lambda: str(self.overall_health),
                                                     color=self.get_color_text_health(), font_name='Arial',
                                                     font_size=10, cell=self.cell)
        # Иконка флага у юнита на карте
        self.flag_unit = interfacesp.ImageMapObject(self.screen, 86 / 2 + 22, 100 / 2 - 20,
                                                    self.get_icon_mini_flag(), cell=self.cell)
        self.flagpole = interfacesp.ImageMapObject(self.screen, 86 / 2 + 20, 100 / 2 - 20,
                                                   pg.image.load('Other/Flags_mini/flagpole.png'), cell=self.cell)

        # Иконка модификатора у юнита
        self.icon_modifier = None

    def Draw(self):
        """ Отрисовка юнита на тактической карте """
        self.icon_unit.Draw()
        self.text_unit.Draw(centralized=True)
        self.text_health.Draw(centralized=True)
        # Древко флага и флаг
        self.flagpole.Draw()
        self.flag_unit.Draw()

    def get_game_object_dict(self):
        """ Извлекает словарь объекта для последующей сериализации """

        game_object_dict = {
            'id_unit': self.id_unit, 'cell': self.cell.cell_id,
            'type_military_unit': self.type_military_unit.value, 'name_unit': self.name_unit,
            'max_count': self.max_count, 'current_count': self.current_count,
            'health_unit': self.health_unit, 'armor': self.armor,
            'fire_on_infantry': self.fire_on_infantry, 'fire_on_armor': self.fire_on_armor,
            'fire_on_aviation': self.fire_on_aviation, 'overall_health': self.overall_health,
            'fire_on_fortification': self.fire_on_fortification, 'motion': self.motion,
            'range_fire': self.range_fire, 'moral': self.moral,
            'state': self.state.id_state if self.state else 0,
            'salvo_per_turn': self.salvo_per_turn, 'move_per_turn': self.move_per_turn,
            'remains_move': self.remains_move, 'remains_salvo': self.remains_move}

        return game_object_dict

    def change_cell(self, old_cell, new_cell):
        """ Перемещаем юнит с одной ячейки на другую - делается ход
         :param old_cell - ячейка, с которой убирается юнит
         :param new_cell - ячейка, на которую перемещается юнит"""

        # Выключаем анимацию у ячейки
        if self.cell.map_manager.animations:
            self.cell.map_manager.animations.stop_playing_animation(self.cell, name_animation='action')

        # Переносим объект с одной ячейки на другую
        self.cell = new_cell
        new_cell.object_cell_list.append(self)
        new_cell.state = self.state
        old_cell.object_cell_list.remove(self)
        old_cell.state = None

        # Меняем атрибуты в ячейки в отрисовываемых элементах юнита
        self.icon_unit.cell = new_cell
        self.text_unit.cell = new_cell
        self.text_health.cell = new_cell
        self.flag_unit.cell = new_cell
        self.flagpole.cell = new_cell

        # Убавляем сделанный ход их возможных ходов юнита
        self.remains_move -= 1

        # Включаем анимацию активности, если юнит имеет ходы
        if self.remains_move > 0:
            animations.Animation(self.cell.map_manager.animations, self.cell.map_manager.animations.action_set,
                                 self.cell, 0, 7, animation_finite=False, name_animation='action')

    def open_fire(self, enemy_unit):
        """ Открытие огня по вражескому юниту
         :param enemy_unit - объект вражеского юнита """

        damage = self.calculate_damage_done(enemy_unit)
        if enemy_unit:
            enemy_unit.get_hit(damage)

        # Убавляем сделанный залп из возможных для юнита залпов
        self.remains_salvo -= 1

        return damage

    def get_hit(self, damage):
        """ Получение ущерба при вражеской атаке
         :param damage - нанесенный ущерб """

        # Получаем новое количество единиц в подразделении, округлив в большую сторону общее здоровье
        # после нанесенного ущерба
        self.current_count = math.ceil((self.overall_health - damage)/self.health_unit)
        self.overall_health -= damage

        # Юнит уничтожен
        if self.overall_health <= 0:
            self.delete_unit()
        # Юнит получил ущерб, совместимый с жизнью - обновляем надпись о здоровье
        else:
            # Надпись о здоровье юнита
            self.text_health = interfacesp.TextMapObject(self.screen, 86 / 2, 100 / 2 - 30,
                                                         lambda: str(self.overall_health),
                                                         color=self.get_color_text_health(), font_name='Arial',
                                                         font_size=10, cell=self.cell)

    def delete_unit(self):
        """ Удаляем объект юнита """

        # Удаляем юнита из реестра юнитов государства на карте

        if self in self.cell.map_manager.dict_list_unit_in_states.get(self.state.name_state):
            self.cell.map_manager.dict_list_unit_in_states.get(self.state.name_state).remove(self)
        # Удаляем юнита из реестра объектов ячейки
        if self in self.cell.object_cell_list:
            self.cell.object_cell_list.remove(self)
        # Удаляем ссылку ячейки владеющее ей государство
        self.cell.state = None
        self.cell.map_manager.check_of_state_without_units(self.state)
        Logging.logging_event(f" Уничтожен юнит {self.type_military_unit.name} страны "
                              f"{self.state.name_state} на ячейке {self.cell.cell_id}.")
        # Удаляем объект юнита
        del self

    def calculate_damage_done(self, enemy_unit):
        """ Расчет ущерба, нанесенного вражескому юниту
         :param enemy_unit - объект вражеского юнита """

        infantry_list = [
            guidestorage.MilitaryUnits.militia, guidestorage.MilitaryUnits.infantry,
            guidestorage.MilitaryUnits.elite_infantry, guidestorage.MilitaryUnits.motorized_infantry,
            guidestorage.MilitaryUnits.marines, guidestorage.MilitaryUnits.airborne_troops,
            guidestorage.MilitaryUnits.light_antitank_cannon_50, guidestorage.MilitaryUnits.antitank_cannon_76,
            guidestorage.MilitaryUnits.heavy_antitank_cannon_100, guidestorage.MilitaryUnits.cannon_76,
            guidestorage.MilitaryUnits.cannon_120, guidestorage.MilitaryUnits.cannon_150,
            guidestorage.MilitaryUnits.howitzer_120, guidestorage.MilitaryUnits.howitzer_150,
            guidestorage.MilitaryUnits.howitzer_200, guidestorage.MilitaryUnits.howitzer_300,
            guidestorage.MilitaryUnits.mortar_50, guidestorage.MilitaryUnits.mortar_80,
            guidestorage.MilitaryUnits.mortar_120
        ]

        armored_list = [
            guidestorage.MilitaryUnits.mechanized_infantry, guidestorage.MilitaryUnits.self_propelled_cannon_76,
            guidestorage.MilitaryUnits.self_propelled_cannon_120, guidestorage.MilitaryUnits.self_propelled_cannon_150,
            guidestorage.MilitaryUnits.self_propelled_cannon_200, guidestorage.MilitaryUnits.light_tank_50,
            guidestorage.MilitaryUnits.self_propelled_antitank_76, guidestorage.MilitaryUnits.middle_tank_76,
            guidestorage.MilitaryUnits.self_propelled_antitank_100, guidestorage.MilitaryUnits.heavy_tank_100,
            guidestorage.MilitaryUnits.self_propelled_antitank_120, guidestorage.MilitaryUnits.super_heavy_tank_120
        ]

        damage = 0

        if type(enemy_unit) == MilitaryTacticUnit:
            if enemy_unit.type_military_unit in infantry_list:
                damage = self.current_count * self.fire_on_infantry
            elif enemy_unit.type_military_unit in armored_list:
                damage = self.current_count * self.fire_on_armor

        return damage

    def get_color_text_health(self):
        """ Извлекает цвет для надписи со здоровьем юнита в зависимости от уровня здоровья """
        if self.overall_health/(self.max_count*self.health_unit) > 0.75:
            color = 'green'
        elif 0.75 >= self.overall_health/(self.max_count*self.health_unit) > 0.5:
            color = 'yellow'
        elif 0.5 >= self.overall_health/(self.max_count*self.health_unit) > 0.25:
            color = 'orange'
        else:
            color = 'red'

        return color

    def get_icon_mini_flag(self):
        """ Извлечение изображения мини флага для юнита """
        if not self.state:
            image_flag = pg.image.load('Other/Flags_mini/None_state.png')
        else:
            image_flag = pg.image.load(self.state.flag_mini)

        return image_flag

    @staticmethod
    def get_icon_unit(type_unit: guidestorage.MilitaryUnits):
        """ Извлечение изображения для каждого типа юнита
         :param type_unit: тип юнита класса guidestorage.MilitaryUnits"""
        path_icon_unit = {
            # Пехота и мотопехота
            guidestorage.MilitaryUnits.militia.name: r'MapObject/Units/inf_1_35.png',
            guidestorage.MilitaryUnits.infantry.name: r'MapObject/Units/inf_2_35.png',
            guidestorage.MilitaryUnits.elite_infantry.name: r'MapObject/Units/inf_3_35.png',
            guidestorage.MilitaryUnits.motorized_infantry.name: r'MapObject/Units/mot_inf_35.png',
            guidestorage.MilitaryUnits.mechanized_infantry.name: r'MapObject/Units/mech_inf_35.png',

            # Артиллерия
            guidestorage.MilitaryUnits.light_antitank_cannon_50.name: r'MapObject/Units/antitank_l_35.png',
            guidestorage.MilitaryUnits.antitank_cannon_76.name: r'MapObject/Units/antitank_m_35.png',
            guidestorage.MilitaryUnits.heavy_antitank_cannon_100.name: r'MapObject/Units/antitank_h_35.png',
            guidestorage.MilitaryUnits.cannon_76.name: r'MapObject/Units/cannon_76_35.png',
            guidestorage.MilitaryUnits.cannon_120.name: r'MapObject/Units/cannon_122_35.png',
            guidestorage.MilitaryUnits.cannon_150.name: r'MapObject/Units/cannon_150_35.png',
            guidestorage.MilitaryUnits.howitzer_120.name: r'MapObject/Units/howitzer_122_35.png',
            guidestorage.MilitaryUnits.howitzer_150.name: r'MapObject/Units/howitzer_150_35.png',
            guidestorage.MilitaryUnits.howitzer_200.name: r'MapObject/Units/howitzer_200_35.png',
            guidestorage.MilitaryUnits.howitzer_300.name: r'MapObject/Units/howitzer_300_35.png',
            guidestorage.MilitaryUnits.mortar_50.name: r'MapObject/Units/mortar_50_35.png',
            guidestorage.MilitaryUnits.mortar_80.name: r'MapObject/Units/mortar_80_35.png',
            guidestorage.MilitaryUnits.mortar_120.name: r'MapObject/Units/mortar_120_35.png',

            # САУ
            guidestorage.MilitaryUnits.self_propelled_cannon_76.name: r'MapObject/Units/say_76_35.png',
            guidestorage.MilitaryUnits.self_propelled_cannon_120.name: r'MapObject/Units/say_120_35.png',
            guidestorage.MilitaryUnits.self_propelled_cannon_150.name: r'MapObject/Units/say_150_35.png',
            guidestorage.MilitaryUnits.self_propelled_cannon_200.name: r'MapObject/Units/say_200_35.png',
            guidestorage.MilitaryUnits.self_propelled_antitank_76.name: r'MapObject/Units/say_at_76_35.png',
            guidestorage.MilitaryUnits.self_propelled_antitank_100.name: r'MapObject/Units/say_at_100_35.png',
            guidestorage.MilitaryUnits.self_propelled_antitank_120.name: r'MapObject/Units/say_at_120_35.png',

            # Танки
            guidestorage.MilitaryUnits.light_tank_50.name: r'MapObject/Units/tank_l_35.png',
            guidestorage.MilitaryUnits.middle_tank_76.name: r'MapObject/Units/tank_m_35.png',
            guidestorage.MilitaryUnits.heavy_tank_100.name: r'MapObject/Units/tank_h_35.png',
            guidestorage.MilitaryUnits.super_heavy_tank_120.name: r'MapObject/Units/tank_sh_35.png'
        }

        return pg.image.load(path_icon_unit.get(type_unit.name))

    @staticmethod
    def get_path_icon_unit(type_unit: guidestorage.MilitaryUnits):
        """ Извлечение изображения для каждого типа юнита
         :param type_unit: тип юнита класса guidestorage.MilitaryUnits"""
        path_icon_unit = {
            # Пехота и мотопехота
            guidestorage.MilitaryUnits.militia.name: r'MapObject/Units/inf_1_35.png',
            guidestorage.MilitaryUnits.infantry.name: r'MapObject/Units/inf_2_35.png',
            guidestorage.MilitaryUnits.elite_infantry.name: r'MapObject/Units/inf_3_35.png',
            guidestorage.MilitaryUnits.motorized_infantry.name: r'MapObject/Units/mot_inf_35.png',
            guidestorage.MilitaryUnits.mechanized_infantry.name: r'MapObject/Units/mech_inf_35.png',

            # Артиллерия
            guidestorage.MilitaryUnits.light_antitank_cannon_50.name: r'MapObject/Units/antitank_l_35.png',
            guidestorage.MilitaryUnits.antitank_cannon_76.name: r'MapObject/Units/antitank_m_35.png',
            guidestorage.MilitaryUnits.heavy_antitank_cannon_100.name: r'MapObject/Units/antitank_h_35.png',
            guidestorage.MilitaryUnits.cannon_76.name: r'MapObject/Units/cannon_76_35.png',
            guidestorage.MilitaryUnits.cannon_120.name: r'MapObject/Units/cannon_122_35.png',
            guidestorage.MilitaryUnits.cannon_150.name: r'MapObject/Units/cannon_150_35.png',
            guidestorage.MilitaryUnits.howitzer_120.name: r'MapObject/Units/howitzer_122_35.png',
            guidestorage.MilitaryUnits.howitzer_150.name: r'MapObject/Units/howitzer_150_35.png',
            guidestorage.MilitaryUnits.howitzer_200.name: r'MapObject/Units/howitzer_200_35.png',
            guidestorage.MilitaryUnits.howitzer_300.name: r'MapObject/Units/howitzer_300_35.png',
            guidestorage.MilitaryUnits.mortar_50.name: r'MapObject/Units/mortar_50_35.png',
            guidestorage.MilitaryUnits.mortar_80.name: r'MapObject/Units/mortar_80_35.png',
            guidestorage.MilitaryUnits.mortar_120.name: r'MapObject/Units/mortar_120_35.png',

            # САУ
            guidestorage.MilitaryUnits.self_propelled_cannon_76.name: r'MapObject/Units/say_76_35.png',
            guidestorage.MilitaryUnits.self_propelled_cannon_120.name: r'MapObject/Units/say_120_35.png',
            guidestorage.MilitaryUnits.self_propelled_cannon_150.name: r'MapObject/Units/say_150_35.png',
            guidestorage.MilitaryUnits.self_propelled_cannon_200.name: r'MapObject/Units/say_200_35.png',
            guidestorage.MilitaryUnits.self_propelled_antitank_76.name: r'MapObject/Units/say_at_76_35.png',
            guidestorage.MilitaryUnits.self_propelled_antitank_100.name: r'MapObject/Units/say_at_100_35.png',
            guidestorage.MilitaryUnits.self_propelled_antitank_120.name: r'MapObject/Units/say_at_120_35.png',

            # Танки
            guidestorage.MilitaryUnits.light_tank_50.name: r'MapObject/Units/tank_l_35.png',
            guidestorage.MilitaryUnits.middle_tank_76.name: r'MapObject/Units/tank_m_35.png',
            guidestorage.MilitaryUnits.heavy_tank_100.name: r'MapObject/Units/tank_h_35.png',
            guidestorage.MilitaryUnits.super_heavy_tank_120.name: r'MapObject/Units/tank_sh_35.png'
        }

        return path_icon_unit.get(type_unit.name)

    @staticmethod
    def get_text_unit(type_unit: guidestorage.MilitaryUnits):
        """ Извлечение текста для каждого типа юнита: полное и краткое наименование (в кортеже)
         :param type_unit: тип юнита класса guidestorage.MilitaryUnits"""
        text_unit = {
            # Пехота и мотопехота
            guidestorage.MilitaryUnits.militia.name: ('Ополчение', 'Ополчение'),
            guidestorage.MilitaryUnits.infantry.name: ('Пехота', 'Пехота'),
            guidestorage.MilitaryUnits.elite_infantry.name: ('Элитная пехота', 'Эл. пех'),
            guidestorage.MilitaryUnits.motorized_infantry.name: ('Моторизованная пехота', 'Мот. пех'),
            guidestorage.MilitaryUnits.mechanized_infantry.name: ('Механизированная пехота', 'Мех. пех'),

            # Артиллерия
            guidestorage.MilitaryUnits.light_antitank_cannon_50.name: ('Противотанковая пушка, 50мм', 'ПТ-пушка 50мм'),
            guidestorage.MilitaryUnits.antitank_cannon_76.name: ('Противотанковая пушка, 76мм', 'ПТ-пушка 76мм'),
            guidestorage.MilitaryUnits.heavy_antitank_cannon_100.name: ('Противотанковая пушка, 100мм',
                                                                        'ПТ-пушка 100мм'),
            guidestorage.MilitaryUnits.cannon_76.name: ('Пушка 76мм', 'Пушка 76мм'),
            guidestorage.MilitaryUnits.cannon_120.name: ('Пушка 120мм', 'Пушка 120мм'),
            guidestorage.MilitaryUnits.cannon_150.name: ('Пушка 150мм', 'Пушка 150мм'),
            guidestorage.MilitaryUnits.howitzer_120.name: ('Гаубица 120мм', 'Гаубица 120мм'),
            guidestorage.MilitaryUnits.howitzer_150.name: ('Гаубица 150мм', 'Гаубица 150мм'),
            guidestorage.MilitaryUnits.howitzer_200.name: ('Гаубица 200мм', 'Гаубица 200мм'),
            guidestorage.MilitaryUnits.howitzer_300.name: ('Гаубица 300мм', 'Гаубица 300мм'),
            guidestorage.MilitaryUnits.mortar_50.name: ('Миномет 50мм', 'Миномет 50мм'),
            guidestorage.MilitaryUnits.mortar_80.name: ('Миномет 80мм', 'Миномет 80мм'),
            guidestorage.MilitaryUnits.mortar_120.name: ('Миномет 120мм', 'Миномет 120мм'),

            # САУ
            guidestorage.MilitaryUnits.self_propelled_cannon_76.name:
                ('Самоходная артиллерийская установка 76мм', 'САУ 76мм'),
            guidestorage.MilitaryUnits.self_propelled_cannon_120.name:
                ('Самоходная артиллерийская установка 120мм', 'САУ 120мм'),
            guidestorage.MilitaryUnits.self_propelled_cannon_150.name:
                ('Самоходная артиллерийская установка 150мм', 'САУ 150мм'),
            guidestorage.MilitaryUnits.self_propelled_cannon_200.name:
                ('Самоходная артиллерийская установка 200мм', 'САУ 200мм'),
            guidestorage.MilitaryUnits.self_propelled_antitank_76.name:
                ('Противотанковая самоходная артиллерийская установка 76мм', 'ПТ-САУ 76мм'),
            guidestorage.MilitaryUnits.self_propelled_antitank_100.name:
                ('Противотанковая самоходная артиллерийская установка 100мм', 'ПТ-САУ 100мм'),
            guidestorage.MilitaryUnits.self_propelled_antitank_120.name:
                ('Противотанковая самоходная артиллерийская установка 120мм', 'ПТ-САУ 120мм'),

            # Танки
            guidestorage.MilitaryUnits.light_tank_50.name: ('Легкий танк 50мм', 'Л. Танк'),
            guidestorage.MilitaryUnits.middle_tank_76.name: ('Средний танк 760мм', 'С. Танк'),
            guidestorage.MilitaryUnits.heavy_tank_100.name: ('Тяжелый танк 100мм', 'Т. Танк'),
            guidestorage.MilitaryUnits.super_heavy_tank_120.name: ('Супер-тяжелый танк 120мм', 'СТ. Танк')
        }

        return text_unit.get(type_unit.name)
