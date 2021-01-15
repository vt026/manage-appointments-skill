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
        day = message.data.get('day')
        month = message.data.get('month')
        if (day is not None and month is not None):
            self.speak_dialog(self.getAppointmentsOnDate(int(day),int(month)))
        else:
            self.speak_dialog("hello")
        

    @intent_file_handler('appointments.manage.intent')
    def handle_appointments_manage(self, message):
        self.loadCalendars()
        self.speak_dialog(self.getNextAppointment())
        
        
    def loadCalendars(self):
        # Caldav url
        # import secret login code from local file here
    

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
          
            
          
            
        # check the calendar events and parse results..  
        events_fetched = calendars[0].date_search(
            start=datetime.today(), end=datetime(2024, 1, 1), expand=True)
        
        
        
        
        if len(events_fetched)!=0:
            next_appointment = events_fetched.pop()
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
                self.appointment_time = self.appointment_start.strftime(" at %I:%M %p")
            
        else:
            #there are no events in the calendar
            self.nextEvent = False
            print("No events")

    def getNextAppointment(self):
        #returns the next appointment
        if(self.nextEvent==False):
            return "There are no upcoming events"
        else:
            return "Your next appointment is on " + self.appointment_date + self.appointment_time + " and is entitled " + self.appointent_name
        
    def getAppointmentsOnDate(self,day,month):
        year = datetime.today().year
                
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
            
        events_fetched = calendars[0].date_search(
            start=datetime(year,month,day), end=datetime(year,month,day+1), expand=True)
        
        next_appointment = events_fetched.pop()
        event = next_appointment.instance.vevent
        appointent_name = event.summary.value
        return "On the " +str(day) + " of " + str(month) + " you have the following appointments: " + appointent_name
        
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



