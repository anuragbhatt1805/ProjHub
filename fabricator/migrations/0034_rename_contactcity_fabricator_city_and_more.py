# Generated by Django 5.0.6 on 2024-07-25 06:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0033_remove_fabricator_contract'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fabricator',
            old_name='contactCity',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='fabricator',
            old_name='contactCountry',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='fabricator',
            old_name='contactState',
            new_name='state',
        ),
        migrations.RemoveField(
            model_name='fabricator',
            name='contactPerson',
        ),
        migrations.RemoveField(
            model_name='fabricator',
            name='contactPhone',
        ),
        migrations.AddField(
            model_name='fabricator',
            name='zipCode',
            field=models.CharField(default=560045, max_length=6, verbose_name='Zip Code'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PersonName', models.CharField(max_length=150, verbose_name='Full Name')),
                ('designation', models.CharField(max_length=150, verbose_name='Designation')),
                ('phone', models.CharField(max_length=13, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=150, verbose_name='Email Address')),
                ('fabricator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fabricator.fabricator', verbose_name='Fabricator')),
            ],
        ),
    ]
