from django.conf.urls import patterns, url
from securewitness import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^postbulletin/$', views.postbulletin, name='postbulletin'),
	url(r'^login/$', views.login, name='login'),
)
