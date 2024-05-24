import xlsxwriter
import PySimpleGUI as sg

from typing import Union

from datetime import datetime, timedelta

from config_example import (
    COLUMNS_CSV,
    COLUMNS_XLS,
    BASE_PRICE,
    SALE_PRICE,
    COMPANY_NAME,
    HEAD_INFORMATION,
    ROWS_FORMATS,
)

from db_connector import DBConnector   
from testing import Testing 
                 


class Reestr:
    """Класс основной механики"""


    def __init__(self, xls_file: str, start_date: datetime, stop_date: datetime) -> None:
        self.xls_file = xls_file
        self.start_date = start_date
        self.stop_date = stop_date
        self.date_step = timedelta(days=1)
        self.column_data = []


    # Формируем заголовки на каждом листе
    def head_creator(self, workbook: any, price: int) -> Union[int, any]:
        rows = 8
        pixel_to_mm = 7.4
        column_wight_indexes = [10.14, 9.43, 13.86, 15.71, 12.14, 12.43]

        worksheet = workbook.add_worksheet(f"{datetime.strftime(self.stop_date, '%d.%m.%Y')}-{price}")

        worksheet.write(0, 0, COMPANY_NAME)

        worksheet.merge_range(1, 0, 1, 5, HEAD_INFORMATION[0],
                              workbook.add_format(ROWS_FORMATS.get("merge_format_bold")),
                              )
        worksheet.merge_range(2, 0, 2, 5, HEAD_INFORMATION[1],
                              workbook.add_format(ROWS_FORMATS.get("merge_format_bold")),
                              )
        worksheet.merge_range(3, 0, 3, 5, HEAD_INFORMATION[2],
                              workbook.add_format(ROWS_FORMATS.get("merge_format")),
                              )
        worksheet.merge_range(6, 0, 6, 2, HEAD_INFORMATION[3],
                              workbook.add_format(ROWS_FORMATS.get("merge_format_small")),
                              )
        
        worksheet.write(6, 3, f"{datetime.strftime(self.stop_date, '%d.%m.%Y')}")

        # заполнение заголовков столбцов
        for i in range(len(COLUMNS_XLS)):
            worksheet.write(8, i, f"{COLUMNS_XLS[i]}")  
            worksheet.set_column_pixels(i, i, pixel_to_mm * column_wight_indexes[i])  # ширина для каждого столбца
        rows += 1
        return rows, worksheet


    # формируем подписи подвала
    def down_creator(self, workbook: any, worksheet: any, rows: int, price: int) -> None:
        worksheet.write(rows, 0, "Итого за:", workbook.add_format(ROWS_FORMATS.get("text_bold")))
        worksheet.write(rows, 1, f"{datetime.strftime(self.stop_date, '%d.%m.%Y')}",
                        workbook.add_format(ROWS_FORMATS.get("date_format_bold")),
                        )
        worksheet.write_number(rows, 5, price * (rows - 9),
                               workbook.add_format(ROWS_FORMATS.get("summa_format_bold")),
                               )


    # заполняем содержимое столбцов
    def row_writer(self, workbook: any, worksheet: any, rows: int) -> any:
        worksheet.write_datetime(rows, 0, self.column_data[0],
                                 workbook.add_format(ROWS_FORMATS.get("date_format")),
                                    )
        worksheet.write_datetime(rows, 1, self.column_data[1],
                                 workbook.add_format(ROWS_FORMATS.get("time_format")),
                                    )
        if self.column_data[2]:
            worksheet.write_number(rows, 2, int(self.column_data[2]),
                                   workbook.add_format(ROWS_FORMATS.get("rrn_format")),
                                    )
        worksheet.write(rows, 3, f"{self.column_data[3]}", 
                        workbook.add_format(ROWS_FORMATS.get("autorisation_format")),
                            )
        worksheet.write(rows, 4, f"{self.column_data[4]}")
        worksheet.write_number(rows, 5, self.column_data[5],
                               workbook.add_format(ROWS_FORMATS.get("summa_format")),
                                )
        return self
    
  
    # формируем список данных для каждой строки
    def column_data_creator(self, price: int, data_line: list) -> None:
        self.column_data.append(datetime.strptime(data_line.get(COLUMNS_XLS[0]), '%d.%m.%Y').date())
        self.column_data.append(datetime.strptime(data_line.get(COLUMNS_XLS[1]), '%H:%M:%S').time())
        self.column_data.append(data_line.get(COLUMNS_XLS[2]).strip('\u200b'))
        self.column_data.append(data_line.get(COLUMNS_XLS[3]))
        self.column_data.append(data_line.get(COLUMNS_XLS[4]))
        self.column_data.append(price)   


    # формируем реестр
    def create(self) -> None:  
        workbook = xlsxwriter.Workbook(self.xls_file)  # создание xls книги
        # проходим по всему временному интервалу в документе
        while self.stop_date >= self.start_date:
            # формируем и проверяем входные данные алгоритма
            input_data = test_service.check_data(db_connector.export_from_db(self.stop_date))    
            # если данные в порядке
            if input_data:
                # два прохода для двух тарифов
                for price in [BASE_PRICE, SALE_PRICE]:
                    rows, worksheet = type(self).head_creator(self, workbook, price)  # разметка заголовка листа   
                    # итерация по входным данным
                    for data_line in input_data:
                        # проверка по дате
                        if data_line.get(COLUMNS_XLS[0]) == datetime.strftime(self.stop_date, "%d.%m.%Y"):
                            current_price = data_line.get('example_5') # стоимость поездки
                            # проверка соответствия тарифам
                            if (
                                (current_price == BASE_PRICE and price == BASE_PRICE) or 
                                (current_price != BASE_PRICE and price == SALE_PRICE)
                                ):
                                type(self).column_data_creator(self, price, data_line)  # заполнение данных для каждой строки 
                                type(self).row_writer(self, workbook, worksheet, rows) # заполнение содержимого столбцов
                                self.column_data = []
                                rows += 1 # следующая строка

                    # формирование подписи подвала
                    type(self).down_creator(self, workbook, worksheet, rows, price)  
                self.stop_date -= self.date_step # следующая дата
        print("Создание реестра завершено!") 
        workbook.close()
                


