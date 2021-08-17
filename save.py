import csv
import os.path
import pandas as pd

def save_to_file(contents, keyword):
    my_file = f"results/{keyword}.csv"
    if os.path.exists(my_file):
        #머지 시퀀스

        file = open("temp.csv", mode="w", encoding='utf-8-sig', newline='')
        write_row(contents,file)
        
        all_filenames = ["temp.csv", f"results/{keyword}.csv"]
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ]).sort_values(by=['index'], ascending=False)
        
        # combined_csv = pd.read_csv("temp.csv", encoding='utf-8-sig')
        # combined_csv.to_csv(f"results/{keyword}.csv", index=False, mode='a', encoding='utf-8-sig', header=False)

        combined_csv = combined_csv.drop_duplicates(subset = 'index',keep = 'first')
        combined_csv.sort_values(by=['index'], ascending=False)

        combined_csv.to_csv( f"results/{keyword}.csv", index=False, encoding='utf-8-sig')
        
        return
    else:
        #신규파일 생성 시퀀스
        file = open(f"results/{keyword}.csv", mode="w", encoding='utf-8-sig', newline='')
        write_row(contents,file)
        print(f"{file} is Created.")
        return

def write_row(contents, file):
    writer = csv.writer(file)
    writer.writerow(["index", "user", "title", "content", "comment", "link", "date", "veiw", "rate"])
    for content in contents:
        writer.writerow(list(content.values()))
    file.close()