import pandas as pd

# Lista de filmes do PDF
filmes = [
    "Blade Runner",
    "The Matrix",
    "Inception",
]

# Criar um DataFrame (a sua task lê a primeira coluna,
# então vamos nomeá-la para clareza)
df = pd.DataFrame(filmes, columns=['Titulo'])

# Nome do arquivo de saída
nome_arquivo = "filmes_star_wars.xlsx"

# Salvar o DataFrame em um arquivo Excel
# index=False é importante para não criar uma coluna de índice
df.to_excel(nome_arquivo, index=False)

print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
