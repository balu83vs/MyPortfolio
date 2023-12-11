# Итератор Alphabet
"""
class  Alphabet:
    def __init__(self, language):
        self.language = language
        self.lang_dict = {'ru_start': ord('а'), 'ru_end': ord('я'), 'en_start': ord('a'), 'en_end': ord('z')}
        self.index = self.lang_dict.get(f'{self.language}_start')

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            if self.index <= self.lang_dict.get(f'{self.language}_end'):
                return chr(self.index)
            else:
                raise StopIteration
        except StopIteration:
            self.index = self.lang_dict.get(f'{self.language}_start')            
            return chr(self.index)
        finally:
            self.index +=1
    
ru_alpha = Alphabet('en')

for _ in range(40):
    print(next(ru_alpha))
#print(next(ru_alpha))
#print(next(ru_alpha))
"""

# Итератор Xrange
"""
class Xrange:
    def __init__(self, start, end, step = 1):
        self.start = start
        self.base_start = start
        self.end = end
        self.step = step

    def __iter__(self):
        return self
    
    def __next__(self):
        try: 
            if self.base_start < self.end:
                if self.start < self.end:
                    return self.start
                else: 
                    raise StopIteration
            else:
                if self.start > self.end:
                    return self.start
                else: 
                    raise StopIteration         
        finally:
            self.start += self.step

xrange = Xrange(-20, 13, 4)
print(*xrange)

xrange = Xrange(10, -21, -6)
print(list(xrange))

xrange = Xrange(0, 3, 0.5)
print(*xrange, sep='; ')    
"""

# Функция roundrobin - возвращает итератор, генерирующий последовательность из элементов всех переданных итерируемых объектов
"""
from itertools import cycle

def roundrobin(*args):
    iter_list = []
    final_round = len(max(args, key = lambda x: len(x)))
    for el in args:
        iter_list.append(iter(el))
    res_iter = cycle(iter_list)
    for res in res_iter:
        try:
            yield next(res)
        except StopIteration:
            final_round -= 1
            if final_round == 0:
                break

roundrobin('abc', 'd', 'ef')
print(*roundrobin('abc', 'd', 'ef'))
"""

# Функция ranges() - преобразовывать числа из списка numbers в отрезки, представляя их в виде кортежей, где первый элемент кортежа является левой 
# границей отрезка, второй элемент — правой границей отрезка. Полученные кортежи-отрезки функция должна возвращать в виде списка.
"""
def ranges(numbers: list) -> list[tuple]:
    temp_list = []
    res_list = []
    for el in numbers:
        if len(temp_list) == 0:
            temp_list.append(el)    
        elif el - temp_list[-1] == 1:
            temp_list.append(el)
        else:
            res_list.append((temp_list[0], temp_list[-1]))
            temp_list = []  
            temp_list.append(el)  
    if len(temp_list) == 1:
        res_list.append((temp_list[0], temp_list[0]))
    else:    
        res_list.append((temp_list[0], temp_list[-1]))        
    return res_list

numbers = [1, 3, 5, 7]
print(ranges(numbers))
"""