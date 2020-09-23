from pymongo import MongoClient

class MongoProvider:
    def __init__(self):
        client = MongoClient()
        self.db = client.wos
    
    def get_wos_collection(self):
        return self.db.wos

    def get_publications_collection(self):
        return self.db.publications

    def get_authors_collection(self):
        return self.db.authors
    
    def get_clean_authors_collection(self):
        return self.db.clean_authors

    def get_divisions_collecdtion(self):
        return self.db.divisions
