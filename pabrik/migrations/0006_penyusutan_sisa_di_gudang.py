# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pabrik', '0005_auto_20151019_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='penyusutan',
            name='sisa_di_gudang',
            field=models.DecimalField(default=0, max_digits=20, decimal_places=2),
            preserve_default=True,
        ),
    ]
