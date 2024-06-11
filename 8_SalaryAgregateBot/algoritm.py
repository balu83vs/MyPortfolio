import json

from typing import Any

from db_con import DbConnector

from datetime import datetime, timedelta


class Algoritm:
    """
    Класс агрегации статистических данных.

    Принимает временной интервал, период группировки и входные данные из БД
    """

    def __init__(self, dt_from: datetime, dt_upto: datetime, group_type: str, input_data: DbConnector) -> None:
        self._dt_from = datetime.fromisoformat(dt_from)
        self._dt_upto = datetime.fromisoformat(dt_upto)
        self._group_type = group_type
        self._input_data = input_data
        self._cursor = self._input_data.find() 


    def month_days(self, date: datetime) -> int:
        """
        Функция выбора timedelta шага при месячной группировке
        """

        february_days = 28

        if date.year % 4 == 0:
            february_days = 29

        month_days = [31, february_days, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]    

        return month_days[date.month-1]    


    def date_interval_maker(self) -> list:
        """
        Функция генерации временного интервала в соответсвии с периодом группировки
        """

        date_interval = []
        start_date = self._dt_from

        while start_date <= self._dt_upto:
            date_interval.append(start_date)

            if self._group_type == 'hour':
                step = timedelta(hours=1)
            elif self._group_type == 'day': 
                step = timedelta(days=1)  
            elif self._group_type == 'month':
                step = timedelta(days=self.month_days(start_date))
            
            start_date += step
   
        return date_interval    
    

    def date_format(self, date: datetime) -> datetime:
        """
        Функция форматирования даты в соответствии с периодом группировки.

        Даты загрубляются до необходимой неточности.
        """

        year = date.year
        month = date.month
        day = date.day
        hour = date.hour    

        date_format_dict = {
            'month': datetime.strptime(f'{year} {month} 01', '%Y %m %d'),
            'day': datetime.strptime(f'{year} {month} {day}', '%Y %m %d'),
            'hour': datetime.strptime(f'{year} {month} {day} {hour}', '%Y %m %d %H')
            }
        
        formated_date = date_format_dict.get(self._group_type)

        return formated_date
    

    def data_filter_setup(self, group_type: datetime, data: list) -> list:
        """
        Функция фильтрования данных о зарплате в соответствии с нужным шаблоном временного интервала.

        Для каждого временного периода формируется отсортированный список 
        на базе которого, будет сформирован соответсвующий элемент результирующего словаря
        """

        filtered_data = {'hour': filter(lambda x: (x.get('dt').year == group_type.year and 
                                   x.get('dt').month == group_type.month and
                                   x.get('dt').day == group_type.day and
                                   x.get('dt').hour == group_type.hour), data),
                        'day': filter(lambda x: (x.get('dt').year == group_type.year and 
                                   x.get('dt').month == group_type.month and
                                   x.get('dt').day == group_type.day), data), 
                        'month': filter(lambda x: (x.get('dt').year == group_type.year and 
                                   x.get('dt').month == group_type.month), data),                    
        }
        result = list(filtered_data.get(self._group_type))
        return result


    def to_dict(self, filtered_cursor: list) -> dict:
        """
        Функция преобразования отфильтрованного списка в сгруппированный по датам словарь.

        - итерация по интервалу дат
        - подготовка данных для обработки
        - формирование результирующего словаря
        """

        result = dict()

        for date in self.date_interval_maker():

            group_type = self.date_format(date)
            data = self.data_filter_setup(group_type, filtered_cursor)

            if data:
                for el in data:
                    try:
                        result[group_type] += el.get('value')
                    except KeyError:
                        result.setdefault(group_type, el.get('value'))
            else:
                result.setdefault(group_type, 0)  

        return result

    
    def get_result(self):
        """
        Функция обработки и вывода конечного результата

        - формирование отсортированного по временному интервалу списка зарплат
        - преобразование списка зарплат в результирующий словарь
        - преобразование результирующего словаря в JSON для отправки в бот
        """

        filtered_cursor = [el for el in self._cursor 
                           if el.get('dt') >= self._dt_from and el.get('dt') <= self._dt_upto]

        result_dict = self.to_dict(filtered_cursor)

        json_result = json.dumps({"dataset": list(result_dict.values()),
                           "labels": [datetime.isoformat(key) for key in result_dict.keys()]})

        return json_result