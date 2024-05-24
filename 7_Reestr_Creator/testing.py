from datetime import datetime
from csv import DictReader


# Классы ошибок
class CSV_Error(Exception):
    """Ошибка при открытии файла CSV"""

    def __init__(self, message):
        super().__init__(message)

class INPUTDATA_ValueError(Exception):
    """Ошибка входных данных"""

    def __init__(self, message):
        super().__init__(message)

class INPUTDATA_TypeError(Exception):
    """Ошибка типа входных данных"""

    def __init__(self, message):
        super().__init__(message)        

class DateTime_Error(Exception):
    """Ошибка интервала дат"""

    def __init__(self, message):
        super().__init__(message)



class Testing: 
    """Класс тестирования"""


    # Проверка пути к исходному файлу csv
    def check_data_file(self, csv_path: str) -> str:
        try:
            file = open(csv_path)
        except Exception as err:
            raise CSV_Error(f'Ошибка при открытии файла CSV: {err}')
        else:
            print("CSV файл - OK")
            file.close()
            return csv_path
        

    # Проверка данных
    def check_data(self, inputdata: list) -> list:
        # проверка на пустой список
        if not inputdata:
            raise INPUTDATA_ValueError("Данные - Отсутствуют или повреждены!")
        # проверка на несоответсвие формата
        elif not isinstance(inputdata, (list, DictReader)):
            raise INPUTDATA_TypeError("Данные - неверного формата")   
        else:
            print('Данные - OK')  
            return inputdata


    # Проверка формата даты
    def check_formate_date(self, date: str, formate: str) -> datetime:
        try:
            date = datetime.strptime(date, formate) # перевод строки в формат даты и проверка шаблона 
        except Exception as error:
            raise DateTime_Error(f"Ошибка формата одной из дат! {error}") 
        else:
            print("Формат даты соответсвует")
            return date      


    # Проверка последовательности дат
    def check_position_date(self, start_date: str, stop_date: str, formate: str) -> tuple[datetime, datetime]:
        try:
            # проверка формата дат
            start_date = self.check_formate_date(start_date, formate)
            stop_date = self.check_formate_date(stop_date, formate)
        except Exception as error:    
            raise error
        else:    
            # смена позиций дат при несоответсвии порядку убывания
            if start_date > stop_date:
                stop_date, start_date = start_date, stop_date
            print('Интервал дат:', start_date, stop_date)
            return start_date, stop_date