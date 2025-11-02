import pandas as pd

filmes = [
"Star Wars: Episode I – The Phantom Menace",
"Star Wars: Episode II – Attack of the Clones",
"Star Wars: Episode III – Revenge of the Sith",
"Star Wars: Episode IV – A New Hope" ,
"Star Wars: Episode V – The Empire Strikes Back",
"Star Wars: Episode VI – Return of the Jedi",
"Star Wars: Episode VII – The Force Awakens",
"Star Wars: Episode VIII – The Last Jedi",
"Star Wars: Episode IX – The Rise of Skywalker",
"Rogue One: A Star Wars Story",
"Solo: A Star Wars Story",
]

df = pd.DataFrame(filmes)

nome_arquivo = "filmes_star_wars.xlsx"

df.to_excel(nome_arquivo, index=False, header=False)

print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
