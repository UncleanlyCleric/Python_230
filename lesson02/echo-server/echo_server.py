#!/usr/bin/env python3
'''
Lesson02 Echo server.
'''
import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    '''
    This will be the server code.
    '''
    # set an address for our server
    address = ('127.0.0.1', 10000)
    # Creating IPv4 socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    # Set socket option preventing "port is already used" errors
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # Bind sock to the address and begin to listen for incoming connections
    sock.bind(address)
    sock.listen(1)


    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)

            # TODO: make a new socket when a client connects, call it 'conn',
            #       at the same time you should be able to get the address of
            #       the client so we can report it below.  Replace the
            #       following line with your code. It is only here to prevent
            #       syntax errors
            conn, addr = ('foo', ('bar', 'baz'))
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    # TODO: receive 16 bytes of data from the client. Store
                    #       the data you receive as 'data'.  Replace the
                    #       following line with your code.  It's only here as
                    #       a placeholder to prevent an error in string
                    #       formatting
                    data = b''
                    print('received "{0}"'.format(data.decode('utf8')))

                    # TODO: Send the data you received back to the client, log
                    # the fact using the print statement here.  It will help in
                    # debugging problems.
                    print('sent "{0}"'.format(data.decode('utf8')))

                    # TODO: Check here to see whether you have received the end
                    # of the message. If you have, then break from the `while True`
                    # loop.
                    #
                    # Figuring out whether or not you have received the end of the
                    # message is a trick we learned in the lesson: if you don't
                    # remember then ask your classmates or instructor for a clue.
                    # :)
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                # TODO: When the inner loop exits, this 'finally' clause will
                #       be hit. Use that opportunity to close the socket you
                #       created above when a client connected.
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except KeyboardInterrupt:
        # Use the python KeyboardInterrupt exception as a signal to
        # close the server socket and exit from the server function.
        # ctrl-C

        sock.close()
        print('quitting echo server', file=log_buffer)


if __name__ == '__main__':
    server()
    sys.exit(0)
