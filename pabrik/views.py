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