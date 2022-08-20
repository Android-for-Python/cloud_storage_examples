from kivy.app import App
from kivy.utils import platform
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock, mainthread
from kivy.lang import Builder

from functools import partial
from threading import Thread
from os.path import exists, join
from os import remove as remove_file

if platform == 'android':
    from android.storage import app_storage_path

from firestore4kivy import Authorize, Firestore, GeoPoint, TimeStamp, Reference

#######################################################################
# Replace these placeholders
APIKEY = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
PROJECT_ID = 'bbbbbbbbbb'
APIKEY = 'AIzaSyDAoA3Bf1qCD0zpygPvjpeFpvGXSYmcD9E'
PROJECT_ID = 'test-285db'
#######################################################################

#######################################################################
# In a real application these would entered using a Textinput,
# and not be hard coded in the app.
# No need to change these for this demonstration example.
DEMO_NAME = 'Random Hacker Two'
DEMO_ACC  = 'randomhacker2@kivy.org'
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

class RestFirestoreExample(App):
    
    ################################
    # Lifecycle
    ################################

    def build(self):
        self.last_response = None
        self.refresh_timer = None
        self.rv = RV()
        return self.rv 

    def on_start(self):
        if APIKEY == 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' or\
           PROJECT_ID == 'bbbbbbbbbb':
            self.update_label('ERROR: Api-Key or Project-Id not set by user.')
            return
        self.choose_demonstration()

    def on_resume(self):
        self.choose_demonstration()

    def choose_demonstration(self):
        # app behavior depends on token file existance.
        # demonstration0: start, authorized by sign in
        # demonstration1: resume or restart, authorized by token file,
        if exists(self.token_file_path()):
            Thread(target = self.rest_firestore_demonstration1,
                   daemon = True).start()
        else:
            self.rv.data = []
            Thread(target = self.rest_firestore_demonstration0,
                   daemon = True).start()

    ###############################################
    # Demonstration Part 0
    # - create and sign in user,
    # - CRUD demonstrations
    # - create shared data document
    ###############################################
        
    def rest_firestore_demonstration0(self):
        self.update_label('\n\n')
        self.update_label('Starting Firestore Database demonstration.\n')
        auth = Authorize(APIKEY)
        self.db = Firestore(PROJECT_ID)
        
        # Create user
        # In real app: add a dialog to get USER, NAME, and PASSWORD
        success, response = auth.create_user_with_email(DEMO_ACC, DEMO_PW)
        if success:
            self.update_label('"' + DEMO_NAME + '" Account created.')
        elif 'EMAIL_EXISTS' not in response:
            self.update_label(response)
            return

        account_created = success

        if not self.sign_in(auth, DEMO_ACC, DEMO_PW):
            return
        self.update_label('"' + DEMO_NAME + '" Signed in\n')

        # Demonstrate CRUD operations
        self.update_label('Demonstrate CRUD operations')
        
        # Create
        data = {'age': 20, 'location': 'lunar orbit'} 
        result = self.create_private_document('data', data)
        if not result:
            self.update_label('Document Create failed.')
            self.error_cleanup()
            return
        else:
            self.update_label('Document Create succeeded.')

        # Read
        result = self.read_private_document('data')
        if not result or result['age'] != 20:
            self.update_label('Document Read failed.')
            self.error_cleanup()
            return
        else:
            self.update_label('Document Read succeeded.')

        # Update
        data = {'age': 25}
        result = self.update_private_document('data', data)
        if not result:
            self.update_label('Document Update failed.')
            self.error_cleanup()
            return

        # Read
        result = self.read_private_document('data')
        if not result or result['age'] != 25:
            self.update_label('Document Update Test failed.')
            self.error_cleanup()
            return
        else:
            self.update_label('Document Update succeeded.')

        # Delete
        success = self.delete_private_document('data')
        if success:
            self.update_label('Document Delete succeeded.')
        else:
            self.update_label('Document Delete failed.')
            self.error_cleanup()
            return

        # Create document with diverse data types
        #########################################

        result = self.create_shared_document('shared', 'configuration',
                                             self.test_dict())
        if result:
            self.update_label('\nShared Data Document Created.')
        else:
            self.update_label('\nShared Data Document Create failed.')
            self.error_cleanup()
            return

        if account_created:
            # save info about new account for restart/resume 
            result = self.create_private_document('id', {'name' : DEMO_NAME})
            if result:
                self.update_label('User name document created.')
            else:
                self.update_label('User name document create failed.')
                self.error_cleanup()
                return
            
        # User instructions
        self.update_label('\nLook in your Firestore console to see the data.\n')
        if platform in ['android', 'ios']:
            self.update_label('Pause, then resume (or restart) the app.')
        else:
            self.update_label('Exit, then restart the app.')


    ################################
    # Demonstration Part 1
    # - resume app
    # - read user id
    # - read shared document
    # - cleanup
    ################################
        
    def rest_firestore_demonstration1(self):
        if platform in ['ios', 'android']:
            self.update_label('\n------------------------------------------')
        else:
            self.update_label('\n')
            
        self.update_label('\nResuming Firestore Database demonstration.\n')
        auth = Authorize(APIKEY)
        self.db = Firestore(PROJECT_ID)

        if not self.authorize_with_token_file():
            self.update_label('Token based authorization failed.')
            return

        # If only I could remember my name
        result = self.read_private_document('id')
        if result and 'name' in result:
            self.update_label('"' + result['name'] + '" authorized by token.\n')
        else:
            self.update_label('ERROR: Failed to read user name.')
            self.error_cleanup()
            return
        
        # what else do I remember?
        result = self.read_shared_document('shared','configuration')
        if result:
            match, modified = self.test_dict_eq(result, self.test_dict())
            if match:
                self.update_label('Shared document contains correct data.')
            else:
                self.update_label('ERROR: Shared document has incorrect data.')
                self.update_label(modified)
                self.error_cleanup()
                return
        else:
            self.update_label('Shared document read failed.')
            self.error_cleanup()
            return

        # lets try some more complex updates           Equivalent statements
        replace_these = {'b' : False,                # ['b'] = False
                         'd' : {'c' : -43 ,          # ['d']['c'] = -43
                                'e' : [-10,-20,-30]},# ['d']['e'] =[-10,-20,-30]
                         'new' : True,               # ['new'] = True
                         'a' : [(1,'negative'),      # ['a'][1] = 'negative'
                                (4,'new')],}         # ['a'].append('new')

        delete_these =  {'f':'',                     # pop('f')
                         'd': {'d' : {'aa': ''}},    # ['d']['d'].pop('aa')
                         'a': [(0,''),               # d['a'].pop(0)
                               (3, {'yes': ''})] }   # d['a'][2].pop('yes')
        
        result = self.update_shared_document('shared', 'configuration',
                                             replace_these,
                                             delete_these, self.state_machine)
        if result:
            match, modified = self.test_dict_eq(result, self.test_update_dict())
            if match:
                self.update_label('Updated Shared Document has correct data.')
            else:
                self.update_label('ERROR: Updated Shared document incorrect.')
                self.update_label(modified)
                self.error_cleanup()
                return
        else:
            self.update_label('Updated shared document read failed.')
            self.error_cleanup()
            return

        # Delete data and user
        self.delete_shared_document('shared','configuration')
        self.delete_private_document('id')
        self.update_label('\nDeleted demonstration data.')
        auth.delete_user(self.last_response)
        self.authorize_actions(False, {})
        self.update_label('Deleted demonstration account.')
        self.update_label('\nSUCCESS.')

    # for update test above
    def state_machine(self, data):
        data['i'] += 10
    
    ###############################
    # Auth Utilities
    ###############################

    def sign_in(self, auth, user, password):
        success, response = auth.sign_in_with_email(user, password)
        self.authorize_actions(success, response)
        return success

    def authorize_with_token_file(self):
        auth = Authorize(APIKEY)
        refresh_token = self.read_token_file()
        success, response = auth.sign_in_with_token(refresh_token)
        self.authorize_actions(success, response)
        return success

    def authorize_after_timeout(self, response, dt):       
        self.refresh_timer = None
        auth = Authorize(APIKEY)
        success, response = auth.sign_in_with_token(response['refreshToken'])
        self.authorize_actions(success, response)

    def authorize_actions(self, success, response):
        if self.refresh_timer:
            Clock.unschedule(self.refresh_timer)
        if success:
            self.db.enable_database(response)
            self.write_token_file(response)
            self.refresh_timer =\
                Clock.schedule_once(partial(self.authorize_after_timeout,
                                            dict(response)), 3550)
            self.last_response = response
        else:
            self.db.enable_database(None)
            self.delete_token_file()
            self.refresh_timer = None        
            self.last_response = None    


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

    def write_token_file(self, response):
        if response and isinstance(response, dict) and\
           'refreshToken' in response:
            with open(self.token_file_path(), 'w') as f:
                f.write(response['refreshToken'])

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
    # PRIVATE document utilities
    # document name is always localId
    ###############################

    def create_private_document(self, collection, data):
        success, result, update_time = self.db.create(collection, None, data)
        if success:
            return result
        else:
            self.update_label(result)
            return {}

    def read_private_document(self, collection):
        success, result, update_time = self.db.read(collection, None)
        if success:
            return result
        else:
            self.update_label(result)
            return {}

    def update_private_document(self, collection,
                                replace = {}, delete = {}, callback = None):
        success, result, update_time = self.db.update(collection, None,
                                                      replace, delete, callback)
        if success:
            return result
        else:
            self.update_label(result)
            return {}

    def delete_private_document(self, collection):
        success, result, update_time = self.db.delete(collection, None)
        if not success:
            self.update_label(result)
        return success

    ###############################
    # SHARED document utilities
    ###############################

    def create_shared_document(self, collection, document, data):
        success, result, update_time = self.db.create(collection, document,
                                                      data)
        if success:
            return result
        else:
            self.update_label(result)
            return {}

    def read_shared_document(self, collection, document):
        success, result, update_time = self.db.read(collection, document)
        if success:
            return result
        else:
            self.update_label(result)
            return {}

    def update_shared_document(self, collection, document,
                                replace = {}, delete = {}, callback = None):
        success, result, update_time = self.db.update(collection, document,
                                                      replace, delete, callback)
        if success:
            return result
        else:
            self.update_label(result)
            return {}

    def delete_shared_document(self, collection, document):
        success, result, update_time = self.db.delete(collection, document)
        if not success:
            self.update_label(result)
        return success
    

    #########################
    # Testing Utilities
    #########################

    # Reference:
    # https://firebase.google.com/docs/firestore/manage-data/data-types
    def test_dict(self):
        if self.last_response:
            # document that we know exists in the demonstration
            document = self.last_response['localId']
        else:
            document = ''
        return {'i': 7,
                'f': 7.2,
                'b': True,
                'by' : b'00000000000000000000000000f1',
                'n' : None,
                's' : 'whatever',
                'a': ['zero','one', 2, {'yes':True, 'no':False}],
                'get_lost': GeoPoint( 10.5, -100),
                'r': Reference('projects/' + PROJECT_ID +\
                               '/databases/(default)/documents/id/' +\
                               document),
                't': TimeStamp(None),
                'd' : {'booleanValue': 'not a boolean',
                       'b': 'bbb',
                       'c': 42,
                       'd': {'aa' : 'xx', 'bb': 10.2, 'cc' : 10.3,
                             'dd': {'aaa':'a', 'bbb':'b'} },
                       'e': [10,20,30],},
                'big list' : [i * i for i in range(1900)],
                'big dict' : {str(i): i * i for i in range(966)}}

    def test_update_dict(self):
        d = self.test_dict()
        # These are equivalent statements to the update_shared_document above
        # replace
        d['b'] = False
        d['d']['c'] = -43
        d['a'][1] = 'negative'
        d['d']['e'] = [-10,-20,-30]
        d['new'] = True
        d['a'].append('new')
        # delete
        d.pop('f')
        d['d']['d'].pop('aa')
        d['a'][3].pop('yes')   
        d['a'].pop(0)   
        # callback
        d['i'] += 10
        return d

    def test_dict_eq(self, d1, d2):
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        shared_keys = d1_keys.intersection(d2_keys)
        added = d1_keys - d2_keys
        removed = d2_keys - d1_keys
        modified = {o : (d1[o], d2[o]) for o in shared_keys
                    if self.test_custom_neq(d1[o], d2[o])}
        msg = ''
        if added != set():
            msg += 'Added   ' + str(added) + '\n'
        if removed != set():
            msg += 'Removed ' + str(removed) + '\n'
        if modified != {}:
            msg += 'Modified ' + str(modified) + '\n'
        return added == set() and removed == set() and not modified, msg

            
    def test_custom_neq(self, a, b):
        if isinstance(a, GeoPoint):
            return a.get() != b.get()
        elif isinstance(a, TimeStamp):
            return a.get() != b.get()
        elif isinstance(a, Reference):
            return a.get() != b.get()
        else:
            return a != b

    ###############################
    # other utilities
    ###############################

    def error_cleanup(self):
        self.delete_shared_document('shared','configuration')
        self.delete_token_file()
        auth = Authorize(APIKEY)
        auth.delete_user(self.last_response)

    @mainthread
    def update_label(self, string):
        length = 50
        lines = ''
        for i in range(0, len(string), length):
            lines = lines + '\n' + string[0+i:length+i]
        self.rv.data.append({'text' : lines})
            
RestFirestoreExample().run()


