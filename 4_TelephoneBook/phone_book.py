import json
import itertools
import os  

from typing import Any, NoReturn

from config import TYPE_BASE, DB_TXT_FILE, DB_JSON_FILE, MENU_COMMAND_LIST, SHOW_COMMAND_LIST  # импорт настроек
from page_selection import Page_selection  # импорт класса постраничного вывода


# функция проверки файла базы данных
def check_dbfile(file) -> None:
    """
       проверяет, что доступен файл БД и создает новый если не найден 
    """
    try:
        file = open(file)
    except Exception as err:
        print(f'Ошибка {err}. Создан новый файл') 
        open(file, 'a')
    else:
        print('Файл базы данных - OK')
        file.close()



# класс записи в телефонной книге
class Phone_record:
    '''  
    содержит методы для: 
    - преобразования 
    - сравнения
    - вывода 
    информации содержащейся в каждой записи справочника.
    '''
    def __init__(self, last_name: Any, first_name: Any, patronymic: Any,
                 company: Any, work_number: Any, mobile_number: Any) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.company = company
        self.work_number = work_number
        self.mobile_number = mobile_number
    

    # метод вывода записи справочника в виде словаря
    def full_information(self) -> dict[str, Any]:
        return {'Фамилия': self.last_name, 'Имя': self.first_name, 'Отчестно': self.patronymic,
                'Название организации': self.company, 'Телефон рабочий': self.work_number,
                'Телефон личный (сотовый)': self.mobile_number}


    # магический метод равенства двух экземпляров класса Phone_record (запись справочника)
    def __eq__(self, other) -> bool:
        
        return all(
            [(self.last_name == other.last_name or other.last_name == ''),
             (self.first_name == other.first_name or other.first_name == ''),
             (self.patronymic == other.patronymic or other.patronymic == ''),
             (self.company == other.company or other.company == ''),
             (self.work_number == other.work_number or other.work_number == ''),
             (self.mobile_number == other.mobile_number or other.mobile_number == '')]
        )


    # формальное представление записи справочника
    def __str__(self) -> str:
        return f"Фамилия: {self.last_name}  Имя: {self.first_name}  Отчестно: {self.patronymic}  
        Название компании: {self.company}  Телефон рабочий: {self.work_number}  
        Телефон личный (сотовый): {self.mobile_number}"



