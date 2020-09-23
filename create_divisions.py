from mongo.mongo_provider import MongoProvider
import csv
import vector_utils

raw_author_collection = MongoProvider().get_authors_collection()
division_collection = MongoProvider().get_divisions_collecdtion()
publications_collection = MongoProvider().get_publications_collection()

address_to_division = {}

def get_divisions(addresses):
    divisions = set()
    for address in addresses:
        divisions_string = address_to_division.get(address, "")
        if divisions_string:
            divs = [div.strip() for div in divisions_string.split(",")]

            for div in divs:
                divisions.add(div)
    
    return divisions


def populate_address_to_division(path):
    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            address_to_division[row[0]] = row[1]


if __name__ == "__main__":
    print("Creating division entries")
    
    address_div_path = "data/divisions/addresses_to_divs.csv"
    populate_address_to_division(address_div_path)

    division_collection.drop()

    division_data = {}
    for doc in publications_collection.find():
        pub_id = doc["_id"]
        addresses = []
        authors = doc["authors"]
        for author_entry in authors:
            author_addresses = author_entry["addresses"]
            addresses.extend(author_addresses)
    
        divisions = get_divisions(addresses)

        for division in divisions:
            entry = division_data.get(division, {})
            if not entry:
                entry["_id"] = division
                entry["publications"] = [pub_id]
            else:
                entry["publications"].append(pub_id)
            
            division_data[division] = entry
    
    for entry in division_data.values():
        division_collection.insert_one(entry)

    print("Done.")