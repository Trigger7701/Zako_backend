from datetime import date,datetime,timedelta

one_day = timedelta(days=1)
start_day = datetime.now()

even_days = ['Mon', 'Wed', 'Fri']
odd_days = ['Tue', 'Thu', 'Sat']
x=0
while x<12:
    start_day += one_day
    if start_day.strftime('%a') in even_days:
        print((start_day))
        x += 1