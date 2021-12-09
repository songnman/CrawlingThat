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

# print(' '.join(all_list).split(' '))
myset = set(all_list)
result_noun_list = list(myset)
result_noun_list = ''.join(all_list)
result_noun_list = re.sub("\!|\'|\?|\)|\(|\.", "", result_noun_list)

result = result_noun_list
result_noun_list = result_noun_list.split(' ')

print(result.count(result_noun_list[25]))

my_file = 'test.csv'
f = open(my_file,'w', newline='', encoding='utf-8-sig')
writer = csv.writer(f)
for x in range(len(result_noun_list)):
	writer.writerow([result_noun_list[x],result.count(result_noun_list[x])])