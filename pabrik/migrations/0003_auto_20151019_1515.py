# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pabrik', '0002_auto_20151019_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='Outsource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tgl_outsource', models.DateField(verbose_name=b'tanggal')),
                ('keterangan', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Kirim ke Mi An',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Outsource_detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jumlah_outsource', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('bahan_baku', models.ForeignKey(to='pabrik.Bahan_baku')),
                ('outsource', models.ForeignKey(to='pabrik.Outsource')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='bahan_baku',
            name='jumlah_outsource',
            field=models.DecimalField(default=0, verbose_name=b'Jmlh di Mi An', max_digits=20, decimal_places=2),
        ),
    ]
