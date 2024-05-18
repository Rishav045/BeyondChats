import json
import pprint
import openai
import time
from sklearn.metrics.pairwise import cosine_similarity
from translate import Translator
from langdetect import detect

openai.api_key = "sk-proj-hbI0YgCLmWxSTqOBsQAqT3BlbkFJ8PerU3wBNmMNl6bf9HPA"

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-3-small"
    )
    embeddings = [data['embedding'] for data in response['data']]
    return embeddings

def detect_language(text):
    return detect(text)

def translate_text(text, source_lang, target_lang="en"):
    translator = Translator(to_lang=target_lang, from_lang=source_lang)
    translation = translator.translate(text)
    return translation

with open("extracted.json","r") as f:
    data = json.load(f)

data_without_metadata=[]

for item in data:
    data_without_metadata.append(item["data"])

preprocessed_data = []
count =0
for data in data_without_metadata:
    for item in data:
        for i in item["source"]:
            if(len(i["context"])>1):
                temp_str=""
                for text in i["context"]:
                    temp_str+=text
                i["context"]=temp_str
        temp={"id":item["id"],"response":item["response"],"source":item["source"]}
        preprocessed_data.append(temp)


with open("preprocessed_data.json", "w") as f:
    json.dump(preprocessed_data, f)

with open("preprocessed_data.json", "r",encoding='utf-8') as f:
    preprocessed_data = json.load(f)

def prepare_embedding_data(data):
    embedding_data=[]
    ident=1
    temp_list=[]
    for item in data:
        print(f"Processing item {ident}")
        ident+=1
        temp_response=item["response"]
        
        response_lang = detect_language(temp_response)
        if response_lang != "en":
            temp_response = translate_text(temp_response, source_lang=response_lang, target_lang="en")
        temp_list.append(temp_response)
        for source in item["source"]:
            temp_context=source["context"]
            
            # print(temp_context)
            response_lang = detect_language(temp_context)

            if response_lang!="en":
                temp_context=translate_text(temp_context , source_lang=response_lang, target_lang="en")
            temp_list.append(temp_context)
    print(len(temp_list))
    embedding=get_embedding(temp_list)
    with open("embedding.json", "w") as f:
        json.dump(embedding, f)
        

def prepare_final_dataset():
    with open("embedding.json","r",encoding='utf-8') as f:
        embeddings = json.load(f)
    with open("preprocessed_data.json", "r",encoding='utf-8') as f:
        preprocessed_data = json.load(f)
    start=0
    final_dataset=[]
    for item in preprocessed_data:
        source_length = len(item["source"])+1
        combined_embeddings = embeddings[start:start+source_length]
        start+=source_length
        response_embedding=combined_embeddings[0]
        source_embeddings = combined_embeddings[1:]
        temp_source=[]
        source_ident=0
        for i in item["source"]:
            temp_source.append({"id":i["id"], "link":i["link"], "context":i["context"], "embedding":source_embeddings[source_ident]})
            source_ident+=1
        final_dataset.append({"id":item["id"],"response":item["response"],"source":temp_source,"embedding":response_embedding})
    with open("final_dataset.json", "w") as f:
        json.dump(final_dataset, f)

prepare_final_dataset()



        

