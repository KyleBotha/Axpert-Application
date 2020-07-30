import pymongo
import pprint


class ConnectDB:
    def __init__(self, db_url, db_name):
        self.db_url = db_url
        self.db_name = db_name
        self.connect_db(db_url, db_name)

    def connect_db(self, db_url, db_name):
        try:
            self.client = pymongo.MongoClient(db_url)
            self.axpertDB = self.client[db_name]
            self.qpigs_collection = self.axpertDB["QPIGS"]
            self.isConnected = True
            print("Connection established to MongoDB database")
        except:
            self.isConnected = False
            print("Failed to connect to MongoDB database.")

    def insert_one(self, doc, col):
        if(col == "QPIGS"):
            try:
                self.qpigs_collection.insert_one(doc)
                print("Document Inserted.")

            except:
                print("Insert one failed.")

            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(doc)

        else:
            print("Invalid collection specified")
