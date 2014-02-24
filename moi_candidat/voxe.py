#!/usr/bin/env python
import os
import json
import hashlib
import urllib2
from django.conf import settings


class Election(object):
    def __init__(self, id, cache_disabled=False):
        self.id = id
        self.candidatures = []
        self.candidats = []
        self.thematiques = []
        self.propositions = []
        self.cache_disabled = cache_disabled

        self._election_data()

    def _get_data(self, url):
        """Get from cache or from API."""
        key = hashlib.md5(url).hexdigest()
        file_cached = os.path.join(settings.VOXE_CACHE_DIR, '%s.json' % key)
        if not os.path.isfile(file_cached) or self.cache_disabled:
            headers = {
                'User-Agent': 'curl/7.21.0 (x86_64-pc-linux-gnu) libcurl/7.21.0 OpenSSL/0.9.8o zlib/1.2.3.3 libidn/1.8 libssh2/0.18',
                'Accept': '*/*',
            }
            req = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(req)
            raw_json = response.read()
            # Save response to file
            with open(file_cached, 'w') as f:
                f.write(raw_json)
        else:
            # Read response from file
            with open(file_cached) as f:
                raw_json = f.read()
        data = json.loads(raw_json)['response']
        return data

    def _election_data(self):
        url = '%s/elections/%s' % (settings.VOXE_API, self.id)
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
        url = '%s/propositions/search?candidacyIds=%s' % (settings.VOXE_API, ",".join(candidacies_ids))
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
            thematique.sous_thematiques = []
            for subtag in tag['tags']:
                sous_thematique = Thematique(subtag['id'])
                sous_thematique.nom = subtag['name']
                thematique.sous_thematiques.append(sous_thematique)
            self.thematiques.append(thematique)
            for proposition in self.propositions:
                if thematique.id in proposition.tags:
                    thematique.propositions.append(proposition)
                    for sous_thematique in thematique.sous_thematiques:
                        if sous_thematique.id in proposition.tags:
                            sous_thematique.propositions.append(proposition)
                            proposition.sous_thematique = sous_thematique

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
        self.sous_thematiques = []

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.nom.encode('utf-8'))


class Proposition(object):
    def __init__(self, id):
        self.id = id
        self.description = ''
        self.tags = []
        self.sous_thematique = None

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.id)
