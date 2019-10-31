

import pandas as pd
import numpy as np
import datetime
from datetime import datetime

# Print mean for every month
def ShowMonthlyMean(dataFrame):
    for i in range(1,13):
        temporalData = dataFrame[dataFrame.month == i]
        print(i,":", int(temporalData['total_price_with_vat'].mean()),end="| ")
    print("")

# Load data to DataFrame
ordersData = pd.read_csv('ordersLastYear.csv', sep=';', low_memory=True)
ordersData['month'] = pd.DatetimeIndex(ordersData['created_at']).month
ordersData['email'] = ordersData['email'].str.lower()

# Separate data to segments
allOrders = ordersData[ordersData.pricing_group_id != 1]
b2bOrders = ordersData[ordersData.pricing_group_id == 2]
b2cOrders = (ordersData[ordersData.pricing_group_id == 4])
b2cOrders = b2cOrders.append(ordersData[ordersData['pricing_group_id'].isnull()])
regB2COrders = ordersData[ordersData.pricing_group_id == 4]
unregB2COrders = ordersData[ordersData['pricing_group_id'].isnull()]

# meanAll = allOrders['total_price_with_vat'].mean()
# meanB2B = b2bOrders ['total_price_with_vat'].mean()
# meanB2C = b2cOrders['total_price_with_vat'].mean()
# meanRegB2C = regB2COrders['total_price_with_vat'].mean()
# meanUnregB2C = unregB2COrders['total_price_with_vat'].mean()
# 
# print("mean All :",(int(meanAll)))
# ShowMonthlyMean(allOrders)
# print("mean B2B :",(int(meanB2B)))
# ShowMonthlyMean(b2bOrders)
# print("mean B2C :",(int(meanB2C)))
# ShowMonthlyMean(b2cOrders)
# print("mean B2C registered :",(int(meanRegB2C)))
# ShowMonthlyMean(regB2COrders)
# print("mean B2C unregistered :",(int(meanUnregB2C)))
# ShowMonthlyMean(unregB2COrders)


# Multiple orders

testFrame = unregB2COrders.sort_values(by=['email'])
multipleOrders = {}
check = "nothing"
for index, row in testFrame.iterrows():
    if row['email'] == check:
        
        multipleOrders[row['email']]['orderTime'].append(row['created_at'])
        multipleOrders[row['email']]['orderValue'].append(row['total_price_with_vat'])

    else:
        check = row['email']
        multipleOrders[row['email']] = {'orderTime':[row['created_at']],
                                        'orderValue':[row['total_price_with_vat']]}
        
print(testFrame.head())

#newframe = pd.DataFrame.from_dict(multipleOrders, orient='index')
#print(newframe.head())
def CalculationMulitpleOrders(dictionary, name):

    # number of orders                          
    numberOfOrders = len(dictionary['orderValue'])

    # average delay between orders
    ts_list = dictionary['orderTime']
    dif_list = []
    for i in range(len(ts_list)-1):
        dif_list.append((datetime.strptime(ts_list[i], '%Y-%m-%d %H:%M:%S')-datetime.strptime(ts_list[i+1], '%Y-%m-%d %H:%M:%S' )).total_seconds())
    avg = np.mean(dif_list)
    averageTime = abs(int(avg / 60 / 60 / 24))
    
    # average value of order
    va_lst =  dictionary['orderValue']
    averageValue = int(sum(va_lst) / len(va_lst))
    customerReport = [name, numberOfOrders, averageTime, averageValue]
    return(customerReport)



ReturningVisitors = []

for key in multipleOrders:
    if (len((multipleOrders[key]['orderTime']))) > 1:
        ReturningVisitors.append(CalculationMulitpleOrders(multipleOrders[key], key))
 
    else:
        visitor = [key, 1, 0, int(multipleOrders[key]['orderValue'][0])]
        ReturningVisitors.append(visitor)


   # print(len(multipleOrders[key][value]))
customerReportDataFrame = pd.DataFrame(data=ReturningVisitors, columns = ['email', 'numberOfOrders','averageTime','averageValue'])
customerReportDataFrame.set_index('email', inplace = True)
print(customerReportDataFrame.head())

def PercentageOfMultipleOrders(dataframe):
    complete = len(dataframe.index)
    striped = len(dataframe[dataframe.averageTime != 0])
    return(striped/(complete/100))

def MeansOfMultipleOrders(dataframe):
    striped = dataframe[dataframe.averageTime != 0]
    print(striped['numberOfOrders'].mean(), striped['averageTime'].mean(), striped['averageValue'].mean())

print(PercentageOfMultipleOrders(customerReportDataFrame))
MeansOfMultipleOrders(customerReportDataFrame)