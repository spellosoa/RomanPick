import requests as req
from bs4 import BeautifulSoup as bs

async def crawling_isbn(isbn:str):
    isbn = isbn # 수집한 isbn
    url = 'https://dl.nanet.go.kr/search/searchInnerList.do'
    data = {
        "searchType" :  "INNER_SEARCH",
        #"searchQuery" : "+9791190299770",
        "resultType" : "INNER_SEARCH_DETAIL",
        "queryText":f"{isbn}:ALL:AND",
        "selZone":"ALL",
        "dpBranch":"ALL",
        "synonymYn" :"Y",
        #"asideState":"true",
        #"hanjaYn":"Y",
        #"totalSizeByMenu" : 1,
        #"totalSize":1,
        "searchMethod" : "L",
        "searchClass":"S",
        #"prevQueryText":"9791190299770:ALL:AND"
    }
    res = req.post(url,data=data)
    soup = bs(res.text,'lxml')
    aTag = soup.select('ul.list>li>a')
    jsDetail = aTag[0]['href']
    mono = jsDetail[30:-7]
