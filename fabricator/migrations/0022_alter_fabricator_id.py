# Generated by Django 5.0.6 on 2024-07-15 08:17

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0021_alter_fabricator_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabricator',
            name='id',
            field=models.UUIDField(default=uuid.UUID('8ebd2f6f-87d2-4084-8e65-6775a319b3af'), editable=False, primary_key=True, serialize=False),
        ),
    ]
