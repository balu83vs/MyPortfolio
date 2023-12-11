import csv
import xlsxwriter

from datetime import datetime, timedelta 
from config_example import COLUMNS_CSV, COLUMNS_XLS, BASE_PRICE, SALE_PRICE
from config_example import COMPANY_NAME, HEAD_INFORMATIOM, ROWS_FORMATS, START_DATE, STOP_DATE

# проверка CSV-файла источника и XLSX-файла реультата 
def check_data_file() -> None:
    input_path = f"{input('Введите название исходного файла: ').split('.')[0]}.csv"
    
    #проверка доступности исходного файла CSV
    try:
        file = open(input_path)
    except Exception as err:
        print(f'Ошибка {err}. Проверьте наличие CSV файла в папке с программой!') 
        check_data_file()
    else:
        print('CSV файл - OK')
        file.close()
        output_path = f"{input('Введите название файла-реестра: ').split('.')[0]}.xlsx"
        return input_path, output_path


# основной класс программы
"""
содержит в себе: 
- методы создания базовой таблицы реестра для каждого тарифа и дня
- заголовка и подвала таблцы
- заполнения строк основными выходными данными
- вывод итоговой суммы за день 
"""
class Reestr:
    def __init__(self):
        self.start_date = datetime.strptime(START_DATE, '%d.%m.%Y') # дата начала реестра
        self.stop_date = datetime.strptime(STOP_DATE, '%d.%m.%Y')   # дата окончания реестра
        self.date_step = timedelta(days=1)
        self.column_data = []


    # основная функция создания реестра
    def create(self, input_path, output_path) -> None:
        
        with open(input_path, 'r', encoding = 'utf-8') as input_file:
            all_data = csv.DictReader(input_file, delimiter=';')
            list_data = [el for el in all_data]

            workbook = xlsxwriter.Workbook(output_path) # создание xls книги

            # проверка соответствию диапазона дат реестра
            while self.stop_date >= self.start_date:
                for price in [BASE_PRICE, SALE_PRICE]:
                    rows, worksheet = type(self).head_creator(self, workbook, price) # разметка заголовка листа
                    for line in list_data:
                        if line.get(COLUMNS_CSV[0]) == datetime.strftime(self.stop_date, '%d.%m.%Y'):
                            if line.get(COLUMNS_XLS[5]) == f'{BASE_PRICE}.0' and price == BASE_PRICE: 
                                type(self).column_data_creator(self, price, line) # заполнение списка значений строки для BASE_PRICE
                                type(self).row_writer(self, workbook, worksheet, rows)
                                self.column_data = [] 
                                rows += 1
                            elif line.get(COLUMNS_XLS[5]) != f'{BASE_PRICE}.0' and price == SALE_PRICE:
                                type(self).column_data_creator(self, price, line) # заполнение списка значений строки для SALE_PRICE
                                type(self).row_writer(self, workbook, worksheet, rows)
                                self.column_data = [] 
                                rows += 1
    
                    type(self).down_creator(self, workbook, worksheet, rows, price) # формирование подписи подвала

                self.stop_date -= self.date_step        
            workbook.close()


    # метод формирования заголовка листа
    def head_creator(self, workbook: any, price: int) -> any:
        rows = 8
        pixel_to_mm = 7.4
        column_wight_indexes = [10.14, 9.43, 13.86, 15.71, 12.14, 12.43]

        worksheet = workbook.add_worksheet(f"{datetime.strftime(self.stop_date, '%d.%m.%Y')}-{price}")

        worksheet.write(0, 0, COMPANY_NAME)
        worksheet.merge_range(1, 0, 1, 5, HEAD_INFORMATIOM[0], 
                              workbook.add_format(ROWS_FORMATS.get('merge_format_bold')))
        worksheet.merge_range(2, 0, 2, 5, HEAD_INFORMATIOM[1], 
                              workbook.add_format(ROWS_FORMATS.get('merge_format_bold')))
        worksheet.merge_range(3, 0, 3, 5, HEAD_INFORMATIOM[2], 
                              workbook.add_format(ROWS_FORMATS.get('merge_format')))
        worksheet.merge_range(6, 0, 6, 2, HEAD_INFORMATIOM[3], 
                              workbook.add_format(ROWS_FORMATS.get('merge_format_small')))
        worksheet.write(6, 3, f"{datetime.strftime(self.stop_date, '%d.%m.%Y')}")

        # заполнение заголовков и установка ширины для каждого столбца
        for i in range(len(COLUMNS_XLS)):
            worksheet.write(8, i, f'{COLUMNS_XLS[i]}')               
            worksheet.set_column_pixels(i, i, pixel_to_mm*column_wight_indexes[i])
        rows += 1
        return rows, worksheet
    

    # метод формирования подписи подвала
    def down_creator(self, workbook, worksheet, rows: int, price: int) -> None:          
        worksheet.write(rows, 0, 'Итого за:', 
                        workbook.add_format(ROWS_FORMATS.get('text_bold')))  
        worksheet.write(rows, 1, f"{datetime.strftime(self.stop_date, '%d.%m.%Y')}", 
                        workbook.add_format(ROWS_FORMATS.get('date_format_bold')))  
        worksheet.write_number(rows, 5, price*(rows-9), 
                               workbook.add_format(ROWS_FORMATS.get('summa_format_bold')))


    # метод заполнения содержимого столбцов
    def row_writer(self, workbook: any, worksheet: any, rows: int) -> any:
        worksheet.write_datetime(rows, 0, self.column_data[0], 
                                 workbook.add_format(ROWS_FORMATS.get('date_format')))
        worksheet.write_datetime(rows, 1, self.column_data[1], 
                                 workbook.add_format(ROWS_FORMATS.get('time_format')))        
        if self.column_data[2]:
            worksheet.write_number(rows, 2, int(self.column_data[2]), 
                                   workbook.add_format(ROWS_FORMATS.get('rrn_format')))       
        worksheet.write(rows, 3, f'{self.column_data[3]}', 
                        workbook.add_format(ROWS_FORMATS.get('autorisation_format')))     
        worksheet.write(rows, 4, f'{self.column_data[4]}')          
        worksheet.write_number(rows, 5, self.column_data[5], 
                               workbook.add_format(ROWS_FORMATS.get('summa_format'))) 
        return self
    

    # метод заполнения данными каждой строки
    def column_data_creator(self, price: int, line: dict) -> None:
        self.column_data.append(datetime.strptime(line.get(COLUMNS_CSV[0]), '%d.%m.%Y').date())
        self.column_data.append(datetime.strptime(line.get(COLUMNS_CSV[1]), '%H:%M:%S').time())
        self.column_data.append(line.get(COLUMNS_CSV[2]).strip('\u200b'))
        self.column_data.append(line.get(COLUMNS_CSV[3]))
        self.column_data.append(line.get(COLUMNS_CSV[4]))
        self.column_data.append(price)



# точка входа
if __name__ == '__main__':  
    # запуск проверки исходного файла
    input_path, output_path = check_data_file()
    
    # запуск основного модуля
    reestr = Reestr()
    reestr.create(input_path, output_path)
