import urllib.request
import json

class AvitoMeetingsClient:
    def __init__(self):
        self.req = ''

    def email_validation(self, x):
        a=0
        y=len(x)
        dot=x.find(".")
        at=x.find("@")
        for i in range (0,at):
            if((x[i]>='a' and x[i]<='z') or (x[i]>='A' and x[i]<='Z')):
                a=a+1
        return a>0 and at>0 and (dot-at)>0 and (dot+1)<y


    def create_meeting(self, name='', date='', time=''):
        print("Creating meeting...")
        command = "create_meeting"
        if name == '':
            name = input("Enter meeting name: ")
        if date == '':
            date = input("Enter date 'YYYY-MM-DD': ")
        if time == '':
            time = input("Enter time 'HH:MM': ")
        body = {'command' : command, 'name' : name, 'date' : date, 'time' : time}
        result = self.send_to_server(body)
        print(result)
        return result


    def delete_meeting(self,  name=''):
        print("Deleting meeting...")
        command = "delete_meeting"
        if name == '':
            name = input("Enter meeting name: ")
        body = {'command' : command, 'name' : name}
        result = self.send_to_server(body)
        print(result)
        return result


    def add_participant(self, name='', surname='', email='', meeting_name=''):
        print("Creating participant...")
        command = "add_participant"
        if name == '':
            name = input("Enter participant's name: ")
        if surname == '':
            surname = input("Enter participant's surname: ")
        if email == '':
            email = input("Enter participant's email: ")
        if not self.email_validation(email):
            print('This email is not ok, either enter non existing meeting name to cancel,'
                  'or be warned that this participant will not have valid contact email')
            email = "none"
        if meeting_name == '':
            meeting_name = input("Enter meeting name: ")
        body = {'command' : command, 'name' : name, 'surname' : surname, 'email' : email, 'meeting_name' : meeting_name}
        result = self.send_to_server(body)
        print(result)
        return result


    def delete_participant(self, name='', surname='', meeting_name=''):
        print("Deleting participant...")
        command = "delete_participant"
        if name == '':
            name = input("Enter participant's name: ")
        if surname == '':
            surname = input("Enter participant's surname: ")
        if meeting_name == '':
            meeting_name = input("Enter meeting name: ")
        body = {'command' : command, 'name' : name, 'surname' : surname, 'meeting_name' : meeting_name}
        result = self.send_to_server(body)
        print(result)
        return result


    def show_all_meetings(self):
        print("Showing all meetings...")
        command = "show_all_meetings"
        body = {'command' : command}
        result = self.send_to_server(body)
        print(result)
        return result


    def help_me(self):
        print("Available commands:\n"
              "Create meeting: 1\n"
              "Delete meeting: 2\n"
              "Add participant: 3\n"
              "Delete participant: 4\n"
              "Show all meetings: 5\n"
              "End your work: 6\n"
              "This menu: help_me")


    def finish(self):
        print("Goodbye!")
        return "Exit"


    def send_to_server(self, body):
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
        self.req.headers.update({'Content-Length': len(jsondataasbytes)})
        #print(jsondataasbytes, req)
        response = urllib.request.urlopen(self.req, jsondataasbytes)
        #print(body.get('command'))
        response_ret = response.read().decode('utf-8')
        return response_ret


    def default(self):
        print("Unknown command, please try again")
        self.help_me()


    def switch(self, command):
        working = {
            '1': self.create_meeting,
            '2': self.delete_meeting,
            '3': self.add_participant,
            '4': self.delete_participant,
            '5': self.show_all_meetings,
            '6': self.finish,
            'help_me': self.help_me
        }
        response = working.get(command, self.default)()
        return response



    def start(self):
        myurl = "http://localhost:8000"
        self.req = urllib.request.Request(myurl)
        self.req.add_header('Content-Type', 'application/json')
        user_input = ""
        print("Greetings! Please enter code of command, or help to list all codes")

    def run(self):
        self.start()
        while True:
            user_input = input("\nEnter command: ")
            if self.switch(user_input) == "Exit":
                return 1

