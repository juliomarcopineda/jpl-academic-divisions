from mongo.mongo_provider import MongoProvider
import csv
import sys
import uuid


jpl_address_check = [
    "jet prop lab",
    "4800 oak grove dr",
    "jpl",
    "nasa jet prop lab",
    "jet prop laboratory",
    "jet propulsion lab",
    "jet prop labs",
    "nasa jpl",
    "jet propusl laborotory",
    "dept jet prop lab"
]


visited_names = {}


def is_jpl_address(address):
    address_split = [s.strip().lower() for s in address.split(",")]

    for address_part in address_split:
        if address_part in jpl_address_check:
            return True

    return False


def is_caltech_address(address):
    return "CALTECH" in address and not is_jpl_address(address)


if __name__ == "__main__":
    mongo_provider = MongoProvider()
    publication_collection = mongo_provider.get_publications_collection()
    
    print("Determining author entries")

    author_data_dict = {}
    for idx, doc in enumerate(publication_collection.find()):
        if idx % 1000 == 0:
            print(f"STATUS: {idx}")

        document_id = doc["_id"]
        author_entries = doc["authors"]
        for author_entry in author_entries:
            # Set up data entry for author name
            name = author_entry["name"]
            key = None
            if name in visited_names:
                key = visited_names[name]
            else:
                key = str(uuid.uuid4())
                visited_names[name] = key

            # Get entry
            entry = author_data_dict.get(key, {})
            entry["_id"] = key

            # Determine affiliations
            valid_author = False
            affiliations = set(affiliation for affiliation in entry.get("affiliations", []))

            addresses = author_entry["addresses"]
            valid_addresses = set(a for a in entry.get("addresses", []))
            for address in addresses:
                if is_jpl_address(address):
                    valid_author = True
                    affiliations.add("JPL")
                    valid_addresses.add(address)
                elif is_caltech_address(address):
                    valid_author = True
                    affiliations.add("Caltech")
                    valid_addresses.add(address)
            
            # Don't store data if author is not Caltech or JPL
            if not valid_author:
                continue
            
            entry["affiliations"] = [affiliation for affiliation in affiliations]
            entry["addresses"] = [address for address in valid_addresses]
            entry["name"] = name

            # Add in document id list
            publications = entry.get("publications", [])
            publications.append(document_id)
            entry["publications"] = publications

            author_data_dict[key] = entry
    print(f"STATUS: {idx}")

    print("Inserting to authors publication_collection")
    print(f"Number of entries: {len(author_data_dict)}")
    authors_collection = mongo_provider.get_authors_collection()
    authors_collection.drop()
    for entry in author_data_dict.values():
        authors_collection.insert_one(entry)

    print("Done.")