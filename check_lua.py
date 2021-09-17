from ntpath import join
import luadata
import re
import csv
import pandas as pd
import os.path

from os import listdir
from os.path import isfile, join, splitext

def LoadData(path):
	code = open(path,'r', encoding='utf-8-sig')
	lines = code.read()
	lines = re.sub('--.+', '', lines)
	lines = lines.replace(' ','')
	lines = lines.replace('\t','')
	lines = lines.replace('\n','')
	lines = lines.replace('/','/')
	code.close()
	data = luadata.unserialize(lines,encoding='utf-8-sig')
	return data

def ExtractUnitScript(path):
	try:
		my_file = 'UnitInfo/TEST1.csv'
		# if os.path.exists(my_file):
		# 	os.remove(my_file)
		# f = open(my_file,'w', newline='')
		# writer = csv.writer(f)
		# writer.writerow(["UnitName","Tag","DictName","StateIndex","EventName","EventIndex","Key","Value"])
		unit_name = splitext(path)[0]
		data = LoadData(join(Script_Path,path))
		f = open("temp.csv",'w', newline='')
		writer = csv.writer(f)
		writer.writerow(["UnitName","Tag","DictName","StateIndex","EventName","EventIndex","Key","Value"])
		StateSet_List = ["m_listAttackStateData","m_listSkillStateData","m_listHyperSkillStateData","m_listHitCriticalFeedBack"]
		StateInfo_List = ["m_StateName"]
		StateInfo_Avoid_List = ["m_NKM_UNIT_STATE_TYPE"]
		state_index = 0
	# for k,v in data:
	# 	if v["StataName"] == "StateName": break
		for k, v in data.items():
			if isinstance(v, list):
				for item in v: #?리스트니까 For문 돌려야됨
					for i, j in item.items():
						list_count = 0
						if isinstance(j, list): #?리스트일 경우 스테이트 이벤트
							tag = "StateEvent"
							list_count = len(j)
							for item in j:
								if isinstance(item, dict):
									for x, y in item.items():
										writer.writerow([unit_name,tag,k,state_index,i,j.index(item)+1,x,y])
								else: 
									writer.writerow([unit_name,tag,k,state_index,i,j.index(item)+1,item,None])
							continue
						elif k in StateSet_List: #?스테이트묶음 종류에 포함될 경우 스테이트묶음
							tag = "StateSet"
						else: #?나머지는 전부 스테이트 정보
							tag = "StateInfo"
						if i in StateInfo_List and k not in StateSet_List : state_index += 1 #! 인포셋에 걸리면 스테이트인덱스 증가
						if i in StateInfo_Avoid_List and k not in StateSet_List : continue
						writer.writerow([unit_name,tag,k,state_index,None,0,i,j])
			else:
				tag = "BasicInfo"
				writer.writerow([unit_name,tag,None,state_index,None,0,k,v]) #?유닛 정보
		f.close()
		all_filenames = ["temp.csv", my_file]
		combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
		combined_csv.to_csv( my_file, index=False, encoding='utf-8-sig')
		os.remove("temp.csv")
	except Exception as e:
		print(path +" : "+ str(e))

def ExtractDamageTemplet(data):
	f = open('TEST1.csv','w', newline='')
	writer = csv.writer(f)
	writer.writerow([None,None,"Key","Value",None,"index"])
	state_index = 0
	# for k,v in data:
	# 	if v["StataName"] == "StateName": break
	for item in data:
		# print(type(item))
		for k, v in item.items():
			if k == "m_DamageTempletName": state_index += 1
			writer.writerow([None,None,k,v,None,None,0,state_index]) #?유닛 정보


Templet_Path = "C:\\DOC_leeseunghwan.dev\\CounterSide\\CODE\\CSClient\\Assets\\ASSET_BUNDLE\\AB_SCRIPT\\AB_SCRIPT_UNIT_DATA\\"
Script_Path = f"{Templet_Path}AB_SCRIPT_UNIT_DATA_UNIT_TEMPLET\\"
Unit_Templet = "LUA_UNIT_TEMPLET_BASE.txt"
Unit1 = "NKM_UNIT_CA_JOO_SHI_YOON.txt"
Unit2 = "NKM_UNIT_S_TIDE_SHOTGUN.txt"

# print(join(Templet_Path,Unit_Templet))
# print(join(Script_Path,Unit1))

onlyfiles = [f for f in listdir(Script_Path) if isfile(join(Script_Path, f) ) and splitext(f)[1] == ".txt"]
# for item in onlyfiles:
# 	print(item)'
ExtractUnitScript(Unit2)
for unit in onlyfiles:
	ExtractUnitScript(unit)


df1 = {}
df2 = {}
df3 = {}
df1 = pd.DataFrame.from_dict(df1, orient='index')
df2 = pd.DataFrame.from_dict(df2, orient='index')
df3 = pd.DataFrame.from_dict(df3, orient='index')

writer = pd.ExcelWriter("LUAsheet.xlsx", engine = 'xlsxwriter')
df1.to_excel(writer, sheet_name = 'x1')
df2.to_excel(writer, sheet_name = 'x2')
df3.to_excel(writer, sheet_name = 'x3')
writer.save()