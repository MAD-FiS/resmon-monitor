from mongoAccess import mongo3
import datetime
import json
import dateutil.parser


class ValidationError:
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return '' + error + '. '


class MetaValidator:
    MANDATORY_FIELDS = ["session_id", "hostname",
                        "metrics", "session_start_date"]

    def __init__(self, metaRecord):
        self.metaRecord = metaRecord

    def hasMandatoryFields(self):
        validationErrors = list()

        for field in self.MANDATORY_FIELDS:
            error = self.hasMandatoryField(field)
            if error:
                validationErrors.append(error)

        return validationErrors

    def hasMandatoryField(self, fieldName):
        if fieldName not in self.metaRecord:
            return ValidationError(
                "Metadata does not contain mandatory: " + fieldName)

    def getValidationErrors(self):
        return self.hasMandatoryFields()


def parse_request(environ, db):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except(ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    content = request_body.decode('utf-8')

    js = json.loads(content)

    if js['type'] == 'meta':
        record = {}
        for entry in js['data']:
            record.update(entry) 
        validationErrors = MetaValidator(record).getValidationErrors()
        print(validationErrors)
        if validationErrors:
            feedback = '\n'.join([str(error) for error in validationErrors])
            print(feedback)
            return feedback
        else:
            db.insert(record, "metaCollection")

    elif js['type'] == 'data':
        for value in js['data']:
            datetime_object = datetime.datetime.strptime(
                value['date'].split(".")[0], '%Y-%m-%d %H:%M:%S')
            value['date'] = datetime_object
            db.insert(value, "dataCollection")

    return ''


def app(environ, start_response):
    status = '200 OK'
    response = dict()

    db = mongo3.DB('', '', '172.17.0.2', 27017, "monitorDatabase")

    feedback = parse_request(environ, db)
    if feedback != '':
        status = '400 Bad Request'
        response["Details"] = feedback

    response_headers = [('Content-type', 'text/plain')]

    start_response(status, response_headers)

    return[json.dumps(response).encode()]
