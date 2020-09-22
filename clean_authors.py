from mongo.mongo_provider import MongoProvider

raw_authors_collection = MongoProvider().get_authors_collection()
clean_authors_collection = MongoProvider().get_clean_authors_collection()


def get_last_name_to_ids(entries):
    last_name_to_ids = {}
    for entry in entries:
        _id = entry["_id"]
        full_name = entry["name"]
        last_name = full_name.split(",")[0]

        ids = last_name_to_ids.get(last_name, [])
        ids.append(_id)
        last_name_to_ids[last_name] = ids
    
    return last_name_to_ids


def get_full_name_to_ids(author_ids):
    pass


def get_deduplicated_authors():
    data = []

    raw_author_docs = [doc for doc in raw_authors_collection.find()]
    last_name_to_ids = get_last_name_to_ids(raw_author_docs)

    for last_name, author_ids in last_name_to_ids.items():


    return data


if __name__ == "__main__":
    clean_authors_collection.drop()

    deduped_entries = get_deduplicated_authors()