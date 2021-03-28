from datetime import date
import json
from pyjpboatrace import PyJPBoatrace
import pandas as pd

# initialize
boatrace_tools = PyJPBoatrace(use_cache=True)

# get data 2019,1,26,8,1

errors = pd.read_csv("./log.csv", names=('types', 'year',
                     'month', 'day', 'st', 'rid'))

# for i, row in errors.iterrows():
#    if row["types"] == "just_before_info":
#        dic = boatrace_tools.get_just_before_info(d=date(row["year"],row["month"],row["day"]), stadium=row["st"], race=row["rid"])
#        print (dic)


for i, row in errors.iterrows():
    if row["types"] == "race_result":
        dic = boatrace_tools.get_race_result(d=date(
            row["year"], row["month"], row["day"]), stadium=row["st"], race=row["rid"])
        print(dic)

# close (you can use 'with' statement)
boatrace_tools.close()