# класс телефонной книги 
class Phone_book:
    ''' 
    обеспечивает: 
    - добавление новых записей 
    - поиск и редактирование имеющихся записей
    содержит статические методы для загрузки и выгрузки информации в файл БД
    '''


    # метод добавления новой записи
    def add_record(self) -> NoReturn:
        record = Phone_record(input('Введите Фамилию: '), input('Введите Имя: '), input('Введите Отчество: '),
                              input('Введите Название компании: '), input('Телефон рабочий: '),
                              input('Телефон личный (сотовый): '))
        
        # проверка типа базы данных
        if TYPE_BASE == 1:
            records_data_txt = type(self).txt_load()
            type(self).txt_upload_new(record, records_data_txt)
        else:
            records_data_json = type(self).json_load()
            type(self).json_upload(record, records_data_json)


    # метод редактирования записи
    def edit_record(self, record_id: str) -> NoReturn | str:

        # проверка типа базы данных
        if TYPE_BASE == 1:
            records_data = type(self).txt_load()
            db_file = DB_TXT_FILE
        else:
            records_data = type(self).json_load()
            db_file = DB_JSON_FILE

        if records_data.get(record_id):
            record = Phone_record(input('Введите Фамилию: '), input('Введите Имя: '), input('Введите Отчество: '),
                                  input('Введите Название компании: '),
                                  input('Телефон рабочий: '), input('Телефон личный (сотовый): '))
            
            records_data[record_id].update(record.full_information())
            
            # проверка корректности создания новой записи
            try:
                type(self).record_modification(db_file, records_data)
            except Exception as err:
                print('В процессе добавления новой записи возникла ошибка', err) 
            else:
                print('Новая запись успешно добавлена')       
        else:
            print(f'Запись с record_id: {record_id} не найдена!')


    # мтод поиска записей по одному или нескольким критериям
    def find_record(self, search_points: dict) -> dict:
        find_res_dict = {}

        # проверка типа базы данных
        if TYPE_BASE == 1:
            records_data = type(self).txt_load()
        else:
            records_data = type(self).json_load()

        # блок обработки данных и поиска совпадений по критериям поиска
        if records_data:
            find_record = Phone_record(*list(search_points.values()))
            for key, value in records_data.items():
                current_record = Phone_record(*list(value.values()))
                if current_record == find_record:
                    find_res_dict.setdefault(
                        key, current_record.full_information())
        return find_res_dict


    # метод загрузки данных из TXT файла 
    @staticmethod
    def txt_load() -> dict:
        records_data = {}

        # открываем файл БД для добавления записей
        with open(DB_TXT_FILE, 'w+', encoding='utf-8') as db_txt_file_in:
            records_data_txt = itertools.dropwhile(
                lambda x: len(x) == 0, db_txt_file_in)
            while True:
                try:
                    record_id = next(records_data_txt).strip(
                        '\n').split(': ')[1]
                    record_data = Phone_record(
                        *[next(records_data_txt).strip('\n').split(': ')[1] for _ in range(6)]).full_information()
                    next(records_data_txt)
                    records_data.setdefault(record_id, record_data)
                except StopIteration:
                    break
        return records_data


    # метод обновления данных в TXT файле 
    @staticmethod
    def txt_upload_new(record, records_data: dict) -> NoReturn:

        # определение порядкового номера записи
        if len(records_data) < 1:
            record_id = '0'
        else:
            record_id = int(list(records_data.keys())[-1])+1

        # открываем файл БД для добавления записей    
        with open(DB_TXT_FILE, 'w+', encoding='utf-8') as db_txt_file_out:
            record_data = record.full_information()
            db_txt_file_out.write(f'record_id: {str(record_id)}'+'\n')
            for key, value in record_data.items():
                db_txt_file_out.write(f'{key}: {str(value)}'+'\n')
            db_txt_file_out.write('-'*30+'\n')


    # метод загрузки данных из JSON файла 
    @staticmethod
    def json_load() -> dict:

        # открываем файл БД для чтения записей
        with open(DB_JSON_FILE, 'r', encoding='utf-8') as db_json_file_out:
            try:
                records_data_json = json.load(db_json_file_out)
            except:
                records_data_json = {}
            finally:
                return records_data_json


    # метод обновления данных в JSON файле
    @staticmethod
    def json_upload(record, records_data_json: dict) -> NoReturn:
        record_id = 0
        record_data = record.full_information()

        # проверка корректности записи для добавления
        if records_data_json:
            record_id = int(list(records_data_json.keys())[-1]) + 1
            records_data_json.update({record_id: record_data})
        else:
            records_data_json = {record_id: record_data}

        # открываем файл БД для записи    
        with open(DB_JSON_FILE, 'w', encoding='utf-8') as db_json_file_in:
            json.dump(records_data_json, db_json_file_in,
                      indent=4, ensure_ascii=False)


    # метод выгрузка измененных данных в файл БД
    @staticmethod
    def record_modification(db_file: str, records_data: dict) -> NoReturn:

        # открываем файл БД для записи
        with open(db_file, 'w', encoding='utf-8') as db_file_out:
            db_file_out.truncate(0)

            # проверка типа базы данных
            if TYPE_BASE == 1:
                for record_id, record_data in records_data.items():
                    db_file_out.write(f'record_id: {str(record_id)}'+'\n')
                    for key, value in record_data.items():
                        db_file_out.write(f'{key}: {str(value)}'+'\n')
                    db_file_out.write('-'*30+'\n')
            else:
                json.dump(records_data, db_file_out,
                          indent=4, ensure_ascii=False)


