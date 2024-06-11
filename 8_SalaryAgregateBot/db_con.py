import os

from pymongo import MongoClient


HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


class DbConnector:
    """
    Класс взаимодействия с базой данных mongodb
    """

    def __init__(self, host=HOST, port=int(PORT), db_name=DB_NAME, 
                       collection_name=COLLECTION_NAME):
        self._host = host
        self._port = port 
        self._db_name = db_name
        self._collection_name = collection_name

    # установка соединения (подключение клиента)
    def add_client(self):
        client = MongoClient(host=self._host, port=self._port)    
        return client
    
    # выбор базы данных (подключение БД)
    def start_connect(self):
        db = self.add_client()[self._db_name]
        return db
    
    # выбор коллекции (выбор необходимой коллекции)
    def choice_collection(self):
        db_collection = self.start_connect()[self._collection_name]
        return db_collection