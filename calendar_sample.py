import sys

import tkinter
import tkinter.messagebox as mbox
import datetime

from oauth2client import client
from googleapiclient import sample_tools
from meeting import Meeting

def main(argv):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar.readonly')
    window = tkinter.Tk()
    window.wm_withdraw()
    try:
        utc = datetime.datetime.utcnow()
        calendar_id = 'cortiz@thoughtworks.com'
        time_min = utc.strftime("%Y-%m-%dT%H:%M") + ':00Z'
        time_max = utc.strftime("%Y-%m-%dT%H") + ':59:59Z'
        meeting_list = list()
        while True:
            calendar_list = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max).execute()
            for calendar_list_entry in calendar_list['items']:
                if 'summary' in calendar_list_entry:
                    summary = clean_string(calendar_list_entry['summary'])
                else:
                    summary = ''
                if 'location' in calendar_list_entry:
                    location = clean_string(calendar_list_entry['location'])
                else:
                    location = ''
                meeting_list.append(Meeting(calendar_list_entry['start'], calendar_list_entry['end'], summary, location))
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        mbox.showinfo('Próxima reunión:', print_Meetinges(meeting_list))
    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')

def clean_string(string_to_clean):
    result = ''
    string_without_special_characters = [string_to_clean[j] for j in range(len(string_to_clean)) if ord(string_to_clean[j]) in range(65536)]
    for character in string_without_special_characters:
        result = result + character
    return result

def print_Meetinges(meeting_list):
    result = ''
    separator = '-----------------'
    for meeting in meeting_list:
        result = result + separator + '\n'
        result = result + str(meeting) + '\n'
        result = result + separator + '\n'
    return result

if __name__ == '__main__':
    main(sys.argv)
