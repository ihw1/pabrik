# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bahan_baku',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama', models.CharField(max_length=60)),
                ('jumlah', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
            ],
            options={
                'verbose_name': 'bahan baku',
                'verbose_name_plural': 'bahan baku',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bahan_baku_produk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jumlah_bahan', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('bahan_baku', models.ForeignKey(to='pabrik.Bahan_baku')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pembelian',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nomor_nota', models.IntegerField(default=0)),
                ('tgl_beli', models.DateField(verbose_name=b'tanggal')),
                ('supplier', models.CharField(max_length=60)),
                ('harga_total', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
            ],
            options={
                'verbose_name_plural': 'pembelian',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pembelian_detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jumlah_beli', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('harga_bahan', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('bahan_baku', models.ForeignKey(to='pabrik.Bahan_baku')),
                ('pembelian', models.ForeignKey(to='pabrik.Pembelian')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Penjualan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nomor_nota', models.IntegerField(default=0)),
                ('tgl_jual', models.DateField(verbose_name=b'tanggal')),
                ('harga_total', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('terkirim', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(to='pabrik.Customer')),
            ],
            options={
                'verbose_name_plural': 'penjualan',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Penjualan_detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jumlah_produk', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('harga_produk', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('penjualan', models.ForeignKey(to='pabrik.Penjualan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Penjualan_pembayaran',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tgl_bayar', models.DateField(verbose_name=b'tanggal')),
                ('jumlah_bayar', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('penjualan', models.ForeignKey(to='pabrik.Penjualan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Produk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama', models.CharField(max_length=60)),
                ('jumlah', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('harga', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
            ],
            options={
                'verbose_name_plural': 'produk',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Produk_harga_special',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('harga', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('customer', models.ForeignKey(to='pabrik.Customer')),
                ('produk', models.ForeignKey(to='pabrik.Produk')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Produk_produksi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tgl_produksi', models.DateField(verbose_name=b'tgl produksi')),
                ('jumlah', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('produk', models.ForeignKey(to='pabrik.Produk')),
            ],
            options={
                'verbose_name': 'produksi',
                'verbose_name_plural': 'produksi',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='penjualan_detail',
            name='produk',
            field=models.ForeignKey(to='pabrik.Produk'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bahan_baku_produk',
            name='produk',
            field=models.ForeignKey(to='pabrik.Produk'),
            preserve_default=True,
        ),
    ]
