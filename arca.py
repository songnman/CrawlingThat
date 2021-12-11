import requests, time, random, csv
from bs4 import BeautifulSoup
import os.path
import dateutil.parser
from save import save_to_file
import re
import smtplib
from email.message import EmailMessage
from datetime import date
from fragments import extract_keyword_count

def email_alert(subject, body, to):
	msg = EmailMessage()
	msg.set_content(body)
	msg['subject'] = subject
	msg['to'] = to
	
	user = "songnman+python@gmail.com"
	msg['from'] = user
	password = "dwkajyynglqfaehn"
	
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(user, password)
	server.send_message(msg)
	server.quit

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
#*리스트 긁어오기
def extract_arca_list(start_page, last_page, word):
	last_page += start_page - 1
	result_contents = []

	file_word = re.sub("[\/:*?\"<>|]", "", word)#[2021-12-07 10:02:56]파일 이름 수정 로드 / 세이브 모두 대응
	if(word == "All_Time") :
		d1 = date.today().strftime("%Y%m%d")
		file_word = f"Daily_Results/{d1}"
		pass
	my_file = f"results/{file_word}.csv"
	if os.path.exists(my_file):
		f = open(f"results/{file_word}.csv",'r', encoding='utf-8-sig', newline='')
		rdr = csv.DictReader(f)
		for line in rdr:
			content = {
					'index': line['index'],
					'user' : line['user'],
					'title': line['title'],
					'content': line['content'],
					'comment' : line['comment'],
					'link': line['link'],
					'date': line['date'],
					'view': line['view'],
					'rate': line['rate'],
					'comment_count': line['comment_count']
			}
			result_contents.append(content)
		print(f'{word}\'s Search List')
		pass

	for page in range(start_page, last_page + 1):
		print(f"Processing Page: {page}/{last_page}")
		if(word == "All_Time") : result = requests.get(f"{GALLARY_URL}?&p={page}",headers=headers)
		else : result = requests.get(f"{GALLARY_URL}?&p={page}&target=title_content&keyword={word}",headers=headers)
		soup = BeautifulSoup(result.text, 'html.parser')
		results = soup.find('div', {"class": "list-table"}).find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['vrow'])

		TotlaListCount = len(results)
		CurrentListCount = 0
		contents = []

		#* 내부 컨텐츠 생성
		for result in results:
			CurrentListCount += 1
			# sys.stdout.write("\033[F")
			# sys.stdout.flush()
			print(f"\rExtract Contents: {CurrentListCount}/{TotlaListCount}", end='', flush = True)


			#*[2021-08-29 21:55:58] 매칭용 리스트를 생성
			match_content = {}
			index = Extract_index(result)
			rate = Extract_rate(result)
			comment_count = Extract_Comment_Count(result)
			for item in result_contents :
				if item["index"] == index :
					match_content = item

			#*[2021-08-28 03:44:27] 해당 게시물이 저장되어있고, 추천수가 똑같을 경우 스크랩을 하지 않는다.
			if match_content and int(float(match_content['rate'])) == int(float(rate)) and int(float(match_content['comment_count'])) == int(float(comment_count)) :
				print('\r',end='')
				continue
			
			content = extract_contents(result)
			contents.append(content)
			
			#*[2021-08-29 22:57:42]스크랩 주기 설정하는 부분
			wait_time = round(random.uniform(1.0,7.0),3)
			print(f" [{wait_time}]", end='\n')
			time.sleep(wait_time)
			pass
		save_to_file(contents,file_word)
		if(word == "All_Time") : extract_keyword_count(d1)
		pass
	return contents

def Extract_rate(result):
	if result.find('span', {"class": "title"}):
		rate = result.find('span', {"class": "vcol col-rate"}).text
		return rate
	else:
		return 0

def Extract_index(result):
	index = result.attrs['href'].split('/b/counterside/')[1].split('?')[0]
	return index

#*싱글 긁어오기
def extract_arca_single(index):
	contents = []
	result = requests.get(f"{GALLARY_URL}/{index}", headers=headers)
	soup = BeautifulSoup(result.text, 'html.parser')
	anchor = f"{GALLARY_URL}/{index}"
	inner_content = extract_inner_content(soup)
	inner_comments = extract_inner_comments(soup)

	title = soup.find('div', {"class": "title"}).text
	# user = soup.find('span', {'class' : 'user-info'}).find('a').text
	date = dateutil.parser.parse(soup.find('span', {"class": "date"}).find('span', {"class" : "body"}).time['datetime']).astimezone().strftime("%Y-%m-%d %H:%M:%S")
	view = soup.find_all('span', {"class": "body"})[3].text
	rate = soup.find('span', {"class": "body"}).text
	comment_count = 0
	content = {
			'index': int(index),
			# 'user' : user,
			'title': title,
			'content': inner_content,
			'comment' : inner_comments,
			'link': anchor,
			'date': date,
			'view': view,
			'rate': rate,
			'comment_count' : int(comment_count),
	}
	contents.append(content)
	return contents

#*컨텐츠 긁어오기
def extract_contents(html):
	try:
		index = Extract_index(html)
		if html.find('span', {"class": "title"}) :
			title = html.find('span', {"class": "title"}).text
			user = html.find('span', {'class' : 'user-info'}).span.attrs['data-filter']
			anchor = f"{GALLARY_URL}/{index}"
			date = dateutil.parser.parse(html.find('span', {"class": "vcol col-time"}).time['datetime']).astimezone().strftime("%Y-%m-%d %H:%M:%S")
			view = html.find('span', {"class": "vcol col-view"}).text
			rate = Extract_rate(html)
			result = requests.get(anchor, headers=headers)
			soup = BeautifulSoup(result.text, 'html.parser')
			inner_content = extract_inner_content(soup)
			inner_comments = extract_inner_comments(soup)
			comment_count = Extract_Comment_Count(html)
			pass
		else: #!(권한 없음) 예외처리
			title = html.find('span', {"class": "vcol col-title"}).i.text
			user = None
			anchor = None
			date = None
			view = 0
			rate = 0
			inner_content = None
			inner_comments = None
			comment_count = 0
			pass
	except:
		print(html)
		email_alert("Error has been occured. Check out.",html.text, "songnman@gmail.com" )

	return {
			'index': int(index),
			'user' : user,
			'title': title,
			'content': inner_content,
			'comment' : inner_comments,
			'link': anchor,
			'date': date,
			'view': int(view),
			'rate': int(rate),
			'comment_count' : int(comment_count),
	}

def Extract_Comment_Count(html):
	if html.find('span', {"class": "comment-count"}):
		comment_count = html.find('span', {"class": "comment-count"}).text.strip("[]")
	else:
		comment_count = 0
	return comment_count

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