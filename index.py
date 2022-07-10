import pandas as pd
import assets.dataFuncs as df

table = pd.read_excel("excel.xlsx")

newCols = [
  "call_time",
  "date",
  "isCrossed",
  "cross_id",
  "crossed_time"
]

useCols = {
  "START": "inicio",
  "END": "final",
  "NAME": "nome"
}

df.createHeaders(table, newCols)

df.setTotalTime(
  table,
  useCols["START"],
  useCols["END"],
  newCols[0]
)

names = df.getValuesFromTable(
  table, useCols["NAME"]
)

personal_tables = df.getPersonalTables(
  table,
  names,
  useCols["NAME"]
)

df.setDay(
  table,
  personal_tables,
  useCols["START"],
  newCols[1]
)

for pTable in personal_tables: 
  diff_days = df.getDiferentDays(
    pTable,
    useCols["START"]
  )

  daily_tables = df.getPersonalTables(
    pTable,
    diff_days,
    newCols[1]
  )

  for dayTable in daily_tables:
    dayTable = df.setCrossAttr(
      dayTable,
      newCols[2],
      newCols[3],
      [
        useCols["START"],
        useCols["END"]
      ]
    )

    df.replacer(pTable, dayTable)

  df.replacer(table, pTable)

idTableNames = df.getValuesFromIds(
  table,
  newCols[3]
)
idTables = df.getPersonalTables(
  table,
  idTableNames,
  newCols[3]
)

for idTable in idTables:
  
  idTable[ newCols[4] ] = idTable[ newCols[0] ].sum()

  df.replacer(table, idTable)

table.to_excel("files/step1.xlsx", index=False)