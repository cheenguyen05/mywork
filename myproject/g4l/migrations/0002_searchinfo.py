# Generated by Django 3.2 on 2024-07-17 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('g4l', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('school', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
            ],
        ),
    ]
