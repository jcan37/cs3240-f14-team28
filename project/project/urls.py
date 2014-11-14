from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/securewitness/')),
    url(r'^securewitness/', include('securewitness.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

admin.site.site_header = 'SecureWitness Administration'