# основная функция
def start_phone_book() -> NoReturn:
    ''' 
        формирует приветствие и первоначальный запуск основного меню,
        а также может предоставлять пользователю возможость выбора 
        формата файла БД (по умолчанию TXT)
    '''
    print('Добро пожаловать в программу телефонный справочник!')

    # print('Пожалуйста выберите тип базы данных:')
    # print('Введите 1 - TXT БД'+' '*5 + 'Введите 2 - JSON БД')
    # db_type = int(input())
    # phone_book = Phone_book(db_type)

    phone_book = Phone_book()
    menu_function(phone_book)  # запуск основного меню


# функция основного меню
def menu_function(phone_book) -> NoReturn:
    ''' 
        обеспечивает основной пользовательский интерфейс
        содержит все основные команды и логику взаимодействия 
        с пользователем на первом уровне
    '''
    current_command = ''
    print('ОСНОВНОЕ МЕНЮ')
    print(MENU_COMMAND_LIST)

    # основная петля главного меню
    while current_command != 'exit':
        print('Введите команду:')
        current_command = input()

        # команда добавление новой записи
        if current_command == 'add':  
            phone_book.add_record()

        # команда для редактирования записи
        if current_command == 'edit':  
            print('Введите record_id записи')
            record_id = input()
            phone_book.edit_record(record_id)

        # команда поиск записи
        if current_command == 'find':  
            print('Введите попорядку все необходимые критерии поиска.')
            print('Если критерий не должен учавствовать в поиске оставьте его пустым')
            search_points = {'last_name': input(), 'first_name': input(), 'patronymic': input(
            ), "company": input(), "work_number": input(), "mobile_number": input()}
            find_result = phone_book.find_record(search_points)
            if find_result:
                page_selection = Page_selection(find_result, len(find_result))
                menu_show(phone_book, page_selection)
            else:
                print('Поиск не дал результатов!')

        # команда постраничного просмотра
        if current_command == 'show':  
            search_points = {'last_name': '', 'first_name': '', 'patronymic': '',
                             "company": '', "work_number": '', "mobile_number": ''}
            find_result = phone_book.find_record(search_points)
            if find_result:
                records_on_page = int(input('Введите размерность страницы: '))
                page_selection = Page_selection(find_result, records_on_page)
                menu_show(phone_book, page_selection)
            else:
                print('Справочник пуст')

    # очистка консоли после завершения программы
    def clear(): return os.system('cls')
    clear()


# функция меню постраничного просмотра
def menu_show(phone_book, page_selection) -> NoReturn:
    ''' 
        содержит дополнительные команды и логику взаимодействия с пользователем 
        в режиме постраничного вывода записей после поиска по критериям и вывода информации о записях 
    '''
    current_command = ''
    for page in page_selection.show_range():
        record = Phone_record(*page.values())
        print(record)  # вывод записи справочника в удобном нам виде
    print('-'*150)  # украшение
    print(
        f'страница {page_selection.current_page} из {page_selection.total_pages} страниц')
    print(SHOW_COMMAND_LIST)  # вывод вариантов команд постраничного посмотра

    # основная петля меню постраничого просмотра
    while True:
        current_command = input()
        if current_command == 'next':
            page_selection.next_page()
        if current_command == 'previous':
            page_selection.prev_page()
        if current_command == 'first':
            page_selection.first_page()
        if current_command == 'last':
            page_selection.last_page()
        if current_command == 'exit':
            menu_function(phone_book)
            break
        menu_show(phone_book, page_selection)


# точка входа
if __name__ == '__main__':  
    # проверка типа файла БД
    if TYPE_BASE == 1: 
        check_dbfile(DB_TXT_FILE)
    else:
        check_dbfile(DB_JSON_FILE)

    # запуск основного модуля
    start_phone_book()
