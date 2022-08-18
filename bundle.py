from random import randint

import pandas as pd

class createToken():

  def __init__(self):

    self.tokenList = []

    self.alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    

  def create(self, size=12):

    token = self.generate(size)

    isNew = self.verifier(token)

    while True:

      if isNew:

        break

      else:

        token = self.generate(size)

        isNew = self.verifier(token)

    self.tokenList.append(token)

    return token

  def generate(self, size):

    size = int(size/2)

    token = ""

    for _ in range(0, size):

      token += str(randint(0, 9))

      token += self.alpha[randint(0, 51)]

    return token

  

  def verifier(self, token):

    if token not in self.tokenList:

      return True

    else:

      return False

    

    

def replacer(oldTable, newVals):

  if type(oldTable) == type(pd.DataFrame()):

    if len(newVals) > 1:

      for line, value in newVals.iterrows():

        oldTable.loc[line] = value

    else:

      if len(newVals) == 0:

        return 

      oldTable.loc[newVals.index[0]] = newVals.loc[newVals.index[0]]

  else:

    return

  

  

def setProjectCall(Table, startCol, endCol, newCol):

  Table.loc[:,newCol] = (Table[endCol] - Table[startCol]) > 1

def filterBy(Table, column, value):

  return Table.loc[Table[column] == value]

def separateDuplicates(table, col):

  return table.loc[not table.duplicates()]

  

def createHeaders(table, headers):

  for header in headers:

    table.loc[:, header] = None

def getValuesFromTable(table, col): 

  names = []

  for line, value in table.iterrows():

    if value[col] not in names:

      names.append(value[col])

  return names

def getValuesFromIds(table, idCol): 

  names = []

  for line, value in table.iterrows():

    if value[idCol] != None:

      if value[idCol] not in names:

        names.append(value[idCol])

  return names

def getPersonalTables(table, names, col):

  newNames = []

  for name in names: 

    newNames.append(table.loc[table[col] == name].copy(deep=False))

  return newNames

def setTotalTime(table, startCol, endCol, col):

  table.loc[:, [col]] = table[endCol] - table[startCol]

def getDiferentDays(table, startCol):

  days = []

  for line, value in table.iterrows():

    if tsDay(value[startCol]) not in days:

      days.append(tsDay(value[startCol]))

  return days

def tsDay(ts):

  return str(ts).split(" ")[0]

def setDay(oldTable, tables, startCol, col):

  for table in tables:

    for line, value in table.iterrows():

      table.loc[line, col] = tsDay(value[startCol])

    replacer(oldTable, table)

def getFirstAndLast(table):

  first = None

  last = None

  for line, _ in table.iterrows():

    if first is None:

      first = line

    last = line

  return [first, last]

def getNextIndex(indexArray, curr):

  indexArray = indexArray.tolist()

  if(curr in indexArray):

    return indexArray[indexArray.index(curr) + 1]

  else:

    print("erro em dataFuncs/getNextIndex()")

def getPrevIndex(indexArray, curr):

  indexArray = indexArray.tolist()

  if(curr in indexArray):

    return indexArray[indexArray.index(curr) - 1]

  else:

    print("erro em dataFuncs/getPrevIndex()")

