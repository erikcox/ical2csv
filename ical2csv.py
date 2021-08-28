#!/usr/bin/python3

import csv
import datetime
import os.path
import pytz
import sys

from icalendar import Calendar

# use this for events that do not have its own timezone


class CalendarEvent:
    """Calendar event class"""
    summary = ''
    uid = ''
    description = ''
    location = ''
    start = ''
    end = ''
    url = ''
    CALENDAR_TIMEZONE = None


def open_cal():
    events = []
    if os.path.isfile(filename):
        if file_extension == 'ics':
            print("Extracting events from file:", filename, "\n")
            f = open(sys.argv[1], 'rb')
            gcal = Calendar.from_ical(f.read())
            gcal.CALENDAR_TIMEZONE = pytz.timezone(gcal.get("X-WR-TIMEZONE").encode('utf8').decode())
            for component in gcal.walk():
                event = CalendarEvent()
                if component.get('TRANSP') == 'TRANSPARENT': continue  # skip event that have not been accepted
                if component.get('SUMMARY') is None: continue  # skip blank items
                event.summary = component.get('SUMMARY')
                event.uid = component.get('UID')
                if component.get('DESCRIPTION') is None: continue  # skip blank items
                event.description = component.get('DESCRIPTION')
                event.location = component.get('LOCATION')
                if hasattr(component.get('dtstart'), 'dt'):
                    event.start = component.get('dtstart').dt
                if hasattr(component.get('dtend'), 'dt'):
                    event.end = component.get('dtend').dt
                event.url = component.get('URL')
                events.append(event)
            f.close()
            return events, gcal
        else:
            print("You entered ", filename, ". ")
            print(file_extension.upper(), " is not a valid file format. Looking for an ICS file.")
            exit(0)
    else:
        print("I can't find the file ", filename, ".")
        print("Please enter an ics file located in the same folder as this script.")
        exit(0)


def csv_write(icsfile):
    csvfile = icsfile[:-3] + "csv"
    try:
        with open(csvfile, 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(headers)
            for event in sortedevents:
                values = (event.summary.encode('utf8').decode(), event.uid,
                          event.description.encode('utf8').decode(),
                          event.location, event.start, event.end, event.url)
                wr.writerow(values)
            print("Wrote to ", csvfile, "\n")
    except IOError:
        print("Could not open file! Please close Excel!")
        exit(0)


def debug_event(class_name):
    print("Contents of ", class_name.name, ":")
    print(class_name.summary)
    print(class_name.uid)
    print(class_name.description)
    print(class_name.location)
    print(class_name.start)
    print(class_name.end)
    print(class_name.url, "\n")


def format_all_day_events(event_list, default_timezone=pytz.timezone("UTC"),
                          default_start_time=datetime.time(hour=9, minute=0, second=0),
                          default_end_time=datetime.time(hour=17, minute=0, second=0)
                          ):
    _events = event_list
    for e in _events:
        if isinstance(e.start, datetime.datetime) or isinstance(e.end, datetime.datetime):
            pass
        # if there is no start-end time (event happening for the whole day
        else:
            # change event's start and end timezone to timezone of the whole calendar itself
            timezone = default_timezone
            # print(timezone)
            # change event's start and end time to some arbitrary time
            # I prefer 9 - 5 events
            e.start = datetime.datetime.combine(e.start, default_start_time)
            e.end = datetime.datetime.combine(e.end, default_end_time)

            # change timezone
            if timezone is not None:
                e.start = e.start.replace(tzinfo=timezone)
                e.end = e.end.replace(tzinfo=timezone)

            else:
                # error when e.create.tzinfo is None (which should never really happen)
                e.start = e.start.replace(tzinfo=default_timezone)
                e.end = e.end.replace(tzinfo=default_timezone)
            # print("Start time: {start}, end time: {end}".format(start=e.start, end=e.end))
    return _events


if __name__ == "__main__":
    filename = sys.argv[1]
    # TODO: use regex to get file extension (chars after last period), in case it's not exactly 3 chars.
    file_extension = str(sys.argv[1])[-3:]
    headers = ('Summary', 'UID', 'Description', 'Location', 'Start Time', 'End Time', 'URL')
    events, calendar = open_cal()
    formatted_events = format_all_day_events(events, default_timezone=calendar.CALENDAR_TIMEZONE)
    sortedevents = sorted(formatted_events, key=lambda obj: obj.start)
    csv_write(filename)

# debug_event(event)
