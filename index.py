import pandas as pd
import assets.dataFuncs as df

initialTable = pd.read_excel("excel.xlsx")

newCols = [
  "call_time",
  "date",
  "isCrossed",
  "cross_id",
  "crossed_time",
  "crossed_real_time",
  "porcentagem",
  "fraction"
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

df.createHeaders(initialTable, newCols)

table = initialTable.copy(deep=False)

table = df.filterBy(table, useCols["STATUS"], "closed")


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
  ## COLUNA CROSSEDTIME = soma de todos os elementos com o id referente
  idTable[ newCols[4] ] = idTable[ newCols[0] ].sum()
  
  ## COLUNA REAL CROSSEDTIME = TEMPO TOTAL DIÁRIO DENTRE OS CRUZADOS [NÃO POR CHAMADO, POR DIA[CRSSD]]
  idTable[ newCols[5] ] = idTable[ useCols["END"] ].max() - idTable[ useCols["START"] ].min()

for idTable in idTables:
  df.replacer(table, idTable)

## coluna de porcento é = tempo dos cruzados / tempo de chamado
df.createPercentCol(table, newCols[6], newCols[4], newCols[0])
## coluna fracionada[calculo final] é = (tempo real[ReCrTime] / 100) * (col porcentagem * 100)
#_# ou valor padrão carregado como coluna 0 caso não seja uma valor cruzado
df.createFractCol(table, newCols[7], newCols[5], newCols[6], newCols[0])

df.replacer(initialTable, table)

# df.removeInternalCols(table, internalCols)

initialTable.to_excel("files/final.xlsx", index=False)
