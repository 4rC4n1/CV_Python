import pandas as pd
import numpy
import datetime

#month_no = 3
#d = datetime.datetime(1,month_no,1)
#print(d.strftime('%B'))
#
# Load data to DataFrame
itemsInOrders = pd.read_csv('last_month.csv', sep=';', low_memory=True)

#itemsInOrders['year'] = pd.DatetimeIndex(itemsInOrders['created_at']).year
#itemsInOrders['month'] = pd.DatetimeIndex(itemsInOrders['created_at']).month
print(itemsInOrders.head())

# Group same items and their quantity
f = {'order_id': 'first', 'name': 'first', 'price_with_vat': 'first', 'quantity': 'sum', 'catnum': 'first'}
itemsConsolidated = (itemsInOrders
                     .groupby(['product_id'], as_index=False).agg(f))
print(itemsConsolidated.head())

# Multiply quantity with price with vat
def GetItemValues(dataFrame):

    dataFrame['item_value'] = dataFrame.price_with_vat * dataFrame.quantity
    dataFrame = dataFrame.sort_values(by=['item_value'], ascending=False)
    return(dataFrame)

currentDataFrame = GetItemValues(itemsConsolidated)

 
# Return top 20% products from dataset by their value
def GetTopProducts(dataFrame):

    revenueSum = int(dataFrame['item_value'].sum())
    topPercentile = revenueSum * 0.2
    topRowCount = 0

    for index, row in dataFrame.iterrows():
        topPercentile -= int(row['item_value'])
        topRowCount = topRowCount + 1
        if topPercentile <= 0:
            print(topRowCount)
            break

    return(dataFrame[:topRowCount])
currentDataFrame = GetItemValues(itemsConsolidated)
itemList = GetTopProducts(currentDataFrame)
print(itemList)
test = itemList

# Export
test.to_csv('itemConsolidated.csv', sep=';', encoding='utf-8')
