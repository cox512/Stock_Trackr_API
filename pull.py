import pandas as pd
import random
from alpha_vantage.timeseries import TimeSeries
import time
from dotenv import load_dotenv
load_dotenv()
import sys
# ticker = str(sys.argv[1])

lines = open('.env').read().splitlines()
keys = random.choice(lines) #You can put multiple keys in the keys file. This way you can randomly choose between your keys and get more pulls.
time = TimeSeries(key=keys, output_format='pandas')
data, meta_data = time.get_intraday(symbol='AAPL', interval='1min', outputsize='full') #Look at docs for more options.
# print(ticker)
print(data)

i = 1

close_data = data['4. close']
percent_change = close_data.pct_change() #pct_change() is a built in pandas function

# print(percent_change)

last_change = percent_change[-1]
if abs(last_change) > 0.0004: #if absolute value of the last change is above 0.0004%, send an alert
    print("AAPL Alert:" + last_change)
