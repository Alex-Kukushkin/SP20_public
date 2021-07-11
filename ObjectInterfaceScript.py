import pygame as pg
import WorkDataBases as wdb
import datetime as dt


class GameObject:
    """ Базовый класс объекта """
    def __init__(self, x, y, w, h):
        self.bounds = pg.rect.Rect(x, y, w, h)


class TextObject:
    """ Текстовый объект """
    def __init__(self, surface, x, y, text_func, color, font_name, font_size, name=''):
        self.surface = surface
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pg.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text_func())
        self.name = name

    def Draw(self, centralized=False):
        text_surface, self.bounds = self.get_surface(self.text_func())
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2,
                   self.pos[1])
        else:
            pos = self.pos
        self.surface.blit(text_surface, pos)

    def get_surface(self, text):
        text = str(text)
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()


class TextMapObject(TextObject):
    """ Текстовый объект на карте, привязанный к ячейкам """
    def __init__(self, surface, x, y, text_func, color, font_name, font_size, cell, name=''):
        super().__init__(surface, x, y, text_func, color, font_name, font_size, name)
        self.cell = cell

    def Draw(self, centralized=False):
        text_surface, self.bounds = self.get_surface(self.text_func())
        if centralized:
            pos = (self.cell.centrX + self.cell.map_manager.map_coordinates[0] + self.pos[0] - self.bounds.width // 2,
                   self.cell.centrY + self.cell.map_manager.map_coordinates[1] + self.pos[1])
        else:
            pos = (self.cell.centrX + self.cell.map_manager.map_coordinates[0] + self.pos[0],
                   self.cell.centrY + self.cell.map_manager.map_coordinates[1] + self.pos[1])
        self.surface.blit(text_surface, pos)


class ImageObject:
    """ Картинка """
    def __init__(self, surface, x, y, image, name=''):
        self.pos = (x, y)
        self.surface = surface
        self.image = image
        self.name = name

    def Draw(self):
        self.surface.blit(self.image, self.pos)


class ImageMapObject(ImageObject):
    """ Иконка на карте, которая привязана к определенной ячейке """
    def __init__(self, surface, x, y, image, cell, name=''):
        super().__init__(surface, x, y, image, name)
        self.cell = cell

    def Draw(self):
        self.surface.blit(self.image, (self.cell.centrX + self.cell.map_manager.map_coordinates[0] + self.pos[0],
                          self.cell.centrY + self.cell.map_manager.map_coordinates[1] + self.pos[1]))


class Button(GameObject):
    """ Кнопка """
    def __init__(self, surface, x, y, w, h, text, icon=None, on_click=lambda: None, padding=0,
                 button_color=(85, 107, 47),
                 button_text_color='red', font_name='Arial', font_size=20, name=''):
        super().__init__(x, y, w, h)
        self.surface = surface
        self.icon = icon
        self.button_color = button_color
        self.state = 'normal'
        self.on_click = on_click
        self.text = TextObject(self.surface, x + w//2 + padding, y + h//4 + padding, lambda: text, button_text_color,
                               font_name, font_size)
        self.name = name

    @property
    def back_color(self):
        return dict(normal=self.button_color,
                    hover='black',
                    pressed='white')[self.state]

    def Draw(self):
        """ Отрисовка кнопки """
        if not self.button_color and self.state == 'normal':
            pass
        else:
            pg.draw.rect(self.surface, self.back_color, self.bounds)

        self.text.Draw(centralized=True)
        if self.icon:
            self.surface.blit(self.icon, (self.bounds.x+2, self.bounds.y+2))

    def handle_mouse_move(self, pos):
        """ Подсветка кнопки при наведении """
        if self.bounds.collidepoint(pos):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        """" Подсветка кнопки при нажатии """
        if self.bounds.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        """ Запуск события при отжатии кнопки, на которой паходится курсор мыши """
        if self.bounds.collidepoint(pos) and self.state == 'pressed':
            self.on_click()
            self.state = 'hover'


