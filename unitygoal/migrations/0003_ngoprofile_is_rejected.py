# Generated by Django 3.2.23 on 2023-11-29 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitygoal', '0002_alter_ngoprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ngoprofile',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]
