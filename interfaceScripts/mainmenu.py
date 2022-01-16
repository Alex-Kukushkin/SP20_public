from interfaceScripts.interfacesp import BaseMenu, TextObject, Button, ImageObject, InputField
import pygame as pg
import databasessp
import datetime as dt
import guidestorage


class MainMenu(BaseMenu):
    """ Основное меню """
    def __init__(self, screen, chief_manager, count_page=0, up_pos=0, scroll=False, length_registry=0):
        """ Инициализация объекта основного меню
            :param screen: ссылка на экземпляр объекта окна программы класса pygame.Surface
            :param chief_manager: ссылка на экземпляр класса главного менеджера ChiefManager
            :param count_page: максимальное количество строк реестра для отрисовки на панели int
            :param up_pos: индекс верхнего элемента для отрисовки реестра int
            :param scroll: поле отображается наличие рееста для скроллирования на панели bool
            :param length_registry: общее количество элементов в списке для скроллирования int """

        super().__init__(screen, chief_manager, count_page=count_page, up_pos=up_pos, scroll=scroll,
                         length_registry=length_registry)
        self.name = 'Основное меню'

        # Список картинок и надписей
        self.image_and_text_list = list()

        # Фон и заголовок страницы меню
        self.menu_paint = pg.image.load('Other/begin_window_cut2.png')
        self.name_menu = TextObject(self.screen, 640, 100, lambda: 'МЕНЮ:', color='red', font_name='Arial',
                                    font_size=36)
        self.animations_set = [pg.image.load(f'Other/Fire_animation4/fire_{i}.png') for i in range(1, 49)]
        self.animations_i = 1

        # Отрисовка страницы главного меню
        self.menu_main()
        self.type_mode = None

    def Draw(self):
        """ Отрисовка страниц меню  """

        # todo Отрисовка анимации огня в главном меню - вынести в класс анимации
        self.screen.blit(self.animations_set[self.animations_i], (0, 0))
        self.animations_i += 1
        if self.animations_i == 48:
            self.animations_i = 1

        self.screen.blit(self.menu_paint, (0, 0))
        self.name_menu.Draw(centralized=True)

        for obj in self.image_and_text_list:
            obj.Draw()

        for button in self.chief_manager.button_list:
            button.Draw()

    def update_registry(self):
        """ Обновление списка при скролле """

        self.menu_saving_projects(self.type_mode)

    # Меню редактора
    def menu_redactor(self):
        """ Меню раздела редактор """

        self.image_and_text_list.clear()
        self.chief_manager.button_list.clear()
        self.up_pos = 0
        self.scroll = False
        self.length_registry = 0
        self.type_mode = None
        self.name_menu.text_func = lambda: 'РЕДАКТОР:'

        button_new = Button(self.screen, 550, 200, 200, 50, 'Назад',
                            on_click=self.menu_main)
        self.chief_manager.button_list.append(button_new)

        button_new_Global = Button(self.screen, 550, 270, 200, 50, 'Новая Global',
                                   on_click=lambda: self.chief_manager.start_map_manager(
                                       'Maps/map5.jpg', (0, 0), guidestorage.OperatingMode.redactor_mode_global))
        self.chief_manager.button_list.append(button_new_Global)

        button_new_Tactic = Button(self.screen, 550, 340, 200, 50, 'Новая Tactic',
                                   on_click=lambda: self.chief_manager.start_map_manager(
                                       'Maps/desert.jpg', (0, 0), guidestorage.OperatingMode.redactor_mode_tactic))
        self.chief_manager.button_list.append(button_new_Tactic)

        button_open_global = Button(self.screen, 550, 410, 200, 50, 'Загрузить Global',
                                    on_click=lambda: self.menu_saving_projects(guidestorage.OperatingMode.
                                                                               redactor_mode_global))
        self.chief_manager.button_list.append(button_open_global)

        button_open_tactic = Button(self.screen, 550, 480, 200, 50, 'Загрузить Tactic',
                                    on_click=lambda: self.menu_saving_projects(guidestorage.OperatingMode.
                                                                               redactor_mode_tactic))
        self.chief_manager.button_list.append(button_open_tactic)

    # Меню раздела Игра
    def menu_game(self):
        """ Меню раздела игра """

        self.image_and_text_list.clear()
        self.chief_manager.button_list.clear()
        self.name_menu.text_func = lambda: 'ИГРА:'

        button_new = Button(self.screen, 550, 200, 200, 50, 'Назад',
                            on_click=self.menu_main)
        self.chief_manager.button_list.append(button_new)

        button_new_Global = Button(self.screen, 550, 270, 200, 50, 'Новая Global',
                                   on_click=lambda: self.chief_manager.start_map_manager(
                                       'Maps/map5.jpg', (0, 0), guidestorage.OperatingMode.game_mode_global))
        self.chief_manager.button_list.append(button_new_Global)

        button_new_Tactic = Button(self.screen, 550, 340, 200, 50, 'Новая Tactic',
                                   on_click=lambda: self.chief_manager.start_map_manager(
                                       'Maps/desert.jpg', (0, 0), guidestorage.OperatingMode.game_mode_tactic))
        self.chief_manager.button_list.append(button_new_Tactic)

        button_open_global = Button(self.screen, 550, 410, 200, 50, 'Загрузить Global',
                                    on_click=lambda: self.menu_saving_games(guidestorage.OperatingMode.
                                                                            game_mode_global))
        self.chief_manager.button_list.append(button_open_global)

        button_open_tactic = Button(self.screen, 550, 480, 200, 50, 'Загрузить Tactic',
                                    on_click=lambda: self.menu_saving_games(guidestorage.OperatingMode.
                                                                            game_mode_tactic))
        self.chief_manager.button_list.append(button_open_tactic)

    # Главное меню
    def menu_main(self):
        """ Главное меню """

        self.name_menu.text_func = lambda: 'МЕНЮ:'

        self.image_and_text_list.clear()
        self.chief_manager.button_list.clear()

        if not self.chief_manager.map_manager_object:
            button_game = Button(self.screen, 550, 200, 200, 50, 'Играть', on_click=self.menu_game)
            self.chief_manager.button_list.append(button_game)

            button_redactor = Button(self.screen, 550, 270, 200, 50, 'Редактор', on_click=self.menu_redactor)
            self.chief_manager.button_list.append(button_redactor)

            button_setting = Button(self.screen, 550, 340, 200, 50, 'Настройки', on_click=quit)
            self.chief_manager.button_list.append(button_setting)

            button_quit = Button(self.screen, 550, 410, 200, 50, 'Выход', on_click=quit)
            self.chief_manager.button_list.append(button_quit)
        else:
            button_resume = Button(self.screen, 550, 200, 200, 50, 'Продолжить',
                                   on_click=self.chief_manager.resume_in_map)
            self.chief_manager.button_list.append(button_resume)

            button_save = Button(self.screen, 550, 270, 200, 50, 'Сохранить', on_click=self.window_save_project)
            self.chief_manager.button_list.append(button_save)

            button_game = Button(self.screen, 550, 340, 200, 50, 'Играть',
                                 on_click=self.chief_manager.start_map_manager)
            self.chief_manager.button_list.append(button_game)

            button_redactor = Button(self.screen, 550, 410, 200, 50, 'Редактор', on_click=self.menu_redactor)
            self.chief_manager.button_list.append(button_redactor)

            button_setting = Button(self.screen, 550, 480, 200, 50, 'Настройки', on_click=quit)
            self.chief_manager.button_list.append(button_setting)

            button_quit = Button(self.screen, 550, 550, 200, 50, 'Выход', on_click=quit)
            self.chief_manager.button_list.append(button_quit)

    def menu_saving_projects(self, type_mode: guidestorage.OperatingMode):
        """ Меню загрузки сохраненных проектов редактора
            :param type_mode: 'экземпляр класа режима работы с проектом guidestorage.OperatingMode """

        self.chief_manager.button_list.clear()
        self.image_and_text_list.clear()
        string_page = 8
        self.type_mode = type_mode

        self.name_menu.text_func = lambda: 'СОХРАНЕННЫЕ ПРОЕКТЫ:'

        img_panel = ImageObject(self.screen, 290, 150, pg.image.load('Other/panel_700_500.png'))
        self.image_and_text_list.append(img_panel)

        list_project = databasessp.SaveAndLoad.get_list_saves_project(type_mode)

        description_project = TextObject(self.screen, 310, 170, lambda: 'Проекты:', color='white', font_name='Arial',
                                         font_size=30)
        self.image_and_text_list.append(description_project)

        date_create = TextObject(self.screen, 600, 180, lambda: 'Дата создания:', color='white', font_name='Arial',
                                 font_size=20)
        self.image_and_text_list.append(date_create)

        date_create = TextObject(self.screen, 780, 180, lambda: 'Дата изменения:', color='white', font_name='Arial',
                                 font_size=20)
        self.image_and_text_list.append(date_create)

        if list_project:
            if len(list_project) > string_page:
                self.scroll = True
                self.length_registry = len(list_project)
                y = 215
                i = 0
                for project in list_project:
                    if self.up_pos <= i < (self.up_pos + string_page):
                        self.button_load_project(y, project)
                        y += 53
                    i += 1
            else:
                y = 210
                for project in list_project:
                    self.button_load_project(y, project)
                    y += 53

        else:
            no_projects = TextObject(self.screen, 410, 300, lambda: 'Нет сохраненных проектов!', color='white',
                                     font_name='Arial', font_size=30)
            self.image_and_text_list.append(no_projects)

        button_back = Button(self.screen, 550, 660, 150, 50, 'Назад', on_click=self.menu_redactor)
        self.chief_manager.button_list.append(button_back)

    def menu_saving_games(self, type_mode: guidestorage.OperatingMode):
        """ Меню загрузки сохраненных игр
            :param type_mode: 'экземпляр класа режима работы с проектом guidestorage.OperatingMode """

        self.chief_manager.button_list.clear()
        self.image_and_text_list.clear()
        string_page = 8
        self.type_mode = type_mode

        self.name_menu.text_func = lambda: 'СОХРАНЕННЫЕ ИГРЫ:'

        img_panel = ImageObject(self.screen, 290, 150, pg.image.load('Other/panel_700_500.png'))
        self.image_and_text_list.append(img_panel)

        list_project = databasessp.SaveAndLoad.get_list_saves_project(type_mode)

        description_project = TextObject(self.screen, 310, 170, lambda: 'Игры:', color='white', font_name='Arial',
                                         font_size=30)
        self.image_and_text_list.append(description_project)

        date_create = TextObject(self.screen, 600, 180, lambda: 'Дата создания:', color='white', font_name='Arial',
                                 font_size=20)
        self.image_and_text_list.append(date_create)

        date_create = TextObject(self.screen, 780, 180, lambda: 'Дата изменения:', color='white', font_name='Arial',
                                 font_size=20)
        self.image_and_text_list.append(date_create)

        if list_project:
            if len(list_project) > string_page:
                self.scroll = True
                self.length_registry = len(list_project)
                y = 215
                i = 0
                for project in list_project:
                    if self.up_pos <= i < (self.up_pos + string_page):
                        self.button_load_project(y, project)
                        y += 53
                    i += 1
            else:
                y = 210
                for project in list_project:
                    self.button_load_project(y, project)
                    y += 53

        else:
            no_projects = TextObject(self.screen, 410, 300, lambda: 'Нет сохраненных игр!', color='white',
                                     font_name='Arial', font_size=30)
            self.image_and_text_list.append(no_projects)

        button_back = Button(self.screen, 550, 660, 150, 50, 'Назад', on_click=self.menu_game)
        self.chief_manager.button_list.append(button_back)

    def menu_new_games(self, type_mode: guidestorage.OperatingMode):
        """ Меню загрузки сохраненных игр
            :param type_mode: 'экземпляр класа режима работы с проектом guidestorage.OperatingMode """

        self.chief_manager.button_list.clear()
        self.image_and_text_list.clear()
        string_page = 8
        self.type_mode = type_mode

        self.name_menu.text_func = lambda: 'СОХРАНЕННЫЕ ИГРЫ:'

        img_panel = ImageObject(self.screen, 290, 150, pg.image.load('Other/panel_700_500.png'))
        self.image_and_text_list.append(img_panel)

        list_project = databasessp.SaveAndLoad.get_list_saves_project(type_mode)

        description_project = TextObject(self.screen, 310, 170, lambda: 'Игры:', color='white', font_name='Arial',
                                         font_size=30)
        self.image_and_text_list.append(description_project)

        date_create = TextObject(self.screen, 600, 180, lambda: 'Дата создания:', color='white', font_name='Arial',
                                 font_size=20)
        self.image_and_text_list.append(date_create)

        date_create = TextObject(self.screen, 780, 180, lambda: 'Дата изменения:', color='white', font_name='Arial',
                                 font_size=20)
        self.image_and_text_list.append(date_create)

        if list_project:
            if len(list_project) > string_page:
                self.scroll = True
                self.length_registry = len(list_project)
                y = 215
                i = 0
                for project in list_project:
                    if self.up_pos <= i < (self.up_pos + string_page):
                        self.button_load_project(y, project)
                        y += 53
                    i += 1
            else:
                y = 210
                for project in list_project:
                    self.button_load_project(y, project)
                    y += 53

        else:
            no_projects = TextObject(self.screen, 410, 300, lambda: 'Нет сохраненных игр!', color='white',
                                     font_name='Arial', font_size=30)
            self.image_and_text_list.append(no_projects)

        button_back = Button(self.screen, 550, 660, 150, 50, 'Назад', on_click=self.menu_game)
        self.chief_manager.button_list.append(button_back)

    def button_load_project(self, y, saved_project):
        """ Строка сохраненных проектов или игр
        :param y: координата высоты отрисовки строки
        :param saved_project: экземпляры объектов класса сохранениий SaveAndLoadObject """

        button_project = Button(self.screen, 310, y, 250, 40, saved_project.name, font_size=16,
                                on_click=lambda: saved_project.load_project(self.chief_manager))
        self.chief_manager.button_list.append(button_project)

        # date_today = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        date_create = TextObject(self.screen, 600, y + 10, lambda: saved_project.datetime_create[:-7],
                                 color='white', font_name='Arial', font_size=14)
        self.image_and_text_list.append(date_create)

        date_change = TextObject(self.screen, 780, y + 10, lambda: saved_project.datetime_last_saving[:-7],
                                 color='white', font_name='Arial', font_size=14)
        self.image_and_text_list.append(date_change)

        button_delete_project = Button(self.screen, 930, y-2, 44, 44, '', icon=pg.image.load('Icons/delete_img.png'),
                                       font_size=16, on_click=quit)
        self.chief_manager.button_list.append(button_delete_project)

    def window_save_project(self):
        """ Окно сохранения проекта """

        self.chief_manager.button_list.clear()
        self.image_and_text_list.clear()

        self.name_menu.text_func = lambda: 'СОХРАНИТЬ ПРОЕКТ:'

        img_panel = ImageObject(self.screen, 290, 150, pg.image.load('Other/panel_700_500.png'))
        self.image_and_text_list.append(img_panel)

        # Описание уровня города
        description_input = TextObject(self.screen, 530, 220, lambda: 'Сохранить проект как: ',
                                       color='white', font_name='Arial', font_size=20)
        self.chief_manager.button_list.append(description_input)

        # Окно ввода названия файла сохранения
        name_save = 'Project_' + str(dt.datetime.now().strftime("%d.%m.%Y %H-%M-%S")) + '.db'
        name_save_input = InputField(self.screen, 440, 250, 400, 50, text=name_save, name='save_input',
                                     on_click=lambda: self.set_new_name_save_project(name_save_input))
        self.chief_manager.button_list.append(name_save_input)
        name_file = name_save

        # Кнопка сохранения проекта
        button_save = Button(self.screen, 550, 320, 150, 50, 'Сохранить',
                             on_click=lambda: self.save_project(name_file, name_save_input))
        self.chief_manager.button_list.append(button_save)

        # Возврат в предыдущее меню
        button_back = Button(self.screen, 550, 580, 150, 50, 'Назад', on_click=self.menu_redactor)
        self.chief_manager.button_list.append(button_back)

    @staticmethod
    def set_new_name_save_project(input_field):
        """ Установка названия проекта в поле ввода
        :param input_field: ссылка на экземпляр объекта поля ввода InputField """

        new_text = input_field.text_displayed.strip()[:-1]
        input_field.text_displayed = input_field.text_original = new_text

    def save_project(self, name_file, input_field):
        """ Сохранение проекта
        :param name_file: имя сохрпняемого проекта
        :param input_field: ссылка на экземпляр объекта поля ввода InputField """

        if not input_field.editing:
            name_saves = input_field.text_original
        else:
            name_saves = input_field.text_displayed.strip()[:-1]

        if self.chief_manager.map_manager_object:
            databasessp.create_DB(name_file, name_saves, self.chief_manager.map_manager_object)
        self.menu_redactor()
