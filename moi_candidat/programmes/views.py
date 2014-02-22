import re
import csv
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.formtools.wizard.views import SessionWizardView

from programmes.models import Candidat, Proposition, Thematique
from programmes.forms import ThematiqueForm

import voxe


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


def resultat(request):
    votes = request.session['results']

    election = voxe.Election(settings.VOXE_ELECTION_ID)
    candidats = election.candidats
    candidats_total = len(candidats)
    propositions = election.propositions
    propositions_total = len(propositions)
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
    context = {'results': results_sorted}
    return render(request, 'resultat.html', context)


def get_thematique_forms():
    election = voxe.Election(settings.VOXE_ELECTION_ID)
    thematiques = election.thematiques
    count = len(thematiques)

    thematique_forms = [ThematiqueForm for each in range(count)]
    if not thematique_forms:
        return [ThematiqueForm]
    return thematique_forms


def programmes(request):
    candidats = Candidat.objects.all()
    thematiques = Thematique.objects.all()
    propositions = Proposition.objects.all().order_by('candidat')
    context = {'thematiques': thematiques,'candidats': candidats, 'propositions':propositions}
    return render(request, 'programme.html', context)


class ChoisirWizard(SessionWizardView):
    form_list = get_thematique_forms()
    template_name = 'choisir.html'

    def done(self, form_list, **kwargs):
        results = []
        for form in form_list:
            results.append(form.cleaned_data['proposition'])
        self.request.session['results'] = results
        
        return HttpResponseRedirect('/resultat/')

    def get_context_data(self, **kwargs):
        election = voxe.Election(settings.VOXE_ELECTION_ID)
        thematiques = election.thematiques
        context = super(ChoisirWizard, self).get_context_data(**kwargs)
        form_name = str(context['form'])
        form_id_regex = re.search('name="(\d+)\-', form_name)
        form_current = int(form_id_regex.groups()[0])
        for idx, t in enumerate(thematiques):
            if form_current == idx:
                context['thematique'] = t
        return context


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
