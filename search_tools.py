import json
import re
from nltk.stem import PorterStemmer
from normalise_ryan import preproc

def load_inverted_index(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

def normalize_query(query):
    tokens = re.findall(r'\w+', query.lower())  
    query_token = [preproc(token) for token in tokens if preproc(token)]
    #len_query = len(query_token)
    #print(query_token[0])
    return query_token

def boolean_search(query, inverted_index):
    tokens = re.findall(r'\".*?\"|\w+|\b(?:AND|OR|NOT)\b', query)

    query_terms = []
    operators = []

    for token in tokens:
        upper_token = token.upper()
        if upper_token in {"AND", "OR", "NOT"}:
            operators.append(upper_token)
        else:
            query_terms.append(token)

    normalized_terms = [normalize_query(term)[0] for term in query_terms if normalize_query(term)]  

    results = set()
    if normalized_terms and normalized_terms[0] in inverted_index:
        results = set(inverted_index[normalized_terms[0]].keys())

    for i, term in enumerate(normalized_terms[1:]):
        if term in inverted_index:
            term_docs = set(inverted_index[term].keys())

            if i < len(operators):
                operator = operators[i]

                if operator == "AND":
                    results &= term_docs  
                elif operator == "OR":
                    results |= term_docs 
                elif operator == "NOT":
                    results -= term_docs  

    return sorted(results)

def phrase_search(query, inverted_index):
    query_terms = normalize_query(query)
    results = set()

    if query_terms[0] in inverted_index:
        candidate_docs = set(inverted_index[query_terms[0]].keys())

        for doc in candidate_docs:
            positions = inverted_index[query_terms[0]][doc]
            for position in positions:
                match = all(
                    doc in inverted_index.get(query_terms[i], {}) and
                    (position + i) in inverted_index[query_terms[i]][doc]
                    for i in range(1, len(query_terms))
                )
                if match:
                    results.add(doc)

    return sorted(results)

def search_inverted_index(json_file, query):
    inverted_index = load_inverted_index(json_file)

    if '"' in query:
        return phrase_search(query.replace('"', ''), inverted_index)  
    else:
        return boolean_search(query, inverted_index)