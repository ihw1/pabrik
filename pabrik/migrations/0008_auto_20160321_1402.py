# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pabrik', '0007_penyusutan_di_outsource'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama', models.CharField(max_length=200)),
                ('telp', models.CharField(max_length=50, null=True, blank=True)),
                ('alamat', models.CharField(max_length=200, null=True, blank=True)),
                ('kategori', models.CharField(max_length=50, null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'supplier',
                'verbose_name_plural': 'supplier',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='customer',
            name='alamat',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='telp',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pembelian',
            name='supplier',
            field=models.ForeignKey(to='pabrik.Supplier'),
        ),
    ]
