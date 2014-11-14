from django.conf.urls import patterns, url
from securewitness import views

urlpatterns = patterns('securewitness.views',
	url(r'^index/$', 'index', name='index'),
	url(r'^postbulletin/$', 'postbulletin', name='postbulletin'),
)
