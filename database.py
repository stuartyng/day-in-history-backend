#  @rondevv
#  FARMSTACK Tutorial - Sunday 13.06.2021

import motor.motor_asyncio
from model import Article, Config, Todo
import pydantic
from bson import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://ronaldhoxha:W3Odfb3oew61mKBq@cluster0.bzlecay.mongodb.net/?retryWrites=true&w=majority')
# databases
database_todo = client.TodoList
database_Main = client.HistoryNews

# collections
collection = database_todo.todo
articleCollection = database_Main.Article
configCollection = database_Main.Config


#CONFIG
async def fetch_config():
    document = await configCollection.find_one()
    return Config(**document)

async def fetch_one_todo(title):
    document = await collection.find_one({"title": title})
    return document

async def fetch_one_article(title):
    document = await articleCollection.find_one({"title": title})
    return document

async def fetch_all_todos():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos

async def fetch_all_articles():
    articles = []
    cursor = articleCollection.find({})
    async for document in cursor:
        articles.append(Article(**document))
    return articles

async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    return document

async def create_article(article):
    document = article
    result = await articleCollection.insert_one(document)
    return document


async def update_todo(title, desc):
    await collection.update_one({"title": title}, {"$set": {"description": desc}})
    document = await collection.find_one({"title": title})
    return document

async def update_article(title, body):
    await articleCollection.update_one({"title": title}, {"$set": {"description": body}})
    document = await articleCollection.find_one({"title": title})
    return document

async def remove_todo(title):
    await collection.delete_one({"title": title})
    return True

async def remove_article(title):
    await articleCollection.delete_one({"title": title})
    return True