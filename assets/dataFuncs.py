from random import randint
import pandas as pd

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
  
  
# def removeLinesWithValue(Table, column, value):
#   del Table.loc[Table[column] == value]
  
def filterBy(Table, column, value):
  return Table.loc[Table[column] == value]


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
  for line, values in table.iterrows():
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



def tokenCreator():
  alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
  token = ""
  for _ in range(0, 6):
    token += str(randint(0, 9))
    token += alph[randint(0, 51)]
  return token



def setCrossAttr(
  DayTable,
  flagCol,
  idCol,
  compCols
):

  DayTable = DayTable.sort_values(by=compCols[0]) ## compcols 0 é coluna de inicio e compcols1 é final

  firstVl, lastVl = getFirstAndLast(DayTable)

  IndexOrder = DayTable.loc[:].index.values

  id = tokenCreator()

  if firstVl == lastVl:
    DayTable.loc[firstVl, flagCol] = False

  else:
    for line, value in DayTable.iterrows():

      if line == firstVl:
        nextLine = DayTable.loc[getNextIndex(IndexOrder, line), compCols[0]]

        if value[compCols[1]] < nextLine: 
          DayTable.loc[line, flagCol] = False
          id = tokenCreator()

        else:
          DayTable.loc[line, flagCol] = True
          DayTable.loc[line, idCol] = id

      elif line == lastVl:
        prevLine = DayTable.loc[getPrevIndex(IndexOrder, line), compCols[1]]

        if value[compCols[0]] > prevLine:
          DayTable.loc[line, flagCol] = False
          id = tokenCreator()

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
          id = tokenCreator()
          
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
      table.loc[line, col] = table.loc[line, divCol] / 100 * table.loc[line, perCol] * 100
    else:
      table.loc[line, col] = value[defaultCol]

def removeInternalCols(table, cols):
  for col in cols:
    del table[col]

