from mycroft import MycroftSkill, intent_file_handler
from caldav.examples.nextcloud_starter import Calendar

class ManageAppointments(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        calendar = Calendar()
        print("Next Appointment: " + calendar.getEventName())

        

    @intent_file_handler('appointments.manage.intent')
    def handle_appointments_manage(self, message):
        print(message)
        self.speak_dialog('appointments.manage')


def create_skill():
    return ManageAppointments()

