# Generated by Django 3.0.5 on 2020-04-22 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUser', '0005_auto_20200422_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginAuditLogModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=128, null=True)),
                ('ip', models.CharField(blank=True, max_length=128, null=True)),
                ('HTTP_ORIGIN', models.CharField(blank=True, max_length=256, null=True)),
                ('status', models.CharField(choices=[('SUCCESS', 'SUCCESS'), ('FAILURE', 'FAILURE')], max_length=128)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loginauditlogmodel_approved_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]