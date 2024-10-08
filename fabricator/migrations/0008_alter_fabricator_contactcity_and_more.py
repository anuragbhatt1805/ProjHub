# Generated by Django 5.0.6 on 2024-07-05 11:49

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0007_alter_fabricator_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabricator',
            name='contactCity',
            field=models.CharField(max_length=150, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='fabricator',
            name='contactCountry',
            field=models.CharField(max_length=150, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='fabricator',
            name='contactPerson',
            field=models.CharField(max_length=150, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='fabricator',
            name='contactPhone',
            field=models.CharField(max_length=13, verbose_name='Contact Number'),
        ),
        migrations.AlterField(
            model_name='fabricator',
            name='contactState',
            field=models.CharField(max_length=150, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='fabricator',
            name='fabName',
            field=models.CharField(max_length=150, unique=True, verbose_name='Fabricator Name'),
        ),
        migrations.AlterField(
            model_name='fabricator',
            name='id',
            field=models.UUIDField(default=uuid.UUID('984e9b9a-370d-4a2a-b5bb-adc48ced1787'), editable=False, primary_key=True, serialize=False),
        ),
    ]
