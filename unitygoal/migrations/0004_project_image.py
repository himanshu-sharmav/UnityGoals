# Generated by Django 3.2.23 on 2023-11-29 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitygoal', '0003_ngoprofile_is_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.FileField(null=True, upload_to='project_pic/'),
        ),
    ]
