from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .models import Upload, Report
from .tasks import processar_upload



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


def delete_arquivo_reports(request, id):

    if not id:
        return JsonResponse({'Erro': 'ID não fornecido!'}, status=400)

    try:
        report = Upload.objects.get(id=id)
    except Upload.DoesNotExist:
        return JsonResponse({'Erro': 'ID do objeto não existe!'}, status=400)

    report.delete()

    return JsonResponse({"message": "Reports  excluido com sucesso."})