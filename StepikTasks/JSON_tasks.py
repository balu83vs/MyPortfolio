# Бассейны (Определяет подходящий бассей. Выводит его размеры и адрес.)
"""
import json
from datetime import time, datetime

with open('pools.json', encoding ='utf-8') as input_file:
    time1 = time(10, 00, 00)
    time2 = time(12, 00, 00)
    pools = json.load(input_file)

    res_list = list(filter(lambda x: x if datetime.strptime(x['WorkingHoursSummer']['Понедельник'].split('-')[0], '%H:%M').time() <= time1 \
        and datetime.strptime(x['WorkingHoursSummer']['Понедельник'].split('-')[1], '%H:%M').time() >= time2 else None, pools))

    res_list = sorted(res_list, key = lambda x: x['DimensionsSummer']['Length'], reverse = True)  

    max_lenght = res_list[0]['DimensionsSummer']['Length']  
    
    res_list = list(filter(lambda x: x if x['DimensionsSummer']['Length'] == max_lenght else None, res_list))
    
    max_wight = max([el['DimensionsSummer']['Width'] for el in res_list])
    
    res_list = list(filter(lambda x: x if x['DimensionsSummer']['Width'] == max_wight else None, res_list))

    print(f"{res_list[0]['DimensionsSummer']['Length']}x{res_list[0]['DimensionsSummer']['Width']}")
    print(res_list[0]['Address'])        
 """ 

 # Результаты экзамена (Для каждого студента определяет его максимальную оценку, а также дату и время ее получения. Выводит в виде списка словарей.)
"""
import csv
import json
from datetime import datetime

with open('D:/py_learning/py_programs/JSON/exam_results.csv', encoding = 'utf-8') as csv_input, open('D:/py_learning/py_programs/JSON/best_scores.json', 'w', encoding = 'utf-8') as json_output:
    csv_data = sorted(csv.DictReader(csv_input, delimiter = ','), key = lambda x: x['email'])
    res_dict = dict()

    for el in csv_data:
        res_dict.setdefault(el['email'], list(filter(lambda x: x if x['email'] == el['email'] else None, csv_data)))

    for el in res_dict:
        best_score = max([int(x['score']) for x in res_dict[el]])
        res_dict[el] = list(filter(lambda x: x if int(x['score']) == best_score else None, res_dict[el]))
        if len(res_dict[el]) > 1:
            res_dict[el] = sorted(res_dict[el], key = lambda x: datetime.strptime(x['date_and_time'], '%Y-%m-%d %H:%M:%S'), reverse = True)[0]     
            res_dict[el]['score'] = int(res_dict[el]['score'])  
        else:
            res_dict[el] = res_dict[el][0]
            res_dict[el]['score'] = int(res_dict[el]['score'])

    res_list = [dict(zip(['name', 'surname', 'best_score', 'date_and_time', 'email'], el.values())) for el in res_dict.values()]

    json.dump(res_list, json_output, indent = 3)      
"""
