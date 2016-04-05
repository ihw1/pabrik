from django.conf.urls import patterns, url

from pabrik import views

urlpatterns = patterns('',
                       url(r'^(?P<penjualan_id>\d+)/nota/$', views.nota, name='nota'),
                       url(r'^(?P<nota_gabungan_id>\d+)/nota_gabungan/$', views.nota_gabungan, name='nota_gabungan'),
                       )