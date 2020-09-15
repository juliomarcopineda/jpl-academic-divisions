from mongo.mongo_provider import MongoProvider
import csv
import sys
import uuid


def get_author_key_exact(author_name_dict, name_check):
    for author_key, name in author_name_dict.items():
        if name_check == name:
            return author_key


if __name__ == "__main__":
    mongo_provider = MongoProvider()
    collection = mongo_provider.get_publications_collection()
    
    unique_authors = set()
    for doc in collection.find():
        document_id = doc["_id"]
        author_entries = doc["authors"]
        for author_entry in author_entries:
            name = author_entry["name"]
            unique_authors.add(name)

    author_list = [author for author in unique_authors]
    print(len(author_list))
    sys.exit()
    author_list.sort()
    for author in author_list:
        print(author)

    sys.exit()

    author_name_dict = {}
    author_docs_dict = {}
    author_addresses_dict = {}

    for doc in collection.find():
        document_id = doc["_id"]
        author_entries = doc["authors"]
        for author_entry in author_entries:
            name = author_entry["name"]
            addresses = author_entry["addresses"]

            author_key = get_author_key_exact(author_name_dict, name)
            if not author_key:
                author_key = str(uuid.uuid4())
                
                author_name_dict[author_key] = [name]
                author_docs_dict[author_key] = set()
                author_docs_dict[author_key].add(document_id)
                author_addresses_dict[author_key] = set()
                for address in addresses:
                    author_addresses_dict[author_key].add(address)
            else:
                author_docs_dict[author_key].add(document_id)
                author_addresses_dict[author_key].add(address)
    
    author_name_list = [name for name in author_name_dict.keys()]
    author_name_list.sort()

    for name in author_name_list:
        print(name)
    sys.exit()

    for i in range(len(author_name_list)):
        name1 = author_name_list[i]
        for j in range(i + 1, len(author_name_list)):
            name2 = author_name_list[j]


