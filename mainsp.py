import pygame as pg
from interfaceScripts import interfacesp as isp
from interfaceScripts.mainmenu import MainMenu
from controlScripts import tacticmanager as tm
from controlScripts import globalmanager as gm
import databasessp
import guidestorage as gs


class ChiefManager:
    """ Класс главного менеджера управления окнами и отрисовкой """
    def __init__(self, screen_window: pg.Surface, size_window: tuple):
        self.func = self.draw_menu
        self.func2 = None
        # Ссылка на окно программы класса pygame.Surface
        self.screen = screen_window
        # Размер окна программы
        self.size_window = size_window
        # Список кнопок для отрисовки
        self.button_list = list()
        # Список текстовых и графических объектов для отрисовки
        self.text_and_image_list = list()
        # Ссылка на объект класса mapmanager.MapManager
        self.map_manager_object = None
        # Ссылка на объект меню класса interfasesp.Menu
        self.menu_object = MainMenu(self.screen, self)

        # Объект активного поля ввода
        self.input_field_object = None
        databasessp.SaveAndLoad()
        # Счетчик кадров/времени
        self.timer = 1
        # Метод действий AI
        self.method_AI = None

    # Отрисовка кадров в окне
    def work_flow(self):
        """ Отрисовка кадров в окне """
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        self.func()
        pg.display.update()
        self.timer += 1

        # Срабатывание метода искусственного интеллекта каждые 25 кадров
        if self.method_AI and self.timer % 25 == 0:
            self.method_AI()

    # Отрисовка страницы меню
    def draw_menu(self):
        """ Отрисовка страницы меню """
        self.menu_object.Draw()

    # Отрисовка страницы глобальной карты
    def draw_map(self):
        """ Отрисовка страницы глобальной карты """
        if self.map_manager_object:
            self.map_manager_object.Draw()

    # Реакция на нажатие кнопки мыши
    def button_click(self):
        """ Реакция на нажатие кнопки мыши """
        button_click = False
        for button in self.button_list:
            if button.bounds.collidepoint(event.pos):
                if type(button) == isp.Button or type(button) == isp.CheckBox:
                    button.handle_mouse_down(event.pos)

                elif type(button) == isp.InputField:
                    if self.input_field_object:
                        if self.input_field_object == button:
                            button.field_mouse_down(event.pos)
                            self.input_field_object = None
                        else:
                            self.input_field_object.editing = False
                            self.input_field_object.text_original = self.input_field_object.text_original.strip()
                            self.input_field_object.text_displayed = self.input_field_object.text_original
                            button.field_mouse_down(event.pos)
                            self.input_field_object = button

                    elif not self.input_field_object:
                        self.input_field_object = button
                        button.field_mouse_down(event.pos)

                button_click = True

        if not button_click and self.map_manager_object and not self.map_manager_object.menu_object\
                and CM.func == self.draw_map:
            self.map_manager_object.mouse_click()

    # Реакция на отжатие кнопки мыши
    def button_up(self):
        """ Реакция на отжатие кнопки мыши """

        for button in self.button_list:
            if type(button) == isp.Button or type(button) == isp.CheckBox:
                button.handle_mouse_up(event.pos)

    # Реакция на перемещение кнопки мыши
    def button_motion(self):
        """ Реакция на перемещение кнопки мыши """

        for button in self.button_list:
            if type(button) == isp.Button or type(button) == isp.CheckBox:
                button.handle_mouse_move(event.pos)

    def scroll_up(self):
        """ Реакция на скролл вверх """
        if self and self.menu_object:
            menu_object = self.menu_object if type(self.menu_object) == MainMenu\
                else self.map_manager_object.menu_object

            if menu_object.scroll:
                if menu_object.up_pos - 3 >= 0:
                    menu_object.up_pos -= 3
                    menu_object.update_registry()
                else:
                    menu_object.up_pos = 0
                    menu_object.update_registry()

    def scroll_down(self):
        """ Реакция на скролл вниз """
        if self and self.menu_object:
            menu_object = self.menu_object if type(self.menu_object) == MainMenu \
                else self.map_manager_object.menu_object
            one_page = 8 if type(self.menu_object) == MainMenu else 13
            if menu_object and menu_object.scroll:
                if menu_object.up_pos + 3 <= menu_object.length_registry - one_page:
                    menu_object.up_pos += 3
                    menu_object.update_registry()
                else:
                    menu_object.up_pos = menu_object.length_registry - one_page
                    menu_object.update_registry()

    def start_map_manager(self, maps: str, coord: tuple, operating_mode: gs.OperatingMode, saves=None):
        """ Создание экземпляра объекта карты
        :param maps: путь к файлу карты
        :param coord: координаты угла видимой области на карте
        :param operating_mode: вид режима карты из перечисления OperatingMode
        :param saves объект сохраненного проекта"""

        self.button_list.clear()
        if operating_mode == gs.OperatingMode.redactor_mode_global:
            self.map_manager_object = gm.RedactorManagerGlobal(self, maps, coord, operating_mode, saves)
        elif operating_mode == gs.OperatingMode.game_mode_global:
            self.map_manager_object = gm.GameManagerGlobal(self, maps, coord, operating_mode, saves)
        elif operating_mode == gs.OperatingMode.redactor_mode_tactic:
            self.map_manager_object = tm.RedactorManagerTactic(self, maps, coord, operating_mode, saves)
        elif operating_mode == gs.OperatingMode.game_mode_tactic:
            self.map_manager_object = tm.GameManagerTactic(self, maps, coord, operating_mode, saves)

        self.func = self.draw_map

    # Переход на страницу меню
    def menu_enable(self):
        """ Переход на страницу меню """

        self.button_list.clear()
        xxx = MainMenu(self.screen, self)
        xxx.menu_main()
        self.func = self.draw_menu

    # Возврат на страницу карты
    def resume_in_map(self):
        """ Возврат на страницу карты """

        self.button_list.clear()
        self.map_manager_object.buttons_and_objects_create()
        self.func = self.draw_map

    @staticmethod
    def get_color(pos):

        (screen.get_at(pos))


