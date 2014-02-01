from django.db import models


class Candidat(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    parti = models.CharField(max_length=200)
    

    def __unicode__(self):
        return self.nom


class Thematique(models.Model):
    nom = models.CharField(max_length=200)

    def __unicode__(self):
        return self.nom


class Proposition(models.Model):
    resume = models.TextField()
    description = models.TextField()
    thematique = models.ForeignKey(Thematique)
    candidat = models.ForeignKey(Candidat)

    def __unicode__(self):
        return self.resume
