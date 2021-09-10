from slpp import slpp as lua
import luadata

code = open("NKM_UNIT_BARCODE_C_SISTER.txt",'r', encoding='utf-8-sig')
lines = code.read()
lines = lines.replace(' ','')
lines = lines.replace('\t','')
# lines = lines.replace('\n',' ')
# lines = lines.split(',')
# for line in lines:
	# print(line)


code.close()
print(lines)
# print(type(lines))
# print(type(lua.decode(lines)))
# print(lua.decode(lines))
# data = luadata.write("NKM_UNIT_BARCODE_C_SISTER.txt",'r', encoding="utf-8", indent="\t", prefix="return ")

# data = luadata.read("NKM_UNIT_BARCODE_C_SISTER.txt", encoding="utf-8")
luadata.unserialize(code, encoding="utf-8", multival=False)