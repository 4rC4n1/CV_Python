import sys
import csv
import json
import pandas as pd
import time
import psycopg2
from configparser import ConfigParser
import os

def Config():
    db = {'database': '', 'host': '', 'password': '', 'user': ''}
    return db

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

def GetOrderInfo(orderNumber):

    SQLQuerry = select_orders
    returned_values = pd.DataFrame(db_conection.execute_querry(SQLQuerry, orderNumber))
    print(returned_values)
    return(returned_values)

def GetOrderItems(orderNumber):

    SQLQuerry = select_order_items
    returned_values = pd.DataFrame(db_conection.execute_querry(SQLQuerry,orderNumber)).rename(columns={0:"Catnum", 1:"Nazev", 2:"Ks", 3:"Cena za ks", 4:"Cena celkem"})
    print(returned_values)
    return(returned_values)

if __name__ == '__main__':
    # Connect to database
    db_conection = DBConnection()

    # Menu and choice of desired operation
    menu = {}
    menu['1']="Vyhledat objednávku (číslo objednávky/e-mail/příjmení)" 
    menu['2']="Vyhledat zboží v objednávce (číslo objednávky)"

    while True: 
        options=menu.keys()
        for entry in options: 
            print (entry, menu[entry])

        selection=input("Zvolte možnost: ") 
        if selection =='1': 
            menu_choice = 1 
            searchInput = input("Zadejte číslo objednávky, e-mail nebo příjmení : ").lower()

            # Define querry
            select_orders = """SELECT number, created_at, total_price_with_vat, first_name, last_name, email, telephone, company_name, company_number, street, city, postcode, delivery_first_name, delivery_last_name, delivery_company_name, delivery_telephone, delivery_street, delivery_city, delivery_postcode, name, tracking_number
                FROM "orders"
                LEFT JOIN "transport_translations" ON transport_translations.translatable_id = transport_id 
                WHERE number IN (%s) OR lower(orders.last_name) = '{}' OR lower(orders.email) = '{}'""".format(searchInput, searchInput)
    
            # Connect to database
            db_conection.connect(Config())
            extractedData = GetOrderInfo(searchInput)
            del db_conection  

            break

        elif selection == '2': 
            menu_choice = 2 
            searchInput = input("Zadejte číslo objednávky : ")

            # Define querry
            select_order_items = """SELECT catnum, name, quantity, price_with_vat, total_price_with_vat
                        FROM "order_items"
                        WHERE order_items.order_id = (SELECT orders.id FROM "orders" WHERE orders.number = %s)"""
           
            # Connect to database
            db_conection.connect(Config())
            extractedData = GetOrderItems(searchInput)
            del db_conection  

            break

        else: 
            print ("Chyba! Zadejte možnost [1 nebo 2]:") 

    # Create export file
    extractedData.to_csv('export.csv', header=True, index=False, sep=';', mode='w')
    print("Proveden export")
    time.sleep(2)
    sys.exit(0)