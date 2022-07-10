import pandas as pd
import assets.dataFuncs as df
import assets.utils as ut

table = pd.read_excel("excel.xlsx")

cols = ["call_time", "date", "isCrossed","cross_id", "crossed_time"]

df.createHeaders(table, cols)

df.setTotalTime(table, "inicio", "final", "call_time")

names = df.getValuesFromTable(table, "nome")
personal_tables = df.getPersonalTables(table, names, "nome")

df.setDay(table, personal_tables, "inicio", "date")

for pTable in personal_tables: 
  diff_days = df.getDiferentDays(pTable, "inicio")

  daily_tables = df.getPersonalTables(pTable, diff_days, "date")

  for dayTable in daily_tables:
    dayTable = df.setCrossAttr(dayTable, "isCrossed", "cross_id", ["inicio", "final"])
    df.replacer(pTable, dayTable)

  df.replacer(table, pTable)

idTableNames = df.getValuesFromIds(table, "cross_id")
idTables = df.getPersonalTables(table, idTableNames, "cross_id")

for idTable in idTables:
  idTable["crossed_time"] = idTable["call_time"].sum()
  df.replacer(table, idTable)

table.to_excel("files/step1.xlsx", index=False)