def setCrossAttr(

  DayTable,

  flagCol,

  idCol,

  compCols

):

  tokenCreator = createToken()

  DayTable = DayTable.sort_values(by=compCols[0])

  firstVl, lastVl = getFirstAndLast(DayTable)

  IndexOrder = DayTable.loc[:].index.values

  id = tokenCreator.create(12)

  if firstVl == lastVl:

    DayTable.loc[firstVl, flagCol] = False

  else:

    for line, value in DayTable.iterrows():

      if line == firstVl:

        nextLine = DayTable.loc[getNextIndex(IndexOrder, line), compCols[0]]

        if value[compCols[1]] < nextLine: 

          DayTable.loc[line, flagCol] = False

          id = tokenCreator.create(12)

        else:

          DayTable.loc[line, flagCol] = True

          DayTable.loc[line, idCol] = id

      elif line == lastVl:

        prevLine = DayTable.loc[getPrevIndex(IndexOrder, line), compCols[1]]

        if value[compCols[0]] > prevLine:

          DayTable.loc[line, flagCol] = False

          id = tokenCreator.create(12)

        else:

          DayTable.loc[line, flagCol] = True

          DayTable.loc[line, idCol] = id

      else:

        downCrossed = value[ compCols[ 1 ] ] > DayTable.loc [ getNextIndex(IndexOrder, line), compCols [ 0 ] ]

        upCrossed = value[ compCols[ 0 ] ] < DayTable.loc [

                                            getPrevIndex(

                                              IndexOrder,

                                              line

                                            ),

                                            compCols [ 1 ] ]

        if not downCrossed and not upCrossed:

          DayTable.loc[line, flagCol] = False

        elif downCrossed and not upCrossed:

          DayTable.loc[line, flagCol] = True

          DayTable.loc[line, idCol] = id

        elif upCrossed and not downCrossed:

          DayTable.loc[line, flagCol] = True

          DayTable.loc[line, idCol] = id

          id = tokenCreator.create(12)

        else:

          DayTable.loc[line, flagCol] = True

          DayTable.loc[line, idCol] = id

  return DayTable

def createPercentCol( table, col, dvsCol, dvdCol ):

  for line, value in table.iterrows():

    if(value["isCrossed"]):

      table.loc[line, col] = table.loc[line, dvdCol] / table.loc[line, dvsCol]

    else:

      table.loc[line, col] = 1

def createFractCol(table, col, divCol, perCol, defaultCol):

  for line, value in table.iterrows():

    if(value["isCrossed"]):

      table.loc[line, col] = table.loc[line, divCol] * table.loc[line, perCol]

    else:

      table.loc[line, col] = value[defaultCol]

def removeInternalCols(table, cols):

  for col in cols:

    del table[col]

def removeMultiDays(table, StartCol, EndCol):

  for line, value in table.iterrows():

    start = tsDay(value[str(StartCol)])

    end = tsDay(value[str(EndCol)])

    if start != end:

      table = table.drop(index=line)

  return table

table = pd.read_excel("newPath")

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

createHeaders(table, newCols)

table = removeMultiDays( #new 

  table,

  [useCols["START"],

  useCols["END"]]

)

setTotalTime(

  table,

  useCols["START"],

  useCols["END"],

  newCols[0]

)

names = getValuesFromTable(

  table, useCols["NAME"]

)

personal_tables = getPersonalTables(

  table,

  names,

  useCols["NAME"]

)

setDay(

  table,

  personal_tables,

  useCols["START"],

  newCols[1],

)

for pTable in personal_tables: 

  diff_days = getDiferentDays(

    pTable,

    useCols["START"]

  )

  daily_tables = getPersonalTables(

    pTable,

    diff_days,

    newCols[1]

  )

  for dayTable in daily_tables:

    dayTable = setCrossAttr(

      dayTable,

      newCols[2],

      newCols[3],

      [

        useCols["START"],

        useCols["END"]

      ]

    )

    replacer(pTable, dayTable)

  replacer(table, pTable)

idTableNames = getValuesFromIds(

  table,

  newCols[3]

)

idTables = getPersonalTables(

  table,

  idTableNames,

  newCols[3]

)

for idTable in idTables:

  idTable[ newCols[4] ] = idTable[ newCols[0] ].sum()

  idTable[ newCols[5] ] = idTable[ useCols["END"] ].max() - idTable[ useCols["START"] ].min()

for idTable in idTables:

  replacer(table, idTable)

createPercentCol(table, newCols[6], newCols[4], newCols[0])

createFractCol(table, newCols[7], newCols[5], newCols[6], newCols[0])

table.to_clipboard(index=False)

