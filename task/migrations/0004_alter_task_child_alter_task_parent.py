# Generated by Django 5.0.6 on 2024-07-05 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_alter_assignedlist_approved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='child',
            field=models.ManyToManyField(blank=True, null=True, to='task.task', verbose_name='Child Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.task', verbose_name='Parent Task'),
        ),
    ]
