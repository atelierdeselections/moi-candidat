from django.contrib import admin
from programmes.models import Parti, Candidat, Thematique, Proposition


class CandidatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'parti_list')
    fields = (('nom', 'prenom'), 'partis')


class PropositionAdmin(admin.ModelAdmin):
    list_display = ('resume', 'source', 'candidat', 'thematique')


admin.site.register(Parti)
admin.site.register(Candidat,CandidatAdmin)
admin.site.register(Thematique)
admin.site.register(Proposition, PropositionAdmin)
