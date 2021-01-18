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
        eventname = self.get_response('how do you want to name the nex appointment?')
        self.speak_dialog("The name of the new appointment is: " + eventname)
        

    def getNextAppointment(self):
        #returns the next appointment
        
        events_fetched = self.loadEvents(datetime.today().year,datetime.today().month,datetime.today().day,2024,1,1)
        events_fetched.sort(key=lambda x: x.instance.vevent.dtstart.value.strftime("%Y-%m-%d"))
        
        if len(events_fetched)!=0:
            next_appointment = events_fetched[0]
            self.nextEvent= True
            self.event = next_appointment.instance.vevent
            self.appointent_name = self.event.summary.value
            self.appointment_start = self.event.dtstart.value
            #self.appointment_end = self.event.dtend.value
            
            if self.event.dtstart.value.strftime("%H:%M") == "00:00":
                #the next event is all day
                self.appointment_date = self.appointment_start.strftime("%B %d, %Y")
                self.appointment_time = " all day long"
                print("all day")
            else:
                #the next event has a specific time
                self.appointment_date = self.appointment_start.strftime("%B %d, %Y")
                self.appointment_time = " at " + str(self.appointment_start.hour+1) + self.appointment_start.strftime(":%M %p")
            
        else:
            #there are no events in the calendar
            self.nextEvent = False
            print("No events")
        
        if(self.nextEvent==False):
            return "There are no upcoming events"
        else:
            return "Your next appointment is on " + self.appointment_date + self.appointment_time + " and is entitled " + self.appointent_name
        
    def getAppointmentsOnDate(self,day,month):
        year = datetime.today().year
                
        events_fetched = self.loadEvents(year,month,day,year,month,day)
        if events_fetched == 0:
            return "This is not a day!"
        else:
            if(len(events_fetched)==1):
                result= "On the " +str(day) + ". of " + self.convertIntToMonth(month) + " you have the following appointment: "

                myEvent = events_fetched[0].instance.vevent
                appointent_name = myEvent.summary.value
                result = result + appointent_name
                
                return result
            elif(len(events_fetched)!=0):
                result= "On the " +str(day) + ". of " + self.convertIntToMonth(month) + " you have the following appointments: "
                for event in events_fetched:
                    myEvents = event.instance.vevent
                    appointent_name = myEvents.summary.value
                    result = result + appointent_name  +", "
                
                return result
            else:
                return "On the " +str(day) + ". of " + self.convertIntToMonth(month) + " you have no appointments."
    
    
    def createNewEvent(self,name,month,day,startHour,startMin,endHour,endMin):
        url = "https://" + self.getUsername() + ":" + self.getPassword() + "@next.social-robot.info/nc/remote.php/dav"
        client = caldav.DAVClient(url)
        principal = client.principal()
        # get all available calendars (for this user)
        myCalendar = principal.calendars()[0]
        
        #current timestamp
        DTcurr = datetime.today().strftime('%Y%m%dT%H%M%SZ')
        UID = "neueID"
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



