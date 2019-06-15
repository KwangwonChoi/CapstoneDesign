import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import threading
import time

class FirebaseSupporter:

    def __init__(self):

        cred = credentials.Certificate('path/to/serviceAccountKey.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL':'https://healthcare-d366c.firebaseio.com/'
        })

        self.ref = db.reference()
        self.doctorMessageSize = 4
        self.messageGet = False
        self.doctorEvent = None
        self.doctorParam = None

    def __setattr__(self, key, value):
        super().__setattr__(key,value)

        if(key == 'messageGet' and value == True):
            self.doctorEvent(self.doctorParam)
            self.doctorParam = None
            self.messageGet = False

    def alertRegistration(self, user, state, details):
        alertMessage = {
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") : {
                'state' : state,
                'details' : details
            }
        }

        ref = self.ref.child('Client').child(user).child('alert_log')
        ref.update(alertMessage)

    def listenMessage(self, event):
        self.doctorEvent = event
        thread = threading.Thread(target= self.doctorEventListener)
        thread.start()

    def doctorEventListener(self):
        ref = self.ref.child('Doctor').child('Messages')

        self.doctorMessageSize = len(ref.get())

        while True:
            curMessages = ref.get()

            if len(curMessages) != self.doctorMessageSize:
                i = 1
                for items in curMessages.items():
                    if i > self.doctorMessageSize:
                        self.doctorParam = items
                        self.messageGet = True
                    else:
                        i += 1

            self.doctorMessageSize = len(curMessages)
            time.sleep(3)

