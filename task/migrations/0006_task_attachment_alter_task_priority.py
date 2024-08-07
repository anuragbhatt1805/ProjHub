# Generated by Django 5.0.6 on 2024-07-15 07:24

import task.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_alter_task_child'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to=task.models.uploadTaskFile, verbose_name='Attachment'),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(0, 'Low'), (1, 'Normal'), (2, 'High'), (3, 'Critical')], default=1, verbose_name='Priority'),
        ),
    ]
