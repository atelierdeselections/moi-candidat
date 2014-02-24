import os
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

import voxe


@override_settings(VOXE_ELECTION_ID='5308832950b843643e0000c9')
@override_settings(VOXE_CACHE_DIR=os.path.join(settings.BASE_DIR, 'programmes', 'fixtures'))
class VoxeTestCase(TestCase):
    def setUp(self):
        self.election = voxe.Election(settings.VOXE_ELECTION_ID)

    def test_candidats(self):
        self.assertEqual(len(self.election.candidats), 10)

    def test_thematiques(self):
        self.assertEqual(len(self.election.thematiques), 6)

    def test_propositions(self):
        self.assertEqual(len(self.election.propositions), 297)

    def test_proposition_belongs_sous_thematique(self):
        proposition = self.election.propositions[0]
        self.assertEqual(proposition.sous_thematique.nom, u'Emploi')

    def test_thematique_has_sous_thematique(self):
        thematique = self.election.thematiques[0]
        self.assertEqual(len(thematique.sous_thematiques), 6)
        self.assertEqual(thematique.sous_thematiques[2].nom, u'Vie politique locale')

    def test_thematique_has_propositions(self):
        thematique = self.election.thematiques[0]
        self.assertEqual(len(thematique.propositions), 57)

    def test_sous_thematique_has_propositions(self):
        thematique = self.election.thematiques[0]
        sous_thematique = thematique.sous_thematiques[0]
        self.assertEqual(len(sous_thematique.propositions), 4)
