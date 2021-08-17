import requests
from bs4 import BeautifulSoup

# params = {'id': 'studiobside'}

# &s_type=search_all -> 검색 분류
# &s_keyword=버그 -> 키워드
# &search_pos=-538838 ->10000단위로 끊어서 검색할 때 사용

GALLARY_LIST_URL = "https://gall.dcinside.com/mgallery/board/lists?id=studiobside"
GALLARY_VIEW_URL = "https://gall.dcinside.com/mgallery/board/view/?id=studiobside"
LIMIT = 100
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}


#DC 갤러리 긁어오기
def extract_dc_contents(last_page, word):
    contents = []
    for page in range(1, last_page + 1):
        print(f"Processing Page: {page}/{last_page}")
        result = requests.get(
            f"{GALLARY_LIST_URL}&page={page}&list_num={LIMIT}&s_type=search_all&s_keyword={word}",
            headers=headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find('table', {
            "class": "gall_list"
        }).find_all('tr', {"class": "ub-content us-post"})
        for result in results:
            if result.find('td', {"class": "gall_subject"}).text != '공지':
                content = extract_contents(result)
                contents.append(content)
    return contents

#컨텐츠 긁어오기
def extract_contents(html):
    index = html.find('td', {"class": "gall_num"}).text
    title = html.find('td', {"class": "gall_tit ub-word"}).find("a").text
    anchor = f"{GALLARY_VIEW_URL}&no={index}"
    # inner_content = extract_inner_content(anchor)
    inner_content = None
    date = html.find('td', {"class": "gall_date"})["title"]
    count = html.find('td', {"class": "gall_count"}).text

    return {
        'index': index,
        'title': title,
        'content': inner_content,
        'link': anchor,
        'date': date,
        'count': count
    }


#내부내용 긁어오기
def extract_inner_content(anchor):
    print(f"Extract Inner Contents")
    result = requests.get(anchor, headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    result = soup.find('div', {"class": "writing_view_box"})
    if (result):
        result = result.text
        return result
    else:
        return None
