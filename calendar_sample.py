#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line sample for the Calendar API.
Command-line application that retrieves the list of the user's calendars."""

import sys

import tkinter
import tkinter.messagebox as mbox
import datetime


from oauth2client import client
from googleapiclient import sample_tools


def main(argv):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar.readonly')
    window = tkinter.Tk()
    window.wm_withdraw()
    sesiones = ''
    try:
        utc = datetime.datetime.utcnow()
        calendar_id = 'cortiz@thoughtworks.com'
        time_min = utc.strftime("%Y-%m-%dT%H") + ':00:00Z'
        time_max = utc.strftime("%Y-%m-%dT%H") + ':59:59Z'
        while True:
#            calendar_list = service.calendarList().list(
#                pageToken=page_token).execute()
            calendar_list = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max).execute()
            for calendar_list_entry in calendar_list['items']:
                if 'summary' in calendar_list_entry:
                    sesiones = sesiones + calendar_list_entry['summary'] + '\n'
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        sesiones_sin_emojins = [sesiones[j] for j in range(len(sesiones)) if ord(sesiones[j]) in range(65536)]
        sesiones = ''
        for caracter in sesiones_sin_emojins:
            sesiones = sesiones + caracter
        mbox.showinfo('Próxima reunión:',sesiones)
    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')

if __name__ == '__main__':
    main(sys.argv)
