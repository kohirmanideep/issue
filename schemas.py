from typing import Optional,Dict
from pydantic import BaseModel, Field
class Book(BaseModel):
    Accessnumber:int
    Username:str
    Title:str
    Author:str
    Subject:str
    KeyWord:str
    bookcategory:str
    
    
class ShowBook(BaseModel):
    Accessnumber:int
    Username:str
    Title:str
    Author:str
    Subject:str
    KeyWord:str
    bookcategory:str
    
  
    class Config():
        orm_mode = True