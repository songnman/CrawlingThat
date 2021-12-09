import os.path
from os import listdir
from os.path import isfile, join, splitext, exists
import pandas as pd
import re
import csv

csv_list = [join('results\\',f) for f in listdir('results\\') ]
# print(csv_list)


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

# all_list = title_list + content_list2 + comment_list
all_list = title_list

result_noun_list = ''.join(all_list) #*스트링 하나로 결합
result_noun_list = re.sub("\!|\'|\?|\)|\(|\.", "", result_noun_list) #*결합된 스트링에서 특정 문자 제외
result = result_noun_list #*제외된 문자로 적용

result_noun_list = result_noun_list.split(' ') #* 스트링을 다시 LIST로 결합
result_noun_list = list(set(result_noun_list)) #*결합된 스트링에서 중복값 삭제

my_file = 'test.csv'
if os.path.exists(my_file):
	os.remove('test.csv')
f = open(my_file,'w', newline='', encoding='utf-8-sig')
writer = csv.writer(f)

for x in range(len(result_noun_list)):
	writer.writerow([result_noun_list[x],result.count(result_noun_list[x])])