import pandas as pd
import assets.dataFuncs as df
import assets.utils as ut

table = pd.read_excel("excel.xlsx")

df.createHeaders(table, ["total", "total_dia", "currentDay", "isCrossed","cross_id", "crossed_max_time"])

df.setTotalTime(table, "inicio", "final", "total")

names = df.getValuesFromTable(table, "nome")
personal_tables = df.getPersonalTables(table, names, "nome")

df.setDay(table, personal_tables, "inicio", "currentDay")

ut.space(80, "8")

for pTable in personal_tables: 
  diff_days = df.getDiferentDays(pTable, "inicio")

  daily_tables = df.getPersonalTables(pTable, diff_days, "currentDay")

  for dayTable in daily_tables:
    dayTable["total_dia"] = dayTable["total"].sum()
    df.replacer(pTable, dayTable)

    dayTable = df.setCrossAttr(dayTable, "isCrossed", "cross_id", ["inicio", "final"])
    df.replacer(pTable, dayTable)
  
  ut.space(25, "[]")
  df.replacer(table, pTable)

print(table)
idTableNames = df.getValuesFromIds(table, "cross_id")
idTables = df.getPersonalTables(table, idTableNames, "cross_id")

for idTable in idTables:
  idTable["crossed_max_time"] = idTable["total"].sum()
  ut.space()
  print(idTable)
  ut.space()

table.to_excel("files/step1.xlsx", index=False)