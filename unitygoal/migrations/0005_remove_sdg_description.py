# Generated by Django 3.2.23 on 2023-11-29 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unitygoal', '0004_project_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sdg',
            name='description',
        ),
    ]
