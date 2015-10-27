# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pabrik', '0004_auto_20151019_1601'),
    ]

    operations = [
        migrations.RenameField(
            model_name='penyusutan',
            old_name='jumlah',
            new_name='jumlah_susut',
        ),
    ]
