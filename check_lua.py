import luadata
import re
import csv
import pandas as pd

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
	ExtractUnitTemplet(data)

def ExtractUnitTemplet(data):
	f = open('TEST1.csv','w', newline='')
	writer = csv.writer(f)
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
					elif k in StateSet_List: #?스테이트묶음 종류에 포함될 경우 스테이트묶음
						tag = "StateSet"
					else: #?나머지는 전부 스테이트 정보
						tag = "StateInfo"
					if i in StateInfo_List and k not in StateSet_List : state_index += 1 #! 인포셋에 걸리면 스테이트인덱스 증가
					if i in StateInfo_Avoid_List and k not in StateSet_List : continue
					writer.writerow([tag,k,i,j,list_count,state_index])
		else:
			tag = "BasicInfo"
			writer.writerow([tag,None,k,v,None,state_index]) #?유닛 정보



# NKM_UNIT_CA_JOO_SHI_YOON.txt
# NKM_UNIT_BARCODE_C_SISTER.txt
LoadData("NKM_UNIT_CA_JOO_SHI_YOON.txt")


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