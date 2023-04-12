from django.db import models
import uuid


# Create your models here.
class StatusChoices(models.TextChoices):
    ACTIVE = "active"
    INACTIVE = "inactive"


class DayOfWeek(models.TextChoices):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


class ReportStatus(models.TextChoices):
    RUNNING = 'Running'
    COMPLETE = 'Complete'
    FAILED = 'Failed'


class StoreStatus(models.Model):
    store_id = models.CharField(max_length=20)
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=10, choices=StatusChoices.choices)


class BusinessHour(models.Model):
    store_id = models.CharField(max_length=20)
    dayOfWeek = models.IntegerField(choices=DayOfWeek.choices)
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['store_id', 'dayOfWeek'], name='unique appversion')
        ]


class StoreTimezone(models.Model):
    store_id = models.CharField(max_length=20)
    timezone_str = models.CharField(max_length=50, default="America/Chicago")


class Report(models.Model):
    report_id = models.UUIDField(default=uuid.uuid4,
                                 primary_key=True,
                                 editable=False)

    status = models.CharField(max_length=10, choices=ReportStatus.choices, default=ReportStatus.RUNNING)

    csv_report = models.FileField(upload_to='csvs/', default=None)
