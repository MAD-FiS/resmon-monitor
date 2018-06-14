import json

if __name__ == '__main__':
    jsonString = '{"id" : 5,"names" : ["Rafal", "tomek"]}'
    myJson = json.loads(jsonString)
    print(myJson)
