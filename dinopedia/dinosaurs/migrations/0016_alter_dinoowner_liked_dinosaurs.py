# Generated by Django 4.0.6 on 2022-07-25 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dinosaurs', '0015_alter_dinoowner_petdino'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dinoowner',
            name='liked_dinosaurs',
            field=models.ManyToManyField(blank=True, to='dinosaurs.dinosaur'),
        ),
    ]