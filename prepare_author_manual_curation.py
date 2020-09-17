from mongo.mongo_provider import MongoProvider
import csv

author_collection = MongoProvider().get_authors_collection()
publication_collection = MongoProvider().get_publications_collection()


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


def get_entries_from_ids(entries, ids):
    return [entry for entry in entries if entry.get("_id") in ids]

if __name__ == "__main__":
    output = "data/authors/authors_raw.csv"
    headers = [
        "_id",
        "name",
        "affiliations",
        "title",
        "addresses"
    ]

    author_entries = []
    for doc in author_collection.find():
        publications= doc.get("publications")
        publication_sample = publications[0]
        pub_doc = publication_collection.find_one({"_id": publication_sample})
        title = pub_doc.get("title")

        entry = {
            "_id": doc.get("_id"),
            "name": doc.get("name"),
            "affiliations": doc.get("affiliations"),
            "title": pub_doc.get("title"),
            "addresses": doc.get("addresses")
        }

        author_entries.append(entry)
    
    last_name_to_ids = get_last_name_to_ids(author_entries)

    with open(output, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(headers)

        for last_name, ids in last_name_to_ids.items():
            if len(ids) > 1:
                for entry in get_entries_from_ids(author_entries, ids):
                    row = [entry[header] for header in headers]
                    writer.writerow(row)