class InputField(GameObject):
    """ Поле ввода """

    def __init__(self, surface, x, y, w, h, text='', on_click=lambda: None, padding=0,
                 button_text_color='red', font_name='Arial', font_size=20, name='', type_content='Str'):
        super().__init__(x, y, w, h)
        self.surface = surface
        self.editing = False
        self.on_click = on_click
        self.text_original = text
        self.text_displayed = text
        self.text = TextObject(self.surface, x + padding, y + padding, lambda: self.text_displayed, button_text_color,
                               font_name, font_size)
        self.name = name
        # type_content: 'Str', 'Int', 'Float'
        self.type_content = type_content

    def Draw(self):
        """ Отрисовка кнопки"""
        if self.editing:
            pg.draw.rect(self.surface, (238, 233, 233), self.bounds)
            self.text.Draw()
        elif not self.editing:
            pg.draw.rect(self.surface, (205, 201, 201), self.bounds)
            self.text.Draw()

    def field_mouse_down(self, pos):
        """" Включение/выключение режима редактирования при клике на поле ввода """
        if self.bounds.collidepoint(pos):
            if self.editing:
                self.editing = False
                self.on_click()

            elif not self.editing:
                self.editing = True
                self.text_displayed = self.text_original + '|'

    def key_back_spice(self):
        """ Удаление последнего символа из поля ввода """
        self.text_displayed = self.text_displayed[:-2] + '|'

    def key_other(self, symbol):
        """ Добавление символа в строку при вводе через клавиатуру """
        # self.text_original = self.text_original + symbol
        if self.type_content == 'Int' and symbol not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            symbol = ''
        elif self.type_content == 'Float' and symbol not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'):
            symbol = ''

        self.text_displayed = self.text_displayed[:-1] + symbol + '|'


class CheckBox(Button):
    def __init__(self, surface, x, y, w, h, text='', icon=None, on_click=lambda: None,
                 button_color=(255, 228, 225), name='', condition=False):
        super().__init__(surface, x, y, w, h, text, on_click=on_click, button_color=button_color, name=name)

        # Иконка галочки
        self.icon = pg.image.load('Icons/checkmark.png') if not icon else icon
        self.state = 'normal'

        self.condition = condition

    def Draw(self):
        """ Отрисовка чекбокса """
        pg.draw.rect(self.surface, self.back_color, self.bounds)
        if self.condition:
            self.surface.blit(self.icon, (self.bounds.x, self.bounds.y))

    def handle_mouse_up(self, pos):
        """ Запуск события при отжатии чекбокса, на которой паходится курсор мыши / перегруженный метод родителя"""
        if self.bounds.collidepoint(pos) and self.state == 'pressed':
            self.on_click()
            self.state = 'hover'
            self.condition = not self.condition


