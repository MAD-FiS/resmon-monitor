import json

jsonString = '{"id" : 5,"names" : ["Rafal", "tomek"]}'
myJson = json.loads(jsonString)
print(myJson)
