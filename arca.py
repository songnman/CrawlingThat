import requests, time, random, csv
from bs4 import BeautifulSoup
import os.path
import dateutil.parser
from save import save_to_file

# params = {'id': 'studiobside'}

# &s_type=search_all -> 검색 분류
# &s_keyword=버그 -> 키워드
# &search_pos=-538838 ->10000단위로 끊어서 검색할 때 사용
# &after=8170753 -> 특정날짜를 기준으로 게시물 검색 가능

GALLARY_URL = "https://arca.live/b/counterside"
headers = {
		'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}
#dkssydhdhd

#*리스트 긁어오기
def extract_arca_list(start_page, last_page, word):
	last_page += start_page - 1

	my_file = f"results/{word}.csv"
	if os.path.exists(my_file):
		f = open(f"results/{word}.csv",'r', encoding='utf-8-sig', newline='')
		rdr = csv.reader(f)
		next(rdr)
		data = list()
		for line in rdr:
				data.append(line[0])
		data.sort(reverse = True)
		last_index = data[0]
		print(f'{word}\'s Saved Last Index is : {last_index}')

	for page in range(start_page, last_page + 1):
			print(f"Processing Page: {page}/{last_page}")
			result = requests.get(
					f"{GALLARY_URL}?&p={page}&target=title_content&keyword={word}",
					headers=headers)
			soup = BeautifulSoup(result.text, 'html.parser')
			results = soup.find('div', {"class": "list-table"}).find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['vrow'])

			TotlaListCount = len(results)
			CurrentListCount = 0
			
			#* 미리보기 컨텐츠 생성
			contents = []
			for result in results:
					content = extract_contents(result, False)
					contents.append(content)
			save_to_file(contents,word)
			print("Preview Loaded.")
			
			# #* 내부 컨텐츠까지 생성
			contents.clear()
			for result in results:
					#Delay 넣고 체크 시작
					CurrentListCount += 1
					wait_time = random.uniform(1.0,4.0)
					print(f"Extract Contents: {CurrentListCount}/{TotlaListCount} [{wait_time}]")
					time.sleep(wait_time)
					content = extract_contents(result, True)
					contents.append(content)
	return contents

#*싱글 긁어오기
def extract_arca_single(index):
	contents = []
	result = requests.get(f"{GALLARY_URL}/{index}", headers=headers)
	soup = BeautifulSoup(result.text, 'html.parser')
	print(soup)
	anchor = f"{GALLARY_URL}/{index}"
	inner_content = extract_inner_content(soup)
	inner_comments = extract_inner_comments(soup)
	
	title = soup.find('div', {"class": "title"}).text
	# user = soup.find('span', {'class' : 'user-info'}).find('a').text
	date = dateutil.parser.parse(soup.find('span', {"class": "date"}).find('span', {"class" : "body"}).time['datetime']).astimezone().strftime("%Y-%m-%d %H:%M:%S")
	view = soup.find_all('span', {"class": "body"})[3].text
	rate = soup.find('span', {"class": "body"}).text
	content = {
			'index': index,
			# 'user' : user,
			'title': title,
			'content': inner_content,
			'comment' : inner_comments,
			'link': anchor,
			'date': date,
			'view': view,
			'rate': rate
	}
	contents.append(content)
	return contents

#*컨텐츠 긁어오기
def extract_contents(html, inner_bool):
	index = html.attrs['href'].split('/b/counterside/')[1].split('?')[0]
	if html.find('span', {"class": "title"}) :
		title = html.find('span', {"class": "title"}).text
		user = html.find('span', {'class' : 'user-info'}).span.attrs['data-filter']
		anchor = f"{GALLARY_URL}/{index}"
		date = dateutil.parser.parse(html.find('span', {"class": "vcol col-time"}).time['datetime']).astimezone().strftime("%Y-%m-%d %H:%M:%S")
		view = html.find('span', {"class": "vcol col-view"}).text
		rate = html.find('span', {"class": "vcol col-rate"}).text

		if inner_bool:
			result = requests.get(anchor, headers=headers)
			soup = BeautifulSoup(result.text, 'html.parser')
			inner_content = extract_inner_content(soup)
			inner_comments = extract_inner_comments(soup)
		else: 
			inner_content = '[Gathering...]'
			inner_comments = '[Gathering...]'

	else: #!(권한 없음) 예외처리
		print(html)
		title = html.find('span', {"class": "vcol col-title"}).i.text
		print(title)
		anchor = None
		date = None
		rate = None
		user = None
		view = None
		inner_content = None
		inner_comments = None

	return {
			'index': index,
			'user' : user,
			'title': title,
			'content': inner_content,
			'comment' : inner_comments,
			'link': anchor,
			'date': date,
			'view': view,
			'rate': rate
	}

#*내용 긁어오기
def extract_inner_content(soup):
	result_content = soup.find('div', {"class": "article-content"})

	if (result_content):
			result_content = result_content.text

			return result_content
	else:
			return None

#*코멘트 긁어오기
def extract_inner_comments(soup):
	comments = []
	print()
	result_comments = soup.find('div', {"class": "article-comment"}).find_all('div', {'class' : 'comment-wrapper'})
	if result_comments:
		for comment in result_comments:
			dic = {}
			if comment.find('div', {'class' : 'text'}):
				dic['user'] = comment.find(attrs={"data-filter":True})['data-filter']
				dic['comment'] = comment.find('div', {'class' : 'text'}).text
			else :
				dic['user'] = comment.find(attrs={"data-filter":True})['data-filter']
				dic['comment'] = '(emoticon)'
			comments.append(dic)
		return comments
	else:
			return None