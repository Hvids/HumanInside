# Generated by Django 3.1.2 on 2020-10-16 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20201015_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pages',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
