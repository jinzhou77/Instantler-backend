# Generated by Django 2.2 on 2019-04-13 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('User', '0004_usertype'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('american', models.IntegerField(default=0)),
                ('seafood', models.IntegerField(default=0)),
                ('steak', models.IntegerField(default=0)),
                ('fast', models.IntegerField(default=0)),
                ('bar', models.IntegerField(default=0)),
                ('finedining', models.IntegerField(default=0)),
                ('chinese', models.IntegerField(default=0)),
                ('japanese', models.IntegerField(default=0)),
                ('korean', models.IntegerField(default=0)),
                ('mexican', models.IntegerField(default=0)),
                ('pizza', models.IntegerField(default=0)),
                ('breakfast', models.IntegerField(default=0)),
                ('noodle', models.IntegerField(default=0)),
                ('italian', models.IntegerField(default=0)),
                ('mediterranean', models.IntegerField(default=0)),
                ('french', models.IntegerField(default=0)),
                ('vegetarian', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
