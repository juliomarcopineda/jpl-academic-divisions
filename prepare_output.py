from mongo.mongo_provider import MongoProvider
import csv
import vector_utils

division_collection = MongoProvider().get_divisions_collection()
clean_authors_collection = MongoProvider().get_clean_authors_collection()
publications_collection = MongoProvider().get_publications_collection()


def write_data(data, path):
    with open(path, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        headers = data[0].keys()
        writer.writerow(headers)
        for entry in data:
            row = [entry[header] for header in headers]
            writer.writerow(row)


def division_top_terms(path, n):
    data = []

    for author_doc in division_collection.find():
        division = author_doc["_id"]
        vector = author_doc["tfidf_vector"]

        for idx, token in enumerate(vector.keys()):
            if idx == n:
                break
                
            weight = vector.get(token)

            entry = {
                "division": division,
                "term": token,
                "weight": weight
            }
            data.append(entry)
    
    write_data(data, path)


def author_top_terms(path, n):
    data = []

    for author_doc in clean_authors_collection.find():
        author_id = author_doc["_id"]
        name = author_doc["name"]
        vector = author_doc["tfidf_vector"]

        for idx, token in enumerate(vector.keys()):
            if idx == n:
                break
                
            weight = vector.get(token)

            entry = {
                "author_id": author_id,
                "name": name,
                "term": token,
                "weight": weight
            }
            data.append(entry)
    
    write_data(data, path)


def write_author_jpl_titles(path):
    data = []

    for author_doc in clean_authors_collection.find():
        author_id = author_doc["_id"]
        name = author_doc["name"]
        publications = author_doc["publications"]

        titles = []
        for pub_doc in publications_collection.find({"_id": {"$in": publications}}):
            title = pub_doc.get("title")
            titles.append(title)
        
        for title in titles:
            entry = {
                "author_id": author_id,
                "name": name,
                "title": title
            }
            data.append(entry)
        
    write_data(data, path)


def author_division_similarity(path):
    data = []

    div_docs = [doc for doc in division_collection.find()]
    for idx, author_doc in enumerate(clean_authors_collection.find()):
        if idx % 100 == 0:
            print(f"STATUS: {idx}")

        author_id = author_doc["_id"]
        name = author_doc["name"]
        author_vector = author_doc["tfidf_vector"]
        for div_doc in div_docs:
            division = div_doc["_id"]
            div_vector = div_doc["tfidf_vector"]
            score = vector_utils.calculate_similarity(author_vector, div_vector)

            entry = {
                "author_id": author_id,
                "name": name,
                "division": division,
                "score": score
            }
            data.append(entry)
    print(f"STATUS: {idx}")
    write_data(data, path)


if __name__ == "__main__":
    n = 100
    print(f"Writing Top {n} terms for each division")
    division_top_terms("data/output/division_top_terms.csv", n)
    print(f"Writing Top {n} terms for each JPL author")
    author_top_terms("data/output/authors_top_terms.csv", n)
    print("Writing sample publication titles for each author")
    write_author_jpl_titles("data/output/author_titles.csv")
    print(f"Writing similarity scores")
    author_division_similarity("data/output/author_div_sim.csv")
    print("Done.")