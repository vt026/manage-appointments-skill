# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:43:02 2020

@author: Christian
"""

# https://github.com/python-caldav/caldav

import caldav
from caldav.elements import dav

# Caldav url
# import secret login code from local file here
username = ""
password = ""

url = "https://" + username + ":" + password + "@next.social-robot.info/nc/remote.php/dav"

#vcal = """BEGIN:VCALENDAR
#VERSION:2.0
#PRODID:-//Example Corp.//CalDAV Client//EN
#BEGIN:VEVENT
#UID:1234567890
#DTSTAMP:20100510T182145Z
#DTSTART:20100512T170000Z
#DTEND:20100512T180000Z
#SUMMARY:This is an event
#END:VEVENT
#END:VCALENDAR
#"""

# example event object
#<VCALENDAR| [<VERSION{}2.0>, <CALSCALE{}GREGORIAN>, 
#             <PRODID{}-//Sabre//Sabre VObject 4.1.6//EN>, 
#             <VEVENT| [<UID{}e8e55e25-1d7c-4bc5-a115-29480d076a30>, 
#                       <DTSTART{}2020-02-17 09:30:00+00:00>, 
#                       <DTEND{}2020-02-17 10:50:00+00:00>, 
#                       <CREATED{}2020-02-16 19:53:30+00:00>, 
#                       <DTSTAMP{}2020-02-16 19:54:08+00:00>, 
#                       <LAST-MODIFIED{}2020-02-16 19:54:08+00:00>, 
#                       <SEQUENCE{}2>, 
#                       <SUMMARY{}Testtermin>]>]>

# open connection to calendar
client = caldav.DAVClient(url)
principal = client.principal()
# get all available calendars (for this user)
calendars = principal.calendars()
print(calendars)

# check the calendar events and parse results..