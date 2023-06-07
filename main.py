from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import urllib.parse
from camera import *
from pydantic import BaseModel

class novel(BaseModel):
    novel_no : int
    novel_nm : str
    novel_writer : str
    novel_synopsis : str
    novel_cover : str



app = FastAPI()
templates = Jinja2Templates(directory="RomanPick")
app.mount("/RomanPick", StaticFiles(directory="RomanPick"), name="RomanPick")


@app.get("/")
def read_root(request:Request):
    return templates.TemplateResponse('01_intro.html',{"request" : request})

@app.get("/main")
def read_main(request:Request):
    return templates.TemplateResponse('02_main.html', {"request" : request})

@app.get("/main/{item}")
def pick_cluster(request:Request, item:str):
    decoded_item = urllib.parse.unquote(item)
    return templates.TemplateResponse('03_heart.html', {"request" : request})

@app.get("/main/{item}/title")
def item_title(request:Request, item:str):
    decoded_item = urllib.parse.unquote(item)
    return templates.TemplateResponse('List_title.html', {"request" : request})

@app.get("/main/{item}/keyword")
def item_title(request:Request, item:str):
    decoded_item = urllib.parse.unquote(item)
    return templates.TemplateResponse('List_keyWord.html', {"request" : request})

@app.get("/camera_start")
def start_camera():
    data = run_camera()
    return data
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

# @app.get("/aa/")
# def aa():
#     return 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa'

# @app.get("/item")
# def insert_item():
#     db.execute_insert(book.dict())
#     print(book)
#     return  {"message": "Book inserted successfully"}

# @app.get("/book")
# def insert_item(num:int, title:str):
#     values = {"num": num, "title": title}
#     db.execute_insert1(values)
#     return  {"message": "Book inserted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)