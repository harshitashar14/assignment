# Generated by Django 4.2 on 2023-04-07 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesshour',
            name='dayOfWeek',
            field=models.IntegerField(choices=[(6, 'SUN'), (5, 'SAT'), (2, 'WED'), (0, 'MON'), (4, 'FRI'), (1, 'TUE'), (3, 'THU')]),
        ),
    ]