# Generated by Django 3.0.5 on 2020-05-03 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poke_calc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='aloan',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='galarian',
            field=models.NullBooleanField(default=False),
        ),
    ]