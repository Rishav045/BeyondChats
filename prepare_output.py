import json
import time
from sklearn.metrics.pairwise import cosine_similarity
from translate import Translator
from langdetect import detect
import numpy as np

def detect_language(text):
    return detect(text)

def translate_text(text, source_lang, target_lang="en"):
    translator = Translator(to_lang=target_lang, from_lang=source_lang)
    translation = translator.translate(text)
    return translation

def get_output_by_id(id, similarity_threshold=0.5):
    with open("final_dataset.json", "r") as f:
        data = json.load(f)

    citation = []
    for item in data:
        if item["id"] == id:
            print(item["response"])
            for i in item["source"]:
                print(i["id"])
                response_embedding = np.array(item["embedding"]).reshape(1, -1)
                source_embedding = np.array(i["embedding"]).reshape(1, -1)
                similarity_score = cosine_similarity(response_embedding, source_embedding)[0][0]
                print(f"Similarity score: {similarity_score}")
                if similarity_score >= similarity_threshold:
                    citation.append({
                        "id": str(i["id"]),
                        "link": str(i["link"]),
                        "context": i["context"]
                    })
            print(len(citation))
            return citation

    return []  # Return an empty list if no matching item is found

# Example usage
print(get_output_by_id(102))
# def get_output_by_response(Response , Source):


    
            
