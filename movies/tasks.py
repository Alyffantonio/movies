from celery import shared_task
from django.conf import settings
from .models import Upload, Movie, Report
import pandas as pd
import os
from .omdb_client import find_data_omdb
from .selenium_scraper import get_rotten_tomatoes, get_metacritic


@shared_task
def processar_upload(upload_id):
    try:
        upload = Upload.objects.get(pk=upload_id)
        caminho = upload.arquivo.path

        print(f"iniciando processamento do upload: {upload.titulo}")

        df = pd.read_excel(caminho, header=None)

        for _, linha in df.iterrows():
            titulo = str(linha.iloc[0].strip())

            dados = find_data_omdb(titulo)

            movie = Movie.objects.create(
                upload=upload,
                titulo=dados.get('Title', titulo),
                ano=dados.get('Year'),
                elenco=dados.get('Actors'),
                diretor=dados.get('Director'),
                sinopse=dados.get('Plot'),
                genero=dados.get('Genre'),
                nota_imdb=dados.get('imdbRating'),
            )

            print(f"Buscando notas para: {movie.titulo}")

            rotten_score = get_rotten_tomatoes(movie.titulo)
            metacritic_score = get_metacritic(movie.titulo)

            movie.nota_rotten = rotten_score
            movie.nota_metacritic = metacritic_score

            movie.save()

            print(f"notas de '{movie.titulo}' atualizadas: Rotten={rotten_score} Metacritic={metacritic_score}")

        report_path = generate_report(upload_id)

        Report.objects.create(
            upload=upload,
            arquivo=report_path,
        )

        upload.processado = True
        upload.save()

        print(f"upload '{upload.titulo}' processado com sucesso!")

    except Exception as e:
        print(f"erro ao processar upload {upload_id}: {e}")
        raise e


def generate_report(upload_id):
    upload = Upload.objects.get(id=upload_id)
    movies = Movie.objects.filter(upload=upload).values()

    df = pd.DataFrame(movies)

    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_localize(None)

    os.makedirs(os.path.join(settings.MEDIA_ROOT, "reports"), exist_ok=True)

    report_name = f"relatorio_{upload.id}_{upload.titulo.replace(' ', '_')}.xlsx"
    absolute_path = os.path.join(settings.MEDIA_ROOT, "reports", report_name)
    relative_path = os.path.join("reports", report_name)

    df.to_excel(absolute_path, index=False)

    print(f"relatorio gerado: {absolute_path}")

    return relative_path

