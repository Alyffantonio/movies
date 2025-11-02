from django.shortcuts import render
from .models import  Report


def page_inicial(request):

    reports = Report.objects.all().order_by('-created_at')

    context = {
        'reports': reports,
    }

    return render(request, 'movies/base.html', context)




