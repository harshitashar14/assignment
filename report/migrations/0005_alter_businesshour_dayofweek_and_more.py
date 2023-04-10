# Generated by Django 4.2 on 2023-04-08 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_alter_businesshour_dayofweek'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesshour',
            name='dayOfWeek',
            field=models.IntegerField(choices=[(5, 'SAT'), (6, 'SUN'), (1, 'TUE'), (0, 'MON'), (4, 'FRI'), (2, 'WED'), (3, 'THU')]),
        ),
        migrations.AlterField(
            model_name='businesshour',
            name='end_time_local',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='businesshour',
            name='start_time_local',
            field=models.TimeField(),
        ),
    ]
