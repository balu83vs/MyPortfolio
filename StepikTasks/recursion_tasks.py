# Функция get_all_values() - определяет все значения, которые соответствуют ключу key в словаре nested_dicts и всех его вложенных словарях, 
# и возвращает их в виде множества. Если ключа key нет ни в одном словаре, функция должна вернуть пустое множество.
"""
def get_all_values(my_dict, my_key):
    res_set = set()
    
    for k, v in my_dict.items():
        if k == my_key:
            res_set.add(v)
        if isinstance(v, dict):
            res_set.update(get_all_values(v, my_key))
    return res_set

    
my_dict = {
           'Arthur': {'hobby': 'videogames', 'drink': 'cacao'}, 
           'Timur': {'hobby': 'math'},
           'Dima': {
                   'hobby': 'CS',
                   'sister':
                       {
                         'name': 'Anna',
                         'hobby': 'TV',
                         'age': 14
                       }
                   }
           }
result = get_all_values(my_dict, 'age')
print(*result)    
"""    

# Функция dict_travel() - выводит все пары ключ-значение словаря nested_dicts, а также значения всех его дочерних словарей.
"""
def dict_travel(data, res_str = ''):
    for k,v in sorted(data.items()):
        if isinstance(v, dict):
            dict_travel(v, res_str + f'{k}.')
        else:
            print(f'{res_str}{k}: {v}')

data = {'firstname': 'Тимур', 'lastname': 'Гуев', 'birthdate': {'day': 10, 'month': 'October', 'year': 1993},'address': {'streetaddress': 'Часовая 25, кв. 127', 'city': {'region': 'Московская область', 'type': 'город', 'cityname': 'Москва'}, 'postalcode': '125315'}}
dict_travel(data)            
"""