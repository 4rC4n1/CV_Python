# ------------------------------------------------------------------------------------------
# STUFF TO ADD LATER
# Text of questions from external .txt file tranfer to dictionary
# RFM analysys
# ------------------------------------------------------------------------------------------

# Imports
import pandas as pd
import csv
import time
import datetime
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# Preparation of DataFrame & selection
df = pd.read_csv('export_3.csv', sep=';',  low_memory = True)    # File import
df = df.rename(columns={"id": "ID",                                     # Renaming columns
                        "order": "Order",
                        "name": "Description",
                        "catnum": "Catalog",
                        "quantity": "Quantity",
                        "price": "UnitPrice",
                        "client": "ClientID",
                        "priceCategory": "PriceCategory",
                        "objednano": "Timestamp",
                        "email": "Email"})

# Filtering unnecessities --> later customizable
df = df[~df.Description.str.contains("Platba|Doprava|Recyklační|Bankovní převod")]

# Selecting custom cluster --> later customizable
  
# Check if user wants to make custom date selection, if not, take data from last year
default_date = input("Do you want to make custom selection by date? (Y/N): ")
if default_date in ['y', 'Y']:

    # Stating date of selection
    df = df[df.Timestamp >= int(datetime.timestamp(datetime.strptime(input("Starting date (DD/MM/YYYY): "),"%d/%m/%Y")))]

    # Ending date of selection
    df = df[df.Timestamp <= int(datetime.timestamp(datetime.strptime(input("Ending date (DD/MM/YYYY): "),"%d/%m/%Y")))]
    
else:
    # Recent year selection
    df = df[df.Timestamp >= int(datetime.timestamp(datetime.now() - timedelta(days=365)))]
    print(df)

# Selection by ClientID
client_registration = input(" [N] No Registration \n [R] Registration \n [A] All \n[ID] ClientID \nWhat is client type?: ")

def filter_by_client_id(client, data_frame):

    if client in ['n','N']:                                 # All clients without registration
        data_frame = data_frame[data_frame.ClientID == 0]
    elif client in ['r','R']:                                 # All clients with registration
        data_frame = data_frame[data_frame.ClientID >= 1]
    elif client in ['a','A']:                                 # All clients
        pass
    else:                                                   # One client with ClientID
        data_frame = data_frame[data_frame.ClientID == int(client)]
    return(data_frame)

df = filter_by_client_id(client_registration, df)

# Selection of client category
client_category = int(input(" [0] All \n [1] Shops \n [2] B2B \2 [3] B2G \n [4] B2C \nPrice category: "))

def filter_by_client_category(category, data_frame):
    if category > 0:
        data_frame = data_frame[data_frame.PriceCategory == client_category]
    else:
        pass
    return(data_frame)

df = filter_by_client_category(client_category,df)

print(df)

# DataFrame check
# df = df[:100000]
# print(df[:10])
# df.info(memory_usage='deep')

# Basket analysis
# Tranform DataFrame to new table
df = df[['Order','Description', 'Quantity']]
basket = (df
          .groupby(['Order', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('Order'))
print (basket)

# Mapping table to analyze data
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1
#basket.to_csv('export_5.csv', sep='\t', encoding='utf-8')
#basket.info(memory_usage='deep')

basket_sets = basket.applymap(encode_units)

# Analysis of sets
frequent_itemsets = apriori(basket_sets, min_support=0.002, use_colnames=True, max_len = 3)
    
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules.head()

rules[ (rules['lift'] >= 100) &
       (rules['confidence'] >= 0.8) ]

# Export of data
print (rules)
rules.to_csv('export.csv', sep='\t', encoding='utf-8')
#rules.info(memory_usage='deep')"""
