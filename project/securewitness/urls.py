from django.conf.urls import patterns, url
from securewitness import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
)
