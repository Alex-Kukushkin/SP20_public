import sqlite3
import os
import datetime as dt
from enum import Enum


class SaveAndLoad:
    def __init__(self):
        self.list_project_redactor = list()
        self.list_save_game = list()


class SaveAndLoadObject:
    def __init__(self, path, game_mode):
        self.path = path
        self.game_mode = game_mode
        self.datetime_create = dt.datetime.today()
        self.datetime_last_saving = dt.datetime.today()


def GetListDirectory(game_mode=1):
    """ Возвращает список папок в папке сохранения проектов """
    directory_root = "SaveEdition/" if game_mode == 1 else "SaveGames/"
    for root, dirs, files in os.walk(directory_root):
        """ Извлекает список сохраненных проектов редактора """
        print('', dirs)
        return dirs


def CreateDB(self, name_directory, map_manager):
    """ Сохранение БД игры или редактора - сериализация объектов в базу даных"""
    if map_manager.operating_mode.value == 1:
        path = f'SaveEdition/{name_directory}/'
    else:
        path = f'SaveGames/{name_directory}/'

    # Таблица настроек
    if not os.path.exists(f'{path}setting.db'):
        # Создаем базу данных настроек при первом сохранении
        self.conn = sqlite3.connect('setting.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS setting (id integer primary key, map text, game_mode integer,
                coordinates_fix_x integer, coordinates_fix_y integer)''')
        self.conn.commit()
        self.c.execute('''INSERT INTO setting(map, game_mode, coordinates_fix_x, coordinates_fix_y) 
               VALUES (?, ?, ?, ?)''', (map_manager.map_path, map_manager.operating_mode.value,
                                        map_manager.coordinates_fix[0], map_manager.coordinates_fix[1]))
        self.conn.commit()
        print(f'OK! Таблица настроек в БД проекта {name_directory} создана')
        self.conn.close()
    else:
        print(f'WARNING! При сохранении проекта: {name_directory} возникла проблема: '
              f'Таблица настроек в БД уже существует')

    # Таблица союзов государств
    if not os.path.exists(f'{name_directory}alliances.db'):
        # Создаем базу данных настроек при первом сохранении
        self.conn = sqlite3.connect('alliances.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS alliances (id integer primary key, name_alliance text, 
                          type_alliance integer)''')
        self.conn.commit()

        i = 1
        for alliance in map_manager.object_operating_mode.list_alliance:
            self.c.execute('''INSERT INTO setting(name_alliance, type_alliance) 
                       VALUES (?, ?)''', (alliance.name_alliance, alliance.type_alliance.value))
            self.conn.commit()
            alliance.id_alliance = i
            i += 1

        print(f'OK! Таблица союзов государств в БД проекта {name_directory} создана')
        self.conn.close()
    else:
        print(f'WARNING! При сохранении проекта: {name_directory} возникла проблема: '
              f' Таблица союзов государств в БД уже существует')

    # Таблица государтв
    if not os.path.exists(f'{name_directory}states.db'):
        # Создаем базу данных государств при первом сохранении
        self.conn = sqlite3.connect('states.db')
        self.c = self.conn.cursor()

        i = 1
        self.c.execute('''CREATE TABLE IF NOT EXISTS states (id integer primary key, name_state text,
               flag_state text,  color_territory text, status_states integer,
               alliance_id integer references alliances(id))''')
        self.conn.commit()
        for state in map_manager.object_operating_mode.list_states:

            self.c.execute('''INSERT INTO setting(name_state, flag_state, color_territory, status_states alliance_id) 
            VALUES (?, ?, ?, ?, ?)''', (state.name_state, state.flag, state.color_territory, state.status_states.value,
                                        state.alliance.id_alliance if state.alliance else None))
            self.conn.commit()
            state.id_state = i

        print(f'OK! Таблица государств в БД проекта {name_directory} создана')
        self.conn.close()
    else:
        print(f'WARNING! При сохранении проекта: {name_directory} возникла проблема: '
              f' Таблица государств в БД уже существует')

    # Таблица ячеек
    if not os.path.exists(f'{name_directory}cells.db'):
        # Создаем базу данных настроек при первом сохранении
        self.conn = sqlite3.connect('cells.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS cells (id integer primary key, coordinate_x integer, 
                  coordinate_y integer, type_cell integer, owner_country_id integer references states(id))''')
        self.conn.commit()

        i = 1
        for cell in map_manager.Cells:
            self.c.execute('''INSERT INTO setting(map) VALUES (?, ?, ?, ?)''', (
                cell.centrX, cell.centrY, cell.Water, cell.state.id_state if cell.state else None))
            self.conn.commit()
            cell.cell_id = i
            i += 1

        print(f'OK! Таблица ячеек в БД проекта {name_directory} создана')
        self.conn.close()
    else:
        print(f'WARNING! При сохранении проекта: {name_directory} возникла проблема: '
              f' Таблица ячеек в БД уже существует')

    # *** Создаём БД прочих объектов карты ***
    for cell in map_manager.Cells:
        # *** Заполняем БД прочих объектов карты ***
        pass


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
def RequestSelectDB(self, selection_fields, database, condition_fields=''):
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
