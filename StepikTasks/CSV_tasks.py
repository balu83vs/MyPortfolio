# Проще, чем кажется (приводит содержимое файла в привычный CSV формат, сгруппировав строки по первому столбцу и назвав первый столбец id_name. 
# Полученный результат функция должна записать в файл condensed.csv)
"""
import csv

def condense_csv(filename, id_name):
    temp_dict = {}
    res_list = []
    columns = []

    with open(filename, encoding = 'utf-8') as input_file, open('condensed.csv', 'w', encoding = 'utf-8', newline = '') as output_file:
        data = [el.strip('\n').split(',') for el in input_file.readlines()]
        columns.append(id_name)
        data.sort(key = lambda x: x[0])
        temp_name = data[0][0]
        for el in data:
            if el[1] not in columns:
                columns.append(el[1])
            if el[0] == temp_name:
                temp_dict.setdefault(id_name, temp_name)
                temp_dict.setdefault(el[1], el[2])
                temp_name = el[0]
            else:
                res_list.append(temp_dict)
                temp_dict = {}
                temp_dict.setdefault(id_name, el[0])
                temp_dict.setdefault(el[1], el[2])
                temp_name = el[0]
        res_list.append(temp_dict)

        output_data = csv.DictWriter(output_file, delimiter = ',', fieldnames = columns)
        output_data.writeheader()

        for el in res_list:
            output_data.writerow(el)    

filename = 'data2.csv'            
id_name = 'object'

condense_csv(filename, id_name)
"""

# Возрастание классов (записывает таблицу классов в файл sorted_student_counts.csv, располагая все столбцы в порядке возрастания классов, 
# при совпадении классов — в порядке возрастания букв.)
"""
import csv

with open("student_counts.csv", encoding = 'utf-8') as input_file, open("sorted_student_counts.csv", 'w', encoding = 'utf-8', newline = '') as output_file:
    data_list = [el for el in csv.DictReader(input_file, delimiter = ',')]
    columns = list(data_list[0].keys())
    new_columns = columns[0:1]
    new_columns.extend(sorted(sorted(columns[1:]), key = lambda x: int(x.split('-')[0])))
    res_file = csv.DictWriter(output_file, delimiter = ',', fieldnames = new_columns)
    res_file.writeheader()
    for el in data_list:
        res_file.writerow(el)
"""

# Голодный студент (определяет и выводит самый дешевый продукт и название магазина, в котором он продается)
"""
import csv

res_dict = {}
win_list = []

with open('prices.csv', encoding = 'utf-8') as file:
    data = csv.DictReader(file, delimiter = ';')
    for el in data:
        temp_key = el.pop('Магазин')
        res_dict.setdefault(temp_key, 
            [list(filter(lambda x: x if int(el[x]) == min([int(el[x]) for x in el]) else None, el))[0], 
                el[list(filter(lambda x: x if int(el[x]) == min([int(el[x]) for x in el]) else None, el))[0]]])

win_list = list(filter(lambda x: x if int(res_dict[x][1]) == min([int(res_dict[el][1]) for el in res_dict]) else None, res_dict))

print(f'{res_dict[win_list[0]][0]}: {win_list[0]}')
"""