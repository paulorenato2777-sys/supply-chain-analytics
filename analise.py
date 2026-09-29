import kagglehub
import os
import pandas as pd

# Base 1 estoque
path1 = kagglehub.dataset_download("andrewniko/dynamic-inventory-dataset-kaizen-analytics")
arq1 = os.path.join(path1, "Dynamic Inventory Analytics.xlsx")

df_inv = pd.read_excel(arq1, sheet_name="Inventory Control")
df_wh  = pd.read_excel(arq1, sheet_name="Warehouse")

# Junta estoque e armazém
df = df_inv.merge(df_wh, left_on="Warehouse ID", right_on="Warehouse Code", how="left")

# Base 2 Pedidos
path2 = kagglehub.dataset_download("fayez1/inventory-management")
arq2 = os.path.join(path2, "Inventory Data.xlsx")



df_ped = pd.read_excel(arq2)
df_ped = df_ped.groupby("SKU ID")["Order Quantity"].sum().reset_index()


# juntando as tabelas de pedido
df = pd.merge(df, df_ped, on="SKU ID", how='left')

df = df.rename(columns={
    "SKU ID": "ID_SKU",
    "Vendor Name": "Fornecedor",
    "Warehouse ID": "ID_Armazem",
    "Current Inventory Quantity": "Estoque_Atual",
    "Cost per SKU": "Custo_por_SKU",
    "Total Value": "Valor_Total",
    "Units (Nos/Kg)": "Unidades",
    "Average Lead Time (days)": "Prazo_Medio_Entrega",
    "Maximum Lead Time (days)": "Prazo_Maximo_Entrega",
    "Unit Price": "Preco_Unitario",
    "Warehouse Code": "Codigo_Armazem",
    "City": "Cidade",
    "Province": "Provincia",
    "Country": "Pais",
    "Latitude": "Latitude",
    "Longitude": "Longitude",
    "Order Date": "Data_Pedido",
    "Order Quantity": "Qtd_Pedido"
})

df = df.fillna(0)
#print(df.tail())
#print(df.columns.tolist())
#print(df.head())

#print(df.isnull().sum())

#print(df)

#print(df['Qtd_Pedido'], df['Estoque_Atual'])

#Ordena o valor do maior para o menor
df = df.sort_values(by='Valor_Total',ascending=False).reset_index(drop=True)

#Calcula por percentual acumulado no estoque
df['Perc_Acumulado']= df['Valor_Total'].cumsum()/df['Valor_Total'].sum()

# classificando a curva de ABC.
df['Curva_ABC'] = pd.cut(
    df['Perc_Acumulado'], 
    bins=[0, 0.80, 0.95, 1.0], 
    labels=['A', 'B', 'C'], 
    include_lowest=True
)

df['Perc_ Saida_Estoque']= (df['Qtd_Pedido']/ df['Estoque_Atual'])*100

print(df['Perc_ Saida_Estoque'])
# Mostra o resultado na tela
print(df[['ID_SKU', 'Valor_Total', 'Curva_ABC']].tail(10))

#Calcula a Demanda Diária Simulada (Venda mensal dividida por 30)
df['Demanda_Diaria'] = df['Qtd_Pedido'] / 30

#Calcula automaticamente em quantos dias o estoque atual vai zerar

df['Dias_Ate_Zerar'] = df['Estoque_Atual'] / df['Demanda_Diaria']

# Remove os erros matemáticos de divisão por zero (inf e NaN) trocando por 0
df['Dias_Ate_Zerar'] = df['Dias_Ate_Zerar'].replace([float('inf'), float('nan')], 0).round(1)


df['Perc_Saida_Estoque'] = (df['Qtd_Pedido'] / df['Estoque_Atual']) * 100
df['Perc_Saida_Estoque'] = df['Perc_Saida_Estoque'].replace([float('inf'), float('nan')], 0).round(1)

#Cria a classificação dinâmica
df['Status_Alerta'] = 'Estoque Saudável (Pode aguardar)'

# calculando se estoque dura menos que o Prazo Médio do fornecedor
filtro_alerta = df['Dias_Ate_Zerar'] <= df['Prazo_Medio_Entrega']
df.loc[filtro_alerta, 'Status_Alerta'] = 'ALERTA: Programar Compra'

# calculando se estoque dura menos que o pior cenário do fornecedor (Prazo Máximo)
filtro_critico = df['Dias_Ate_Zerar'] <= df['Prazo_Maximo_Entrega']
df.loc[filtro_critico, 'Status_Alerta'] = 'CRÍTICO: Risco de Ruptura (Pedir Urgente)'

print(df[['ID_SKU', 'Estoque_Atual', 'Qtd_Pedido', 'Dias_Ate_Zerar', 'Prazo_Maximo_Entrega', 'Status_Alerta']].head(10))


print('='*15)


# ==========≈=≈==
# RELATÓRIOS GERENCIAIS COM SQL 
# =====================================================================
# RELATÓRIOS GERENCIAIS COM SQL (VERSÃO LEVE PARA CELULAR)
# =====================================================================
import sqlite3

# Cria um banco de dados temporário na memória do celular
conn = sqlite3.connect(':memory:')

# Converte o DataFrame do Pandas em uma tabela SQL real chamada df
df.to_sql('df', conn, index=False, if_exists='replace')

print("\n" + "="*50)
print("             RELATÓRIOS VIA CONSULTA SQL             ")
print("="*50)



#Quais são os SKUs Classe A que estão Críticos?
query_criticos = """
    SELECT ID_SKU, Fornecedor, Valor_Total, Dias_Ate_Zerar 
    FROM df 
    WHERE Curva_ABC = 'A' 
      AND Status_Alerta LIKE '%CRÍTICO%'
    ORDER BY Valor_Total DESC
    LIMIT 5;
"""
print("\n[SQL] Top 5 SKUs Classe A em Risco Crítico:")
cursor = conn.cursor()
cursor.execute(query_criticos)
for linha in cursor.fetchall():
    print(f"SKU: {linha[0]} | Fornecedor: {linha[1]} | Valor: R${linha[2]:.2f} | Dias: {linha[3]}")

#Quanto de dinheiro a gente tem preso por categoria de estoque?
query_capital = """
    SELECT Curva_ABC, 
           COUNT(ID_SKU) as Total_Itens,
           SUM(Valor_Total) as Capital_Total_Investido
    FROM df 
    GROUP BY Curva_ABC
    ORDER BY Curva_ABC;
"""
print("\n[SQL] Resumo Financeiro por Classe da Curva ABC:")
cursor.execute(query_capital)
for linha in cursor.fetchall():
    print(f"Classe {linha[0]} | Itens: {linha[1]} | Capital: R${linha[2]:.2f}")

#Quais fornecedores têm mais produtos no estado Crítico?
query_fornecedores = """
    SELECT Fornecedor, 
           COUNT(ID_SKU) as Qtd_Produtos_Criticos
    FROM df 
    WHERE Status_Alerta LIKE '%CRÍTICO%'
    GROUP BY Fornecedor
    ORDER BY Qtd_Produtos_Criticos DESC
    LIMIT 5;
"""
print("\n[SQL] Top 5 Fornecedores com Maior Risco de Ruptura:")
cursor.execute(query_fornecedores)
for linha in cursor.fetchall():
    print(f"Fornecedor: {linha[0]} | Qtd Críticos: {linha[1]}")

# Fecha a conexão do banco
conn.close()
