# Generated by Django 5.0.6 on 2024-07-15 08:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0020_alter_fabricator_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabricator',
            name='id',
            field=models.UUIDField(default=uuid.UUID('ca1e9a0f-aa15-45e7-b0a0-68508ade85ba'), editable=False, primary_key=True, serialize=False),
        ),
    ]
