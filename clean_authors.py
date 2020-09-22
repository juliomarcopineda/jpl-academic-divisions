from mongo.mongo_provider import MongoProvider
import re
from itertools import zip_longest


raw_authors_collection = MongoProvider().get_authors_collection()
clean_authors_collection = MongoProvider().get_clean_authors_collection()


def get_last_name_to_docs(entries):
    last_name_to_ids = {}
    for entry in entries:
        full_name = entry["name"]
        last_name = full_name.split(",")[0]

        author_docs = last_name_to_ids.get(last_name, [])
        author_docs.append(entry)
        last_name_to_ids[last_name] = author_docs
    
    return last_name_to_ids


def is_part_of_group(name, group):
    return all([is_same_name(name, name_check) for name_check in group])


def get_deduplicated_authors():
    data = []

    raw_author_docs = [doc for doc in raw_authors_collection.find()]
    last_name_to_docs = get_last_name_to_docs(raw_author_docs)

    for last_name, author_docs in last_name_to_docs.items():
        full_name_to_doc = {doc["name"]: doc for doc in author_docs}
        groups = []
        for full_name in full_name_to_doc.keys():
            if not groups:
                groups.append([full_name])
            else:
                group_belonging = [
                    is_part_of_group(full_name, group)
                    for group in groups
                ]

                if sum(group_belonging) == 1:
                    pass

                
    return data


def name_splitter(name):
    return re.split("\\s+", re.sub("[,.]", "", name.lower().strip()))


def is_same_name_token(name_token_1, name_token_2):
    if name_token_1 is None or name_token_2 is None:
        return False
    
    return all([c1 == c2 for c1, c2 in zip_longest(name_token_1, name_token_2)])


def is_same_name(name1, name2):
    pass

if __name__ == "__main__":
    # clean_authors_collection.drop()
    # deduped_entries = get_deduplicated_authors()

    name1 = "Pineda, Julio Marco"
    name2 = "Pineda, Julio M."

    name3 = "Yuan, J."
    name4 = "Yuan, John"

    name_group1 = ["Pineda, Julio M.", "Pineda, Julio Marco"]
    name_group2 = ["Pineda, Juan"]
    
    name_tokens_1 = name_splitter(name1)
    name_tokens_2 = name_splitter(name3)

    print(all([is_same_forename(n1, n2) for n1, n2 in zip_longest(name_tokens_1, name_tokens_2)]))