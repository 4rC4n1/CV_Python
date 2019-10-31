import datetime
from dateutil.relativedelta import relativedelta

dates = {}

def Dates_of_last_days(number_of_days, from_date):
    dates_list = []
    d = 0
    while d < number_of_days:
        dates_list.append(from_date - datetime.timedelta(days=d))
        d += 1
    return(dates_list)

def Year_ago_same_day(from_date):
    target_day = datetime.datetime.weekday(from_date)
    day_year_ago = datetime.datetime.weekday(from_date - relativedelta(years=1))
    day_counter = 0
    
    while target_day != day_year_ago:
        day_counter += 1
        if day_year_ago == 6:
            day_year_ago = 0
        else:
            day_year_ago += 1

    return(from_date - relativedelta(years=1, days=(day_counter*-1)))
