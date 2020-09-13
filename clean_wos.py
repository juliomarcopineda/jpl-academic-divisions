from mongo.mongo_provider import MongoClient

wos_fields = [
    "Author Full Name",
    "Document Title",
    "Document Type",
    "Abstract",
    "Author Address",
]

if __name__ == "__main__":
    mongo_provider = MongoClient()
    caltech_wos = mongo_provider.get_caltech_wos_collection()

    for doc in caltech_wos.find():
        entry = {
            header: doc.get(header)
            for header in headers
        }