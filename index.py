import pandas as pd
import assets.dataFuncs as df

table = pd.read_excel("excel.xlsx")

newCols = [
  "call_time",
  "date",
  "isCrossed",
  "cross_id",
  "crossed_time",
  "crossed_real_time",
  "porcentagem",
  "fraction",
  "isProject"
]

internalCols = [
  "call_time",
  "date",
  "isCrossed",
  "cross_id",
  "crossed_time",
  "crossed_real_time"
]

useCols = {
  "START": "inicio",
  "END": "final",
  "NAME": "nome",
  "STATUS": "Description"
}

df.createHeaders(table, newCols)

table = df.removeMultidays(
  table,
  [useCols["START"],
  useCols["END"]]
)

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
  newCols[1],
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

  idTable[ newCols[5] ] = idTable[ useCols["END"] ].max() - idTable[ useCols["START"] ].min()

for idTable in idTables:
  df.replacer(table, idTable)

df.createPercentCol(table, newCols[6], newCols[4], newCols[0])

df.createFractCol(table, newCols[7], newCols[5], newCols[6], newCols[0])


table.to_clipboard(index=False)

table.to_excel("files/final.xlsx", index=False)
