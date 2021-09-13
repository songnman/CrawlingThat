import luadata
import re
import csv
import pandas as pd


path = "NKM_UNIT_BARCODE_C_SISTER.txt"
path = "NKM_UNIT_CA_JOO_SHI_YOON.txt"
code = open(path,'r', encoding='utf-8-sig')
lines = code.read()
lines = re.sub('--.+', '', lines)
lines = lines.replace(' ','')
lines = lines.replace('\t','')
lines = lines.replace('\n','')
lines = lines.replace('/','/')
code.close()

# print(lines)
data = luadata.unserialize(lines,encoding='utf-8-sig')
# print(data)
df1 = {}
df2 = {}
df3 = {}
f = open('TEST1.csv','w', newline='')
writer = csv.writer(f)
for k, v in data.items():
	if isinstance(v, list):
		for item in v:
			for i, j in item.items():
				if isinstance(j, list):
					for item in j:
						for x, y in item.items():
								# print(type(y))
							if isinstance(y, list):
								for item in y:
									print(type(item))
									writer.writerow([k,i,x,item])
							else:
								writer.writerow([k,i,x,y])
				else:
					writer.writerow([k,i,j,None])
	else:
		writer.writerow([k,v,None,None])

# dict1 = data
# df = pd.DataFrame(data=dict1, index=[0])
# df = (df.T)
# print (df)
# df.to_excel('dict1.xlsx')

df1 = pd.DataFrame.from_dict(df1, orient='index')
df2 = pd.DataFrame.from_dict(df2, orient='index')
df3 = pd.DataFrame.from_dict(df3, orient='index')


writer = pd.ExcelWriter("LUAsheet.xlsx", engine = 'xlsxwriter')
df1.to_excel(writer, sheet_name = 'x1')
df2.to_excel(writer, sheet_name = 'x2')
df3.to_excel(writer, sheet_name = 'x3')
writer.save()