from django.conf.urls import patterns, url

from pabrik import views

urlpatterns = patterns('',
                       url(r'^(?P<penjualan_id>\d+)/nota/$', views.nota, name='nota'),
                       )