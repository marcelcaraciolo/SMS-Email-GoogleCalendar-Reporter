'''
SMS/E-mail Report Manager.

A simple script for sending SMS's when there is some problems during the execution of a task.

It uses the Google Calendar Engine Notifications to send SMS/E-mail.

'''

__author__ = 'caraciol@gmail.com (Marcel Caraciolo)'

import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import string
import time

USUARIO = 'GOOGLE EMAIL'
PASSWORD = 'YOUR PASSWORD'

class CalendarReportManager(object):
    
    def __init__(self,email,password):
        self.cal_client = gdata.calendar.service.CalendarService()
        self.cal_client.email = email
        self.cal_client.password = password
        self.cal_client.source = 'Report Manager v0.1'
        self.cal_client.ProgrammaticLogin()
    
    def _AddReminder(self, event, minutes=10):
    
        for a_when in event.when:
            if len(a_when.reminder) > 0:
                a_when.reminder[0].minutes = minutes
            else:
                a_when.reminder.append(gdata.calendar.Reminder(minutes=minutes))

        return self.cal_client.UpdateEvent(event.GetEditLink().href, event)

    
    def setEventReport(self,title,msg,where,start_time=None,end_time=None,minutes=60):
        new_event =  self._InsertEvent(title,msg,where,start_time,end_time)
        self._AddReminder(new_event,minutes)
    
    def _InsertEvent(self,title,msg,where,start_time=None,end_time=None,recurrence_data=None):
        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=title)
        event.content = atom.Content(text=msg)
        event.where.append(gdata.calendar.Where(value_string=where))
        
        if recurrence_data is not None:
            # Set a recurring event
            event.recurrence = gdata.calendar.Recurrence(text=recurrence_data)
        else:
            if start_time is None:
                # Use current_time + 1 hour and 15 min for the start_time and have the event for 4 minutes.
                start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',  time.gmtime(time.time() + 4500))
                end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 4740))
            event.when.append(gdata.calendar.When(start_time=start_time,end_time=end_time))

        new_event = self.cal_client.InsertEvent(event, 
            '/calendar/feeds/default/private/full')

        return new_event


if __name__ == '__main__':
    crm = CalendarReportManager(USUARIO,PASSWORD)
    crm.setEventReport('ALERT','Fail in execution of the script execute.sh', 'Project: Atepassar-Recommendation')
