import csv
import os.path
import pandas as pd

def save_to_file(contents, keyword):
	# keyword = re.sub("[\/:*?\"<>|]", "", keyword) #[2021-12-07 01:21:15] 파일 이름 수정
	my_file = f"results/{keyword}.csv"
	temp_file = f"results/{keyword}_temp.csv"
	if os.path.exists(my_file):
		#*머지 시퀀스

		file = open(temp_file, mode="w", encoding='utf-8-sig', newline='')
		write_row(contents,file)
		
		all_filenames = [temp_file, my_file]
		combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
		combined_csv = combined_csv.drop_duplicates(subset = 'index',keep = 'first')
		combined_csv = combined_csv.sort_values(by=['index'], ascending=False)
		combined_csv.to_csv( my_file, index=False, encoding='utf-8-sig')
		
		os.remove(temp_file)
		print("\nScrap Complete.")
		return
	else:
		#*신규파일 생성 시퀀스
		file = open(my_file, mode="w", encoding='utf-8-sig', newline='')
		write_row(contents,file)
		print(f"\n{file} is Created.")
		return

def write_row(contents, file):
	writer = csv.writer(file)
	writer.writerow(["index", "user", "title", "content", "comment", "link", "date", "view", "rate", "comment_count"])
	for content in contents:
		writer.writerow(list(content.values()))
	file.close()