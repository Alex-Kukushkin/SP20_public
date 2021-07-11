import pygame as pg
import ObjectInterfaceScript as ms
import MapManagerSP20 as mm
import WorkDataBases as wdb


class ChiefManager:
    """ Класс главного менеджера управления окнами и отрисовкой """
    def __init__(self, screen_window):
        self.func = self.DrawMenu
        self.screen = screen_window
        self.button_list = list()
        self.text_and_image_list = list()
        self.map_manager_object = None
        self.menu_object = ms.Menu(self.screen, self)

        # Объект активного поля ввода
        self.input_field_object = None
        wdb.GetListDirectory()

    # Отрисовка кадров в окне
    def Workflow(self):
        """ Отрисовка кадров в окне """
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        self.func()

        pg.display.update()

    # Отрисовка страницы меню
    def DrawMenu(self):
        """ Отрисовка страницы меню """
        self.menu_object.Draw()

    # Отрисовка страницы глобальной карты
    def DrawMap(self):
        """ Отрисовка страницы глобальной карты """
        if self.map_manager_object and type(self.map_manager_object) == mm.MapManager:
            self.map_manager_object.Draw()

    # Реакция на нажатие кнопки мыши
    def ButtonClick(self):
        """ Реакция на нажатие кнопки мыши """
        button_click = False
        for button in self.button_list:
            if button.bounds.collidepoint(event.pos):
                if type(button) == ms.Button or type(button) == ms.CheckBox:
                    button.handle_mouse_down(event.pos)

                elif type(button) == ms.InputField:
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
                and CM.func == self.DrawMap:
            self.map_manager_object.MouseClick()

    # Реакция на отжатие кнопки мыши
    def ButtonUp(self):
        """ Реакция на отжатие кнопки мыши """
        for button in self.button_list:
            if type(button) == ms.Button or type(button) == ms.CheckBox:
                button.handle_mouse_up(event.pos)

    # Реакция на перемещение кнопки мыши
    def ButtonMotion(self):
        """ Реакция на перемещение кнопки мыши """
        for button in self.button_list:
            if type(button) == ms.Button or type(button) == ms.CheckBox:
                button.handle_mouse_move(event.pos)

    # Создание экземпляра объекта глобальной карты
    def MMBegin(self):
        """ Создание экземпляра объекта глобальной карты """
        self.button_list.clear()
        self.map_manager_object = mm.MapManager(screen, self, size, 'Maps/map5.jpg', (0, 0))
        self.func = self.DrawMap

    # Переход на страницу меню
    def MenuEnable(self):
        """ Переход на страницу меню """
        self.button_list.clear()
        ms.Menu.MenuMain(self.menu_object)
        self.func = self.DrawMenu

    # Возврат на страницу карты
    def Resume(self):
        """ Возврат на страницу карты """
        self.button_list.clear()
        mm.MapManager.ButtonsAndObjectsCreate(self.map_manager_object)
        self.func = self.DrawMap

    @staticmethod
    def Get_color(pos):
        print(screen.get_at(pos))


# Основная ветка программы
if __name__ == "__main__":
    pg.init()
    size = (1280, 720)
    screen = pg.display.set_mode(size)
    pg.display.set_caption('STATE PROJECT 20')
    battalion_commander_img = pg.image.load('Other/battalion_commander.gif')

    pg.display.set_icon(battalion_commander_img)

    FPS = 24
    clock = pg.time.Clock()
    CM = ChiefManager(screen)
    while True:
        # Запуск метода отрисовки контента
        CM.Workflow()

        # Обработка событий игры
        for event in pg.event.get():
            # Выход из игры
            if event.type == pg.QUIT:
                quit()

            # Реакция игры на нажатие клавишь мыши
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # левая кнопка мыши
                    # if CM.map_manager_object and CM.func == CM.DrawMap:
                    #    CM.map_manager_object.MouseClick()
                    CM.ButtonClick()
                    CM.Get_color(event.pos)

                elif event.button == 3:  # правая кнопка мыши
                    if CM.map_manager_object and not CM.map_manager_object.doMove:
                        CM.map_manager_object.coordinates_fix = event.pos
                    if CM.map_manager_object:
                        CM.map_manager_object.doMove = True

            # Реакция игры на отжатие клавишь мыши
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:  # правая кнопка мыши
                    if CM.map_manager_object:
                        CM.map_manager_object.doMove = False
                elif event.button == 1:
                    CM.ButtonUp()

            # Реакция игры на движение мыши
            elif event.type == pg.MOUSEMOTION:
                CM.ButtonMotion()

                if CM.map_manager_object and not CM.map_manager_object.menu_object and \
                        CM.func == CM.DrawMap:
                    if CM.map_manager_object and CM.map_manager_object.doMove:
                        CM.map_manager_object.MouseRightDown()

            # Реакция игры на нажатие клавишь клавиатуры
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    if CM.input_field_object and len(CM.input_field_object.text_original) > 0:
                        CM.input_field_object.key_back_spice()
                else:
                    if CM.input_field_object:
                        CM.input_field_object.key_other(event.unicode)
