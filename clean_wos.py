import re
import sys
import text_cleaner


from pprint import pprint
from mongo.mongo_provider import MongoProvider


mongo_provider = MongoProvider()
author_address_regex = r";\s*(?![^[]*])"
bracket_regex = r"\[(.*?)\]"
publications_collection = mongo_provider.get_publications_collection()
wos_collection = mongo_provider.get_wos_collection()


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


def clean_entries():
    for idx, doc in enumerate(wos_collection.find(no_cursor_timeout=True)):
        if idx % 1000 == 0:
            print(f"STATUS: {idx}")
        
        if publications_collection.count_documents({"_id": _id}) == 0:
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

            # Clean text
            raw_text = title + " " + abstract
            cleaned_text = text_cleaner.clean_text(raw_text)
            tokens = text_cleaner.tokenize_text(cleaned_text)

            cleaned_entry["tokens"] = tokens

            publications_collection.insert_one(cleaned_entry)

    print(f"STATUS: {idx}")


if __name__ == "__main__":
    publications_collection.drop()
    clean_entries()
