import requests
from bs4 import BeautifulSoup
import pandas as pd
from googlesearch import search
import ollama
import json


def search_wiki(toSearch):
    suffix = f"{toSearch} wikipedia"
    real = search(suffix, num_results=2)
    links = list(real)
    return links[0]

def search_news(llmResp:str):
    links = {}
    llmHeadline = json.loads(llmResp)

    for key,value in llmHeadline.items():
        prefix = f"Latest News 2024 : {value} -Research"
        real = search(prefix, num_results=2)
        sentiLink = list(real)
        links[key] = sentiLink[0]
    
    final_links = json.dumps(links)
    print(final_links)
    return final_links

def context_extract(url:str):
    context = ""
    try:
        page = requests.get(url)
    except Exception as e:
        print(e)
    soup = BeautifulSoup(page.text, 'html.parser')

    for i in range(0,6):
        context += (soup.find_all('p')[i].get_text())
    
    return context


## prompt = task to do -> context -> response in the format
def headline_generate(subject,context):
    task = f"Generate 3 news headlines on the topic {subject}, one which is negative in sentiment, one which is positive in sentiments and one which is neutral informative news based on the follwing context:"
    response_format = "now, give output in the form of a JSON nothing else should be written in your response except this json object. JSON Object format should be {sentiment : headline}."
    prompt = f"{task} {context} {response_format}"
    ollama_response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': f"{prompt}"}])['message']['content']
    return ollama_response




