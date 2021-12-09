import os.path
from os import listdir
from os.path import isfile, join, splitext, exists
import pandas as pd
import re
import csv

def extract_keyword_count():
	# csv_list = [join('results\\',f) for f in listdir('results\\') ]
	csv_list = ['results\\All_result.csv']
	
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
	
	result_noun_list = ''.join(all_list) #*스트링 하나로 결합
	result_noun_list = re.sub("\!|\'|\?|\)|\(||\.|(emoticon)", "", result_noun_list) #*결합된 스트링에서 특정 문자 제외
	result = result_noun_list #*제외된 문자로 적용
	
	result_noun_list = result_noun_list.split(' ') #* 스트링을 다시 LIST로 결합
	result_noun_list = list(set(result_noun_list)) #*결합된 스트링에서 중복값 삭제
	
	my_file = 'test.csv'
	if os.path.exists(my_file):
		os.remove(my_file)
	f = open(my_file, mode="w", encoding='utf-8-sig', newline='')
	writer = csv.writer(f)
	writer.writerow(["Keyword","count"])
	
	deny_list = []
	list_file = "Deny_List.csv"
	if os.path.exists(list_file):
		csvfile = open(list_file,'r', encoding='utf-8-sig', newline='')
		rdr = csv.reader(csvfile)
		for line in rdr:
			deny_list.append(line[0])
	
	for x in range(len(result_noun_list)):
		if(result_noun_list[x] in deny_list or len(result_noun_list[x]) < 2 ):continue
		writer.writerow([result_noun_list[x],result.count(result_noun_list[x])])