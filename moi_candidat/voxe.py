#!/usr/bin/env python
import hashlib
import requests
from django.core.cache import cache

API = 'http://voxe.org/api/v1'


class Election(object):
    def __init__(self, id):
        self.id = id
        self.candidatures = []
        self.candidats = []
        self.thematiques = []
        self.propositions = []

        self._election_data()

    def _get_data(self, url):
        key = hashlib.md5(url).hexdigest()
        data = cache.get(key)
        if not data:
            r = requests.get(url)
            data = r.json()['response']
            cache.set(key, data)
        return data

    def _election_data(self):
        url = '%s/elections/%s' % (API, self.id)
        data_election = self._get_data(url)

        for candidacy in data_election['election']['candidacies']:
            candidature = Candidature(candidacy['id'])
            for candidate in candidacy['candidates']:
                candidat = Candidat(candidate['id'])
                candidat.nom = candidate['lastName']
                candidat.prenom = candidate['firstName']
                candidat.photo_url = candidate['photo']['sizes']['medium']['url']
                candidature.candidats.append(candidat)
                self.candidats.append(candidat)
            self.candidatures.append(candidature)

        candidacies_ids = [c.id for c in self.candidatures]
        url = '%s/propositions/search?candidacyIds=%s' % (API, ",".join(candidacies_ids))
        data = self._get_data(url)
        for p in data['propositions']:
            proposition = Proposition(p['id'])
            proposition.description = p['text']
            proposition.tags = [t['id'] for t in p['tags']]
            for candidature in self.candidatures:
                if p['candidacy']['id'] == candidature.id:
                    proposition.candidature = candidature
            self.propositions.append(proposition)

        for tag in data_election['election']['tags']:
            thematique = Thematique(tag['id'])
            thematique.nom = tag['name']
            for proposition in self.propositions:
                if thematique.id in proposition.tags:
                    thematique.propositions.append(proposition)
            self.thematiques.append(thematique)

    def candidature_by_candidat(self, candidat):
        for candidature in self.candidatures:
            candidats_ids = [c.id for c in candidature.candidats]
            if candidat.id in candidats_ids:
                return candidature

    def propositions_by_candidat(self, candidat):
        propositions = []
        for proposition in self.propositions:
            candidature = self.candidature_by_candidat(candidat)
            if proposition.candidature.id == candidature.id:
                propositions.append(proposition)
        return propositions


class Candidature(object):
    def __init__(self, id):
        self.id = id
        self.candidats = []

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.id)


class Candidat(object):
    def __init__(self, id):
        self.id = id
        self.nom = ''
        self.prenom = ''
        self.photo_url = ''

    def __repr__(self):
        fullname = "%s %s" % (self.prenom, self.nom)
        return "<%s: %s>" % (self.__class__.__name__, fullname.encode('utf-8'))


class Thematique(object):
    def __init__(self, id):
        self.id = id
        self.nom = ''
        self.propositions = []

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.nom.encode('utf-8'))


class Proposition(object):
    def __init__(self, id):
        self.id = id
        self.description = ''
        self.tags = []

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.id)
