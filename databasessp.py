import sqlite3
import os
import datetime as dt
import guidestorage
import json
import statessp
import pygame as pg


class SaveAndLoad:
    def __init__(self):
        """ Создает базу данных с информацией по сохраненным проектам, если её нет """
        self.list_project_redactor = list()
        self.list_save_game = list()
        if not os.path.exists('Saves/saves_db.db'):
            # Создаем базу данных настроек при первом входе
            with sqlite3.connect('Saves/saves_db.db') as con:
                print('Создаём базу данных saves_db')
                cur = con.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS saves (id integer primary key, path text, mode integer,
                date_create timestamp, date_change timestamp)''')
                con.commit()
                print('OK! Таблица информации по сохраненным проектам создана создана')

    def update_saved_project(self):
        """ Проверяет соответствие БД имеющимся в наличии файлам """

    @classmethod
    def get_list_saves_project(cls, game_mode: guidestorage.OperatingMode):
        """ Извлекает список с объектами SaveAndLoadObject по выбранному режиму работы
        :param game_mode: режим работы с проектом"""
        list_save_and_load_object = list()
        list_files = get_list_files_of_directory(game_mode)
        for files in list_files:
            with sqlite3.connect(get_folder(game_mode) + files) as con:
                cur = con.cursor()
                request = """ SELECT path_game, name_game, game_mode, date_create, date_change FROM settings """
                cur.execute(request)
                data = cur.fetchall()[0]
                list_save_and_load_object.append(SaveAndLoadObject(data[0], data[1], data[2], data[3], data[4]))

        return list_save_and_load_object


class SaveAndLoadObject:
    """  """
    def __init__(self, path, name, game_mode, date_create, date_change):
        self.path = path
        self.name = name
        self.game_mode = guidestorage.OperatingMode.get_instance(game_mode)
        self.datetime_create = date_create
        self.datetime_last_saving = date_change

    def load_project(self, chief_manager):
        """ Загружает сохраненные проекты и игры """
        with sqlite3.connect(get_folder(self.game_mode) + self.path + '.db') as con:
            cur = con.cursor()
            request = """ SELECT map_manager FROM settings """
            cur.execute(request)
            map_manager_str = cur.fetchall()[0][0]
            map_manager_dict = eval(map_manager_str)

            chief_manager.map_manager_object = None
            chief_manager.start_map_manager(map_manager_dict.get('map_path'),
                                            tuple(map_manager_dict.get('map_coordinates')),
                                            guidestorage.OperatingMode.get_instance(
                                                map_manager_dict.get('operating_mode')), self)

    def get_list_states(self):
        """ Извлекает список объектов государств """

        state_list = list()
        with sqlite3.connect(get_folder(self.game_mode) + self.path + '.db') as con:
            cur = con.cursor()
            request = """ SELECT state FROM states """
            cur.execute(request)
            states_str = cur.fetchall()

            for state in states_str:
                state_dict = eval(state[0])
                state_object = statessp.States(state_dict.get('name_state'), state_dict.get('flag'),
                                               state_dict.get('flag_mini'), state_dict.get('color_territory'),
                                               status_states=guidestorage.StatusState.get_instance(state_dict.get(
                                                   'status_states')), id_state=state_dict.get('id_state'),
                                               alliance=statessp.Alliance.get_object_alliance_by_id(state_dict.get(
                                                   'alliance')))
                if state_object.status_states in (guidestorage.StatusState.state_in_the_game,
                                                  guidestorage.StatusState.state_for_game,
                                                  guidestorage.StatusState.state_player):
                    state_object.object_color_territory = pg.image.load(state_object.color_territory)

                state_list.append(state_object)

        return state_list

    def get_list_alliances(self):
        """ Извлекает список объектов альянсов """

        alliances_list = list()
        with sqlite3.connect(get_folder(self.game_mode) + self.path + '.db') as con:
            cur = con.cursor()
            request = """ SELECT alliance FROM alliances """
            cur.execute(request)
            alliances_str = cur.fetchall()

            for alliance in alliances_str:
                alliance_dict = eval(alliance[0])
                alliance_object = statessp.Alliance(alliance_dict.get('name_alliance'),
                                                    guidestorage.TypeAlliance.get_instance(alliance_dict.get(
                                                        'type_alliance')), id_alliance=alliance_dict.get('id_alliance'))
                alliances_list.append(alliance_object)

        return alliances_list

    def get_dict_cells(self):
        """ Извлекает список словарей с информацией для десериализации ячеек """
        cell_list = list()
        with sqlite3.connect(get_folder(self.game_mode) + self.path + '.db') as con:
            cur = con.cursor()
            request = """ SELECT cell FROM cells """
            cur.execute(request)
            cell_str = cur.fetchall()

            for cell in cell_str:
                cell_dict = eval(cell[0])
                cell_list.append(cell_dict)

        return cell_list

    def get_dict_unit(self):
        """ Извлекает список словарей с информацией для десериализации юнитов """
        unit_list = list()
        with sqlite3.connect(get_folder(self.game_mode) + self.path + '.db') as con:
            cur = con.cursor()
            request = """ SELECT game_object FROM game_objects """
            cur.execute(request)
            unit_str = cur.fetchall()

            for unit in unit_str:
                unit_dict = eval(unit[0])
                unit_list.append(unit_dict)

        return unit_list

    def save_note_about_project(self):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(''' UPDATE notes SET item_id=?, typeitem_id=?, dateoperation=?, descriptoionoperation=?,
                               sumoperation=?, increase=?, source=?, typeinvestment_id=?, countnote=?, priseunit=? 
                                WHERE id=? ''', ())
            con.commit()

    def delete_saves_project(self):
        """ Удаляет файл сохраненного проекта или игры """
        pass


def get_folder(game_mode: guidestorage.OperatingMode):
    """ Возвращает папку в зависимости от типа Режима работы на карте
     :param game_mode: Режима работы на карте """
    if game_mode == guidestorage.OperatingMode.redactor_mode_global:
        directory_root = "Saves/SaveEditionGlobal/"
    elif game_mode == guidestorage.OperatingMode.redactor_mode_tactic:
        directory_root = "Saves/SaveEditionTactic/"
    elif game_mode == guidestorage.OperatingMode.redactor_mode_tactic:
        directory_root = "Saves/SaveGamesGlobal/"
    else:
        directory_root = "Saves/SaveGamesTactic/"

    return directory_root


def get_list_files_of_directory(game_mode: guidestorage.OperatingMode):
    """ Возвращает список сохранений в папке сохранения проектов """

    for root, dirs, files in os.walk(get_folder(game_mode)):
        """ Извлекает список сохраненных проектов редактора """
        return files


def create_DB(name_file, name_game, map_manager):
    """ Сохранение БД игры или редактора - сериализация объектов в базу даных"""

    directory_root = get_folder(map_manager.operating_mode)
    path = directory_root + name_file + '.db'

    # Таблица настроек
    if not os.path.exists(path):
        # Создаем базу данных настроек при первом сохранении
        with sqlite3.connect(path) as conn:
            # Сериализуем объект MapManager в формате JSON
            # Записываем поля объект MapManager в словарь
            map_manager_dict = {
                'map_path': map_manager.map_path, 'map_coordinates': map_manager.map_coordinates,
                'coordinates_fix': map_manager.coordinates_fix, 'operating_mode': map_manager.operating_mode.value
            }
            map_manager_json = str(json.dumps(map_manager_dict))

            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS settings(id integer primary key, path_game text, name_game text,
             game_mode integer, date_create timestamp, date_change timestamp, map_manager text)''')

            conn.commit()
            cur.execute('''INSERT INTO settings(path_game, name_game, game_mode,date_create, date_change, map_manager) 
            VALUES (?, ?, ?, ?, ?, ?)''', (
                name_file, name_game, map_manager.operating_mode.value, str(dt.datetime.today()),
                str(dt.datetime.today()), map_manager_json))
            conn.commit()
            print(f'OK! Таблица настроек в БД проекта {name_file} создана')

            # Таблица союзов государств
            cur.execute('''CREATE TABLE IF NOT EXISTS alliances (id integer primary key, alliance text)''')
            conn.commit()

            for alliance in map_manager.list_alliance:
                alliances_dict = {
                    'id_alliance': alliance.id_alliance, 'name_alliance': alliance.name_alliance,
                    'type_alliance': alliance.type_alliance.value
                }
                alliances_json = str(json.dumps(alliances_dict, ensure_ascii=False))

                cur.execute('''INSERT INTO alliances(alliance) VALUES (?)''', (alliances_json,))
                conn.commit()

            print(f'OK! Таблица союзов государств в БД проекта {name_file} создана')

            # Таблица государтв
            cur.execute('''CREATE TABLE IF NOT EXISTS states (id integer primary key, state text)''')
            conn.commit()
            for state in map_manager.list_states:
                alliance = state.alliance.id_alliance if state.alliance else 0
                state_dict = {
                    'id_state': state.id_state, 'name_state': state.name_state, 'state_player': str(state.state_player),
                    'flag': state.flag, 'flag_mini': state.flag_mini, 'color_territory': state.color_territory,
                    'status_states': state.status_states.value, 'alliance': alliance
                }
                state_json = str(json.dumps(state_dict, ensure_ascii=False))

                cur.execute('''INSERT INTO states(state) VALUES (?)''', (state_json,))
                conn.commit()

            print(f'OK! Таблица государств в БД проекта {name_file} создана')

            # Таблица ячеек
            cur.execute('''CREATE TABLE IF NOT EXISTS cells (id integer primary key, cell text)''')
            conn.commit()

            for cell in map_manager.Cells:
                cell_dict = {
                    'cell_id': cell.cell_id, 'centrX': cell.centrX, 'centrY': cell.centrY, 'Water': cell.Water,
                    'state': cell.state.id_state if cell.state else 0
                }

                cell_json = str(json.dumps(cell_dict))
                cur.execute('''INSERT INTO cells(cell) VALUES (?)''', (cell_json,))
                conn.commit()

            print(f'OK! Таблица ячеек в БД проекта {name_file} создана')

            # Таблица игровых объектов
            cur.execute('''CREATE TABLE IF NOT EXISTS game_objects (id integer primary key, game_object text)''')
            conn.commit()

            for cell in map_manager.Cells:
                for game_object in cell.object_cell_list:
                    # TODO написать метод для составления разных словарей для объектов разных типов, пока только
                    #  для тактических юнитов
                    game_object_dict = {
                        'id_unit': game_object.id_unit, 'cell': game_object.cell.cell_id,
                        'type_military_unit': game_object.type_military_unit.value, 'name_unit': game_object.name_unit,
                        'max_count': game_object.max_count, 'current_count': game_object.current_count,
                        'health_unit': game_object.health_unit, 'armor': game_object.armor,
                        'fire_on_infantry': game_object.fire_on_infantry, 'fire_on_armor': game_object.fire_on_armor,
                        'fire_on_aviation': game_object.fire_on_aviation, 'overall_health': game_object.overall_health,
                        'fire_on_fortification': game_object.fire_on_fortification, 'motion': game_object.motion,
                        'range_fire': game_object.range_fire, 'moral': game_object.moral,
                        'state': game_object.state.id_state if game_object.state else 0,
                        'salvo_per_turn': game_object.salvo_per_turn, 'move_per_turn': game_object.move_per_turn,
                        'remains_move': game_object.remains_move, 'remains_salvo': game_object.remains_move
                    }
                    game_object_json = str(json.dumps(game_object_dict, ensure_ascii=False))
                    cur.execute('''INSERT INTO game_objects(game_object) VALUES (?)''', (game_object_json,))
                    conn.commit()

            print(f'OK! Таблица игровых объектов в БД проекта {name_file} создана')
    else:
        print(f'WARNING! При сохранении проекта: {name_file} возникла проблема: БД уже существует')


# Метод изменения данных одного поля
def UpdateNoteDB(self, database, field, idname, data, iditem):
    """ Метод изменения данных одного поля таблицы """
    name_db = '{}.db'.format(database)
    self.conn = sqlite3.connect(name_db)
    self.c = self.conn.cursor()
    request = 'UPDATE {} SET {}=? WHERE {}=?'.format(database, field, idname)
    # print(request)
    self.c.execute(request, (data, iditem))
    self.conn.commit()
    print('В БД изменена запись по статье в одном поле {}-{}'.format(data, iditem))
    self.conn.close()


# Метод запроса данных
def request_select_DB(self, selection_fields, database, condition_fields=''):
    namedb = '{}.db'.format(database)
    self.conn = sqlite3.connect(namedb)
    self.c = self.conn.cursor()

    if condition_fields == '':
        request = 'SELECT {} FROM {} '.format(selection_fields, database)
    else:
        request = 'SELECT {} FROM {} WHERE {}'.format(selection_fields, database, condition_fields)

    # print(request)
    self.c.execute(request)
    data = self.c.fetchall()
    self.conn.close()
    return data
