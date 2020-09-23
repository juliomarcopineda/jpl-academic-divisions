def calculate_similarity(v1, v2):
    score = 0
    for token, w1 in v1.items():
        w2 = v2.get(token, 0)
        score += w1 * w2


def get_unique_tokens(vectors):
    tokens = set()
    for vector in vectors:
        for token in vector.keys():
            tokens.add(token)

    return tokens


def get_average_vectors(vectors):
    token_weight_list = {}
    unique_tokens = get_unique_tokens(vectors)
    for vector in vectors:
        for token in unique_tokens:
            weight = vector.get(token, 0.0)
            weight_list = token_weight_list.get(token, [])
            weight_list.append(weight)
            token_weight_list[token] = weight_list
    
    average_vector = {}
    for token, weight_list in token_weight_list.items():
        average_vector[token] = sum(weight_list) / len(weight_list)
    
    return average_vector
        