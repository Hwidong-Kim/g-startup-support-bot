import json
from bs4 import BeautifulSoup
from urllib.request import urlopen

issue_trend_result = list()
def getChild(pageUrl, childPageId):
    contents = list()
    childPageUrl = pageUrl +"&id="+str(childPageId) + "&schBdcode=&schGroupCode=&bdExt9=&bdExt10=&bdExt11=&bdUseyn=&schM=view"
    response =urlopen(childPageUrl)
    page = BeautifulSoup(response, 'html.parser')
    thumbList = page.find(class_="board_contents")
    for imgTag in thumbList.find_all("img"):
        contents.append(imgTag["alt"])
    return contents
def getMain(pageNumber):
    mainPageUrl ='https://www.k-startup.go.kr/web/contents/webKSTARTUP_ISSE_TRD.do?page='+pageNumber
    response =urlopen(mainPageUrl)
    page = BeautifulSoup(response, 'html.parser')

    isse_trd = page.find(class_="gallery_list kstartup_isse_trd")
    for liTag in isse_trd.find_all("li"):
        titleName = liTag.find("a")["title"]
        childPageId = liTag.find("a")["onclick"].split("\'")[1]
        titleLogoUrl = liTag.find(class_="thumb").find("img")['src']

        rootJson = {
            'title':{
                'name':titleName,
                'logo_url':titleLogoUrl
            },
            'contents':getChild(mainPageUrl, childPageId)
        }
        issue_trend_result.append(rootJson)
        

def saveToJson(data, filename, encoding='utf-8'):
    with open(filename, 'w', encoding=encoding) as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

        
def app():
    pageNumber = 1
    for i in range(1,pageNumber+1):
        getMain(str(i))
    saveToJson(issue_trend_result, 'issue_trend_result.json')
app()

