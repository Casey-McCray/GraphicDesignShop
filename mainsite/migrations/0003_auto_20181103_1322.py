# Generated by Django 2.1.1 on 2018-11-03 07:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0002_auto_20181103_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
    ]
