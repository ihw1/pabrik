# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pabrik', '0006_penyusutan_sisa_di_gudang'),
    ]

    operations = [
        migrations.AddField(
            model_name='penyusutan',
            name='di_outsource',
            field=models.BooleanField(default=False, verbose_name=b'Di Mi An'),
            preserve_default=True,
        ),
    ]
