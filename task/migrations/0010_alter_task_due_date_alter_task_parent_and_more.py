# Generated by Django 5.0.6 on 2024-07-15 08:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_alter_task_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(verbose_name='Due Date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.task', verbose_name='Parent Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('ASSINGED', 'Assigned'), ('ON-HOLD', 'On-Hold'), ('BREAK', 'Break'), ('APPROVED', 'Approved'), ('COMPLETE', 'Completed')], default='ASSIGNED', max_length=255, verbose_name='Status'),
        ),
    ]
