# Generated by Django 3.1.2 on 2020-10-31 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_auto_20201031_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('type_price', models.CharField(max_length=255)),
                ('type_schedule', models.CharField(max_length=255)),
                ('time_learn', models.CharField(max_length=255)),
                ('one_duration', models.CharField(max_length=255)),
                ('name_org', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('underground', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='LastSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('score', models.FloatField(blank=True, default=None, null=True)),
                ('id_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.section')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.user')),
            ],
        ),
    ]
