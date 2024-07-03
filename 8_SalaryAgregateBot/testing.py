import json

ERROR_MESAGE = 'Невалидный запрос. Пример запроса: {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}'


class JsonError(Exception):
    """
    Пользовательское исключение
    """
    
    def __init__(self):
        self.message = ERROR_MESAGE


class TypeError(Exception):
    """
    Пользовательское исключение
    """
    
    def __init__(self):
        self.message = "Не правильный тип данных на входе"        


class TestInputData:
    """
    Класс тестирования входных данных

    Проверка соответсвия JSON

    Проверка типа данных на выходе из преобразования JSON

    Преобразование в JSON

    Формирование необходимых пользовательских исключений при наличии ошибок
    """
    
    def __init__(self, input_data):
        self._input_data = input_data


    def json_check(self):
        try:
            json_data = json.loads(self._input_data)
            if type(json_data) is not dict:
                raise JsonError
        except json.JSONDecodeError:
            raise JsonError
        else:
            return json_data   