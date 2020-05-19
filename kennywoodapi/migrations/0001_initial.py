# Generated by Django 3.0.6 on 2020-05-19 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('area',),
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_members', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': (django.db.models.expressions.OrderBy(django.db.models.expressions.F('user.date_joined'), nulls_last=True),),
            },
        ),
        migrations.CreateModel(
            name='ParkArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('theme', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('theme',),
            },
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starttime', models.IntegerField()),
                ('attraction', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='kennywoodapi.Attraction')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='kennywoodapi.Customer')),
            ],
            options={
                'verbose_name': 'itinerary',
                'verbose_name_plural': 'itineraries',
                'ordering': ('starttime',),
            },
        ),
        migrations.AddField(
            model_name='attraction',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='kennywoodapi.ParkArea'),
        ),
    ]
