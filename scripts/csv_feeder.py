import asyncio
import csv
import datetime, pytz
from itertools import islice

from report.models import StoreStatus, StoreTimezone, BusinessHour


def feed_csvs_in_database():
    with open('csvs/Menu hours.csv') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            obj, created = BusinessHour.objects.update_or_create(store_id=row[0],
                                                                 dayOfWeek=int(row[1]),
                                                                 defaults={
                                                                     'start_time_local': row[2],
                                                                     'end_time_local': row[3]},
                                                                 )


def feed_timezone_csv():
    pass


async def feed_store_staus_csv():
    with open('csvs/store status.csv') as file:
        reader = csv.reader(file)
        next(reader)
        object_to_feed = []
        for row in reader:
            obj = StoreStatus(store_id=row[0],
                              status=row[1],
                              )
            try:
                obj.timestamp_utc = pytz.utc.localize(
                    datetime.datetime.strptime(
                        row[2],
                        "%Y"
                        "-%m"
                        "-%d "
                        "%H"
                        ":%M"
                        ":%S"
                        ".%f "
                        "%Z"))
            except:
                obj.timestamp_utc = pytz.utc.localize(
                    datetime.datetime.strptime(
                        row[2],
                        "%Y"
                        "-%m"
                        "-%d "
                        "%H"
                        ":%M"
                        ":%S "
                        "%Z"))

            object_to_feed.append(obj)

        batch_size = 100
        curr = 0
        while True:
            batch = object_to_feed[curr:curr + batch_size]
            curr = curr + batch_size
            if not batch:
                break
            await StoreStatus.objects.abulk_create(batch, batch_size)


# feed_csvs_in_database()
# c = feed_store_staus_csv()
#
# asyncio.run(c)


def feed_timezone_csvs_in_database():
    with open('csvs/timezone_data.csv') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            obj, created = StoreTimezone.objects.update_or_create(store_id=row[0],

                                                                  defaults={
                                                                      'timezone_str': row[1]
                                                                  }
                                                                  )


# feed_timezone_csvs_in_database()
