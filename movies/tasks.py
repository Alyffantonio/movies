from celery import shared_task
from django.conf import settings
from .models import Upload, Movie, Report
import pandas as pd
import requests
import os


@shared_task
def processar_upload(upload_id):
    try:
        upload = Upload.objects.get(pk=upload_id)
        caminho = upload.arquivo.path

        print(f"🟡 Iniciando processamento do upload: {upload.titulo}")

        df = pd.read_excel(caminho)

        for _, linha in df.iterrows():
            titulo = str(linha[0].strip())

            dados = find_data_omdb(titulo)

            Movie.objects.create(
                upload=upload,
                titulo=dados.get('Title', titulo),
                ano=dados.get('Year'),
                elenco=dados.get('Actors'),
                sinopse=dados.get('Plot'),
                genero=dados.get('Genre'),
                nota_imdb=dados.get('imdbRating'),
            )

        report_path = generate_report(upload_id)

        Report.objects.create(
            upload=upload,
            arquivo=report_path,
        )

        upload.processado = True
        upload.save()

        print(f"✅ Upload '{upload.titulo}' processado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao processar upload {upload_id}: {e}")
        raise e


def find_data_omdb(titulo):
    try:
        api_key = getattr(settings, 'OMDB_API_KEY', None)
        url = "https://www.omdbapi.com/"
        params = {"t": titulo, "apikey": api_key}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Falha na API OMDb para '{titulo}': {response.status_code}")
            return {}

    except Exception as e:
        print(f"❌ Erro na consulta OMDb para '{titulo}': {e}")
        return {}


def generate_report(upload_id):
    upload = Upload.objects.get(id=upload_id)
    movies = Movie.objects.filter(upload=upload).values()

    df = pd.DataFrame(movies)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "reports"), exist_ok=True)

    report_name = f"relatorio_{upload.id}_{upload.titulo.replace(' ', '_')}.xlsx"
    absolute_path = os.path.join(settings.MEDIA_ROOT, "reports", report_name)
    relative_path = os.path.join("reports", report_name)

    df.to_excel(absolute_path, index=False)

    print(f"📊 Relatório gerado: {absolute_path}")

    return relative_path

