# Generated by Django 4.2 on 2023-04-11 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0011_report_alter_businesshour_dayofweek'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesshour',
            name='dayOfWeek',
            field=models.IntegerField(choices=[('0', 'Mon'), ('1', 'Tue'), ('2', 'Wed'), ('3', 'Thu'), ('4', 'Fri'), ('5', 'Sat'), ('6', 'Sun')]),
        ),
        migrations.AlterField(
            model_name='storestatus',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=10),
        ),
    ]