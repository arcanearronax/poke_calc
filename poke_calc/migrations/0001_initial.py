# Generated by Django 3.0.6 on 2020-05-18 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CPMultiplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('multipler', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('poke_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('dex_id', models.IntegerField()),
                ('form', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PokemonStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_atk', models.IntegerField()),
                ('base_def', models.IntegerField()),
                ('base_sta', models.IntegerField()),
                ('poke', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poke_calc.Pokemon')),
            ],
        ),
        migrations.CreateModel(
            name='Evolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='poke_calc.Pokemon')),
                ('poke', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pre', to='poke_calc.Pokemon')),
            ],
        ),
    ]