class Menu:
    def __init__(self, screen, chief_manager):
        self.chief_manager = chief_manager
        self.screen = screen

        # Список картинок и надписей
        self.image_and_text_list = list()

        # Фон и заголовок страницы меню
        self.menu_paint = pg.image.load('Other/begin_window_cut2.png')
        self.name_menu = TextObject(self.screen, 640, 100, lambda: 'МЕНЮ:', color='red', font_name='Arial',
                                    font_size=36)
        self.animations_set = [pg.image.load(f'Other/Fire_animation4/fire_{i}.png') for i in range(1, 49)]
        self.animations_i = 1
        # Отрисовка страницы главного меню
        self.MenuMain()

    # Отрисовка страниц меню
    def Draw(self):
        """ Отрисовка страниц меню  """
        self.screen.blit(self.animations_set[self.animations_i], (0, 0))
        self.animations_i += 1
        if self.animations_i == 48:
            self.animations_i = 1
            print('self.animations_i', self.animations_i)

        self.screen.blit(self.menu_paint, (0, 0))
        self.name_menu.Draw(centralized=True)

        for obj in self.image_and_text_list:
            obj.Draw()

        for button in self.chief_manager.button_list:
            button.Draw()

    # Меню редактора
    def MenuRedactor(self):
        """ Меню редактора """
        self.image_and_text_list.clear()
        self.chief_manager.button_list.clear()
        self.name_menu.text_func = lambda: 'РЕДАКТОР:'

        button_new = Button(self.screen, 550, 200, 150, 50, 'Назад', on_click=self.MenuMain)
        self.chief_manager.button_list.append(button_new)

        button_new = Button(self.screen, 550, 270, 150, 50, 'Новая', on_click=self.chief_manager.MMBegin)
        self.chief_manager.button_list.append(button_new)

        button_open = Button(self.screen, 550, 340, 150, 50, 'Загрузить', on_click=self.MenuSavingProjects)
        self.chief_manager.button_list.append(button_open)

    # Главное меню
    def MenuMain(self):
        """ Главное меню """
        self.name_menu.text_func = lambda: 'МЕНЮ:'

        self.image_and_text_list.clear()
        self.chief_manager.button_list.clear()

        if not self.chief_manager.map_manager_object:
            button_game = Button(self.screen, 550, 200, 150, 50, 'Играть', on_click=self.chief_manager.MMBegin)
            self.chief_manager.button_list.append(button_game)

            button_redactor = Button(self.screen, 550, 270, 150, 50, 'Редактор', on_click=self.MenuRedactor)
            self.chief_manager.button_list.append(button_redactor)

            button_setting = Button(self.screen, 550, 340, 150, 50, 'Настройки', on_click=quit)
            self.chief_manager.button_list.append(button_setting)

            button_quit = Button(self.screen, 550, 410, 150, 50, 'Выход', on_click=quit)
            self.chief_manager.button_list.append(button_quit)
        else:
            button_resume = Button(self.screen, 550, 200, 150, 50, 'Продолжить', on_click=self.chief_manager.Resume)
            self.chief_manager.button_list.append(button_resume)

            button_save = Button(self.screen, 550, 270, 150, 50, 'Сохранить', on_click=quit)
            self.chief_manager.button_list.append(button_save)

            button_game = Button(self.screen, 550, 340, 150, 50, 'Играть', on_click=self.chief_manager.MMBegin)
            self.chief_manager.button_list.append(button_game)

            button_redactor = Button(self.screen, 550, 410, 150, 50, 'Редактор', on_click=self.MenuRedactor)
            self.chief_manager.button_list.append(button_redactor)

            button_setting = Button(self.screen, 550, 480, 150, 50, 'Настройки', on_click=quit)
            self.chief_manager.button_list.append(button_setting)

            button_quit = Button(self.screen, 550, 550, 150, 50, 'Выход', on_click=quit)
            self.chief_manager.button_list.append(button_quit)

    def MenuSavingProjects(self):
        """ Меню загрузки сохраненных проектов редактора """
        self.chief_manager.button_list.clear()
        self.image_and_text_list.clear()

        self.name_menu.text_func = lambda: 'СОХРАНЕННЫЕ ПРОЕКТЫ:'

        img_panel = ImageObject(self.screen, 290, 150, pg.image.load('Other/panel_700_500.png'))
        self.image_and_text_list.append(img_panel)

        list_project = wdb.GetListDirectory()

        description_project = TextObject(self.screen, 310, 170, lambda: 'Проекты:', color='white', font_name='Arial',
                                         font_size=30)
        self.image_and_text_list.append(description_project)

        date_create = TextObject(self.screen, 600, 180, lambda: 'Дата создания:', color='white', font_name='Arial',
                                 font_size=20)
        self.image_and_text_list.append(date_create)

        date_create = TextObject(self.screen, 800, 180, lambda: 'Дата изменения:', color='white', font_name='Arial',
                                 font_size=20)
        self.image_and_text_list.append(date_create)

        y = 210
        for project in list_project:
            self.ButtonLoadProject(y, project)
            y += 50

        button_new = Button(self.screen, 550, 660, 150, 50, 'Назад', on_click=self.MenuRedactor)
        self.chief_manager.button_list.append(button_new)




    def ButtonLoadProject(self, y , name):
        """ Строка сохраненных проектов или игр """
        button_project = Button(self.screen, 310, y, 250, 40, name, on_click=quit)
        self.chief_manager.button_list.append(button_project)

        date_today = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        date_create = TextObject(self.screen, 600, y + 10, lambda: date_today, color='white', font_name='Arial',
                                 font_size=16)
        self.image_and_text_list.append(date_create)

        date_change = TextObject(self.screen, 800, y + 10, lambda: date_today, color='white', font_name='Arial',
                                 font_size=16)
        self.image_and_text_list.append(date_change)


