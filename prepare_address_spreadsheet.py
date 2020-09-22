from mongo.mongo_provider import MongoProvider
import csv


author_collection = MongoProvider().get_authors_collection()
jpl_address_check = [
    "jet prop lab",
    "4800 oak grove dr",
    "jpl",
    "nasa jet prop lab",
    "jet prop laboratory",
    "jet propulsion lab",
    "jet prop labs",
    "nasa jpl",
    "jet propusl laborotory"
]

def is_jpl_address(address):
    address_split = [s.strip().lower() for s in address.split(",")]

    for address_part in address_split:
        if address_part in jpl_address_check:
            return True

    return False

if __name__ == "__main__":
    output = "data/authors/addresses.csv"

    caltech_addresses = set()
    for doc in author_collection.find():
        affiliations = doc.get("affiliations")
        if "Caltech" in affiliations:
            addresses = doc.get("addresses")
            for address in addresses:
                if not is_jpl_address(address):
                    caltech_addresses.add(address)
    
    with open(output, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["address"])
        for address in caltech_addresses:
            writer.writerow([address])
