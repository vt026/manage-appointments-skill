from mycroft import MycroftSkill, intent_file_handler, intent_handler
from datetime import datetime
import sys
import caldav
from caldav.elements import dav
    


class ManageAppointments(MycroftSkill):
        
    def __init__(self):
        MycroftSkill.__init__(self)        
              
        
    @intent_handler('appointments.manage.date.intent')
    def handle_date_search(self, message):
        day = self.convertOrdinalToCardinalNumber(message.data.get('day'))
        month = self.convertMonthToInt(message.data.get('month'))
        if (day is not None and month is not None):
            self.speak_dialog(self.getAppointmentsOnDate(int(day),int(month)))
        else:
            self.speak_dialog("hello")
        

    @intent_file_handler('appointments.manage.intent')
    def handle_appointments_manage(self, message):
        self.speak_dialog(self.getNextAppointment())
        
        
    @intent_file_handler('appointments.manage.newEvent.intent')
    def handle_createNewEvent(self,message):
        day = self.convertOrdinalToCardinalNumber(message.data.get('day'))
        month = self.convertMonthToInt(message.data.get('month'))
        eventname = self.get_response('how do you want to name the nex appointment?')
        
        startDate = self.get_response('When does the appointment start?')
        startHour = self.getHour(startDate)
        startMin = self.getMinutes(startDate)
        
        endDate = self.get_response('When does the appointment end?')
        endHour = self.getHour(endDate)
        endMin = self.getMinutes(endDate)
        
        
        self.createNewEvent(eventname,month,day,int(startHour),startMin,int(endHour),endMin)
        self.speak_dialog("The appointment " + eventname + "  was succesfully created")
    
    def getNextAppointment(self):
        '''Notallday wird zuerst ausgegeben!
        
        '''
        #returns the next appointment
        
        events_fetched = self.loadEvents(datetime.today().year,datetime.today().month,datetime.today().day,2024,1,1)
        events_fetched.sort(key=lambda x: x.instance.vevent.dtstart.value.strftime("%Y-%m-%d"))
        
        
        if len(events_fetched)!=0:
            events = []
            for event in events_fetched:
                if events_fetched[0].instance.vevent.dtstart.value.strftime("%Y-%m-%d") == event.instance.vevent.dtstart.value.strftime("%Y-%m-%d"):
                    events.append(event)
            events_allDay = []
            events_notAllDay = []
            for i in events_fetched:
                if i.instance.vevent.dtstart.value.strftime("%H:%M") == "00:00":
                    events_allDay.append(i)
                else:
                    events_notAllDay.append(i)
            events_notAllDay.sort(key=lambda x: x.instance.vevent.dtstart.value)
            events_allDay.sort(key=lambda x: x.instance.vevent.dtstart.value)
            
            for i in events_allDay:
                print( i.instance.vevent.summary.value)
            for i in events_notAllDay:
                print(i.instance.vevent.summary.value)
            
              
            
            if len(events_notAllDay) == 0 :
                name = events_allDay[0].instance.vevent.summary.value
                date = events_allDay[0].instance.vevent.dtstart.value.strftime("%B %d, %Y")
                time = " all day long"
                print("all day") 
                return "Your next appointment is on " + date + time + " and is entitled " + name
            elif len(events_allDay) == 0 :
                next_appointment = events_notAllDay[0]
                self.nextEvent= True
                self.event = next_appointment.instance.vevent
                self.appointent_name = self.event.summary.value
                self.appointment_start = self.event.dtstart.value
                self.appointment_date = self.appointment_start.strftime("%B %d, %Y")
                self.appointment_time = " at " + str(self.appointment_start.hour+1) + self.appointment_start.strftime(":%M %p")
                
                return "Your next appointment is on " + self.appointment_date + self.appointment_time + " and is entitled " + self.appointent_name
            
            else:
                firstAllDay = events_allDay[0].instance.vevent.dtstart.value.strftime("%B %d, %Y")
                firstNotAllDay = events_notAllDay[0].instance.vevent.dtstart.value.strftime("%B %d, %Y")
                
                print(firstAllDay)
                print(firstNotAllDay)
                print(firstAllDay > firstNotAllDay)
                print(firstAllDay < firstNotAllDay)
                
                if(firstAllDay < firstNotAllDay):
                    name = events_allDay[0].instance.vevent.summary.value
                    date = events_allDay[0].instance.vevent.dtstart.value.strftime("%B %d, %Y")
                    time = " all day long"
                    print("all day") 
                    return "Your next appointment is on " + date + time + " and is entitled " + name
                else:
                    next_appointment = events_notAllDay[0]
                    self.nextEvent= True
                    self.event = next_appointment.instance.vevent
                    self.appointent_name = self.event.summary.value
                    self.appointment_start = self.event.dtstart.value
                    self.appointment_date = self.appointment_start.strftime("%B %d, %Y")
                    self.appointment_time = " at " + str(self.appointment_start.hour+1) + self.appointment_start.strftime(":%M %p")
                    
                    return "Your next appointment is on " + self.appointment_date + self.appointment_time + " and is entitled " + self.appointent_name

        
        else:
            #there are no events in the calendar
            self.nextEvent = False
            return "There are no upcoming events"
        
        
        
        
    def getAppointmentsOnDate(self,day,month):
        year = datetime.today().year
        
        events_fetched = self.loadEvents(year,month,day,year,month,day)
        events_allDay = []
        events_notAllDay = []
        for i in events_fetched:
            if i.instance.vevent.dtstart.value.strftime("%H:%M") == "00:00":
                events_allDay.append(i)
            else:
                events_notAllDay.append(i)
        events_notAllDay.sort(key=lambda x: x.instance.vevent.dtstart.value)
        
        if events_fetched == 0:
            return "This is not a day!"
        else:
            if len(events_allDay) == 0 and len(events_notAllDay) == 0:
                return "On the " +str(day) + ". of " + self.convertIntToMonth(month) + " you have no appointments."
            elif (len(events_allDay) == 1 and len(events_notAllDay) == 0) or (len(events_allDay) == 0 and len(events_notAllDay) == 1):
                result= "On the " +str(day) + ". of " + self.convertIntToMonth(month) + " you have the following appointment: "
                
                if len(events_allDay) == 1:
                    myEvent = events_allDay[0].instance.vevent
                    appointent_name = myEvent.summary.value
                    result = result + appointent_name
                else:
                    myEvent = events_notAllDay[0].instance.vevent
                    appointent_name = myEvent.summary.value
                    result = result + appointent_name
                
                return result
            
            else:
                result= "On the " +str(day) + ". of " + self.convertIntToMonth(month) + " you have the following appointments: "
            
                for event in events_allDay:
                    myEvents = event.instance.vevent
                    appointent_name = myEvents.summary.value
                    result = result + appointent_name  +", "
                    
                for event in events_notAllDay:
                    myEvents = event.instance.vevent
                    appointent_name = myEvents.summary.value
                    result = result + appointent_name  +", "
                
                return result
    
    
    def createNewEvent(self,name,month,day,startHour,startMin,endHour,endMin):
        url = "https://" + self.getUsername() + ":" + self.getPassword() + "@next.social-robot.info/nc/remote.php/dav"
        client = caldav.DAVClient(url)
        principal = client.principal()
        # get all available calendars (for this user)
        myCalendar = principal.calendars()[0]
        
        #current timestamp
        DTcurr = datetime.today().strftime('%Y%m%dT%H%M%SZ')
        UID = DTcurr = datetime.today().strftime('%Y%m%dT%H%M%SZ')
        summary = name
        start = datetime(datetime.today().year, month, day, startHour-1, startMin)
        end = datetime(datetime.today().year, month, day, endHour-1, endMin)
        DTstart =   start.strftime('%Y%m%dT%H%M%SZ')
        DTend = end.strftime('%Y%m%dT%H%M%SZ')
        myNewEvent = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:ownCloud Calendar
