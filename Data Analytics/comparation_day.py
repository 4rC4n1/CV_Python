import sys
sys.path.append('/Database connection/')
import time
import csv
import datetime
from datetime import date, timedelta
from config import Config
from connection import DBConnection
from functions import Dates_of_last_days
from functions import Year_ago_same_day
import json
import pandas as pd
import matplotlib.pyplot as plt

select_orders = """SELECT total_price_with_vat, orders.created_at
                FROM "orders"
                LEFT JOIN  users ON users.id = orders.customer_id
                WHERE DATE(orders.created_at) = %s AND (gtm_calculation IS NULL OR gtm_calculation = '1' OR users.pricing_group_id = '4')
                ORDER BY orders.created_at ASC"""

def Get_day_values(querryDate):
    
    SQLQuerry = select_orders
    nameValue = 'Value ' + str(querryDate.year)
    nameTime = 'Time ' + str(querryDate.year)
    parameter = str(querryDate.strftime('%Y-%m-%d'))

    returned_values = pd.DataFrame(db_conection.execute_querry(SQLQuerry,parameter), index=None, columns=[nameValue, nameTime])
    returned_values[nameValue].astype(int)
    returned_values[nameValue] = returned_values[nameValue].apply(lambda x: round(x, 0))
    returned_values[nameTime].astype(datetime.datetime)
    return(returned_values)

if __name__ == '__main__':
    # basic parameter for script in future
    given_date = datetime.date.today()# - timedelta(days=1)
    period = 1
    
    # Connect to database
    db_conection = DBConnection()
    db_conection.connect(Config())
    
    # Get lists of dates from parameters
    data_last_year = Get_day_values(Year_ago_same_day(given_date))
    data_today = Get_day_values(given_date)
    final_frame = pd.concat([data_last_year.reset_index(drop=True), data_today.reset_index(drop=True)], axis=1) 
    
    final_frame.loc['Total'] = [final_frame.iloc[:,0].sum(),  final_frame.iloc[:,1].count(), final_frame.iloc[:,2].sum(),final_frame.iloc[:,3].count()]
    final_frame.loc['Average'] = [(int(final_frame.iloc[:,0].sum()/final_frame.iloc[:,1].count())),'-' ,(int(final_frame.iloc[:,2].sum()/final_frame.iloc[:,3].count())),'-']
    pd.set_option('display.max_rows', final_frame.shape[0]+1)
    print(final_frame)
 

    # Disconect from database
    del db_conection   