# Основная ветка программы
if __name__ == "__main__":
    # Создание окна программы
    pg.init()
    size = (1280, 720)
    screen = pg.display.set_mode(size)
    pg.display.set_caption('STATE PROJECT 20')
    pg.display.set_icon(pg.image.load('Other/battalion_commander.gif'))
    # Обновление экрана
    FPS = 10
    clock = pg.time.Clock()
    # Запуск генератора контента
    CM = ChiefManager(screen, size)
    while True:
        # Запуск метода отрисовки контента
        CM.work_flow()

        # Обработка событий, вызванных игроком
        for event in pg.event.get():
            # Выход из игры
            if event.type == pg.QUIT:
                quit()

            # Реакция игры на нажатие клавиш мыши
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # левая кнопка мыши
                    CM.button_click()

                elif event.button == 3:  # правая кнопка мыши
                    if CM.map_manager_object and not CM.map_manager_object.doMove:
                        CM.map_manager_object.coordinates_fix = event.pos
                    if CM.map_manager_object:
                        CM.map_manager_object.doMove = True

                elif event.button == 4:  # Скролл вверх
                    CM.scroll_up()

                elif event.button == 5:  # Скролл вниз
                    CM.scroll_down()

            # Реакция игры на отжатие клавиш мыши
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:  # правая кнопка мыши
                    if CM.map_manager_object:
                        CM.map_manager_object.doMove = False
                elif event.button == 1:
                    CM.button_up()

            # Реакция игры на движение мыши
            elif event.type == pg.MOUSEMOTION:
                CM.button_motion()

                if CM.map_manager_object and not CM.map_manager_object.menu_object and \
                        CM.func == CM.draw_map:
                    if CM.map_manager_object and CM.map_manager_object.doMove:
                        CM.map_manager_object.move_map_with_right_down_mouse_button()

            # Реакция игры на нажатие клавишь клавиатуры
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    if CM.input_field_object and len(CM.input_field_object.text_original) > 0:
                        CM.input_field_object.key_back_spice()
                else:
                    if CM.input_field_object:
                        CM.input_field_object.key_other(event.unicode)
