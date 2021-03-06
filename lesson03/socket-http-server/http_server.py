#!/usr/bin/env python3
'''
Socket based http_server for Python 230 UW PCE
'''
# pylint: disable = R1702, W0702, W0612
import socket
import sys
import traceback
import os
import mimetypes
import subprocess

def response_ok(body=b'This is a minimal response', mimetype=b'text/plain'):
    '''
    returns a basic HTTP response
    Ex:
        response_ok(
            b'<html><h1>Welcome:</h1></html>',
            b'text/html'
        ) ->
    '''
    b'''
        HTTP/1.1 200 OK\r\n
        Content-Type: text/html\r\n
        \r\n
        <html><h1>Welcome:</h1></html>\r\n
    '''

    return b'\r\n'.join([
        b'HTTP/1.1 200 OK',
        b'Content-Type: ' + mimetype,
        b'',
        body
    ])


def response_method_not_allowed():
    '''Returns a 405 Method Not Allowed response'''

    return b'\r\n'.join([
        b'HTTP/1.1 405 Method Not Allowed',
        b'',
        b'Whatever you are trying is not allowed.'
        ])


def response_not_found():
    '''Returns a 404 Not Found response'''

    return b'\r\n'.join([
        b'HTTP/1.1 404 Not Found',
        b'',
        b'You done looked for something not here.'
    ])


def parse_request(request):
    '''
    Given the content of an HTTP request, returns the path of that request.

    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    '''

    method, path, version = request.split('\r\n')[0].split(' ')

    if method != 'GET':
        raise NotImplementedError

    return path


def response_path(path):
    '''
    This method should return appropriate content and a mime type.

    If the requested path is a directory, then the content should be a
    plain-text listing of the contents with mimetype `text/plain`.

    If the path is a file, it should return the contents of that file
    and its correct mimetype.

    If the path does not map to a real location, it should raise an
    exception that the server can catch to return a 404 response.

    Ex:
        response_path('/a_web_page.html') -> (b'<html><h1>North Carolina...',
                                            b'text/html')

        response_path('/images/sample_1.png')
                        -> (b'A12BCF...',  # contents of sample_1.png
                            b'image/png')

        response_path('/') -> (b'images/, a_web_page.html, make_type.py,...',
                             b'text/plain')

        response_path('/a_page_that_doesnt_exist.html') -> Raises a NameError

    '''

    home_dir = os.path.abspath('webroot')

    location = os.path.join(home_dir, path[1:])

    try:
        if path.endswith('.py'):
            results = subprocess.run(['python', location], capture_output=True)
            content = results.stdout
            mimetype = b'text/html'

        if os.path.isdir(location):
            listing = [item for item in os.listdir(location)]
            content = '\r\n'.join(listing).encode('utf-8')
            mimetype = b'text/plain'

        else:
            with open(location, 'rb') as file:
                content = file.read()
            file_type = mimetypes.guess_type(path)[0]
            mimetype = file_type.encode('utf-8')

    except FileNotFoundError:
        raise NameError

    return content, mimetype


def server(log_buffer=sys.stderr):
    '''
    This is the server code itself.
    '''
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Instancing a server on {0}:{1}'.format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('Waiting for connection', file=log_buffer)
            conn, addr = sock.accept()

            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                request = ''

                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break


                print('Connection request received:\n{}\n\n'.format(request))

                try:
                    path = parse_request(request)
                    content, mimetype = response_path(path)
                    response = response_ok(body=content, mimetype=mimetype)

                except NotImplementedError:
                    response = response_method_not_allowed()

                except NameError:
                    response = response_not_found()

                conn.sendall(response)

            except KeyboardInterrupt:
                raise KeyboardInterrupt

            except:
                traceback.print_exc()

            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return
    except:
        traceback.print_exc()


if __name__ == '__main__':
    server()
    sys.exit(0)
