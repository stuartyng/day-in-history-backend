#  @rondevv
#  FARMSTACK Tutorial - Sunday 13.06.2021

# Pydantic allows auto creation of JSON Schemas from models
from ast import List
import datetime
from typing import Optional
from pydantic import BaseModel
from typing import List

x = datetime.datetime.now()
x = str(x.date)


# classes
class Todo(BaseModel):
    title: str
    description: str

class Article(BaseModel):
    _id: Optional[str] = ''
    Category: Optional[str] = ''
    title: str
    featured: Optional[bool] = False
    body: str
    readcount: Optional[int] = None
    dayOfTheYear: Optional[str] = ''
    datecreated: Optional[str] = ''
    image: Optional[str] = ''
    video: Optional[str] = ''
    author: Optional[str] = ''


#Config
class PeriodRange:
    begin: int
    end: int

    def __init__(self, begin: int, end: int) -> None:
        self.begin = begin
        self.end = end


class Config:
    _id: str
    headlines_per_category_count: int
    article_body_character_limit: int
    open_ai_request_sleep_mls: int
    headline_retry_count: int
    categories: List[str]
    period_range: PeriodRange
    get_headlines_phrase: str
    write_essay_phrase: str

    def __init__(self, _id: str, headlines_per_category_count: int, headline_retry_count: int, article_body_character_limit: int, open_ai_request_sleep_mls: int, categories: List[str], period_range: PeriodRange, get_headlines_phrase: str, write_essay_phrase: str) -> None:
        self._id = _id
        self.headlines_per_category_count = headlines_per_category_count
        self.article_body_character_limit = article_body_character_limit
        self.open_ai_request_sleep_mls = open_ai_request_sleep_mls
        self.categories = categories
        self.period_range = period_range
        self.get_headlines_phrase = get_headlines_phrase
        self.write_essay_phrase = write_essay_phrase
        self.headline_retry_count = headline_retry_count


