# OrderedDict

# custom_sort()
"""
from collections import OrderedDict

def get_key(data, value):
    for k, v in data.items():
        if v == value:
            return k

def custom_sort(data, by_values=False):
# Функция сортировки словаря ordered_dict

    if by_values is True:
        for value in sorted(data.values()):
            data.move_to_end(get_key(data, value))
    else:
        for key in sorted(data):
            data.move_to_end(key)
            
data = OrderedDict(Dustin=29, Anabel=17, Brian=40, Carol=16)
custom_sort(data, by_values=False)
print(data)
"""