# Generated by Django 5.0.6 on 2024-07-25 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_project_tool'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='connectionDesign',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='miscDesign',
            field=models.BooleanField(default=False),
        ),
    ]
