from django.shortcuts import render
from programmes.models import Candidat, Proposition, Thematique


def index(request):
    return render(request, 'index.html')


def indexcandidat(request):
    latest_candidat_list = Candidat.objects.all().order_by('parti')[:5]
    context = {'latest_candidat_list': latest_candidat_list}
    return render(request, 'indexCandidat.html', context)


def indexproposition(request):
    latest_proposition_list = Proposition.objects.all()
    context = {'latest_proposition_list': latest_proposition_list}
    return render(request, 'indexProposition.html', context)


def questions(request):
    thematique = Thematique.objects.all().order_by('?')[0]
    context = {'thematique': thematique}
    return render(request, 'questions.html', context)
