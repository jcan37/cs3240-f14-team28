from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

from securewitness import views

urlpatterns = patterns('',
                       url(r'^$', RedirectView.as_view(url='/securewitness/index/')),
                       url(r'^securewitness/', include('securewitness.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)

admin.site.site_header = 'SecureWitness Administration'
