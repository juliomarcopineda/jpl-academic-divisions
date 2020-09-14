import re
import sys

from pprint import pprint
from mongo.mongo_provider import MongoProvider


mongo_provider = MongoProvider()
author_address_regex = r";\s*(?![^[]*])"
bracket_regex = r"\[(.*?)\]"
publications_collection = mongo_provider.get_publications_collection()


def get_collection_by_organization(organization):
    if organization == "Caltech":
        return mongo_provider.get_caltech_wos_collection()
    else:
        return mongo_provider.get_jpl_wos_collection()


def parse_author_address_stirng(author_address_string):
    author_addresses = [
        author_address
        for author_address in re.split(author_address_regex, author_address_string)
    ]

    author_to_addresses = {}
    for author_address in author_addresses:
        match = re.search(bracket_regex, author_address)

        if not match:
            continue

        address = author_address[match.span()[1]:].strip()

        author_list_string = match.group(1)
        authors = [author.strip() for author in author_list_string.split(";")]
        for author in authors:
            if author in author_to_addresses:
                author_to_addresses[author].add(address)
            else:
                author_to_addresses[author] = set()
                author_to_addresses[author].add(address)
    
    return author_to_addresses


def clean_entries(organization):
    wos_collection = get_collection_by_organization(organization)
    
    for idx, doc in enumerate(wos_collection.find()):
        cleaned_entry = {}

        # Raw data
        _id = doc["_id"]
        author_list_string = doc["Author Full Name"]
        title = doc.get("Document Title")
        doc_type = doc.get("Document Type")
        abstract = doc.get("Abstract")
        author_address_string = doc["Author Address"]

        cleaned_entry["_id"] = _id
        cleaned_entry["title"] = title
        cleaned_entry["abstract"] = abstract
        cleaned_entry["documentType"] = doc_type
        cleaned_entry["organization"] = organization

        # Parse the author list
        authors = [author.strip() for author in author_list_string.split(";")]

        # Get author to addresses dict
        author_to_addresses = parse_author_address_stirng(author_address_string)

        author_entries = []
        for author in authors:
            author_entry = {}
            address_set = author_to_addresses.get(author, "")

            author_entry["name"] = author
            author_entry["addresses"] = [address for address in address_set]
            author_entries.append(author_entry)

        cleaned_entry["authors"] = author_entries

        publications_collection.insert_one(cleaned_entry)


if __name__ == "__main__":
    publications_collection.drop()

    for organization in ["Caltech", "JPL"]:
        clean_entries(organization)