class MenuMapManager:
    """ Отрисовка окон меню в режиме карты """
    def __init__(self, screen, map_manager, x, y, w, h, name, func, type_panel='fill_color', size_panel=1):
        # Ссылка на окно игры
        self.screen = screen

        # Ссылка на экмемпляр класса MapManager
        self.map_manager = map_manager

        # Панель окна меню
        self.menu_panel = GameObject(x, y, w, h)

        # 'fill_color' - прямоугольная область, заполненная цветом
        # 'transparent panel' - полупрозрачная панель с рамкой
        img_panel = None
        if type_panel == 'transparent panel':
            if size_panel == 1:
                img_panel = 'Other/panel_600_400.png'
            elif size_panel == 2:
                img_panel = 'Other/panel_700_500.png'
            else:
                img_panel = 'Other/panel_900_600.png'

        if img_panel:
            img_panel = pg.image.load(img_panel)
            sz = img_panel.get_size()
            w = sz[0]
            h = sz[1]

        self.menu_panel = GameObject(x, y, w, h)

        self.img_panel = ImageObject(self.screen, x, y, img_panel) if img_panel else None

        # Заголовок окна меню
        self.name_menu = TextObject(self.screen, x + w//2, y+20, lambda: name + ':', color='white', font_name='Arial',
                                    font_size=20)

        # Устанавливаем ссылку на текущий объект меню в экмемпляр класса MapManager
        self.map_manager.menu_object = self

        # Удаляем кнопки ячеек
        self.map_manager.MapManagerButtonClear()

        # Кнопка закрытия меню
        icon_close_img = pg.image.load('Icons/delete_icon_25.gif')
        button_close = Button(self.screen, x + w - 31, y + 2, 29, 29, '', icon=icon_close_img, on_click=self.Close)
        self.map_manager.chief_manager.button_list.append(button_close)
        self.map_manager.button_cell_list.append(button_close)

        # Запускаем функцию отрисовки кнопок панели (возможно и других элементов)
        func(self)

    # Отрисовка панели и заголовка меню
    def Draw(self):
        """ Отрисовка панели и заголовка меню """
        if not self.img_panel:
            pg.draw.rect(self.screen, (139, 134, 130), self.menu_panel.bounds)
        elif self.img_panel:
            self.img_panel.Draw()
        self.name_menu.Draw(centralized=True)

    # Закрытие окна меню
    def Close(self):
        """" Закрытие окна меню """
        # Удаляем кнопки меню
        self.map_manager.MapManagerButtonClear()

        # Отрисовываем кнопки ячейки
        if self.map_manager.CellSelected:
            self.map_manager.CellMenu()

        # Удаляем ссылку на объект меню в экмемпляре класса MapManager
        self.map_manager.menu_object = None


class MenuMapManagerWithTabs(MenuMapManager):
    def __init__(self, screen, map_manager, x, y, w, h, name, func, func_tabs):
        super().__init__(screen, map_manager, x, y, w, h, name, func, type_panel='transparent panel', size_panel=3)
        self.name_menu.pos = (self.name_menu.pos[0], self.name_menu.pos[1] + 70)
        self.func_tabs = func_tabs
        self.func_tabs(self)


class IndicatorOfLongProcess:
    """ Блокировка экрана и отображение индикатора прогресса выполнения при запуске длительных операций """
    def __init__(self, screen, chief_manager, description_process, func):
        self.screen = screen
        self.chief_manager = chief_manager
        self.description_process = description_process
        self.func = func
        self.__percent_process = 0

        self.closing_panel = ImageObject(self.screen, 0, 0, pg.image.load('Other/closing_panel.png'))

        # Текст описания длительного процесса
        self.description_text = TextObject(self.screen, 640, 305, lambda: self.description_process, color='white',
                                           font_name='Arial', font_size=20)
        self.chief_manager.map_manager_object.indicator_process = self

    def Draw(self):
        # Отрисовка закрывающей панели
        self.closing_panel.Draw()

        # Отрисовка панели контента
        pg.draw.rect(self.screen, (205, 183, 181), (490, 285, 300, 150))

        # Отрисовка текста описания длительного процесса
        self.description_text.Draw(centralized=True)

        # Отрисовка индикатора процесса
        pg.draw.line(self.screen, (139, 125, 123), (530, 365), (750, 365), width=10)
        pg.draw.line(self.screen, (139, 125, 123), (530, 395), (750, 395), width=10)
        pg.draw.line(self.screen, (139, 125, 123), (530, 365), (530, 405), width=10)
        pg.draw.line(self.screen, (139, 125, 123), (750, 365), (750, 405), width=10)
        pg.draw.line(self.screen, (50, 205, 50), (540, 375), (int(540+(2*self.percent_process)), 375), width=20)

    # Закрытие окна меню
    def Close(self):
        """" Закрытие блокирующего окна """
        # Удаляем ссылку на объект панели в экземпляре ChiefManager
        self.chief_manager.map_manager_object.indicator_process = None

    def SetPercentProcess(self, percent):
        """ Устанавливает процент выполнения процесса, если он равен 100, то окно закрывается  """
        if percent < 100:
            self.percent_process = percent
        else:
            self.Close()

    @property
    def percent_process(self):
        return self.__percent_process

    @percent_process.setter
    def percent_process(self, percent_process):
        try:
            percent_process = int(percent_process)

            if percent_process < 0:
                percent_process = 0
            elif percent_process > 100:
                percent_process = 100

            self.__percent_process = percent_process
        except ValueError:
            print('WARNING: Прогресс выполнения процесса должен быть целым числом от 0 до 100')
