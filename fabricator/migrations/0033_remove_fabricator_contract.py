# Generated by Django 5.0.6 on 2024-07-25 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0032_alter_fabricator_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fabricator',
            name='contract',
        ),
    ]
