# Generated by Django 5.0.6 on 2024-07-16 06:13

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0028_alter_fabricator_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabricator',
            name='id',
            field=models.UUIDField(default=uuid.UUID('3a6b1fb2-d2ec-48a2-9618-b3c2ac83c94c'), editable=False, primary_key=True, serialize=False),
        ),
    ]
