# -*- coding: utf-8 -*-
import hashlib
from django.db import models


class Resultat(models.Model):
    hashcode = models.CharField(u'Hashcode dans les URLs de partage', max_length=200)
    propositions_csv = models.CharField(u'Une liste de Propositions ID separés par des virgules sans espaces', max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.propositions_csv

    def save(self, *args, **kwargs):
        if not self.hashcode:
            self.hashcode = hashlib.md5(self.propositions_csv).hexdigest()
        super(Resultat, self).save()