BEGIN:VEVENT
CREATED;VALUE=DATE-TIME:""" + DTcurr + """
UID:""" + UID + """
LAST-MODIFIED;VALUE=DATE-TIME:""" + DTcurr + """
DTSTAMP;VALUE=DATE-TIME:""" + DTcurr + """
SUMMARY:""" + summary + """
DTSTART;VALUE=DATE-TIME:""" + DTstart + """
DTEND;VALUE=DATE-TIME:""" + DTend + """
CLASS:PUBLIC
END:VEVENT
END:VCALENDAR
 """
        
    
        my_event = myCalendar.save_event(myNewEvent)
        
        return "The event "+ summary + " was created succesfully."
    
    
    
    def loadEvents(self , fromYear, fromMonth, fromDay, toYear, toMonth, toDay):
        url = "https://" + self.getUsername() + ":" + self.getPassword() + "@next.social-robot.info/nc/remote.php/dav"
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
                print("Name: %-20s  URL: %s" % (c.name, c.url))
        else:
            print("your principal has no calendars")
        try:     
            events_fetched = calendars[0].date_search(
                start=datetime(fromYear,fromMonth,fromDay), end=datetime(toYear,toMonth,toDay+1), expand=True)
            return events_fetched
        except ValueError:
            return 0
   
    def convertMonthToInt(self, month):
        if month.lower() == 'january':
            return 1
        elif month.lower() == 'february':
            return 2
        elif month.lower() == 'march':
            return 3
        elif month.lower() == 'april':
            return 4
        elif month.lower() == 'may':
            return 5
        elif month.lower() == 'june':
            return 6
        elif month.lower() == 'july':
            return 7
        elif month.lower() == 'august':
            return 8
        elif month.lower() == 'september':
            return 9
        elif month.lower() == 'october':
            return 10
        elif month.lower() == 'november':
            return 11
        elif month.lower() == 'december':
            return 12
        
        
        
    def convertIntToMonth(self, month):
        if month == 1:
            return "January"
        elif month == 2:
            return "February"
        elif month == 3:
            return "March"
        elif month == 4:
            return "April"
        elif month == 5:
            return "March"
        elif month == 6:
            return "June"
        elif month == 7:
            return "July"
        elif month == 8:
            return "August"
        elif month == 9:
            return "September"
        elif month == 10:
            return "October"
        elif month == 11:
            return "November"
        elif month == 12:
            return "December"
        else:
            return 0
        
    def convertOrdinalToCardinalNumber(self, ordinalString):
        if ordinalString[1].isnumeric():
            return int(ordinalString[0:2])
        else:
            return int(ordinalString[0])
        
    def getHour(self, string):
        
        result = string
        if(string.startswith("at ")):
            result = string.replace("at ","",1)

        result = result.split(":")
        
        return int(result[0])
            
    def getMinutes(self, string):
        result = string
        if(string.startswith("at ")):
            result = string.replace("at ","",1)
            
        if(":" not in string):
            return 0
        else: 
            result = result.split(":")
            return int(result[1])
        
        

            
        
    def getUsername(self):
        with open('pw.txt','r') as file:
            data = file.read().splitlines()
        
        username = data[0]
        return username
    
    def getPassword(self):
        with open('pw.txt','r') as file:
            data = file.read().splitlines()
        
        password = data[1]
        return password

def create_skill():
    return ManageAppointments()



