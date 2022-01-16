class Logging:
    """ Логирование событий """
    @staticmethod
    def logging_event(text):
        """ Запись логов (пока в консоль, потом возможно и в файл)
         :param text: выводимый текст логов"""
        print(text)
