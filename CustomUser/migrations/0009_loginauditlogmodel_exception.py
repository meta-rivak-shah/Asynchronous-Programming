# Generated by Django 3.0.5 on 2020-04-26 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUser', '0008_auto_20200425_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginauditlogmodel',
            name='exception',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
