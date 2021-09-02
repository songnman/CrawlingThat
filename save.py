import csv
import os.path
import pandas as pd
import gspread
import gspread_dataframe as gd

# gc = gspread.oauth()

def save_to_file(contents, keyword):
	my_file = f"results/{keyword}.csv"
	if os.path.exists(my_file):
		#*머지 시퀀스

		file = open(f"{keyword}_temp.csv", mode="w", encoding='utf-8-sig', newline='')
		write_row(contents,file)
		
		all_filenames = [f"{keyword}_temp.csv", my_file]
		combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
		combined_csv = combined_csv.drop_duplicates(subset = 'index',keep = 'first')
		combined_csv = combined_csv.sort_values(by=['index'], ascending=False)
		combined_csv.to_csv( my_file, index=False, encoding='utf-8-sig')
		
		# ws = gc.open("CrawlingThat").worksheet("TEST1")
		# existing = gd.get_as_dataframe(ws)
		gd.set_with_dataframe(ws, combined_csv)
		
		os.remove(f"{keyword}_temp.csv")
		print("Scrap Complete.")
		return
	else:
		#*신규파일 생성 시퀀스
		file = open(my_file, mode="w", encoding='utf-8-sig', newline='')
		write_row(contents,file)
		print(f"{file} is Created.")
		return

def write_row(contents, file):
	writer = csv.writer(file)
	writer.writerow(["index", "user", "title", "content", "comment", "link", "date", "view", "rate", "comment_count"])
	for content in contents:
		writer.writerow(list(content.values()))
	file.close()