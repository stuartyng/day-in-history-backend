#  @rondevv
#  FARMSTACK Tutorial - Sunday 13.06.2021

# import asyncio
import asyncio
from datetime import date
from datetime import datetime
import http
import time
from typing import Union
from fastapi import FastAPI, Request, Body, Depends, HTTPException, Security, status
import httpx
from pydantic import BaseModel
from fastapi.security import APIKeyHeader, APIKeyQuery
from dataclasses import dataclass
from typing import List
import json
import os
import openai
import pydantic
import regex
import pandas as pd
from bson import ObjectId
from supabase import create_client, Client
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str


import requests

from model import Article, Todo
# from send import run

# azure imports and variables
# import asyncio
# from azure.servicebus.aio import ServiceBusClient
# from azure.servicebus import ServiceBusMessage
# from azure.identity.aio import DefaultAzureCredential

# FULLY_QUALIFIED_NAMESPACE = "dayInHistory.servicebus.windows.net"
# ARTICLE_QUEUE_NAME = "articlequeue"
# HEADLINE_QUEUE_NAME = "headlinequeue"
# credential = DefaultAzureCredential()


# OPEN AI TO DO SEPARATE

OAI_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"

# @dataclass
# class Message:
#     role: str
#     content: str

# @dataclass
# class OpenAiHeadlines(BaseModel):
#     model: str
#     messages: List[Message]

    # Define a list of valid API keys
OPENAI_API_KEY = "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"

# # Define the name of query param to retrieve an API key from
# api_key_query = APIKeyQuery(name="api-key", auto_error=False)
# # Define the name of HTTP header to retrieve an API key from
# api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


# def get_api_key(
#     api_key_query: str = Security(api_key_query),
#     api_key_header: str = Security(api_key_header),
# ):
#     """Retrieve & validate an API key from the query parameters or HTTP header"""
#     # If the API Key is present as a query param & is valid, return it
#     if api_key_query in API_KEYS:
#         return api_key_query

#     # If the API Key is present in the header of the request & is valid, return it
#     if api_key_header in API_KEYS:
#         return api_key_header

#     # Otherwise, we can raise a 401
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid or missing API Key",
#     )
# 

from database import (
    create_article,
    fetch_all_articles,
    fetch_config,
    fetch_one_article,
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    remove_article,
    update_article,
    update_todo,
    remove_todo,
)

# an HTTP-specific exception class  to generate exception information

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

origins = [
    "*",
]

# what is a middleware? 
# software that acts as a bridge between an operating system or database and applications, especially on a network.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

# @app.get("/api/todo")
# async def get_todo():
#     response = await fetch_all_todos()
#     return response

# @app.get("/api/todo/{title}", response_model=Todo)
# async def get_todo_by_title(title):
#     response = await fetch_one_todo(title)
#     if response:
#         return response
#     raise HTTPException(404, f"There is no todo with the title {title}")

# @app.post("/api/todo/", response_model=Todo)
# async def post_todo(todo: Todo):
#     response = await create_todo(todo.dict())
#     if response:
#         return response
#     raise HTTPException(400, "Something went wrong")

# @app.put("/api/todo/{title}/", response_model=Todo)
# async def put_todo(title: str, desc: str):
#     response = await update_todo(title, desc)
#     if response:
#         return response
#     raise HTTPException(404, f"There is no todo with the title {title}")

# @app.delete("/api/todo/{title}")
# async def delete_todo(title):
#     response = await remove_todo(title)
#     if response:
#         return "Successfully deleted todo"
#     raise HTTPException(404, f"There is no todo with the title {title}")

#open ai api SECOND FUNCTION

# @app.post("/api/article/OpenAI_custom", tags=["Article"])
# async def post_article_custom(category: str, start_date: date):
       

#     try:
#         config = await fetch_config()

#         #Get date range and iterate
#         articleList = []
        
#         #OG
#         phrase = config.get_headlines_phrase.replace("REPLACE_CATEGORY", category)
#         phrase = phrase.replace("REPLACE_HEADLINE_COUNT", str(config.headlines_per_category_count))
#         #1978-01-21
#         phrase = phrase.replace("REPLACE_DATE", str(start_date.strftime("%B %d, %Y")))
#         print(phrase)

#         openai.api_key = OPENAI_API_KEY
        
#         # list models
#         models = openai.Model.list()

#         # print the first model's id
#         print(models.data[0].id)

#         rawHeadlines = ""
#         number = 0
        
#         # create a chat completion
#         print("*openai.ChatCompletion.create*")
#         chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": phrase}])
#         # print the chat completion
#         print("print the chat completion: ")
#         print(chat_completion.choices[0].message.content)
#         rawHeadlines = chat_completion.choices[0].message.content

#         # ### uhhh
            
#         print("rawHeadlines is: " + rawHeadlines)
#         startIndex = str(rawHeadlines).index('1.')
#         OpenAiMessage = rawHeadlines[0:startIndex]
#         print("OpenAiMessage is: " + OpenAiMessage)
#         headlines_String = rawHeadlines[startIndex-1:len(rawHeadlines)]
#         print("headlines_String is: " + headlines_String)
#         # print("index is: " + str(startIndex))
        
