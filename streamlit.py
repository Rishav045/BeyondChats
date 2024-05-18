import json
import time
from sklearn.metrics.pairwise import cosine_similarity
from translate import Translator
from langdetect import detect
import numpy as np
import streamlit as st

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
    response_text = ""
    for item in data:
        if item["id"] == id:
            response_text = item["response"]
            for i in item["source"]:
                response_embedding = np.array(item["embedding"]).reshape(1, -1)
                source_embedding = np.array(i["embedding"]).reshape(1, -1)
                similarity_score = cosine_similarity(response_embedding, source_embedding)[0][0]
                citation.append({
                    "id": str(i["id"]),
                    "link": str(i["link"]),
                    "context": i["context"],
                    "similarity_score": similarity_score,
                    "relevant": similarity_score >= similarity_threshold
                })
            break

    return response_text, citation

# Streamlit app
def main():
    st.title("Context Relevance App")

    # Get user input
    id = st.text_input("Enter the ID number of the response (1 to 124):")
    similarity_threshold = st.slider("Similarity Threshold", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    if id:
        # Convert id to integer
        try:
            id = int(id)
            if id < 1 or id > 124:
                st.error("ID must be between 1 and 124.")
            else:
                # Get the output by ID
                response_text, citation = get_output_by_id(id, similarity_threshold)

                # Display the response text
                st.subheader("Response Text")
                st.write(response_text)

                # Display the relevant citation sources
                st.subheader("Relevant Citation Sources")
                relevant_sources = [source for source in citation if source["relevant"]]
                for source in relevant_sources:
                    st.markdown(
                        f'<div style="display: flex; align-items: center;">'
                        f'<span style="color: green; font-size: 20px; margin-right: 10px;">✔</span>'
                        f'<div>'
                        f'<p>ID: {source["id"]}</p>'
                        f'<p>Link: <a href="{source["link"]}" target="_blank">{source["link"]}</a></p>'
                        f'<p>Context: {source["context"]}</p>'
                        f'<p>Similarity Score: {source["similarity_score"]:.2f}</p>'
                        f'</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                # Display the irrelevant citation sources
                st.subheader("Irrelevant Citation Sources")
                irrelevant_sources = [source for source in citation if not source["relevant"]]
                for source in irrelevant_sources:
                    st.markdown(
                        f'<div style="display: flex; align-items: center;">'
                        f'<span style="color: red; font-size: 20px; margin-right: 10px;">✖</span>'
                        f'<div>'
                        f'<p>ID: {source["id"]}</p>'
                        f'<p>Link: <a href="{source["link"]}" target="_blank">{source["link"]}</a></p>'
                        f'<p>Context: {source["context"]}</p>'
                        f'<p>Similarity Score: {source["similarity_score"]:.2f}</p>'
                        f'</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )
        except ValueError:
            st.error("ID must be a valid integer.")

if __name__ == "__main__":
    main()