class GUI:
    """Класс пользовательского интерфейса"""


    # подготовка и загрузка основного интерфейса программы
    def window_initialize(self, csv: str = '', start_date: str = '', stop_date: str = '') -> sg.Window:

        # преобразование даты в строку
        if not isinstance(start_date, str):
            start_date = datetime.strftime(start_date, "%d.%m.%Y")
        if not isinstance(stop_date, str):
            stop_date = datetime.strftime(stop_date, "%d.%m.%Y")

        # набор элементов окна
        layout = [
            # поле ввода пути исходного файла
            [sg.Text("CSV-файл", size=(15, 1), auto_size_text=False, justification="right",),
             sg.InputText(default_text=csv, key="csv_file"),
             sg.FileBrowse("...", target="csv_file", initial_folder="csv_files"),
             sg.Button('OK')],
            # поле ввода пути файла реестра 
            [sg.Text("Файл реестра", size=(15, 1), auto_size_text=False, justification="right",),
             sg.InputText("Reestr_", key="reestr_file"),],
            # ручной ввод начала периода реестра 
            [sg.Text("Начало периода", size=(15, 1), auto_size_text=False, justification="right",),
             sg.InputText(default_text=start_date, key="start_date"),
             sg.CalendarButton("...", target="start_date", pad=None, format=("%d.%m.%Y"), close_when_date_chosen=True),],
            # ручной ввод конца периода реестра
            [sg.Text("Конец периода", size=(15, 1), auto_size_text=False, justification="right",),
             sg.InputText(default_text=stop_date, key="stop_date"),
             sg.CalendarButton("...", target="stop_date", pad=None, format=("%d.%m.%Y"), close_when_date_chosen=True),],
            # кнопки управления
            [sg.Button("Сформировать"), sg.Button("Закрыть")],
                ]
        
        # инициализация интерфейса
        window = sg.Window(f"Формирование реестра {COMPANY_NAME}", layout)
        return window


    # запуск интрефейса программы
    def user_interface(self) -> None:

        # установка темы окна
        sg.theme("DarkGreen")

        # формирование пользовательского интерфейса
        window = self.window_initialize()  
        
        # рабочая петля интерфейса
        while True:  
            event, values = window.read() # чтение события и данных из полей

            # условия выхода из программы
            if event in [sg.WIN_CLOSED, "Закрыть"]:  
                window.close()  # закрываем окно интерфейса
                db_connector.clear_db() # очистка БД
                break  

            # подготовка входных данных из CSV    
            if event == "OK":
                try:
                    db_connector.clear_db() # очистка БД

                    # формирование таблицы данных на основании CSV файла
                    db_connector.create_db_table()
                    db_connector.import_csv_to_db(values.get('csv_file'))

                    # автоматическое определение временных интервалов
                    start_date, stop_date = db_connector.min_max_date()

                    # проверка порядка и формата дат, а также их преобразование в datetime    
                    start_date, stop_date = test_service.check_position_date(start_date, stop_date, "%Y.%m.%d")
                except Exception as err:
                # при наличии ошибок останов программы 
                    sg.popup(no_titlebar=True, custom_text=f'{err}', )   
                else:
                    # закрываем окно интерфейса
                    window.close()  
                    # формирование пользовательского интерфейса с новыми данными
                    window = self.window_initialize(values.get('csv_file'), start_date, stop_date) 


            # запуск формирования реестра
            if event == "Сформировать":

                xlsx_files = values.get('reestr_file')  # файл назначения xlsx

                # проверка формата и порядка дат   
                try:
                    start_date, stop_date = test_service.check_position_date(values.get('start_date'), values.get('stop_date'), "%d.%m.%Y")
                except Exception as err:
                    sg.popup(no_titlebar=True, custom_text='Проблема с временным интервалом! Проверьте корректность дат.', )  
                else:
                    # экземпляр класса механики формирования реестра
                    reestr = Reestr(
                                    f'reestrs/{xlsx_files.split(".")[0]}.xlsx',
                                    start_date,
                                    stop_date,
                                )
                    # запуск основного модуля
                    try:
                        reestr.create()
                    except Exception as err:   
                        sg.popup(no_titlebar=True, custom_text=f"Создание реестра не завершено. Ошибка {err}!")
                    else:
                        sg.popup(no_titlebar=True, custom_text="Создание реестра завершено!")
        


# точка входа
if __name__ == "__main__":

    # подключаем пользовательский интерфейс
    gui = GUI() 
    test_service = Testing()
    db_connector = DBConnector() 
    gui.user_interface()
