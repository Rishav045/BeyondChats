import json
import time
from sklearn.metrics.pairwise import cosine_similarity
from translate import Translator
from langdetect import detect
import numpy as np

# Function to detect the language of a given text
def detect_language(text):
    return detect(text)

# Function to translate text from a source language to a target language (default: English)
def translate_text(text, source_lang, target_lang="en"):
    translator = Translator(to_lang=target_lang, from_lang=source_lang)
    translation = translator.translate(text)
    return translation

# Function to get the output by ID
def get_output_by_id(id, similarity_threshold=0.5):
    # Load data from "final_dataset.json" file
    with open("final_dataset.json", "r") as f:
        data = json.load(f)
    
    citation = []
    
    # Iterate over the data to find the item with the specified ID
    for item in data:
        if item["id"] == id:
            print(item["response"])
            
            # Iterate over the sources of the item
            for i in item["source"]:
                print(i["id"])
                
                # Reshape the response embedding and source embedding
                response_embedding = np.array(item["embedding"]).reshape(1, -1)
                source_embedding = np.array(i["embedding"]).reshape(1, -1)
                
                # Calculate the cosine similarity between the response embedding and source embedding
                similarity_score = cosine_similarity(response_embedding, source_embedding)[0][0]
                print(f"Similarity score: {similarity_score}")
                
                # Check if the similarity score is above the threshold
                if similarity_score >= similarity_threshold:
                    # Append the relevant source information to the citation list
                    citation.append({
                        "id": str(i["id"]),
                        "link": str(i["link"]),
                        "context": i["context"]
                    })
            
            print(len(citation))
            return citation
    
    # Return an empty list if no matching item is found
    return []

# Example usage
print(get_output_by_id(102))

# def get_output_by_response(Response , Source):
