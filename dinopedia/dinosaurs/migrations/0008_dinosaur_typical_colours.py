# Generated by Django 4.0.6 on 2022-07-23 13:44

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dinosaurs', '0007_alter_dinosaur_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='dinosaur',
            name='typical_colours',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=12, null=True), null=True, size=4),
        ),
    ]