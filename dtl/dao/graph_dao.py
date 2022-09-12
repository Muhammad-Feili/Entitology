import mysql.connector
from runtime_config import RuntimConfig


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class GraphDao(Singleton):
    def __init__(username=RuntimConfig.USERNAME, password=RuntimConfig.PASSWORD,
                 hostname=RuntimConfig.HOSTNAME, database=RuntimConfig.DATABASE):

        self._username = username
        self._password = password
        self._hostname = hostname
        self._database = database

        self.connect()

    def connect(self):
        self.connection = mysql.connector.connect(username=self._username,
                                                 password=self._password,
                                                 hostname=self._hostname,
                                                 database=self._database)


    def get_row(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query_result)
        result = cursor.fetchone()
        cursor.close()


        return result

    def get_rows(self, query):
        cursor = connection.cursor()
        cursor.execute(query_result)
        result = cursor.fetchall()
        cursor.close()

        return result
