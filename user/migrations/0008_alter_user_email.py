# Generated by Django 5.0.6 on 2024-08-12 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_remove_taskrecord_punch_pushrecord_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, null=True, verbose_name='Email Address'),
        ),
    ]
