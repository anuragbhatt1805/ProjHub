# Generated by Django 5.0.6 on 2024-07-05 14:41

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0014_alter_fabricator_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabricator',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6f60c060-3d53-41bd-a7ed-27749325b6e9'), editable=False, primary_key=True, serialize=False),
        ),
    ]
