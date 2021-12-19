import os.path
import pandas as pd
import csv
import string
from wordcloud import WordCloud
def extract_keyword_count(d1):
	my_file = f"results/Daily_Results/{d1}.csv"
	if not os.path.exists(my_file): print(f"No such file : \"{my_file}\"")
	
	# csv_list = [join('results\\',f) for f in listdir('results\\') ]
	# csv_list = ['results\\All_result.csv']
	csv_list = [my_file]
	
	combined_csv = pd.concat([pd.read_csv(f) for f in csv_list ])
	title_list = combined_csv['title'].tolist()
	content_list = combined_csv['content'].tolist()
	content_list2 = []
	for item in content_list:
		if not isinstance(item,str): continue
		else : content_list2.append(item)
	comment_list = []
	comment_dict = combined_csv['comment'].to_list()
	for item in comment_dict:
		if isinstance(item,str): item = eval(item)
		else : continue
		for i in item:
			comment_list.append(i['comment'])

	
	all_list = title_list + content_list2 + comment_list
	# all_list = title_list
	
	delete_list = []
	list_file = "Delete_List.csv"
	if os.path.exists(list_file):
		csvfile = open(list_file,'r', encoding='utf-8-sig', newline='')
		rdr = csv.reader(csvfile)
		for line in rdr:
			delete_list.append(str(line[0]))
	
	deny_list = []
	list_file = "Deny_List.csv"
	if os.path.exists(list_file):
		csvfile = open(list_file,'r', encoding='utf-8-sig', newline='')
		rdr = csv.reader(csvfile)
		for line in rdr:
			deny_list.append(line[0])
	
	noun_filter = []
	list_file = "Noun_Filter.csv"
	if os.path.exists(list_file):
		csvfile = open(list_file,'r', encoding='utf-8-sig', newline='')
		rdr = csv.reader(csvfile)
		for line in rdr:
			noun_filter.append(line[0])
	csvfile.close()
	
	result_noun_list = ' '.join(all_list) #*스트링 하나로 결합
	result_noun_list = result_noun_list.replace(string.punctuation,"").replace(",","").replace("'","").replace('"','').replace('\n',' ').replace(' ',' ') #*[2021-12-09 16:04:29] 제거 되기 어려운 부분들 새로 추가
	for x in range(len(delete_list)) :
		result_noun_list = result_noun_list.replace(delete_list[x],"") #*[2021-12-09 16:04:16]제외되는 부분을 외부 csv 파일로 변경
	result_noun_list = result_noun_list.split(' ') #* 스트링을 다시 LIST로 결합
	result_only_list = list(set(result_noun_list)) #*결합된 스트링에서 중복값 삭제
	
	#*[2021-12-20 01:32:41] 조사 필터 추가
	TotalCount = len(noun_filter)
	CurrentCount = 0
	Noun_Ratio = {}
	for x in noun_filter:
		CurrentCount += 1
		Noun_Ratio[x] = 0
		print(f"[{CurrentCount}/{TotalCount}] Filter Progress. \r", end='', flush = True)
		for only in result_only_list:
			if only+x in result_only_list:
				Noun_Ratio[x] += 1
				result_only_list.remove(only+x)
		pass
	result_only_list.remove(d1)
	print("", end='\n')
	print(Noun_Ratio)
	
	my_file = f"results/Daily_Results_Count/{d1}.csv"
	if os.path.exists(my_file):
		os.remove(my_file)
	f = open(my_file, mode="w", encoding='utf-8-sig', newline='')
	writer = csv.writer(f)
	writer.writerow(["Keyword","count"])
	
	TotalCount = len(result_only_list)
	CurrentCount = 0
	result_merge_list = [] #* [2021-12-14 02:25:44] 바로 내려적지 않고, 리스트로 묶어서 처리
	for noun in result_only_list:
		CurrentCount += 1
		print(f"[{CurrentCount}/{TotalCount}] Count Progress. \r", end='', flush = True)
		noun_count = sum(noun in s for s in result_noun_list)
		if(noun in deny_list or len(noun) < 2 or len(noun) > 8 or noun_count < 2):continue
		result_merge_list.append([noun,noun_count])
		pass
	result_merge_list.sort(key=lambda x : x[1], reverse= True) #*[2021-12-14 02:24:19] 배열 그룹의 [1]를 내림차순으로 정렬
	for item in result_merge_list:
		writer.writerow(item)
	f.close()
	print("", end='\n')
	CreateWC(d1)

def CreateWC(d1):
	wc_list = []
	my_file = f"results/Daily_Results_Count/{d1}.csv"
	if os.path.exists(my_file):
		f = open(my_file, mode="r", encoding='utf-8-sig', newline='')
		rdr = csv.reader(f); next(rdr)
		for line in rdr: wc_list.append([line[0],int(line[1])])
		f.close()
	wc = WordCloud(font_path='Pretendard-ExtraBold.ttf',	background_color= 'white',
	width= 1000, height= 1000, max_words= 200, max_font_size= 300, min_font_size= 20)
	wc.generate_from_frequencies(dict(wc_list))
	wc.to_file(f'results/WordCloud/{d1}.png')
	print("Word Cloud Created.")
	#*https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html

#TODO 이제 날짜별, 테마별로 묶어서 결과값 내보내는 과정이 필요함. Date로 검색범위 설정? 웹에서 날짜 고르면 결과 확인 가능하게 만들 수 있을까?
#* 조사 삭제 or 포함 하는부분이 필요함 (https://ratsgo.github.io/korean%20linguistics/2017/03/15/words/)
extract_keyword_count("오로치")
# CreateWC()