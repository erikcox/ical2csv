#!/usr/bin/python3

import sys
import os.path
from icalendar import Calendar
import recurring_ical_events
from bs4 import BeautifulSoup
import warnings
from dateutil.parser import parse
import datetime

warnings.filterwarnings("ignore", category=UserWarning, module='bs4') # We don't want warnings about URL's. We just what the URL printed, if there.

if len(sys.argv) <= 1:
    print("Please call this script with an ics-file as parameter.\n")
    print("Even better, call it with start and end dates:\n")
    print(sys.argv[0] + " myexport.ics 20210101 20210201")
    print(sys.argv[0] + " myexport.ics 2021-01-01T00:00:00 2021-01-31T23:59:59\n")
    exit(1)

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
            revents = recurring_ical_events.of(gcal).between(istart,istop)

#           for component in gcal.walk():
            for component in revents:
                event = CalendarEvent("event")
                v=(dir(component).count('get'))
                if (v != 0):
                     if component.get('TRANSP') == 'TRANSPARENT': continue #skip all day events and the like
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
    evcount=0
    evskip=0
    print("Processing events :", end=" ")
    try:
        with open(txtfile, 'w') as myfile:
            for event in sortedevents:

                if prevdate != event.start.strftime("%Y-%m-%d") and spent > 0: # Make a header for each day
                    if prevdate != '': # If you don't want a summary of the time spent added, comment this section. 
                        th=divmod(spent, 3600)[0]
                        tm=divmod(spent, 3600)[1]/60
                        myfile.write("\nTime Total: " + '{:02.0f}'.format(th) + ":" + '{:02.0f}'.format(tm) + "\n")
                        spent=0
                if event.start.timestamp() > istart.timestamp() and event.start.timestamp() < istop.timestamp():
                    if prevdate != event.start.strftime("%Y-%m-%d"): # Make a header for each day
                        prevdate = event.start.strftime("%Y-%m-%d")
                        myfile.write("\nWorklog, " + prevdate + "\n===================\n")

                    duration = event.end - event.start
                    ds = duration.total_seconds()
                    spent += ds
                    hours = divmod(ds, 3600)[0]
                    minutes = divmod(ds,3600)[1]/60
                    description=removehtml(event.description.encode('utf-8').decode())
                    values = event.start.strftime("%H:%M") + " - " + event.end.strftime("%H:%M") + " (" + '{:02.0f}'.format(hours) + ":" + '{:02.0f}'.format(minutes) + ") " + event.summary.encode('utf-8').decode()
                    if event.location != '': values = values + " [" + event.location + "]" # Only include location if there is one

                    # Remove Google Meet and Skype Meeting part of description
                    trimmed=description.split('-::~')[0].split('......')[0]
                    #print("DescLen: " + str(len(description)) + " TrimmedLen: " + str(len(trimmed)) + " : " + trimmed) # For debugging
                    description=trimmed
                    if description != '':
                        values = values + "\n" + description + "\n"
                    myfile.write(values+"\n")
                    print("", end=".")
                    evcount+=1
                else:
                    print("", end="S")
                    evskip+=1

            print("\n\nWrote " + str(evcount) + " events to ", txtfile, " and skipped ", str(evskip), " events\n")
    except IOError:
        print("Could not open file!")
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

istart=datetime.datetime.fromtimestamp(0) # Start of UNIX epoch (1970-01-01T00:00:00)
istop=datetime.datetime.fromtimestamp(4102441200) # The year 2100. Hopefully this will not be in use by then ...

if len(sys.argv) > 3:
   if sys.argv[2] != '':
#      istart=parse(sys.argv[2]).timestamp()
      istart=parse(sys.argv[2])
   if sys.argv[3] != '':
#      istop=parse(sys.argv[3]).timestamp()
      istop=parse(sys.argv[3])

open_cal()
sortedevents=sorted(events, key=lambda obj: obj.start)
txt_write(filename)
#debug_event(event)
