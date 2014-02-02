from django.conf.urls import patterns, include, url
from programmes.views import ChoisirWizard

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'profilitique.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'programmes.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^candidats/$', 'programmes.views.indexcandidat'),
	url(r'^proposition/$', 'programmes.views.indexproposition'),

	url(r'^choisir/$', 'programmes.views.choisir'),
	url(r'^programmes/$', 'programmes.views.programmes'),
    #(r'^choisir/$', ChoisirWizard.as_view(template_name='choisir.html')),

)
