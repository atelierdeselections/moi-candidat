from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.formtools.wizard.views import SessionWizardView

from programmes.models import Candidat, Proposition, Thematique
from programmes.forms import Thematique1, Thematique2



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


def choisir(request):
    thematique = Thematique.objects.all().order_by('?')[0]
    context = {'thematique': thematique}
    return render(request, 'questions.html', context)


class ChoisirWizard(SessionWizardView):
    form_list = [Thematique1, Thematique2]
    template_name = 'choisir.html'

    def done(self, form_list, **kwargs):
        #do_something_with_the_form_data(form_list)
        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context = super(ChoisirWizard, self).get_context_data(**kwargs)

        thematique = Thematique.objects.all().order_by('?')[0]
        context['thematique'] = thematique

        return context
