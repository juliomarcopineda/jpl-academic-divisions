from mongo.mongo_provider import MongoProvider
import re
from itertools import zip_longest
import uuid
import csv


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


def determine_display_name(raw_names):
    display_name = ""
    for name in raw_names:
        if len(name) > len(display_name):
            display_name = name

    return display_name


def merge_docs(dup_docs):
    _id = uuid.uuid4()
    raw_names = []
    affiliations_merge = set()
    addresses_merge = set()
    publications_merge = set()
    for doc in dup_docs:
        name = doc["name"]
        affiliations = doc["affiliations"]
        addresses = doc["addresses"]
        publications = doc["publications"]

        raw_names.append(name)
        affiliations_merge.update(affiliations)
        addresses_merge.update(addresses)
        publications_merge.update(publications)
    
    display_name = determine_display_name(raw_names)

    return {
        "_id": _id,
        "name": display_name,
        "raw_names": raw_names,
        "affiliations": [a for a in affiliations_merge],
        "addresses": [address for address in addresses_merge],
        "publications": [pub for pub in publications_merge]
    }
        

def get_deduplicated_authors():
    data = []

    raw_author_docs = [doc for doc in raw_authors_collection.find({"affiliations": {"$in": "JPL"}})]
    last_name_to_docs = get_last_name_to_docs(raw_author_docs)

    for last_name, author_docs in last_name_to_docs.items():
        full_name_to_doc = {doc["name"]: doc for doc in author_docs}
        full_names = full_name_to_doc.keys()
        groups = get_name_groups(full_names)
        for group in groups:
            dup_docs = [full_name_to_doc[full_name] for full_name in group]
            dedup_doc = merge_docs(dup_docs)
            data.append(dedup_doc)

    return data


def name_splitter(name):
    results = []
    split = re.split("\\s+-*", re.sub("[,.]", "", name.lower().strip()))
    for n in split:
        if "-" in n:
            results.extend(n.split("-"))
        else:
            results.append(n)

    return results

def is_same_name_token(name_tokens_1, name_tokens_2):
    if name_tokens_1 is None or name_tokens_2 is None:
        return False

    return all([c1[0] == c2[0] for c1, c2 in zip(name_tokens_1, name_tokens_2)])


def is_same_name(name1, name2):
    name_tokens_1 = get_forenames(name1)
    name_tokens_2 = get_forenames(name2)

    if len(name_tokens_1) == 1 and len(name_tokens_2) == 1:
        return name_tokens_1[0] == name_tokens_2[0]
    elif len(name_tokens_1) == 1 or len(name_tokens_2) == 1:
        return False
    
    return is_same_name_token(name_tokens_1, name_tokens_2)


def is_part_of_group(name, group):
    return all([is_same_name(name, name_check) for name_check in group])


def get_forenames(fullname):
    fullname_split = fullname.split(",")
    return name_splitter(" ".join(fullname_split[1:]))


def get_name_groups(full_names):
    groups = []
    for full_name in full_names:
        if not groups:
            groups.append([full_name])
        else:
            group_belonging = [
                idx
                for idx, group in enumerate(groups)
                if is_part_of_group(full_name, group)
            ]
            if len(group_belonging) == 1:
                groups[group_belonging[0]].append(full_name)
            else:
                groups.append([full_name])

    return groups


def print_group_results(names):
    print(names)
    for idx, group in enumerate(get_name_groups(names)):
        print(f"Group {idx}: {group}")
    

def _test():
    names_1 = [
        "Bates, Christopher M.",
        "Bates, K. H.",
        "Bates, Kelvin H."
    ]
    names_2 = [
        "Benner, L.",
        "Benner, L. A.",
        "Benner, L. A. M.",
        "Benner, Lance",
        "Benner, Lance A. M.",
        "Benner, Lance. A. M.",
    ]
    names_3 = [
        "Bern, James",
        "Bern, Zvi"
    ]
    names_4 = [
        "Huang, C. -K.",
        "Huang, Calvin",
        "Huang, Chen-Kuo",
        "Huang, Chi-Chien Nelson",
        "Huang, De",
        "Huang, H. -H.",
        "Huang, Hsin-Hua",
        "Huang, Huiqian",
        "Huang, Jing-Shun",
        "Huang, Jining",
        "Huang, Justin",
        "Huang, Lei",
        "Huang, M.",
        "Huang, Mong-Han",
    ]
    names_5 = [
        "Castillo-Rogez, J.",
        "Castillo-Rogez, J. C.",
        "Castillo-Rogez, Julie",
        "Castillo-Rogez, Julie C."
    ]
    names_6 = [
        "Chary, R-R.",
        "Chary, R.",
        "Chary, R. -R.",
        "Chary, R. R.",
        "Chary, Ranga",
        "Chary, Ranga Ram",
        "Chary, Ranga-Ram"
    ]
    print_group_results(names_1)
    print()
    print_group_results(names_2)
    print()
    print_group_results(names_3)
    print()
    print_group_results(names_4)
    print()
    print_group_results(names_5)
    print()
    print_group_results(names_6)


if __name__ == "__main__":
    clean_authors_collection.drop()
    deduped_entries = get_deduplicated_authors()

    output = "data/authors/authors_dedup.csv"

    with open(output, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        headers = deduped_entries[0].keys()
        writer.writerow(headers)
        for entry in deduped_entries:
            row = [entry[header] for header in headers]
            writer.writerow(row)
