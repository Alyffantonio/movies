import pandas as pd

filmes = [
    "Blade Runner",
    "The Matrix",
    "Inception",
]


df = pd.DataFrame(filmes, columns=['Titulo'])

nome_arquivo = "filmes.xlsx"


df.to_excel(nome_arquivo, index=False)

print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