#         #FIXME split the headlines by numbers list 1. 2. 3. ...
#         # headlines = regex.split("\d+(?:\.\d+)*[\s\S]*?\w+\.", headlines_String)
#         headline_list =  regex.split("\d+\.", str(headlines_String))
#         print("test test test")
#         print("headline_list: ")
#         print(headline_list)


#         # CUSTOM HEADLINES TEST
#         # headline_list = {"red sparrow", "blue bird"}

#         # creating list
#         list = []
#         today = date.today()

#         #for every single headline in the list, create headlines
#         for headline in headline_list:
#             print("foreach headline isCUSTOM: " + headline)
            
#             d1 = today.strftime("%d/%m/%Y")

#             #TODO RETRY 5 TIMES UNTIL ARTICLE IS NOT EMPTY
#             essay = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Write a " + str(config.article_body_character_limit) + " character essay about the topic of" + headline}])
            
#             article = Article(title=headline, body=essay.choices[0].message.content, datecreated=date.today().strftime("%Y-%m-%d"), dayOfTheYear=start_date.strftime("%Y-%m-%d"), Category=category)
            
#             try:
                
#                 # doc = vars(article)
#                 #add to mongo
#                 result = await create_article(article.dict())
#                 #FIXME RETURNS JUST FOR ONE ARTICLE / ONE DAY / do for every day in date range
#                 # return result
        
#             except Exception as error:
            
#                 return ('An exception occurred: {}'.format(error))
#             # appending instances to list
#             # list.append(Article(title=headline, body=essay.choices[0].message.content, date=date.today()))
#             articleList.append(Article(title=headline, body=essay.choices[0].message.content, date=date.today()))

#             # if list:
#             #     return list
#             # raise HTTPException(400, "Something went wrong")
            
#         if articleList:
#                 return articleList
#         raise HTTPException(400, "Something went wrong")
    
#     except Exception as error:
#         return ('An exception occurred: {}'.format(error))


##open ai api
@app.post("/api/article/OpenAI", tags=["Article"])
async def post_article(start_date: date, end_date: date):
       

    try:
        config = await fetch_config()

        #Get date range and iterate
        daterange = pd.date_range(str(start_date), end_date)
        articleList = []
        
        day_of_month = start_date
        time_periods_list = config.time_periods

        #old for loop (for single_date in daterange)
        #new should be for all the date ranges in the config.time_periods
        for time_period in time_periods_list:

            #TODO refactor each_category
            #creating articles for every single category in the config file
            #**********************************************************************
            #run using async
            run_each_category = each_category(day_of_month, time_period)
            # asyncio.run(run_create_articles)
            articleList += await run_each_category
            #**********************************************************************

            
        if articleList:
                return articleList
        raise HTTPException(400, "Something went wrong")
    
    except Exception as error:
        return ('An exception occurred: {}'.format(error))

async def each_category( day_of_month: date, time_period: str):
    articleList = []
    #
    try:
        config = await fetch_config()
        # for each category in Config.categories 
        for category in config.categories:

                #Sleep
                time.sleep(config.open_ai_request_sleep_mls)

                phrase = config.get_headlines_phrase.replace("REPLACE_CATEGORY", category)
                phrase = phrase.replace("REPLACE_HEADLINE_COUNT", str(config.headlines_per_category_count))
                #1978-01-21
                phrase = phrase.replace("REPLACE_DATE", str(day_of_month.strftime("%B %d")))
                # phrase should just be a date without a year - 01/01 / xxxx
                phrase = phrase.replace("REPLACE_YEAR", time_period)
                print(phrase)

                openai.api_key = OPENAI_API_KEY
                
                # list models
                models = openai.Model.list()

                # print the first model's id
                print(models.data[0].id)

                rawHeadlines = ""
                number = 0
                hasHeadlines = False
                print("hasHeadlines is " + str(hasHeadlines))
                #keep creating headlines if openAI fails to generate headlines the first time
                while hasHeadlines==False & number < config.headline_retry_count:
                    print("WHILE hasHeadlines is " + str(hasHeadlines))
                    print("WHILE retryCount is " + str(config.headline_retry_count))
                    
                    # create a chat completion
                    print("*openai.ChatCompletion.create*")
                    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": phrase}])
                    # print the chat completion
                    print("print the chat completion: ")
                    print(chat_completion.choices[0].message.content)
                    rawHeadlines = chat_completion.choices[0].message.content
                    number = number + 1

                    if "1." in rawHeadlines: 
                        hasHeadlines=True
                        print("*hasHeadlines = " + str(hasHeadlines))

                if hasHeadlines:
                    
                    print("rawHeadlines is: " + rawHeadlines)
                    startIndex = str(rawHeadlines).index('1.')
                    OpenAiMessage = rawHeadlines[0:startIndex]
                    print("OpenAiMessage is: " + OpenAiMessage)

                    # headlines_String = rawHeadlines[startIndex-1:len(rawHeadlines)]
                    # print("headlines_String is: " + headlines_String)
                    # print("index is: " + str(startIndex))
                    
                    #FIXME split the headlines by numbers list 1. 2. 3. ...
                    # headlines = regex.split("\d+(?:\.\d+)*[\s\S]*?\w+\.", headlines_String)
                    # headline_list =  regex.split("\d+\. ", str(headlines_String))
                    if "1) " in rawHeadlines:
                        headline_list =  regex.split("\d+\) ", str(rawHeadlines))
                    else:
                        headline_list =  regex.split("\d+\. ", str(rawHeadlines))

                    print("headline_list: ")
                    print(headline_list)

                    # creating list
                    list = []
                    today = date.today()

                    #TODO refacted "create_articles"... 
                    #**********************************************************************
                    category_string = str(category)
                    # single_date_string = day_of_month.strftime("%Y-%m-%d")
                    single_date_string = day_of_month.strftime("%m-%d")

                    time.sleep(config.open_ai_request_sleep_mls)
                    #run using async
                    run_create_articles = create_articles_from_headlineList(headline_list, single_date_string, category_string)
                    # asyncio.run(run_create_articles)
                    articleList += await run_create_articles
                    #**********************************************************************
                    
                else:
                    return ('No Headlines were received')
            # return....
    except Exception as error:
        return ('An exception occurred: {} in each_category'.format(error))
    return articleList

