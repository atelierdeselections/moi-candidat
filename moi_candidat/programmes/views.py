import csv
import random
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.formtools.wizard.views import SessionWizardView

from programmes.models import Resultat
from programmes.forms import PreThematiqueForm, ThematiqueForm

import voxe


def index(request):
    return render(request, 'index.html')


def programmes(request):
    election = voxe.Election(settings.VOXE_ELECTION_ID)
    candidats = election.candidats
    thematiques = election.thematiques
    propositions = election.propositions
    context = {'thematiques': thematiques, 'candidats': candidats, 'propositions': propositions}
    return render(request, 'programmes.html', context)


def resultat(request, hashcode):
    resultat = get_object_or_404(Resultat, hashcode=hashcode)
    votes = resultat.propositions_csv.split(',')

    election = voxe.Election(settings.VOXE_ELECTION_ID)
    candidats = election.candidats
    thematiques = election.thematiques
    thematiques_total = len(thematiques)

    results = []
    for candidat in candidats:
        propositions_candidat = election.propositions_by_candidat(candidat)
        votes_per_candidat = 0
        for proposition in propositions_candidat:
            if proposition.id in votes:
                votes_per_candidat += 1
        percent = int(votes_per_candidat/(thematiques_total * 1.0) * 100)
        results.append((percent, candidat))
    results_sorted = sorted(results, key=lambda tup: tup[0], reverse=True)

    current_url = request.build_absolute_uri()

    context = {'resultat': resultat, 'results': results_sorted, 'current_url': current_url}
    return render(request, 'resultat.html', context)


def mon_programme(request, hashcode):
    resultat = get_object_or_404(Resultat, hashcode=hashcode)
    votes = resultat.propositions_csv.split(',')

    election = voxe.Election(settings.VOXE_ELECTION_ID)
    propositions = election.propositions

    propositions_selected = []
    for proposition in propositions:
        if proposition.id in votes:
            propositions_selected.append(proposition)

    current_url = request.build_absolute_uri()

    context = {'resultat': resultat, 'propositions': propositions_selected, 'current_url': current_url}
    return render(request, 'mon-programme.html', context)


def get_thematique_forms():
    thematique_forms = [ThematiqueForm for each in range(settings.MOICANDIDAT_NB_ETAPES)]
    thematique_forms.insert(0, PreThematiqueForm)
    return thematique_forms


class ChoisirWizard(SessionWizardView):
    form_list = get_thematique_forms()
    template_name = 'choisir.html'

    def __init__(self, *args, **kwargs):
        super(ChoisirWizard, self).__init__(*args, **kwargs)
        self.election = voxe.Election(settings.VOXE_ELECTION_ID)

    def get_form(self, step=None, data=None, files=None):
        form = super(ChoisirWizard, self).get_form(step, data, files)

        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == '0':
            choices = []
            for t in self.election.thematiques:
                for s in t.sous_thematiques:
                    if len(s.propositions) > 2:
                        choices.append((s.id, s.nom))
            form.fields['sous_thematiques'].choices = choices
        return form

    def get_context_data(self, form, **kwargs):
        context = super(ChoisirWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current != '0':
            # Get data from first step
            selected = self.get_cleaned_data_for_step('0')['sous_thematiques']
            current_step = int(self.steps.current) - 1
            for t in self.election.thematiques:
                for s in t.sous_thematiques:
                    if s.id == selected[current_step]:
                        random.shuffle(s.propositions)
                        context['thematique'] = s
                        break
        context['nb_etapes'] = settings.MOICANDIDAT_NB_ETAPES
        return context

    def done(self, form_list, **kwargs):
        results = []
        for form in form_list:
            if 'proposition' in form.cleaned_data:
                results.append(form.cleaned_data['proposition'])

        propositions_csv = ",".join(results)
        try:
            resultat = Resultat.objects.get(propositions_csv=propositions_csv)
        except Resultat.DoesNotExist:
            resultat = Resultat(propositions_csv=propositions_csv)
            resultat.save()

        return HttpResponseRedirect('/resultat/%s/' % resultat.hashcode)


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nantes-municipales-2014.csv"'

    writer = csv.writer(response)
    election = voxe.Election(settings.VOXE_ELECTION_ID)

    candidats = election.candidats
    rows = []
    longest_row = 0
    for candidat in candidats:
        row = []
        fullname = "%s %s" % (candidat.prenom, candidat.nom)
        row.append(fullname.encode('utf-8'))

        for proposition in election.propositions_by_candidat(candidat):
            row.append(proposition.description.encode('utf-8'))
        row_size = len(row)
        if row_size > longest_row:
            longest_row = row_size
        rows.append(row)

    filled_rows = []
    for row in rows:
        new_row = []
        for i in range(longest_row):
            try:
                new_row.append(row[i])
            except IndexError:
                new_row.append('')
        filled_rows.append(new_row)
    transposed = zip(*filled_rows)

    for row in transposed:
        writer.writerow(list(row))

    return response
