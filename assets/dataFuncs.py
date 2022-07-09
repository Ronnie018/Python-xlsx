from random import randint
import pandas as pd
import assets.utils as ut

def replacer(oldTable, newVals):
  if type(oldTable) == type(pd.DataFrame()):
    if(len(newVals) > 1):
      for line, value in newVals.iterrows():
        oldTable.loc[line] = value
    else:
      oldTable.loc[newVals.index[0]] = newVals.loc[newVals.index[0]]
  else: 
    return



def createHeaders(table, headers):
  if type(table) == type(pd.DataFrame()):

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
  return str(ts)[0:10]



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
    print("something went wrong!")


def getPrevIndex(indexArray, curr):
  indexArray = indexArray.tolist()
  if(curr in indexArray):
    return indexArray[indexArray.index(curr) - 1]
  else:
    print("something went wrong!")



def tokenCreator():
  alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
  token = ""
  for _ in range(0, 6):
    token += str(randint(0, 9))
    token += alph[randint(0, 51)]
  return token



def setCrossAttr(DayTable, flagCol, idCol, compCols):

  DayTable = DayTable.sort_values(by=compCols[0])

  firstVl, lastVl = getFirstAndLast(DayTable)

  IndexOrder = DayTable.loc[:].index.values

  id = tokenCreator()

  if firstVl == lastVl:
    DayTable.loc[firstVl, flagCol] = False
  else:
    for line, value in DayTable.iterrows():

      
      ut.space(60, "+_")
      print(DayTable.loc[line])
      ut.space(60, "+_")

      isCrossed = True

      if line == firstVl:
        print("_______ é first ________")
        if value[compCols[1]] < DayTable.loc[getNextIndex(IndexOrder, line), compCols[0]]:
          isCrossed = False
          DayTable.loc[line, flagCol] = False
          id = tokenCreator()
        else:
          DayTable.loc[line, flagCol] = True
          DayTable.loc[line, idCol] = id
      elif line == lastVl:
        print("_______ é last ________")
        if value[compCols[0]] > DayTable.loc[getPrevIndex(IndexOrder, line), compCols[1]]:
          isCrossed = False
          DayTable.loc[line, flagCol] = False
          id = tokenCreator()
        else:
          DayTable.loc[line, flagCol] = True
          DayTable.loc[line, idCol] = id
      else:
        downCrossed = value[compCols[1]] > DayTable.loc[getNextIndex(IndexOrder, line), compCols[0]]
        upCrossed = value[compCols[0]] < DayTable.loc[getPrevIndex(IndexOrder, line), compCols[1]]
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
