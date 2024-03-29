from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from securewitness import views

urlpatterns = patterns('securewitness.views',
                       url(r'^$', RedirectView.as_view(url='/securewitness/index/')),
                       url(r'^index/$', 'index', name='index'),
                       url(r'^signup/$', 'signup', name='signup'),
                       url(r'^post/$', 'post', name='post'),
                       url(r'^download/(?P<fname>[0-9]+_.+)/$', 'download', name='download'),
                       url(r'^move/(?P<folder_id>\d+)/(?P<bulletin_id>\d+)/$', 'move_bulletin', name='move_bulletin'),
                       url(r'^copy/bulletin/(?P<b_id>\d+)/$', 'copy_bulletin', name='copy_bulletin'),
                       url(r'^delete/bulletin/(?P<b_id>\d+)/$', 'delete_bulletin', name='delete_bulletin'),
                       url(r'^copy/folder/(?P<folder_id>\d+)/$', 'copy_folder', name='copy_folder'),
                       url(r'^delete/folder/(?P<folder_id>\d+)/$', 'delete_folder', name='delete_folder'),
)
