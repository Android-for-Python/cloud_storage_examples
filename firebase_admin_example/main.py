from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import mainthread
from firebase_admin import credentials, auth, initialize_app
from threading import Thread

class AdminApp(App):
    def build(self):
        self.label = Label()
        return self.label

    def on_start(self):
        Thread(target = self.admin_demo, daemon = True).start()

    def admin_demo(self):
        # Use the key
        #############
        cred = credentials.Certificate('./service_account_key.json')
        initialize_app(cred)

        # Admin task, list all the project user emails
        ##############################################
        self.update_label('List of users:')
        for user in auth.list_users().iterate_all():
            self.update_label('    ' + user.email)

    @mainthread
    def update_label(self, string):
        length = 42
        for i in range(0, len(string), length):
            self.label.text = self.label.text + '\n' + string[0+i:length+i]

AdminApp().run()

