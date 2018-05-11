from mongoAccess import mongo3
import datetime
import json

def parse_request(environ,db):

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except(ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    content = request_body.decode('utf-8')

    js = json.loads(content)
    if js['TYPE'] == 'META':
        db.insert(js)
    elif js['TYPE'] == 'DATA':
        for value in js['DATA']:
            datetime_object = datetime.datetime.strptime(value['DATE'].split(".")[0], \
                            '%Y-%m-%d %H:%M:%S')
            value['DATE'] = datetime_object
            db.insert(value)

def app(environ, start_response):
    status = '200 OK'
    db = mongo3.DB('', '', '172.17.0.2', 27017, "test", "myCollection")

    parse_request(environ,db)
    response_headers = [('Content-type', 'text/plain')]

    start_response(status, response_headers)

    return["".encode()]
