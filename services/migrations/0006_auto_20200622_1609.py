# Generated by Django 2.1.5 on 2020-06-22 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_contactus'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContactUs',
            new_name='Contact',
        ),
        migrations.RenameModel(
            old_name='Services',
            new_name='Service',
        ),
    ]
