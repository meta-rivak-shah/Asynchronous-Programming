# Generated by Django 3.0.5 on 2020-04-27 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUser', '0009_loginauditlogmodel_exception'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customusermodel',
            old_name='is_active',
            new_name='active',
        ),
    ]
