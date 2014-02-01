from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'profilitique.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^candidats/$', 'programmes.views.indexcandidat'),
	url(r'^proposition/$', 'programmes.views.indexproposition'),
    url(r'^questions/$', 'programmes.views.questions'),
)
