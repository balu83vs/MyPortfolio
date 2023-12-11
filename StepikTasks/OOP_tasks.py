#Реализуйте класс исключений DomainException. Также реализуйте класс Domain для работы с доменами. Класс Domain должен поддерживать три способа 
#создания своего экземпляра: напрямую через вызов класса, а также с помощью двух методов класса from_url() и from_email()
"""
from re import fullmatch, sub, split

class DomainException(Exception): # класс исключений
    def __str__(self):
        return 'Недопустимый домен, url или email'

class Domain:                     # класс для работы с доменами
    def __init__(self, domen):
        self.domen = type(self).check_domen(domen)

    def __str__(self):
        return f'{self.domen}'    

    @classmethod
    def from_url(cls, domen):     # отсекаем лишнее
        domen = sub(r'https://', '', domen)
        domen = sub(r'http://', '', domen)
        return cls(cls.check_domen(domen))
    
    @classmethod
    def from_email(cls, domen):   # убираем название почты и собачку
        domen = split(r'@', domen, maxsplit=1)
        if fullmatch(r'[a-zA-Z]+', domen[0]):
            return cls(cls.check_domen(domen[-1]))
        else:
            raise DomainException

    @staticmethod
    def check_domen(domen):         # проверка домена на валидность
        if fullmatch(r'[a-zA-Z]+\.[a-zA-Z]+', domen):
            return domen
        else:
            raise DomainException
        
domain1 = Domain('pygen.ru')                       # непосредственно на основе домена
domain2 = Domain.from_url('https://pygen.ru')      # на основе url-адреса
domain3 = Domain.from_email('support@pygen.ru')    # на основе адреса электронной почты

print(str(domain1))                                # pygen.ru
print(str(domain2))                                # pygen.ru
print(str(domain3))                                # pygen.ru
"""      


# таблицы рекордов, которую можно будет обновлять с учетом итоговых результатов игрока.
"""
class HighScoreTable:
    def __init__(self, max_score, iterable = []):
        self.max_score = max_score
        self.iterable = iterable
    
    @property
    def scores(self):
        self.iterable = sorted(self.iterable, reverse = True)
        self.iterable = self.iterable[:]
        return self.iterable

    def update(self, figure):
        if len(self.iterable) >= self.max_score:
            if min(self.iterable) < figure:
                self.iterable.remove(min(self.iterable))
                self.iterable.append(figure) 
        else:    
            self.iterable.append(figure)    

    def reset(self):
        return self.iterable.clear()
    
high_score_table = HighScoreTable(3)

print(high_score_table.scores)    # []
high_score_table.update(10)
high_score_table.update(8)
high_score_table.update(12)
print(high_score_table.scores)    # [12, 10, 8]

high_score_table.update(6)
high_score_table.update(7)
print(high_score_table.scores)    # [12, 10, 8]
high_score_table.update(9)
print(high_score_table.scores)    # [12, 10, 9]

high_score_table.reset()
print(high_score_table.scores)
"""  


# обработка данных с разбивкой по страницам
"""
class Pagination:
    def __init__(self, alphabet, number):
        self.alphabet = alphabet
        self.number = number
        self.index = 1
        if len(alphabet)%self.number > 0:
            self.max_page = len(alphabet)//self.number + 1   
        else:
            self.max_page = int(len(alphabet)/self.number)    

    def get_visible_items(self):
        return self.alphabet[self.number*(self.index-1) : self.number*(self.index)]  

    def next_page(self):
        self.index += 1
        self.index = self.check_number()
        return self

    def prev_page(self):
        self.index -= 1
        self.index = self.check_number() 
        return self

    def first_page(self):
        self.index = 1
        return self

    def last_page(self):
        self.index = self.max_page 
        return self

    def go_to_page(self, page):
        self.index = page
        self.index = self.check_number()
        return self

    def check_number(self):
        if self.index > self.max_page:
            self.index = self.max_page
        if self.index < 1:
            self.index = 1    
        return self.index   

    @property
    def total_pages(self):
        return self.max_page
    
    @property
    def current_page(self):
        return self.index


alphabet = list('abcdefghijklmnopqrstuvwxyz')

pagination = Pagination(alphabet, 4)
print(pagination.get_visible_items())    # ['a', 'b', 'c', 'd']

pagination.next_page()
print(pagination.get_visible_items())    # ['e', 'f', 'g', 'h']

pagination.last_page()
print(pagination.get_visible_items())    # ['y', 'z']

pagination.first_page()
pagination.next_page().next_page()   
print(pagination.get_visible_items())    # ['i', 'j', 'k', 'l']

print(pagination.total_pages)            # 7
print(pagination.current_page)           # 3

pagination.first_page()
pagination.prev_page()
print(pagination.get_visible_items())    # ['a', 'b', 'c', 'd']

pagination.last_page()
pagination.next_page()
print(pagination.get_visible_items())    # ['y', 'z']

pagination.go_to_page(-100)
print(pagination.get_visible_items())    # ['a', 'b', 'c', 'd']

pagination.go_to_page(100)
print(pagination.get_visible_items())    # ['y', 'z']
"""


# Классы Testpaper и Student - 
"""
class Testpaper:
    def __init__(self, spec, true_answers, pass_degrees):
        self.spec = spec
        self.true_answers = true_answers
        self.pass_degrees = pass_degrees

class Student:
    def __init__(self):
        self.res_dict = {}
    
    def take_test(self, answers, student_answers):

        student_degrees = round((100 / len(answers.true_answers)) * sum([answers.true_answers[i] == student_answers[i] for i in range(len(answers.true_answers))]))

        if  student_degrees >= int(answers.pass_degrees.strip('%')):
            student_pass = 'Passed!'
        else:
            student_pass = 'Failed!'
        self.res_dict.setdefault(answers.spec, f'{student_pass} ({student_degrees}%)')
        return self.res_dict
    
    @property
    def tests_taken(self):
        if self.res_dict:
            return self.res_dict
        return 'No tests taken'
    
testpaper1 = Testpaper('Maths', ['1A', '2C', '3D', '4A', '5A'], '60%')
testpaper2 = Testpaper('Chemistry', ['1C', '2C', '3D', '4A'], '75%')
testpaper3 = Testpaper('Computing', ['1D', '2C', '3C', '4B', '5D', '6C', '7A'], '75%')

student1 = Student()
student2 = Student()
student3 = Student()

student1.take_test(testpaper1, ['1A', '2D', '3D', '4A', '5A'])
student2.take_test(testpaper2, ['1C', '2D', '3A', '4C'])
student2.take_test(testpaper3, ['1A', '2C', '3A', '4C', '5D', '6C', '7B'])

print(student1.tests_taken)    # {'Maths': 'Passed! (80%)'}
print(student2.tests_taken)    # {'Chemistry': 'Failed! (25%)', 'Computing': 'Failed! (43%)'}
print(student3.tests_taken)    # No tests taken
"""