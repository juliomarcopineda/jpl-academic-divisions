from pymongo import MongoClient

class MongoProvider:
    def __init__(self):
        client = MongoClient()
        self.db = client.wos
    
    def get_caltech_wos_collection(self):
        return self.db.caltech_wos
    
    def get_jpl_wos_collection(self):
        return self.db.jpl_wos

    def get_publications_collection(self):
        return self.db.publications