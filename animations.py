import pygame as pg
from interfaceScripts import interfacesp


class Animations:
    """ Анимации на карте """
    def __init__(self, screen, map_manager):
        self.screen = screen
        self.map_manager = map_manager

        # Список кадров для анимации взрыва
        self.explosion_set = [pg.image.load(f'Other/Explosion/Explosion_{i}.png') for i in range(1, 22)]

        # Список кадров для анимации активности юнита
        self.action_set = [pg.image.load(f'Other/Action/action_{i}.png') for i in range(1, 37)]

        self.animations_registry = list()

    def get_count_frames(self, frames_set):
        """ Извлекает количество кадров в анимационном сете """
        count_frames = 0
        if frames_set is self.explosion_set:
            count_frames = 21
        if frames_set is self.action_set:
            count_frames = 36

        return count_frames

    def frame_switching_animations(self):
        """ Переключает кадр всех анимаций """
        for animation in self.animations_registry:
            if type(animation) == Animation or type(animation) == MovingInscription:
                animation.frame_switching()

    def stop_playing_animation(self, cell, name_animation=''):
        """ Прекратить проигрывание текущей анимации
         :param cell: ссылка на экземпляр ячейки
         :param name_animation: имя анимации """

        for animation in self.animations_registry:
            if name_animation:
                if animation.cell is cell and animation.name_animation == name_animation:
                    self.animations_registry.remove(animation)
            else:
                if animation.cell is cell:
                    self.animations_registry.remove(animation)

    def stop_playing_animations_for_name(self, name_animation):
        """ Прекратить проигрывание всех анимаций по имени
         :param name_animation: имя анимации """

        for animation in self.animations_registry:
            if animation.name_animation == name_animation:
                self.animations_registry.remove(animation)


class Animation:
    """ Анимация """
    def __init__(self, animations: Animations, use_animations_set: list, cell, x_coord: int,
                 y_coord: int, animation_finite=True, event=None, name_animation=''):
        # Ссылки на класс анимаций, менеджера карт и окно программы
        self.animations = animations
        self.name_animation = name_animation
        self.map_manager = animations.map_manager
        self.screen = self.map_manager.screen

        # Разовая или бесконечная отрисовка сценария анимации
        self.animation_finite = animation_finite
        # Текущий кадр анимации
        self.animations_i = 1
        # Проигрывающийся анимационный сет
        self.use_animations_set = use_animations_set
        # Количество фреймов в анимационном сете
        self.count_of_frames = Animations.get_count_frames(self.animations, self.use_animations_set)
        # Ячейка к которой привязана анимация
        self.cell = cell
        # Смещение анимации относительно координат ячейки
        self.x_coord = x_coord
        self.y_coord = y_coord

        # Добавляем экземпляр анимации в реестр анимаций класса Animations
        self.animations.animations_registry.append(self)
        # Событие, которое запускается в конце анимации
        self.event = event

    def frame_switching(self):
        """ Переключение кадров анимации """
        if self.animation_finite:
            if self.animations_i == self.count_of_frames:
                self.animations.stop_playing_animation(self.cell, self.name_animation)
                # Запуск события при наличии
                if self.event:
                    self.event()
                    self.event = None
                return
            else:
                next_frame = interfacesp.ImageMapObject(self.screen, self.x_coord, self.y_coord,
                                                        self.use_animations_set[self.animations_i - 1], self.cell)
                self.map_manager.text_and_image_animations_list.append(next_frame)
                self.animations_i += 1
        else:
            if self.use_animations_set:
                next_frame = interfacesp.ImageMapObject(self.screen, self.x_coord, self.y_coord,
                                                        self.use_animations_set[self.animations_i - 1], self.cell)
                self.map_manager.text_and_image_animations_list.append(next_frame)

                if self.animations_i == self.count_of_frames:
                    self.animations_i = 1
                else:
                    self.animations_i += 1


class MovingInscription(interfacesp.TextMapObject):
    """ Двигающиеся надписи """
    def __init__(self, animations: Animations, surface, x, y, text_func, color, font_name, font_size, cell, name='',
                 map_obj=False, registry_obj=False, count_frames=24, event=None, name_animation=''):
        super().__init__(surface, x, y, text_func, color, font_name, font_size, cell, name, map_obj=map_obj,
                         registry_obj=registry_obj)

        self.font_name = font_name
        self.font_size = font_size
        # Ссылки на класс анимаций
        self.animations = animations
        self.name_animation = name_animation
        # Событие, которое запускается в конце анимации
        self.event = event
        # Количество кадров на отрисовку надписи
        self.count_frames = count_frames
        # Текущий кадр анимации
        self.animations_i = 1
        # Добавляем экземпляр анимации в реестр анимаций класса Animations
        self.animations.animations_registry.append(self)

    def frame_switching(self):
        """ Переключение кадров анимации """
        if self.animations_i == self.count_frames:
            self.animations.animations_registry.remove(self)
            # Запуск события при наличии
            if self.event:
                self.event()
            return
        else:
            next_frame = interfacesp.TextMapObject(self.animations.screen, self.pos[0],
                                                   self.pos[1] + round(10-0.3*self.animations_i), self.text_func,
                                                   color=self.color, font_name=self.font_name,
                                                   font_size=round(self.font_size+0.5*self.animations_i),
                                                   cell=self.cell)
            self.animations.map_manager.text_and_image_animations_list.append(next_frame)
            self.animations_i += 1
