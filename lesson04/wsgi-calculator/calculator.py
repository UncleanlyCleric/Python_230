#!/usr/bin/#!/usr/bin/env python3
'''
Python 230 Lesson 04, WSGI Calculator
'''
#pylint: disable=W0703
from functools import reduce
import operator
import traceback

def index():
    '''
    Instructions for using the calculator.
    '''
    body = '''
    You can use this website to add, subtract, multiply, or divide numbers.<br>
    Change the url to specify the function and numbers that you want to use.<br>
    You can enter two or more numbers.<br><br>
    Here are some examples:<br>
<table class="table table-hover">
  <thead>
    <tr class="table-dark">
      <th scope="col">Function</th>
      <th scope="col">Numbers</th>
      <th scope="col">URL</th>
    </tr>
  </thead>
  <tbody>
    <tr class="table-primary">
      <th scope="row">Add</th>
      <td>200 + 50</td>
      <td><a href=http://localhost:8080/add/200/50>http://localhost:8080/add/200/50</a></td>
    </tr>
    <tr class="table-secondary">
      <th scope="row">Subtract</th>
      <td>10 - 8 - 1</td>
      <td><a href=http://localhost:8080/subtract/10/8/1>http://localhost:8080/subtract/10/8/1</a></td>
    </tr>
    <tr class="table-warning">
      <th scope="row">Multiply</th>
      <td>2 * 5 * 3</td>
      <td><a href=http://localhost:8080/multiply/2/5/3>http://localhost:8080/multiply/2/5/3</a></td>
    </tr>
    <tr class="table-info">
      <th scope="row">Divide</th>
      <td>400 / 4</td>
      <td><a href=http://localhost:8080/divide/400/4>http://localhost:8080/divide/400/4</a></td>
    </tr>
  </tbody>
</table>
'''
    return body

def add(*args):
    '''
    Returns a STRING with the sum of the arguments
    '''
    nums = map(int, args)
    total = reduce(operator.add, nums)

    return str(total)


def subtract(*args):
    '''
    Returns a STRING with the difference of the arguments
    '''
    nums = map(int, args)
    total = reduce(operator.sub, nums)

    return str(total)


def multiply(*args):
    '''
    Returns a STRING with the product of the arguments
    '''
    nums = map(int, args)
    total = reduce(operator.mul, nums)

    return str(total)


def divide(*args):
    '''
    Returns a string with the quotient of the arguments
    '''
    nums = map(int, args)

    try:
        total = reduce(operator.truediv, nums)

    except ZeroDivisionError:
        raise ZeroDivisionError

    return str(total)


def resolve_path(path):
    '''
    Should return two values: a callable and an iterable of
    arguments.
    '''

    funcs = {
        "": index,
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide
    }

    path = path.strip("/").split("/")

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]

        if func != index and len(args) <= 1:
            raise ValueError

    except KeyError:
        raise NameError

    return func, args


def card_template():
    '''
    Template for formatting a card.
    '''
    template = '''
    <div class="card">
        <div class="card-header" style="background-color:{}">
            {}
        </div>
        <div class="card-body">
            <h5 class="card-title">{}</h5><br>
            <a href="http://localhost:8080/" class="btn btn-secondary">Return home</a>
        </div>
    </div>
    '''

    return template


def body_template():
    '''
    Template for the website body
    '''
    template = '''
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <title>Web Calculator</title>
  </head>
  <body>
    <div class="container-fluid">
    <h1>Web Calculator, PCE Python 230</h1>
    {}
    </div>
  </body>
</html>
'''
    return template


def application(environ, start_response):
    '''
    This is defining the overall application.  Here we have exception handling,
    and calls for templates.
    '''
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get("PATH_INFO", None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)

        body = func(*args)

        status = "200 OK"

        if func == index:
            body = func(*args)
        else:
            body = card_template().format("#d4edda", "Success", "The answer is: {}"\
            .format(func(*args)))

    except NameError:
        status = "404 Not Found"
        body = card_template().format("#f8d7da", "Error", "Operation not defined")

    except ZeroDivisionError:
        status = "400 Bad Request"
        body = card_template().format("#f8d7da", "Error", "Can't divide by zero")

    except ValueError:
        status = "400 Bad Request"
        body = card_template().format("#f8d7da", "Error", "Please enter two or more numbers")

    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())

    finally:
        final_body = body_template().format(body)
        headers.append(("Content-length", str(len(final_body))))
        start_response(status, headers)

        return [final_body.encode("utf8")]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    SRV = make_server("localhost", 8080, application)
    SRV.serve_forever()
