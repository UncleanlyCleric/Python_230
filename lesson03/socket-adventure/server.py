#!/user/bin/env python3
'''
Python 230 activity.
'''

import socket

# pylint: disable = R0201, R0205, W0613

class Server(object):
    '''
    An adventure game socket server

    An instance's methods share the following variables:

    * self.socket: a 'bound' server socket, as produced by socket.bind()
    * self.client_connection: a 'connection' socket as produced by socket.accept()
    * self.input_buffer: a string that has been read from the connected client and
      has yet to be acted upon.
    * self.output_buffer: a string that should be sent to the connected client; for
      testing purposes this string should NOT end in a newline character. When
      writing to the output_buffer, DON'T concatenate: just overwrite.
    * self.done: A boolean, False until the client is ready to disconnect
    * self.room: one of 0, 1, 2, 3. This signifies which 'room' the client is in,
      according to the following map:

                                     3                      N
                                     |                      ^
                                 1 - 0 - 2                  |

    When a client connects, they are greeted with a welcome message. And then they can
    move through the connected rooms. For example, on connection:

    OK! Welcome to Realms of Venture! This room has brown wall paper!  (S)
    move north                                                         (C)
    OK! This room has white wallpaper.                                 (S)
    say Hello? Is anyone here?                                         (C)
    OK! You say, 'Hello? Is anyone here?'                              (S)
    move south                                                         (C)
    OK! This room has brown wall paper!                                (S)
    move west                                                          (C)
    OK! This room has a green floor!                                   (S)
    quit                                                               (C)
    OK! Goodbye!                                                       (S)

    Note that we've annotated server and client messages with *(S)* and *(C)*, but
    these won't actually appear in server/client communication. Also, you'll be
    free to develop any room descriptions you like: the only requirement is that
    each room have a unique description.
    '''

    game_name = 'Capsized Obiectum'

    def __init__(self, port=50000):
        self.input_buffer = ''
        self.output_buffer = ''
        self.done = False
        self.socket = None
        self.client_connection = None
        self.port = port

        self.room = 0

    def connect(self):
        '''
        Looks to be initializing the connect socket
        '''
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP)

        address = ('127.0.0.1', self.port)
        self.socket.bind(address)
        self.socket.listen(1)

        self.client_connection, address = self.socket.accept()


    def room_description(self, room_number):
        '''
        For any room_number in 0, 1, 2, 3, return a string that 'describes' that
        room.

        Ex: `self.room_number(1)` yields 'Brown wallpaper covers the walls,
        bathing the room in warm light reflected from the half-drawn curtains.'

        :param room_number: int
        :return: str
        '''

        return [
            'You are in a grey room with vines growing on the walls.  The \
vines are blood red, and leave the impression they are following you.  There \
are exits to the west, east, and north.',

            'This room is well lit, and you can see aged floral wallpaper.  \
from the corner of your eyes you can see shapes in the pattern, they disappear\
when you look closer.  There is an exit to the east.',

            'The room is bare cinder block, the fluorescent lights flicker in\
time with your breath.  There is an exit to the west.',

            'A single lightbulb hangs in the center of this red room.  Faint \
voices whisper your name, the whispering is randomly punctuated with a scream.\
There is an exit to the south.',
        ][room_number]


    def greet(self):
        '''
        Welcome a client to the game.

        Puts a welcome message and the description of the client's current room
        into the output buffer.

        :return: None
        '''
        self.output_buffer = 'Welcome to {}! {}'.format(
            self.game_name,
            self.room_description(self.room)
        )

    def get_input(self):
        '''
        Retrieve input from the client_connection. All messages from the client
        should end in a newline character: '\n'.

        :return: None
        '''

        received = b''
        while b'\n' not in received:
            received += self.client_connection.recv(16)

        self.input_buffer = received.decode().strip()


    def move(self, argument):
        '''
        Moves the client from one room to another.

        Examines the argument, which should be one of:

        * 'north'
        * 'south'
        * 'east'
        * 'west'

        'Moves' the client into a new room by adjusting self.room to reflect the
        number of the room that the client has moved into.

        :argument: str
        :return: None
        '''

        if self.room == 0 and argument == 'north':
            self.room = 3

        if self.room == 0 and argument == 'west':
            self.room = 1

        if self.room == 0 and argument == 'east':
            self.room = 2

        if self.room == 1 and argument == 'east':
            self.room = 0

        if self.room == 2 and argument == 'west':
            self.room = 0

        if self.room == 3 and argument == 'south':
            self.room = 0

        self.output_buffer = self.room_description(self.room)


    def say(self, argument):
        '''
        Lets the client speak by putting their utterance into the output buffer.

        For example:
        `self.say('Is there anybody here?')`
        would put
        `You say, 'Is there anybody here?'`
        into the output buffer.

        :param argument: str
        :return: None
        '''

        self.output_buffer = "You say, '{}'".format(argument)


    def quit(self, argument):
        '''
        Quits the client from the server.

        Turns `self.done` to True and puts 'Goodbye!' onto the output buffer.

        Ignore the argument.

        :param argument: str
        :return: None
        '''

        self.done = True
        self.output_buffer = 'Goodbye!'


    def route(self):
        '''
        Examines `self.input_buffer` to perform the correct action.

        For example, if the input buffer contains 'say Is anybody here?' then
        `route` should invoke `self.say('Is anybody here?')`. If the input
        buffer contains 'move north', then `route` should invoke
        `self.move('north')`.

        :return: None
        '''

        received = self.input_buffer.split(' ')

        command = received.pop(0)
        arguments = ' '.join(received)

        {
            'quit': self.quit,
            'move': self.move,
            'say': self.say,
        }[command](arguments)


    def push_output(self):
        '''
        Sends the contents of the output buffer to the client.

        This method should prepend 'OK! ' to the output.

        :return: None
        '''

        self.client_connection.sendall(b'OK! ' + self.output_buffer.encode() + b'\n')


    def serve(self):
        '''
        Looks to be the function that's actually serving data out
        '''
        self.connect()
        self.greet()
        self.push_output()

        while not self.done:
            self.get_input()
            self.route()
            self.push_output()

        self.client_connection.close()
        self.socket.close()
