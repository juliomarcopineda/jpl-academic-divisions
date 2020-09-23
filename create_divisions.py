from mongo.mongo_provider import MongoProvider
import csv

raw_author_collection = MongoProvider().get_authors_collection()
division_collection = MongoProvider().get_divisions_collecdtion()

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
    address_div_path = "data/divisions/addresses_to_divs.csv"
    populate_address_to_division(address_div_path)

    division_collection.drop()

    division_data = {}

    for doc in raw_author_collection.find({"affiliations": "Caltech"}):
        addresses = doc["addresses"]
        publications = doc["publications"]

        divisions = get_divisions(addresses)
        for division in divisions:
            entry = division_data.get(division, {})
            if not entry:
                entry["_id"] = division
                entry["publications"] = publications
            else:
                entry["publications"].extend(publications)
            
            division_data[division] = entry
    
    for division, entry in division_data.items():
        print(division)
        print(entry["publications"][0:10])