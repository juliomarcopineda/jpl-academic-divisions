from mongo.mongo_provider import MongoProvider
import vector_utils

divisions_collection = MongoProvider().get_divisions_collecdtion()
publications_collection = MongoProvider().get_publications_collection()
clean_authors_collection = MongoProvider().get_clean_authors_collection()


def compute_average_vector(publications):
    docs = publications_collection.find({"_id": {"$in": publications}}, {"tfidf_vector": 1})
    vectors = [doc["tfidf_vector"] for doc in docs]

    average_vector = vector_utils.get_average_vector(vectors)
    normalized_vector = vector_utils.normalize_vector(average_vector)
    sorted_normalized_vector = vector_utils.sort_vector(normalized_vector)

    return sorted_normalized_vector


def calculate_division_vectors():
    for doc in divisions_collection.find():
        division = doc["_id"]
        print(division)

        publications = doc["publications"]   
        vector = compute_average_vector(publications)

        filter_doc = {
            "_id": division
        }

        update_doc = {
            "$set": {
                "tfidf_vector": vector
            }
        }
        
        divisions_collection.update_one(filter=filter_doc, update=update_doc)


def calculate_author_vectors():
    for idx, doc in enumerate(clean_authors_collection.find()):
        if idx % 500 == 0:
            print(f"STATUS: {idx}")
        author_id = doc["_id"]

        publications = doc["publications"]   
        vector = compute_average_vector(publications)

        filter_doc = {
            "_id": author_id
        }

        update_doc = {
            "$set": {
                "tfidf_vector": vector
            }
        }

        clean_authors_collection.update_one(filter=filter_doc, update=update_doc)

    print(f"STATUS: {idx}")



if __name__ == "__main__":
    print("Calculating average vectors for divisions")
    calculate_division_vectors()
    print("Calculating average vectors for JPL authors")
    calculate_author_vectors()
    print("Done.")