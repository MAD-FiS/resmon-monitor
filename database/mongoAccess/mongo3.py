#!/usr/bin/env python3
import pymongo as _pm


class DB:
    '''Class handling with MongoDB database'''
    def __init__(self, user=None, pswd=None, host=None, port=None, base=None, collection=None):
        '''Initialize class DB with given options:
        user - MongoDB user authorization (default: przemyslaw)
        pswd - MongoDB password authorization (default: pass)
        host - host on whith database exists
        port - port number (default: 27017)
        base - MongoDB database name (default: przemyslaw)
        collection - collection name (default: student)
        '''
        #self._user = user if user else "admin"
        #self._pswd = pswd if pswd else "admin"
        self._host = host if host else "localhost"
        self._port = port
        self._base = base if base else "admin"
        self._collection_name = collection if collection else "testCollection"

        #self.client = _pm.MongoClient('mongodb://'+self._user+':'+self._pswd+'@'+self._host+'/'+self._base, port=self._port, serverSelectionTimeoutMS=1000)
        self.client = _pm.MongoClient('mongodb://'+self._host+'/'+self._base, port=self._port, serverSelectionTimeoutMS=1000)
        self.client.server_info()
        self.db = self.client[self._base]
        self.col = self.db[self._collection_name]

    def select(self):
        '''Method return all database elements'''
        return '\n'.join([str(i) for i in self.col.find()])

    def find(self,filtr):
        '''Method finds element in base
        filtr - array-lik {'k':v}'''
        return '\n'.join([str(i) for i in self.col.find_one(filtr)])

    def insert(self, item):
        '''Insert element inside collection
        item - array-like {'k1':v1,'k2':v2,...}'''
        self.col.insert(item)

    def update(self, filtr, item):
        '''Update element in collection.
        filtr is given as dict {"key":val}
        item is array {"k1":v1, "k2":v2,...}
        '''
        if self.col.find_one(filtr):
            self.col.update_one(filtr,{"$set":item})
        else:
            self.col.insert(item)

    def remove(self,filtr):
        '''Remove element defined by filtr {'k':v}'''
        self.col.delete_one(filtr)

    def remove_many(self,filtr):
        '''Remove all elements defined by filtr {'k':v}'''
        self.col.delete_many(filtr)

    def removeCollection(self):
        '''Delete all collection'''
        self.col.drop()

    def __str__(self):
        '''Return String containing information about user, host, port, base, collection, and database elements'''
        out = "User: "+self._user+"\n"
        out += "Host: "+self._host+"\n"
        out += "Port: "+str(self._port)+"\n"
        out += "Base: "+self._base+"\n"
        out += "Collection: "+self.col.name+"\n"
        out += "Data in collections:\n    "
        out += "\n    ".join([str(i) for i in self.col.find()])
        return out

if __name__ == '__main__':
    db = DB()
    print(db)
