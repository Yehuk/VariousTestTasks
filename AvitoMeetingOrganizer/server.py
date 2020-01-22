from http.server import HTTPServer, BaseHTTPRequestHandler
import psycopg2
import json
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
conn = psycopg2.connect(dbname='meetings', user='Nikita',
                        password='', host='localhost', port="5432")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()


class AvitoMeetingsServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        return message.encode("utf8")

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("It is not used anyway"))

    def do_POST(self):
        def create_meeting():
            try:
                postgres_insert_query = ' INSERT INTO meeting (NAME, DATE, TIME) VALUES (%s,%s,%s)'
                record_to_insert = (message.get('name'), message.get('date'), message.get('time'))
                cursor.execute(postgres_insert_query, record_to_insert)
                conn.commit()
                return '\nSuccessfully created!'
            except:
                return "\nCouldn't create meeting due to unknown reasons"

        def delete_meeting():
            meeting_name = message.get('name')
            try:
                cursor.execute('DELETE FROM participant USING meeting WHERE meeting.name = %(meeting_name)s'
                               'AND participant.meetingid = meeting.id',
                               {'meeting_name': meeting_name})
                cursor.execute('DELETE FROM meeting WHERE meeting.name = %(meeting_name)s',
                               {'meeting_name': meeting_name})
                conn.commit()
                return "\nSuccessfully deleted or there wasn't "+meeting_name+" in the first place"
            except:
                return "\nCouldn't delete "+meeting_name+" due to unknown problems"

        def add_participant():
            meeting_name = message.get('meeting_name')
            try:
                try:
                    cursor.execute('SELECT * FROM meeting WHERE name = %(meeting_name)s', {'meeting_name': meeting_name})
                    meeting = cursor.fetchall()
                    meeting_id = meeting[0][0]
                    name = message.get('name')
                    surname = message.get('surname')
                    email = message.get('email')
                    #print(name, surname, email, meeting_name, message.get('meeting_name'))
                except:
                    return "There is no meeting called " + meeting_name
                postgres_insert_query = " INSERT INTO participant (NAME, SURNAME, EMAIL, MEETINGID)" \
                                        " VALUES (%s,%s,%s,%s)"
                record_to_insert = (name, surname, email, meeting_id)
                cursor.execute(postgres_insert_query, record_to_insert)
                conn.commit()
                return '\nSuccessfully created!'
            except:
                return "Couldn't add participant due to unknown reasons"


        def delete_participant():
            name = message.get('name')
            surname = message.get('surname')
            meeting_name = message.get('meeting_name')
            try:
                cursor.execute('SELECT participant.id FROM participant, meeting '
                               'WHERE participant.name = %(name)s AND participant.surname = %(surname)s AND'
                               ' meeting.name = %(meeting_name)s',
                               {'name': name, 'surname': surname, 'meeting_name': meeting_name})
                participant_id = cursor.fetchall()[0][0]
                cursor.execute('DELETE FROM participant where id = %(id)s', {'id':participant_id})
                conn.commit()
                return "\nSuccessfully deleted or that person wasn't attending this meeting in the first place"
            except:
                return name + ' ' + surname + " is not participating in " + meeting_name+" or doesn't exist"

        def show_all_meetings():
            try:
                string = ''
                cursor.execute('select * from meeting left join participant on meeting .id=participant.meetingid'
                               ' order by meeting.date asc, participant.id asc')
                previous_id = 0
                for row in cursor:
                    meeting_id = row[0]
                    meeting = row[1]
                    date = row[2]
                    time = row[3]
                    try:
                        name = row[5]
                        surname = row[6]
                        email = row[7]
                        if meeting_id != previous_id:
                            previous_id = meeting_id
                            string += ('Meeting ' + meeting + ' on ' + str(date) + ' at ' + str(time) + ' is going to be attended by:\n')
                        string += ('Name: ' + name + ' ' + surname + ' email: ' + email + '\n')
                    except:
                        if meeting != 0:
                            string += ('Actually, no one is going to attend meeting ' + meeting + '\n')

            except:
                string = ("\nIt seems there are no meetings\n")
            return string

        def switch(command):
            return working.get(command, show_all_meetings)()

        working = {
            'create_meeting': create_meeting,
            'delete_meeting': delete_meeting,
            'add_participant': add_participant,
            'delete_participant': delete_participant,
            'show_all_meetings': show_all_meetings
        }

        headers = vars(self.headers).get('_headers')
        headers = dict(headers)
        content_type = headers["Content-Type"]
        # refuse to accept anything but json
        if content_type != "application/json":
            self.send_response(400)
            self.end_headers()
            return

        content_length = int(headers["Content-Length"])
        message = json.loads(self.rfile.read(content_length))
        command = message.get('command')
        response = switch(command)

        self._set_headers()
        self.wfile.write(self._html(response))


def turn_off():
    conn.close()
    cursor.close()
    pass

def run(server_class=HTTPServer, handler_class=AvitoMeetingsServer, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print("Starting httpd server...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        turn_off()


run()
