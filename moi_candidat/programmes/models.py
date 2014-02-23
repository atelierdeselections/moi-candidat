# -*- coding: utf-8 -*-
import hashlib
from django.db import models


class Parti(models.Model):
    nom = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.nom


class Candidat(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(u'prénom', max_length=200)
    bio = models.TextField(blank=True)
    photo = models.FileField(upload_to='candidats', blank=True)
    partis = models.ManyToManyField(Parti)

    def __unicode__(self):
        return self.nom

    def parti_list(self):
        partis = [p.nom for p in self.partis.all()]
        return ", ".join(partis)
    parti_list.short_description = 'Partis'


class Thematique(models.Model):
    nom = models.CharField(max_length=200)

    class Meta:
        verbose_name = u'thématique'

    def __unicode__(self):
        return self.nom


class Proposition(models.Model):
    resume = models.TextField(u'résumé')
    description = models.TextField()
    source = models.TextField()
    thematique = models.ForeignKey(Thematique, verbose_name=u'thématique')
    candidat = models.ForeignKey(Candidat)

    def __unicode__(self):
        return self.resume

class Resultat(models.Model):
    hashcode = models.CharField(u'Hashcode dans les URLs de partage', max_length=200)
    propositions_csv = models.CharField(u'Une liste de Propositions ID separés par des virgules sans espaces', max_length=200)

    def __unicode__(self):
        return self.propositions_csv

    def save(self, *args, **kwargs):
        if not self.hashcode:
            self.hashcode = hashlib.md5(self.propositions_csv).hexdigest()
        super(Resultat, self).save()
