# Generated by Django 3.2 on 2024-07-29 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('g4l', '0010_todolist_job_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='job_type',
            field=models.CharField(choices=[('daily', 'Hàng ngày'), ('weekly', 'Ngày trong tuần'), ('monthly', 'Ngày trong tháng'), ('one_time', 'Làm trong ngày')], default='one_time', max_length=10),
        ),
    ]
