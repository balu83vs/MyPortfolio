import sqlite3
import csv
from datetime import datetime

from config_example import (
    COLUMNS_CSV, COLUMNS_XLS
)

from testing import Testing



class DBConnector:
    '''Класс работы с базой данных'''


    def __init__(self):
        self.new_columns = {}                               # словарь эталонных и реальных столбцов csv файла

        # названия столбцов таблицы БД
        self.db_table_columns = [column_name.replace(' ', '_') for column_name in COLUMNS_CSV]
        self.db_table_columns.append('example_name')              


    # Функция создания таблицы с названиями столбцов из COLUMNS_CSV
    def create_db_table(self) -> None:

        # Создаем соединение с базой данных
        conn = sqlite3.connect('db/main.db')

        # Создаем курсор для выполнения операций с базой данных
        cursor = conn.cursor()

        # Создаем таблицу
        query = "CREATE TABLE IF NOT EXISTS main_table (id INTEGER PRIMARY KEY AUTOINCREMENT, {})"
        cursor.execute(query.format(
            f"{self.db_table_columns[0]} DATE," + 
            " TEXT,".join(self.db_table_columns[1:]) + 
            " INTEGER"))
        
        # Сохраняем изменения
        conn.commit()

        # Закрываем соединение
        conn.close()


    # Функция импорта содержимого CSV в базу данных
    def import_csv_to_db(self, csv_file: str) -> None:

        row = []

        # Создаем соединение с базой данных
        conn = sqlite3.connect('db/main.db')

        # Создаем курсор для выполнения операций с базой данных
        cursor = conn.cursor()

        # Проверяем корректность пути к csv файлу
        csv_file = Testing().check_data_file(csv_file)
        
        # Открываем csv файл для чтения
        with open(csv_file, "r", encoding="utf-8") as input_file:

            # проверка исходных данных
            input_data = Testing().check_data(csv.DictReader(input_file, delimiter=";"))

            if input_data:    
                # адаптируем надписи столбцов    
                for column in COLUMNS_CSV:
                    for new_column in input_data.fieldnames: 
                        if column in new_column:
                            self.new_columns.setdefault(new_column, column)

                # формируем строку данных для внесения в базу данных
                for data_dict in input_data:
                    for key in self.new_columns.keys():
                            if key == list(self.new_columns.keys())[0]:
                                # отдельно вносим в строку данных дату в формате datetime
                                row.append(datetime.strptime(data_dict.get(key), "%d.%m.%Y"))
                            else:  
                                # вносим все остальные данные
                                row.append(data_dict.get(key))
                    # вносим оплаченную сумму              
                    row.append(int(data_dict.get('example_5').split('.')[0]))          

                    # внесение в таблицу БД строки данных 
                    query = "INSERT INTO main_table ({}) VALUES ({})"    
                    cursor.execute(query.format(
                                            ", ".join(self.db_table_columns), 
                                            ", ".join(["?"] * len(self.db_table_columns))
                                                    ), row)    
                    row = [] # очистка строки данных

                print(f"Внесение данных в БД ... завершена успешно")

                # Сохраняем изменения
                conn.commit()

            # Закрываем соединение
            conn.close()

    
    # получение минимальной и максимальной даты набора
    def min_max_date(self) -> tuple[str, str]:

        # Создаем соединение с базой данных
        conn = sqlite3.connect('db/main.db')

        # Находим минимальную дату
        cursor_1 = conn.cursor()
        query = "SELECT MIN({}) FROM main_table"
        min_date = cursor_1.execute(query.format(self.db_table_columns[0])).fetchone()

        # Находим максимальную дату
        cursor_2 = conn.cursor()    
        query = "SELECT MAX({}) FROM main_table"
        max_date = cursor_2.execute(query.format(self.db_table_columns[0])).fetchone()

        # преобразуем формат %Y-%m-%d в формат %d%m%Y
        min_date = min_date[0].split(' ')[0].replace("-",".")
        max_date = max_date[0].split(' ')[0].replace("-",".")

        return min_date, max_date


    # выгрузка отсортированных по дате данных из БД
    def export_from_db(self, date) -> list:

        print('Проверка формата даты', type(date))

        sorting_data_list = []

        # Создаем соединение с базой данных
        conn = sqlite3.connect('db/main.db')

        # Создаем курсор для выполнения операций с базой данных
        cursor = conn.cursor()

        # Делаем выборку из таблицы по дате 
        query = "SELECT * FROM main_table WHERE {} = ?"  
        sorting_data = Testing().check_data(cursor.execute(query.format(self.db_table_columns[0]), (date,)).fetchall())

        # Если данные в порядке
        if sorting_data:
            # Преобразуем данные в словарь
            for row in sorting_data:
                sorting_date_dict = dict(zip(COLUMNS_XLS, row[1:]))
                date_type_date = datetime.strptime(sorting_date_dict.get(COLUMNS_XLS[0]).split(' ')[0], '%Y-%m-%d')
                date_type_str = datetime.strftime(date_type_date, '%d.%m.%Y')
                sorting_date_dict[COLUMNS_XLS[0]] = date_type_str
                sorting_data_list.append(sorting_date_dict) # формируем общий список словарей данных из БД
            print("Данные готовы к внесению в XLSX файл")       
            return sorting_data_list
    

    # очистка БД
    def clear_db(self) -> None:

        # Создаем соединение с базой данных
        conn = sqlite3.connect('db/main.db')

        # Создаем курсор для выполнения операций с базой данных
        cursor = conn.cursor()

        # Удаляем таблицу если она существует
        query = "DROP TABLE IF EXISTS main_table"
        cursor.execute(query)