# Generated by Django 5.0.6 on 2024-07-05 10:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0006_alter_fabricator_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabricator',
            name='id',
            field=models.UUIDField(default=uuid.UUID('3538af22-db86-47ba-a922-9b00a1bcf903'), editable=False, primary_key=True, serialize=False),
        ),
    ]
