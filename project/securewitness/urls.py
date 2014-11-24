from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from securewitness import views

urlpatterns = patterns('securewitness.views',
                       url(r'^$', RedirectView.as_view(url='/securewitness/index/')),
                       url(r'^index/$', 'index', name='index'),
                       url(r'^signup/$', 'signup', name='signup'),
                       url(r'^post/$', 'post', name='post'),
                       url(r'^download/($w+)', 'download', name='download'),
)
