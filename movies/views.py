from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render
from .models import Upload, Report
from .tasks import processar_upload

def page_inicial(request):

    reports = Report.objects.all().order_by('-created_at')

    context = {
        'reports': reports,
    }

    return render(request, 'movies/base.html', context)


@csrf_exempt
@require_POST
def upload_arquivo(request):

    titulo = request.POST['titulo']
    arquivo = request.FILES['arquivo']

    if not titulo or not arquivo:
        return JsonResponse({"error": "Título e arquivo são obrigatórios."}, status=400)

    upload = Upload.objects.create(titulo=titulo, arquivo=arquivo)

    processar_upload.delay(upload.id)

    return JsonResponse({
        "message": "Upload recebido e processamento iniciado.",
        "upload_id": upload.id,
        "titulo": upload.titulo,
        "arquivo": upload.arquivo.url
    })

