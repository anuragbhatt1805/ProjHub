# Generated by Django 5.0.6 on 2024-07-05 12:03

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0010_alter_fabricator_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabricator',
            name='id',
            field=models.UUIDField(default=uuid.UUID('99375907-d97b-43e0-8286-0420ab5b1555'), editable=False, primary_key=True, serialize=False),
        ),
    ]
