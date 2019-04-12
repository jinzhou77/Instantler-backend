# Generated by Django 2.2 on 2019-04-12 00:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Restaurant', '0007_delete_restaurantreview'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Table', '0003_auto_20190411_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='WSNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waitingNumber', models.IntegerField(default=0)),
                ('servedNumber', models.IntegerField(default=0)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Restaurant.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='WaitingUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myNumber', models.IntegerField()),
                ('tableType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Table.TableType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
