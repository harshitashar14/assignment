import csv
import datetime
import traceback
from io import StringIO

import numpy
import numpy as np
from django.core.files.base import ContentFile
from pytz import timezone
from celery import shared_task

from report.models import Report, ReportStatus, StatusChoices, DayOfWeek, BusinessHour, StoreStatus, StoreTimezone
import pandas as pd
import logging


@shared_task(name="generate_csv_report")
def generate_csv_report(report_id):
    report_obj = Report.objects.get(report_id=report_id)

    try:
        store_timezone_objs = StoreTimezone.objects.all()
        report_df = pd.DataFrame(columns=[
            "store_id", "uptime_last_hour", "uptime_last_day", "update_last_week",
            "downtime_last_hour", "downtime_last_day", "downtime_last_week"])
        store_count = 1
        for store_timezone_obj in store_timezone_objs:
            print("store_count : ", store_count)
            store_count+=1
            store_data = get_store_data(store_timezone_obj)
            report_df.loc[len(report_df.index)] = store_data

        report_csv = report_df.to_csv(columns=["store_id", "uptime_last_hour", "uptime_last_day", "update_last_week",
                                               "downtime_last_hour", "downtime_last_day", "downtime_last_week"],
                                      index=False)

        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(report_csv)

        csv_file = ContentFile(csv_buffer.getvalue().encode('utf-8'))
        report_obj.csv_report.save(f'{str(report_id)}.csv', csv_file)
        report_obj.status = ReportStatus.COMPLETE

    except Exception as e:
        traceback.print_exc()
        report_obj.status = ReportStatus.FAILED

    report_obj.save()


def get_store_data(store_timezone_obj):
    store_id = store_timezone_obj.store_id
    business_hours = BusinessHour.objects.filter(store_id=store_id).order_by('dayOfWeek')
    store_timezone = timezone(store_timezone_obj.timezone_str)

    all_business_hours = []

    all_business_hours = [
        {'start_time_local': datetime.datetime.min.time(), 'end_time_local': datetime.datetime.max.time()} for ind
        in range(7)]

    for bus_hr in business_hours:
        all_business_hours[bus_hr.dayOfWeek] = {
            'start_time_local': bus_hr.start_time_local,
            'end_time_local': bus_hr.end_time_local}

    store_status = StoreStatus.objects.filter(store_id=store_id)

    queryset = store_status.values_list("timestamp_utc", "status")
    df = pd.DataFrame(list(queryset), columns=["timestamp_utc", "status"])

    df_new = fill_missing_values(df)

    # filtering the data inside of business hours

    df_new['timestamp_local'] = pd.to_datetime(df_new['timestamp_utc'].dt.tz_convert(store_timezone))
    df_new['start_time_local'] = df_new['timestamp_local'].dt.weekday.map(
        lambda x: all_business_hours[x]['start_time_local'])
    df_new['end_time_local'] = df_new['timestamp_local'].dt.weekday.map(
        lambda x: all_business_hours[x]['end_time_local'])
    filtered_df = df_new[(df_new['timestamp_local'].dt.time >= df_new['start_time_local']) & (
            df_new['timestamp_local'].dt.time <= df_new['end_time_local'])]

    # uptime downtime calculation
    now = datetime.datetime.now(tz=store_timezone)
    last_hour = now - datetime.timedelta(hours=1)
    last_day = now - datetime.timedelta(days=1)
    last_week = now - datetime.timedelta(days=7)

    # filtered_df.set_index('timestamp_local', inplace=True)

    df_last_hour = filtered_df[(filtered_df['timestamp_local'] >= last_hour) &  (filtered_df['timestamp_local']<=now)]

    uptime_last_hour = len(df_last_hour[df_last_hour['status'] == 'active'])
    downtime_last_hour = len(df_last_hour[df_last_hour['status'] == 'inactive'])

    df_last_day = filtered_df[(filtered_df['timestamp_local'] >= last_day) &  (filtered_df['timestamp_local']<=now)]

    uptime_last_day = round(len(df_last_day[df_last_day['status'] == 'active']) / 60, 2)
    downtime_last_day = round(len(df_last_day[df_last_day['status'] == 'inactive']) / 60, 2)

    df_last_week = filtered_df[(filtered_df['timestamp_local'] >= last_week) &  (filtered_df['timestamp_local']<=now)]

    uptime_last_week = round(len(df_last_week[df_last_week['status'] == 'active']) / 60, 2)
    downtime_last_week = round(len(df_last_week[df_last_week['status'] == 'inactive']) / 60, 2)

    return [str(store_id), uptime_last_hour,
            uptime_last_day, uptime_last_week,
            downtime_last_hour, downtime_last_day, downtime_last_week]


def fill_missing_values(df):
    df.loc[len(df.index)] = [pd.Timestamp.utcnow(), "inactive"]
    df = df.set_index('timestamp_utc')

    df.resample('T').ffill()
    df['status'] = df['status'].interpolate('nearest')
    df.reset_index(inplace=True)

    return df


def filter_business_hours(row):
    print(row)
