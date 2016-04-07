from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views import generic
from pabrik.models import *

def nota(request, penjualan_id):
    try:
        penjualan = Penjualan.objects.get(pk=penjualan_id)
    except Penjualan.DoesNotExist:
        raise Http404
    return render(request, 'pabrik/nota.html', {'penjualan': penjualan})

def nota_gabungan(request, nota_gabungan_id):
    try:
        nota_gabungan = Nota_gabungan.objects.get(pk=nota_gabungan_id)
    except Nota_gabungan.DoesNotExist:
        raise Http404
    return render(request, 'pabrik/nota_gabungan.html', {'nota_gabungan': nota_gabungan})


def print_nota(request, nota_gabungan_id_list):
    nota_gabungan_list = []
    for ng_id in nota_gabungan_id_list.split("A"):
        try:
            nota_gabungan = Nota_gabungan.objects.get(pk=ng_id)
            nota_gabungan_list.append(nota_gabungan)
        except Nota_gabungan.DoesNotExist:
            pass
    return render(request, 'pabrik/print_nota.html', {'nota_gabungan_list': nota_gabungan_list})