# Generated by Django 5.0.6 on 2024-07-15 10:48

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0022_alter_fabricator_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabricator',
            name='id',
            field=models.UUIDField(default=uuid.UUID('96c39cd1-48fe-45b1-b948-8cdc2462f071'), editable=False, primary_key=True, serialize=False),
        ),
    ]