async def create_articles_from_headlineList(headlines_list: list, single_date: str, category_string: str):
    articlesList = []
    articleCounter = 0
    today = date.today()
    print("****ENTERED create_articles...****")
    #
    try:
        config = await fetch_config()
        for headline in headlines_list:

            if headline !="":

                print("foreach headline is (CREATE): " + headline)
                
                #d1 = today.strftime("%d/%m/%Y")
                # datetime object containing current date and time
                now = datetime.now()
                print("Date Now is : " + now.strftime("%Y-%m-%d, %H:%M:%S"))
                
                #TODO RETRY 5 TIMES UNTIL ARTICLE IS NOT EMPTY
                essay = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Write a " + str(config.article_body_character_limit) + "minimum word essay about the topic of" + headline}])
                # print("essay: " + str(essay.choices[0].message.content))
                articleRetryCount=0
                hasArticle=False

                if essay.choices[0].message.content !="":
                    while hasArticle==False & articleRetryCount < config.headline_retry_count:                        

                        article = Article(title=headline, body=essay.choices[0].message.content, datecreated=now.strftime("%Y-%m-%d, %H:%M:%S"), dayOfTheYear=single_date, Category=category_string, readcount=0)
                        articleRetryCount+1
                        if essay.choices[0].message.content!="":
                            hasArticle=True
                            print("article: " + str(article.body))
                            try:

                                #get article image
                                #todo


                                # doc = vars(article)
                                #add to mongo
                                result = await create_article(article.dict())
                                #FIXME RETURNS JUST FOR ONE ARTICLE / ONE DAY / do for every day in date range
                                # return result
                                articleCounter+=1
                                print("FINISHED ARTICLE #" + str(articleCounter) + " FOR CATEGORY: ::::::::::::::::::::::::" + category_string + "::: For date: " + single_date + " Published on " + now.strftime("%Y-%m-%d, %H:%M:%S"))
                            except Exception as error:
                                return ('An exception occurred: {}'.format(error))
                            # appending instances to list
                            # list.append(Article(title=headline, body=essay.choices[0].message.content, date=date.today()))
                            articlesList.append(Article(title=headline, body=essay.choices[0].message.content, date=date.today()))
                else:
                    print("essay machine broke. ")
    except Exception as error:
        return ('An exception occurred: {} in create_articles_from_headlineList'.format(error))
    return articlesList

async def create_image(headline: str, img_size: str):

    url = ""
    key = ""

    supabase: Client = create_client(url, key)

    image_url = ""

    #get image from DALL-E
    response = openai.Image.create(
    prompt=headline,
    n=1,
    size=img_size
    )
    openai_image_url = response['data'][0]['url']

    #STORE IMAGE TO SERVER OR DB AND GET IMAGE ID
    #todo

    return image_url 

@app.get("/api/article", tags=["Article"])
async def get_article():
    response = await fetch_all_articles()
    return response

@app.get("/api/article/{article_id}", response_model=Article, tags=["Article"])
async def get_article_by_title(article_id):
    response = await fetch_one_article(article_id)
    if response:
        return response
    raise HTTPException(404, f"404 Not found")

@app.post("/api/article/", response_model=Article, tags=["Article"])
async def post_article(article: Article):
    response = await create_article(article.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@app.put("/api/article/{title}/", response_model=Article, tags=["Article"])
async def put_article(title: str, body: str):
    response = await update_article(title, body)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")


@app.delete("/api/article/{title}", tags=["Article"])
async def delete_article(title):
    response = await remove_article(title)
    if response:
        return "Successfully deleted todo"
    raise HTTPException(404, f"There is no todo with the title {title}")

#####################################################################################################


