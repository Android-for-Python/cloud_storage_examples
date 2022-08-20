from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock, mainthread
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder

from threading import Thread
from os.path import exists, join
from os import remove as remove_file
import json
import requests

if platform == 'android':
    from android.storage import app_storage_path
    
import pyrebase  

#######################################################################
# Replace these placeholders:
APIKEY = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
PROJECT_ID = 'bbbbbbbbbb'
APIKEY = 'AIzaSyDAoA3Bf1qCD0zpygPvjpeFpvGXSYmcD9E'
PROJECT_ID = 'test-285db'
#
#######################################################################

#######################################################################
# In a real application these would entered using a Textinput,
# and not be hard coded in the app.
# No need to change these for this demonstration example.
DEMO_NAME = 'Random Hacker One'
DEMO_ACC  = 'randomhacker1@kivy.org'
DEMO_PW   = 'cO1jX9qB1xR9lI1g'
#
#######################################################################

################################
# Layout
################################

Builder.load_string('''
<RV>:
    viewclass: 'Label'
    RecycleBoxLayout:
        default_size: None, dp(30)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []    

################################
# App
################################

class Pyrebase4Example(App):
    
    ################################
    # Lifecycle
    ################################

    def build(self):
        self.user = {}
        self.user_id = ''
        self.refresh_timer = None
        self.rv = RV()
        return self.rv         

    def on_start(self):
        if APIKEY == 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' or\
           PROJECT_ID == 'bbbbbbbbbb':
            self.update_label('ERROR: Api-Key or Project-Id not set by user.')
            return
        config = {
            "apiKey": APIKEY,
            "authDomain": PROJECT_ID + '.firebaseapp.com',
            "databaseURL": 'https://' + PROJECT_ID + '-default-rtdb.firebaseio.com',
            "storageBucket": PROJECT_ID + '.appspot.com'
        }
        self.pyre = pyrebase.initialize_app(config)
        self.choose_demonstration()

    def on_resume(self):
        self.choose_demonstration()

    def choose_demonstration(self):
        # app behavior depends on token file existance.
        # demonstration0: start, authorized by sign in
        # demonstration1: resume or restart, authorized by token file,
        if exists(self.token_file_path()):
            Thread(target = self.pyrebase4_demonstration1,
                   daemon = True).start()
        else:
            self.rv.data = []
            Thread(target = self.pyrebase4_demonstration0,
                   daemon = True).start()

    ###############################################
    # Demonstration 0
    # create and sign in user, CRUD demonstrations
    ###############################################
        
    def pyrebase4_demonstration0(self):
        self.update_label('\nStarting Realtime Database demonstration.\n')
        auth = self.pyre.auth()
        db = self.pyre.database()
        account_created = False
        # Create user
        # In real app: add a dialog to get USER, NAME, and PASSWORD
        try:
            response = auth.create_user_with_email_and_password(DEMO_ACC,
                                                                DEMO_PW)
            self.update_label('"' + DEMO_NAME + '" Account created.')
            account_created = True
            if not self.sign_in(auth, DEMO_ACC , DEMO_PW):
                return
        except Exception as e:
            # assume account with this email already created
            if not self.sign_in(auth, DEMO_ACC , DEMO_PW):
                return
        self.update_label('"' + DEMO_NAME + '" Signed in\n')

        # Demonstrate CRUD operations
        self.update_label('Demonstrate CRUD operations')
        
        # Create
        data = {'age': 20, 'location': 'lunar orbit'} 
        self.create_private_document(db, 'data', data)

        # Read
        saved = self.read_private_document(db, 'data')
        if not saved or saved.val()['age'] != 20:
            self.update_label('Document Create and Read failed.')
            self.error_cleanup()
            return
        else:
            self.update_label('Document Create and Read succeeded.')

        # Update
        data = {'age': 25}
        self.update_private_document(db, 'data', data)

        # Read
        saved = self.read_private_document(db, 'data')
        if not saved or saved.val()['age'] != 25:
            self.update_label('Document Update failed.')
            self.error_cleanup()
            return
        else:
            self.update_label('Document Update succeeded.')

        # Delete
        self.delete_private_document(db, 'data')
        result = self.read_private_document(db, 'data')
        if not result or result.val():
            self.update_label('Document Delete failed.')
            self.error_cleanup()
            return
        else:
            self.update_label('Document Delete succeeded.')

        self.update_label('CRUD demonstration succeeded.\n')

        if account_created:
            # Save DEMO_NAME in the db
            self.update_label('Save user name.\n')
            self.create_private_document(db, 'id', {'name' : DEMO_NAME})

        # Create some different data
        self.update_label('Save some more data.\n')
        data = {'status' : {'win': 43, 'loose': 21, 'draw': 7}}
        self.create_private_document(db, 'more_data', data)

        # User instructions
        if platform == 'android':
            self.update_label('Pause, then resume (or restart) app.')
        else:
            self.update_label('Exit, then restart app.')


    ################################
    # Demonstration 1
    # resume app, read database
    ################################
        
    def pyrebase4_demonstration1(self):
        if platform in ['ios', 'android']:
            self.update_label('\n------------------------------------------')
        else:
            self.update_label('\n')
        self.update_label('\nResuming Realtime Database demonstration.\n')
        auth = self.pyre.auth()
        db = self.pyre.database()
        
        if not self.authorize_with_token_file():
            self.update_label('Token based authorization failed.')
            self.error_cleanup()
            return        

        # do I remember my name?
        self.update_label('Welcome Back "' + self.get_user_name(db) + '"')

        # what else do I remember?
        try:
            saved = self.read_private_document(db, 'more_data')
            if saved and saved.val()['status']['win'] == 43:
                self.update_label('Success reading previous data.')
            else:
                self.update_label('Previous data incorrect.')
                self.error_cleanup()
                return
        except Exception as e:
            self.update_label('Error: ' + str(e))
            self.error_cleanup()
            return
        
        # Delete data and user
        self.delete_private_document(db, 'more_data')
        self.delete_private_document(db, 'id')
        self.delete_token_file()
        self.update_label('\nDeleted demonstration data.')
        self.delete_user(self.user['idToken'])
        self.user = None
        self.update_label('Deleted demonstration account.')
        self.update_label('\nSUCCESS.')
        
    ###############################
    # Auth Utilities
    ###############################

    def sign_in(self, auth, user, password):
        response = auth.sign_in_with_email_and_password(user, password)
        success = self.authorize_actions(response)
        if not success:
            self.update_label('Sign in failed.')
        return success

    def authorize_with_token_file(self):
        refresh_token = self.read_token_file()
        auth = self.pyre.auth()
        response = auth.refresh(refresh_token)
        return self.authorize_actions(response)

    def refresh_user(self,dt):
        auth = self.pyre.auth()
        response = auth.refresh(self.user['refreshToken'])
        self.refresh_timer = None
        success = self.authorize_actions(response)
        if not success:
            self.update_label('Please sign in again')
            # In real app: add dialog to get user and password
            self.sign_in(self, auth, DEMO_ACC, DEMO_PW)

    def authorize_actions(self, response):
        fail = 'error' in response
        if self.refresh_timer:
            Clock.unschedule(self.refresh_timer)
        if fail:
            self.user = {'idToken' : '', 'localId' : '', 'refreshToken' : ''}
            self.user_id = ''
            self.delete_token_file()
            self.refresh_timer = None        
        else:
            self.user = response
            if 'localId' in response:
                self.user_id = response['localId']
            elif 'userId' in response:
                self.user_id = response['userId']
            else:
                self.user_id = ''
            self.write_token_file()
            self.refresh_timer = Clock.schedule_once(self.refresh_user, 3500)
        return not fail


    ###############################
    # token file utilities
    ###############################

    def token_file_path(self):
        file_name = 'token.txt'
        if platform == 'android':
            file_path = join(app_storage_path(), file_name)
        elif platform == 'ios':
            file_path = join(getattr(self, 'user_data_dir'), file_name)
        else:
            file_path = join('./', file_name)
        return file_path

    def write_token_file(self):
        if self.user:
            with open(self.token_file_path(), 'w') as f:
                f.write(self.user['refreshToken'])

    def read_token_file(self):
        if exists(self.token_file_path()):
            with open(self.token_file_path(), 'r') as f:
                refresh_token = f.read()
            return refresh_token
        else:
            return ''

    def delete_token_file(self):
        if exists(self.token_file_path()):
            remove_file(self.token_file_path())

    ###############################
    # document utilities
    # document name is user_id
    ###############################

    def create_private_document(self, db, collection, payload):
        try:
            db.child(collection).child(self.user_id).set(payload,
                                                         self.user['idToken'])
        except Exception as e:
            self.update_label(str(e))

    def read_private_document(self, db, collection):
        try:
            return db.child(collection).child(self.user_id).get(self.user['idToken'])
        except Exception as e:
            self.update_label(str(e))
            return None

    def update_private_document(self, db, collection, payload):
        try:
            db.child(collection).child(self.user_id).update(payload,
                                                            self.user['idToken'])
        except Exception as e:
            self.update_label(str(e))

    def delete_private_document(self, db, collection):
        try:
            db.child(collection).child(self.user_id).remove(self.user['idToken'])
        except Exception as e:
            self.update_label(str(e))

    ###############################
    # other utilities
    ###############################

    def get_user_name(self,db):
        saved = self.read_private_document(db, 'id')
        try:
            return saved.val()['name']
        except Exception as e:
            self.update_label(str(e))
            return 'Nameless Fool'

    def delete_user(self, id_token):
        REST_IDENTITY = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/'
        payload = json.dumps({"idToken": id_token})
        url = REST_IDENTITY + 'deleteAccount?key=' + APIKEY
        try:
            r = requests.post(url, data=payload)
            return json.loads(r.text)
        except Exception as e:
            return {'error' : str(e)}

    def error_cleanup(self):
        self.delete_token_file()
        self.delete_user(self.user['idToken'])
        
    @mainthread
    def update_label(self, string):
        length = 50
        lines = ''
        for i in range(0, len(string), length):
            lines = lines + '\n' + string[0+i:length+i]
        self.rv.data.append({'text' : lines})
        
Pyrebase4Example().run()


