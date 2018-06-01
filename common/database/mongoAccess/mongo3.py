#!/usr/bin/env python3
import pymongo as _pm


class DB:
    """Class handling with MongoDB database"""

    def __init__(self, user=None, pswd=None, host=None, port=None, base=None):
        """Initialize class DB with given options:
        user - MongoDB user authorization (default: lucky_pomerange)
        pswd - MongoDB password authorization (default: pass)
        host - host on whith database exists
        port - port number (default: 27017)
        base - MongoDB database name (default: myDatabase)
        """
        # self._user = user if user else "admin"
        # self._pswd = pswd if pswd else "admin"
        self._host = host if host else "localhost"
        self._port = port
        self._base = base if base else "admin"
        # self._collection_name = collection if collection else "testCollection"

        self.client = _pm.MongoClient(
            "mongodb://" + self._host + "/" + self._base,
            port=self._port,
            serverSelectionTimeoutMS=1000,
        )
        self.client.server_info()
        self.db = self.client[self._base]

    def select(self, collName):
        """Method return all collection elements"""
        col = self.db[collName]
        return "\n".join([str(i) for i in col.find()])

    def find(self, filtr, collName):
        """Method finds elements in base
        filtr - array-lik {'k':v}"""
        col = self.db[collName]
        return col.find(filtr)

    def insert(self, item, collName):
        """Insert element inside collection
        item - array-like {'k1':v1,'k2':v2,...}"""
        col = self.db[collName]
        col.insert(item)

    def update(self, filtr, item, collName):
        """Update element in collection.
        filtr is given as dict {"key":val}
        item is array {"k1":v1, "k2":v2,...}
        """
        col = self.db[collName]
        if col.find_one(filtr):
            col.update_one(filtr, {"$set": item})
        else:
            col.insert(item)

    def remove(self, filtr, collName):
        """Remove element defined by filtr {'k':v}"""
        col = self.db[collName]
        col.delete_one(filtr)

    def remove_many(self, filtr, collName):
        """Remove all elements defined by filtr {'k':v}"""
        col = self.db[collName]
        col.delete_many(filtr)

    def removeCollection(self, collName):
        """Delete all collection"""
        col = self.db[collName]
        col.drop()

    def __str__(self, collName):
        """Return String containing information about user, host, port, base, 
        collection, and database elements"""
        col = self.db[collName]
        out = "User: " + self._user + "\n"
        out += "Host: " + self._host + "\n"
        out += "Port: " + str(self._port) + "\n"
        out += "Base: " + self._base + "\n"
        out += "Collection: " + col.name + "\n"
        out += "Data in collections:\n    "
        out += "\n    ".join([str(i) for i in col.find()])
        return out


if __name__ == "__main__":
    db = DB()
    print(db)
