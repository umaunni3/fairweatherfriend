# Generated by Django 3.1.2 on 2020-10-24 20:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.IntegerField()),
                ('past_temps', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None)),
            ],
        ),
    ]
