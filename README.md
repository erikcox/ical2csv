# ical2csv w/sorted events by start date

![alt text](images/ics.png) → ![alt text](images/python.png) → ![alt text](images/csv.png) 

A command line Python script that will read an ics file and write it's contents to a csv file.

## Installation
Download the `ical2csv.py` file.

### Dependencies:
* ***icalendar***
	*  [**Homepage**](http://icalendar.readthedocs.org/)
	*  [**Code**](http://github.com/collective/icalendar)
    * **Installation**: `pip install icalendar`
* ***BeautifulSoup4*** (pip3 install beautifulsoup4)
* ***recurring-ical-events*** (pip3 install recurring-ical-events)
* ***Python* 3**

***Note:*** pip may be called pip3 on some systems with both python2 and python3 as options.

## Usage of ical2csv

Call the script and pass in the location of the ics file.

Ex: `python ical2csv.py event.ics`

# ical2txt w/sorted events by start date

Like ical2csv.py, it parses an ics file and writes the output to a text-file. This is more of an agenda style.

## Installation of ical2txt
Download the script or clone the project and get it from there.

## Usage of ical2txt

Call the script and pass in the location of the ics file.

Ex: `python ical2txt.py event.ics` / `python3 ical2txt.py event.ics`

Note: You can limit output to a certain time period. Useful for week logs and the like:

`./ical2txt.py myexport.ics 20210101 20211231`

`./ical2txt.py myexport.ics 2021-01-01T00:00:00 2021-01-31T23:59:59`

**NEW AS OF 2021-03-28:** Recurring events are now actually processed in ical2txt.py. If no end date is given 5 years from now is chosen.

**NEW AS OF 2021-05-02:** ical2csv.py update with same features as ical2txt.py, except removing Google/Skype meeting details.

## Contributing

1. Fork it!
2. Create your feature branch: git checkout -b my-new-feature
3. Commit your changes: git commit -am 'Add some feature'
4. Push to the branch: git push origin my-new-feature
5. Submit a pull request 😊

## Credits

Lead Developer - ical2csv - [Erik Cox](https://github.com/erikcox/)
Co-developer - ical2csv - [Martin Møller](https://github.com/martinm76)

Developer - ical2txt - [Martin Møller](https://github.com/martinm76)

Python 3 compatibility and improvements - [bozoslivehere](https://github.com/bozoslivehere/)

Logic and adjustments to sort events chronologically (Google Calendar doesn't do this in its export) - [Martin Møller](https://github.com/martinm76)

Removal of HTML code from events - [Martin Møller](https://github.com/martinm76)

Conversion of date object to datetime objects, to allow sort - [Martin Møller](https://github.com/martinm76)

Timezone fixes - [Martin Møller](https://github.com/martinm76)

## License

The MIT License (MIT)

Copyright (c) 2019 Erik Cox

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
