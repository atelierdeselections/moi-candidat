from django.shortcuts import render
from programmes.models import Candidat

# Create your views here.


def index(request):
    latest_candidat_list = Candidat.objects.all().order_by('parti')[:5]
    context = {'latest_candidat_list': latest_candidat_list}
    return render(request, 'index.html', context)
