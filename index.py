import pandas as pd
import dataFuncs as df

table = pd.read_excel("excel.xlsx") ## lê a tabela

df.createHeaders(table, ["inicio2"]) ## adiciona os cabeçalhos

tableCopy = table.loc[table["nome"] == "pessoa1"].copy(deep=False) ## cria copia apenas com os dados que seram úteis

tableCopy.loc[tableCopy["chamado"] == 3, "inicio2"] = "jooj" ## altera o frame de dados

df.replacer(table, tableCopy, "chamado") ## atualiza a planilha com os novos dados

print(table) ## apresenta o resultado final