# Generated by Django 2.1.5 on 2020-06-26 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_events'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Events',
            new_name='Event',
        ),
    ]
