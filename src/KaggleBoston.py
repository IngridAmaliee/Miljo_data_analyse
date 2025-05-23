from datetime import datetime
from meteostat import Stations, Daily
import pandas as pd

# Set time period
start = datetime(2013, 3, 1)
end = datetime(2023, 3, 1)

# Get daily data
data = Daily('72509', start, end)
data = data.fetch()
data=data.reset_index().iloc[:,[0,1,2,3,4,6,7,9]]

data.to_csv('BostonData2.csv',index=False)

