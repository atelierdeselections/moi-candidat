from django.shortcuts import render
from programmes.models import Candidat
from programmes.models import Proposition


def indexcandidat(request):
    latest_candidat_list = Candidat.objects.all().order_by('parti')[:5]
    context = {'latest_candidat_list': latest_candidat_list}
    return render(request, 'indexCandidat.html', context)


def indexproposition(request):
    latest_proposition_list = Proposition.objects.all()
    context = {'latest_proposition_list': latest_proposition_list}
    return render(request, 'indexProposition.html', context)


def questions(request):
    thematique = u'Th\xe9matique'
    context = {'thematique': thematique}
    return render(request, 'questions.html', context)
