from django.contrib import admin
from programmes.models import Candidat, Thematique, Proposition

class CandidatAdmin(admin.ModelAdmin):
	list_display = ('nom', 'prenom','parti')
admin.site.register(Candidat,CandidatAdmin)
admin.site.register(Thematique)
admin.site.register(Proposition)
