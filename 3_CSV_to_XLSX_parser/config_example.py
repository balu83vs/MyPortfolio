"""
стандартный конфигурационный файл

позволяет определить основные справочные данные для конкретного контрагента.
использование внешнего файла конфигурации позволяет добиться универсальности и гибкости решения.

"""
# название компании
COMPANY_NAME = "YOUR_COMPANY_NAME"

# информация для занесения в шапку реестра
HEAD_INFORMATIOM = ["your text_1", "your text_2", "your text_3", "your text_n"]

""" 
названия столбцов в исходном файле CSV

данные названия используются при выборке данных. 
Соответсвенно они должны точно соответсвовать названиям ключевых столбцов в исходном CSV файле 
"""
COLUMNS_CSV = ["example_1", "example_2", "example_3", "example_4", "example_5"]

# названия столбцов в итоговом реестре XLS
COLUMNS_XLS = [
    "example_1",
    "example_2",
    "example_3",
    "example_4",
    "example_5",
    "example_6",
]

# необязательные параметры (используются для конкретного контрагента и могут быть изменены)
BASE_PRICE = 65  # цена
SALE_PRICE = 44  # цена со скидкой

START_DATE = "01.07.2023" # дата начала интервала выборки
STOP_DATE = "11.07.2023"  # дата окончания интервала выборки

# словать форматов столбцов (необходимая переменная для XlsxWriter)
# определяет внешний вид ячеек и записей в них
ROWS_FORMATS = {
    "text_bold": {"bold": True, "align": "right"},
    "date_format": {"num_format": "dd.mm.yyyy"},
    "date_format_bold": {"num_format": "dd.mm.yyyy", "bold": True},
    "time_format": {"num_format": "HH:MM:ss"},
    "rrn_format": {"align": "left", "num_format": "0"},
    "autorisation_format": {"align": "right"},
    "card_number_format": {},
    "summa_format": {"num_format": "0.00"},
    "summa_format_bold": {"num_format": "0.00", "bold": True},
    "merge_format": {"align": "left", "font_size": 12},
    "merge_format_small": {"align": "left"},
    "merge_format_bold": {"align": "left", "font_size": 12, "bold": True},
}
