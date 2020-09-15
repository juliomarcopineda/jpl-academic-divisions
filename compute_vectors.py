from mongo.mongo_provider import MongoProvider
from collections import Counter, OrderedDict

import math


def normalize_vector(vector):
    normalized_vector = {}
    norm_length = math.sqrt(sum(weight * weight for weight in vector.values()))
    for token, weight in vector.items():
        normalized_vector[token] = weight / norm_length
    
    return normalized_vector

if __name__ == "__main__":
    mongo_provider = MongoProvider()
    collection = mongo_provider.get_publications_collection()
    docs = collection.find({}, {"tokens": 1})

    print("Determining document and term frequencies")
    doc_term_freq = {}
    doc_freq = {}
    doc_size = 0
    for doc in docs:
        _id = doc["_id"]
        tokens = doc["tokens"]

        if tokens:
            doc_size += 1
            counter = Counter(tokens)
            total = sum(count for count in counter.values())
            
            term_freq = {}
            for token, count in counter.items():
                term_freq[token] = count / total
                doc_freq[token] = doc_freq.get(token, 0) + 1
            
            doc_term_freq[_id] = term_freq
    
    print(f"Total number of tokens: {len(doc_freq)}")
    print(f"Documents with tokens: {doc_size}")

    print("Calculating Inverse Document Frequencies")
    idf = {}
    for token, doc_count in doc_freq.items():
        idf[token] = math.log(doc_size / doc_count)
    
    
    print("Calculating TF-IDF vectors")
    tfidf_vectors = {}
    for _id, term_freq in doc_term_freq.items():
        tfidf_vector = {}
        for term, freq in term_freq.items():
            tfidf_vector[term] = freq * idf[term]
        tfidf_vectors[_id] = tfidf_vector
    
    print("Updating MongoDB with TF-IDF vectors")
    for _id, vector in tfidf_vectors.items():
        normalized_vector = normalize_vector(vector)
        sorted_normalized_vector = OrderedDict(
            sorted(vector.items(), key=lambda kv: kv[1], reverse=True)
        )
        filter_doc = {
            "_id": _id
        }

        update_doc = {
            "$set": {
                "tfidf_vector": sorted_normalized_vector
            }
        }
        collection.update_one(filter=filter_doc, update=update_doc)

    print("Done.")