from mycroft import MycroftSkill, intent_file_handler
from nextcloud_starter import Calendar

class ManageAppointments(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.calendar = Calendar()

        

    @intent_file_handler('appointments.manage.intent')
    def handle_appointments_manage(self, message):
        print(message)
        self.speak_dialog(self.calendar.getNextAppointment())
        #self.speak_dialog('appointments.manage')


def create_skill():
    return ManageAppointments()




