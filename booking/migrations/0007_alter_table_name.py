# Generated by Django 3.2 on 2022-02-20 19:12

import booking.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_alter_table_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='name',
            field=booking.models.NameField(max_length=15, unique=True),
        ),
    ]
