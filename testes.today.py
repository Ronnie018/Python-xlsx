import pandas as pd

table = pd.read_excel("excel.xlsx")                                        ## lê a tabela

nomes = []                                                                 ## guarda os nomes [pessoa1, pessoa2]


for line, value in table.iterrows():                                       ## loop por entre as linhas da planilha
  table.loc[line, ["day"]] = str(table.loc[line, ["inicio"]].inicio)[0:10] ## pega o dia da data (exclui horas e minutos)
  if table.loc[line, ["nome"]].nome not in nomes: 
    nomes.append(table.loc[line, ["nome"]].nome)                           ## adiciona pessoas distintas

for nome in nomes:                                                         ## trata cada pessoa da lista individualmente (loop por pessoa)
  print("TIMEEE")
  personal_table = table.loc[table["nome"] == nome]                        ## cria uma subtabela apenas com o nome da pessoa atual
  distinct_days = []                                                       ## variável que vai guardar dias distintos onde a pessoa trabalhou
  print(distinct_days)

  for line, value in personal_table.iterrows():                            ## loop por entre as linhas da subtabela
    current_day = personal_table.loc[line, ["day"]].day
    if current_day not in distinct_days:         
      distinct_days.append(current_day)                                    ## adiciona dias distintos da pessoa

  for day in distinct_days:
    diary_table = personal_table.loc[personal_table["day"] == day]         ## esse escopo trabalha em cada dia individualmente
    first_of_the_day = pd.to_datetime(diary_table["inicio"].min())
    last_of_the_day = pd.to_datetime(diary_table["final"].max())
    max_real_time_worked = last_of_the_day - first_of_the_day              
    table.loc[table["day"] == day, "real time worked"] = max_real_time_worked
    total_time_worked = None                                               ## cria variavel que irá somar horas trabalhadas (cruzadas)

    for line, value in diary_table.iterrows():                             ## analisa o chamado individualmente
      call = diary_table.loc[line]
      call_duration = pd.to_datetime(call["final"]) - pd.to_datetime(call["inicio"])
      table.loc[line, "tempo_decorrido"] = call_duration
      print("Line",line)
      if total_time_worked is None: 
        total_time_worked = call_duration
      else:
        total_time_worked += call_duration

print(table.head())