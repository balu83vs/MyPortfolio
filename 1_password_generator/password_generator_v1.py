import random

class Password:
    __passwords = [] #passwords list
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '0123456789'
    symbols = "_-%$#@*^!'"

    def __init__(self) -> None:
        self.password = ''

    # функция генерации пароля
    def password_generator(self) -> str: 
        temp_list = []
        len_password = random.randint(6, 12) # случайная длина пароля

        for _ in range(len_password):
            temp_list.append(random.choice(type(self).alphabet))
            temp_list.append(random.choice(type(self).numbers))
            temp_list.append(random.choice(type(self).symbols))
            self.password += random.choice(temp_list)
            temp_list = []
        
        #проверка на уникальность    
        if self.password in type(self).__passwords:
            self.password_generator()
        else:
            type(self).__passwords.append(self.password)              
            type(self).__init__(self)
        return type(self).__passwords[-1]    


password = Password() # экземпляр класса генерации пароля

print(password.password_generator()) # распечатываем пароль