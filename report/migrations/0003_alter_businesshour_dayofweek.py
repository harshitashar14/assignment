# Generated by Django 4.2 on 2023-04-08 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_alter_businesshour_dayofweek'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesshour',
            name='dayOfWeek',
            field=models.IntegerField(choices=[(3, 'THU'), (6, 'SUN'), (2, 'WED'), (5, 'SAT'), (4, 'FRI'), (0, 'MON'), (1, 'TUE')]),
        ),
    ]
