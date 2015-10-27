# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pabrik.models


class Migration(migrations.Migration):

    dependencies = [
        ('pabrik', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bahan_baku',
            name='jumlah_outsource',
            field=models.DecimalField(default=0, verbose_name=b'Jumlah di Mi An', max_digits=20, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bahan_baku',
            name='keterangan',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pembelian',
            name='keterangan',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='penjualan',
            name='keterangan',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='produk',
            name='keterangan',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='produk_produksi',
            name='keterangan',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pembelian',
            name='supplier',
            field=models.CharField(max_length=60, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='penjualan',
            name='nomor_nota',
            field=models.IntegerField(default=pabrik.models.number, unique=True),
        ),
    ]
