from db_con import DbConnector
from algoritm import Algoritm
from testing import TestInputData


# Функция запуска
def alg_main(conditions):
    """
    - проверка входных данных 
    - вычисление конечного результата
    """
    try:
        conditions = TestInputData(conditions).json_check()
    except Exception as err:
        return err.message
    else:
        current_collection = DbConnector().choice_collection()
        result = Algoritm(
            conditions.get('dt_from'),
            conditions.get('dt_upto'),
            conditions.get('group_type'),
            current_collection
            ).get_result()    
        
        return result