# Generated by Django 3.1.2 on 2020-10-17 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20201017_1502'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LastBooks',
            new_name='LastBook',
        ),
        migrations.RenameModel(
            old_name='LastEvents',
            new_name='LastEvent',
        ),
    ]
