from typing import Optional
from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import urllib.parse
from camera import *
from barcode_crawling import *
from pydantic import BaseModel
from oracleDB import OracleDB
from nltk_token import *

class novel(BaseModel):
    novel_no : int
    novel_nm : str
    novel_writer : str
    novel_synopsis : str
    novel_cover : str
    
db = OracleDB()


app = FastAPI()
templates = Jinja2Templates(directory="RomanPick")
app.mount("/RomanPick", StaticFiles(directory="RomanPick"), name="RomanPick")

# 메인 인트로 화면
@app.get("/")
def read_root(request:Request):
    return templates.TemplateResponse('01_intro.html',{"request" : request})

# 메인 클러스터 선택 화면
@app.get("/main")
def read_main(request:Request):
    return templates.TemplateResponse('02_main.html', {"request" : request})

# 메인 클러스터 선택 화면
@app.get("/searchlist")
def read_main(request:Request):
    return templates.TemplateResponse('search_list.html', {"request" : request})

# 검색 기능
@app.post("/search")
def search(request: Request, input_text: str = Form(...), category: str = Form(...)):
    db.search_novel(category, input_text)
    return {"category": category, "input_text":input_text}
        
# ajax 랜덤 데이터 추출, canvas 출력
@app.get("/main/{item}")
def pick_cluster(request:Request, item:str):
    decoded_item = urllib.parse.unquote(item)
    textList = OracleDB().random_list()
    # 이 라벨로 DB와 연결 후 랜덤 5개 제목, 랜덤 5개 키워드 추출 후 리턴
    # 비동기로 5번 키워드 추출 - 랜덤 소설의 키워드 랜덤 하나씩 총 5개
    return {"textList" :textList}

# DB에서 라벨에 맞는 제목이 word와 같은게 있으면 title로, 없으면 keyword로
@app.get("/main/{item}/{word}")
def item_title(request:Request, item:str, word:str):
    item = urllib.parse.unquote(item)
    word = urllib.parse.unquote(word)
    result = db.novel_nm_select(word)
    
    if result is None:
        # 키워드를 html과 같이 return
        # $(document).ready()를 통해 키워드로 ajax
        # 키워드가 포함된 소설번호의 리스트 추출
        # 리스트 중 랜덤 6개 선택 후 정보 추출
        return templates.TemplateResponse('05_List_keyWord.html', {"request" : request})
    else:
        sinopsis = good_text(result[3])
        data = {
            "novel_no":result[0],
            "novel_nm":result[1],
            "novel_writer":result[2],
            "novel_synopsis":sinopsis,
            "novel_cover":result[4]
        }
        # DB에서 라벨에 맞는 제목이 word와 같은게 있으면 title로, 없으면 keyword로
        return templates.TemplateResponse('04_List_title.html', {"request" : request, "data":data})

# 임시 title 화면
@app.get("/main/{item}/{word}/title")
def item_title(request:Request, item:str):
    return templates.TemplateResponse('04_List_title.html', {"request" : request})

# 임시 keyword 화면
@app.get("/main/{item}/{word}/keyword")
def item_title(request:Request, item:str):
    return templates.TemplateResponse('05_List_keyWord.html', {"request" : request})

# ajax 카메라 동영상 바코드 인식 
@app.get("/camera_start")
async def camera_start():
    data = await run_camera()
    return data

# ajax 이미지에서 바코드 인식
@app.post("/img_barcode")
async def img_barcode(imageFile: UploadFile):
    image = await imageFile.read()
    result = await image_barcode(image)
    return result

# ajax 텍스트로 isbn 입력 
@app.get("/input_isbn")
async def input_isbn(input_isbn: str = Form(...)):
    data = await crawling_isbn(input_isbn)
    return data

# 선택된 소설과 유사한 소설 6개 추출 ajax
@app.get("/cosine/{novel_no}")
async def select_novel(novel_no:str):
    novel_no = urllib.parse.unquote(novel_no)
    novel_no = int(novel_no)
    data = db.select_cosine(novel_no)
    # novel_no로 소설 정보를 다 가져오는 쿼리
    return data

@app.post("/select/novel_no_6")
async def select_novel_6(request:Request):
    data = await request.json()
    novel_list = []
    for val in data.values():
        novel_list.append(db.select_novel(val))
    return novel_list

@app.get("/select/novel_no")
def select_novel(pic_numver:int):
    return db.select_novel(pic_numver)

    
# 임시 DB 연결
@app.get("/book")
def insert_item(num:str, title:str):
    num = int(num)
    values = {"num": num, "title": title}
    db.execute_insert1(values)
    return  {"message": "Book inserted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)