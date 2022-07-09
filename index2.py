import pandas as pd
import assets.dataFuncs as df
import assets.utils as ut

table = pd.read_excel("./files/step1.xlsx")

print(pd.to_datetime(table["total_dia"]))