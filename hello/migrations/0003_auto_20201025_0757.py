# Generated by Django 3.1.2 on 2020-10-25 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20201024_2339'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='weatherrating',
            unique_together=set(),
        ),
    ]
