import pandas as pd

def replacer(oldTable, newVals, col):
  print("replacer function")
  if type(oldTable) == type(pd.DataFrame()):

    for line, value in newVals.iterrows():
      oldTable.loc[line] = value
      
  else: 
    return


def createHeaders(table, headers):
  print("header creator function")
  if type(table) == type(pd.DataFrame()):

    for header in headers:
      table.loc[:, header] = None