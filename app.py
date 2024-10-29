from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from helpers import search_wiki,context_extract,headline_generate,search_news
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class topicModel(BaseModel):
    topic:str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/topic")
async def recieveTopic(topicData: topicModel):
    topic = topicData.topic
    print(f"recieved topic: {topic}")
    url = search_wiki(topic)
    context = context_extract(url)
    headline = headline_generate(topic,context)
    finals = search_news(headline)
    headjson = json.loads(finals)
    return {"message": "Recieved Successfully", "headlines": headjson}



