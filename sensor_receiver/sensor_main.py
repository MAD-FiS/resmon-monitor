from mongoAccess import mongo3
import datetime
import json

def parse_request(environ):

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except(ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    content = request_body.decode('utf-8')

    return json.loads(content)

def app(environ, start_response):
    status = '200 OK'
    db = mongo3.DB('', '', '172.17.0.2', 27017, "test", "myCollection")

    db.insert(parse_request(environ))
    response_headers = [('Content-type', 'text/plain')]

    start_response(status, response_headers)

    return["".encode()]
