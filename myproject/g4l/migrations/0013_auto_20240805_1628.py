# Generated by Django 3.2 on 2024-08-05 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('g4l', '0012_auto_20240730_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='day_of_month',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='todolist',
            name='day_of_week',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='todolist',
            name='specific_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='job_type',
            field=models.CharField(choices=[('Daily', 'Hàng ngày'), ('Weekly', 'Ngày trong tuần'), ('Monthly', 'Ngày trong tháng'), ('One_time', 'Làm trong ngày')], default='Daily', max_length=10),
        ),
    ]
