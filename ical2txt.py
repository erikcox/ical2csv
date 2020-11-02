#!/usr/bin/python3

import sys
import os.path
from icalendar import Calendar
import csv
from bs4 import BeautifulSoup

filename = sys.argv[1]
# TODO: use regex to get file extension (chars after last period), in case it's not exactly 3 chars.
file_extension = str(sys.argv[1])[-3:]
headers = ('Summary', 'UID', 'Description', 'Location', 'Start Time', 'End Time', 'URL')

class CalendarEvent:
    """Calendar event class"""
    summary = ''
    uid = ''
    description = ''
    location = ''
    start = ''
    end = ''
    url = ''

    def __init__(self, name):
        self.name = name

events = []

def removehtml(html):
    # Almost word for word copy from here: https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python

    soup = BeautifulSoup(html, features="html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract() # remove it

    text = soup.get_text() # Get plain text

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def open_cal():
    if os.path.isfile(filename):
        if file_extension == 'ics':
            print("Extracting events from file:", filename, "\n")
            f = open(sys.argv[1], 'rb')
            gcal = Calendar.from_ical(f.read())

            for component in gcal.walk():
                event = CalendarEvent("event")
                if component.get('TRANSP') == 'TRANSPARENT': continue #skip event that have not been accepted
                if component.get('SUMMARY') == None: continue #skip blank items
                event.summary = component.get('SUMMARY')
                event.uid = component.get('UID')
                if component.get('DESCRIPTION') == None: continue #skip blank items
                event.description = component.get('DESCRIPTION')
                event.location = component.get('LOCATION')
                if hasattr(component.get('dtstart'), 'dt'):
                    event.start = component.get('dtstart').dt
                if hasattr(component.get('dtend'), 'dt'):
                    event.end = component.get('dtend').dt


                event.url = component.get('URL')
                events.append(event)
            f.close()
        else:
            print("You entered ", filename, ". ")
            print(file_extension.upper(), " is not a valid file format. Looking for an ICS file.")
            exit(0)
    else:
        print("I can't find the file ", filename, ".")
        print("Please enter an ics file located in the same folder as this script.")
        exit(0)


def txt_write(icsfile):
    txtfile = icsfile[:-3] + "txt"
    prevdate=""
    spent=0
    try:
        with open(txtfile, 'w') as myfile:
            for event in sortedevents:

                if prevdate != event.start.strftime("%Y-%m-%d"): # Make a header for each day
                    if prevdate != '': # If you don't want a summary of the time spent added, comment this section. 
                        th=divmod(spent, 3600)[0]
                        tm=divmod(spent, 3600)[1]/60
                        myfile.write("Time Total: " + '{:02.0f}'.format(th) + ":" + '{:02.0f}'.format(tm) + "\n")
                        spent=0
                    prevdate = event.start.strftime("%Y-%m-%d")
                    myfile.write("\nMMO (IAM) Worklog, " + prevdate + "\n=============================\n")

                if event.end == None: print("Event without end. Me no like: " + prevdate + " - " + event.summary.encode('utf-8').decode())
                duration = event.end - event.start
                ds = duration.total_seconds()
                spent += ds
                hours = divmod(ds, 3600)[0]
                minutes = divmod(ds,3600)[1]/60
                values = event.start.strftime("%H:%M:%S") + " - " + event.end.strftime("%H:%M:%S") + " (" + '{:02.0f}'.format(hours) + ":" + '{:02.0f}'.format(minutes) + ") " + event.summary.encode('utf-8').decode()
                if event.location != '': values = values + " [" + event.location + "]" # Only include location if there is one
                if event.description.rfind('joining options') == -1: # Skip description if it has Google Meeting information
                    values = values + "\n" + removehtml(event.description.encode('utf-8').decode())
                myfile.write(values+"\n")
            print("Wrote to ", txtfile, "\n")
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

open_cal()
sortedevents=sorted(events, key=lambda obj: obj.start)
txt_write(filename)
#debug_event(event)
