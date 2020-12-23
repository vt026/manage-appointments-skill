# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:43:02 2020

@author: Christian
"""

# https://github.com/python-caldav/caldav
from datetime import datetime
import sys
import caldav




class Calendar:
    def __init__(self):
        # Caldav url
        # import secret login code from local file here
        with open('pw.txt','r') as file:
            data = file.read().splitlines()
        
        username = data[0]
        password = data[1]
        
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
        if calendars:
            ## Some calendar servers will include all calendars you have
            ## access to in this list, and not only the calendars owned by
            ## this principal.  TODO: see if it's possible to find a list of
            ## calendars one has access to.
            print("your principal has %i calendars:" % len(calendars))
            for c in calendars:
                calendar_url = c.url
                print("    Name: %-20s  URL: %s" % (c.name, c.url))
        else:
            print("your principal has no calendars")
          
            
          
            
        # check the calendar events and parse results..  
        events_fetched = calendars[0].date_search(
            start=datetime.today(), end=datetime(2024, 1, 1), expand=True)
        
        
        if len(events_fetched)!=0:
            next_appointment = events_fetched.pop()
            appointent_name = next_appointment.vobject_instance.vevent.summary.value
        
            print("Name: " + appointent_name)
            self.eventname = appointent_name
        else:
            self.eventname ="no events";
            print("No events")
        
        
    def getNextAppointment(self):
        return self.eventname
    
    


