from django.db import models

# Create your models here.
STATUS_CHOICES = (
    ("active", "active"),
    ("inactive", "inactive"),
)

DAY_OF_WEEK = {
    (0, 'MON'),
    (1, 'TUE'),
    (2, 'WED'),
    (3, 'THU'),
    (4, 'FRI'),
    (5, 'SAT'),
    (6, 'SUN')
}


class StoreStatus(models.Model):
    store_id = models.CharField(max_length=20)
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=10,choices=STATUS_CHOICES)


class BusinessHour(models.Model):
    store_id = models.CharField(max_length=20)
    dayOfWeek = models.IntegerField(choices=DAY_OF_WEEK)
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['store_id', 'dayOfWeek'], name='unique appversion')
        ]


class StoreTimezone(models.Model):
    store_id = models.CharField(max_length=20)
    timezone_str = models.CharField(max_length=50,default="America/Chicago")

