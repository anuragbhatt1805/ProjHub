# Generated by Django 5.0.6 on 2024-08-12 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_alter_project_connectiondesign_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='customer',
            field=models.BooleanField(default=False, verbose_name='Customer'),
        ),
    ]
