import sys
sys.path.append('/Database connection/')
import psycopg2
from config import Config
import pandas as pd

class DBConnection:
    def __init__(self):
        self._db_connection = None

    def connect(self, login): 
        # try to connect to database
        try:
            print('Connecting to the PostgreSQL database...')
            self._db_connection = psycopg2.connect(**login)
            self._db_cur = self._db_connection.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def execute_querry(self, SQLQuerry,parameter):    
        # execute a statement
        self._db_cur.execute(SQLQuerry, (parameter,))
        self._db_returned = self._db_cur.fetchall()
        return(self._db_returned)
            
    def __del__(self):
        # close the communication with the PostgreSQL
        self._db_cur.close()
        self._db_connection.close()
        print('Database connection closed.')

