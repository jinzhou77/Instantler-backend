# Generated by Django 2.2 on 2019-04-12 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0007_delete_restaurantreview'),
        ('TakeANumber', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waitinguser',
            name='tableType',
        ),
        migrations.AddField(
            model_name='waitinguser',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Restaurant.Restaurant'),
        ),
    ]
