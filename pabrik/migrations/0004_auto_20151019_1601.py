# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pabrik', '0003_auto_20151019_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Penyusutan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tgl_penyusutan', models.DateField(verbose_name=b'tanggal')),
                ('jumlah', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('keterangan', models.TextField(null=True, blank=True)),
                ('bahan_baku', models.ForeignKey(to='pabrik.Bahan_baku')),
            ],
            options={
                'verbose_name': 'penyusutan',
                'verbose_name_plural': 'penyusutan',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'pelanggan', 'verbose_name_plural': 'pelanggan'},
        ),
        migrations.AlterModelOptions(
            name='outsource',
            options={'verbose_name': 'Kiriman ke Mi An', 'verbose_name_plural': 'Kiriman ke Mi An'},
        ),
        migrations.AddField(
            model_name='produk_produksi',
            name='dari_outsource',
            field=models.BooleanField(default=False, verbose_name=b'Dari Mi An'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='outsource_detail',
            name='jumlah_outsource',
            field=models.DecimalField(default=0, verbose_name=b'jumlah', max_digits=20, decimal_places=2),
        ),
    ]
