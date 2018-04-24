from mongoAccess import mongo3
import datetime

def app(environ, start_response):
    status = '200 OK'
    db = mongo3.DB('', '', '172.17.0.2', 27017, "test", "myCollection")
    currentTime = datetime.datetime.now()
    db.insert(
            {
                "time": currentTime
            })
    outputStr = str(currentTime)
    output = bytes(outputStr, 'utf-8')


    responseHeaders = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]

    start_response(status, responseHeaders)

    return [output]
