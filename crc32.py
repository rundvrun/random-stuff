from ctypes import cdll, c_ubyte, c_uint, POINTER, c_char_p, c_char, cast
lib = cdll.LoadLibrary("./CRC32.dll")

#lib.crc32_little.argtypes = [c_uint, POINTER(c_char), c_uint]
#crc32_jx2 = lambda data: c_uint(lib.crc32_little(0, data, len(data))).value
#crc32_jx2 = lambda data: lib.crc32_little(0, cast(data, POINTER(c_char)), len(data))
#crc32_jx2 = lambda data: lib.crc32_little(0, cast(data, c_char_p), len(data))

lib.crc32_little.restype = c_uint
crc32_jx2 = lambda data: lib.crc32_little(0, data, len(data))

lib.db_user.restype = c_char_p
lib.db_host.restype = c_char_p
lib.db_db.restype = c_char_p

f = open("AnalyzeJx2Role.dat", "rb")
data = f.read()
f.close()
sz = len(data)

#crc32 = lib.crc32_little(0, data[8:], int.from_bytes(data[:4], "little") - 8)

main_data = data[8:]
crc32 = lib.crc32_little(0, main_data, len(main_data))

#print(crc32)

mutable_data = bytearray(data)
mutable_data[0] = data[0] + 1
mutable_data[0] = data[0]
#print(data == bytes(mutable_data))

from sqlalchemy import create_engine
import pymysql
charset = "utf8"
host = lib.db_host().decode(charset)
port = lib.db_port()
db = lib.db_db().decode(charset)
user = lib.db_user().decode(charset)
passwd = lib.db_pass()
engine = create_engine(f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset={charset}")
with engine.connect() as con:
	d = con.execute("SELECT FullInfo FROM role")

import re

TCVN3TAB = "µ¸¶·¹¨»¾¼½Æ©ÇÊÈÉË®ÌÐÎÏÑªÒÕÓÔÖ×ÝØÜÞßãáâä«åèæçé¬êíëìîïóñòô-õøö÷ùúýûüþ¡¢§£¤¥¦"  # NOQA
TCVN3TAB = [ch for ch in TCVN3TAB]

UNICODETAB = "àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵĂÂĐÊÔƠƯ"   # NOQA
UNICODETAB = [ch for ch in UNICODETAB]

r = re.compile("|".join(TCVN3TAB))
replaces_dict = dict(zip(TCVN3TAB, UNICODETAB))

#rv = re.compile("|".join(UNICODETAB))
#rv_relplaces_dict = dict(zip(UNICODETAB,TCVN3TAB))

def TCVN3_to_unicode(tcvn3str):
	return r.sub(lambda m: replaces_dict[m.group(0)], tcvn3str)


def unicode_to_TCVN3(unicodestr):
	return r.sub(lambda m: replaces_dict[m.group(0)], unicodestr)

#uni_tcvn = {x:y for (x, y) in list(zip(UNICODETAB, TCVN3TAB))}
#tcvn_uni = {x:y for (x, y) in list(zip(TCVN3TAB, UNICODETAB))}
tcvn_uni = dict(zip(TCVN3TAB, UNICODETAB))
uni_tcvn = dict(zip(UNICODETAB, TCVN3TAB))

def _TCVN3_to_unicode(tcvn3str):
	return "".join(map(lambda x: tcvn_uni[x] if x in tcvn_uni else x, tcvn3str))

def _unicode_to_TCVN3(unicodestr):
	return "".join(map(lambda x: uni_tcvn[x] if x in uni_tcvn else x, unicodestr))
bytes(_unicode_to_TCVN3("Đường môn nhậm hiệp"), encoding='utf8').decode("utf8")
bytearray(_TCVN3_to_unicode('§-êng m«n nhËm hiÖp'), encoding="utf8").decode("utf8")

from struct import unpack, calcsize, pack
fmt = "<2IH4I"
sz = calcsize(fmt)

for row in d:
	data = row[0]
	ddd = unpack(fmt, data[:sz])
	print(ddd)
	print(pack(fmt, *ddd) == data[:sz])
	tmp = data[8:]
	c = (c_ubyte * len(tmp))(*tmp)
	#for i in range(len(c)): c[i] = tmp[i]
	#print(data[4:8])
	crc_db = int.from_bytes(data[4:8], 'little')
	crc_db1 = unpack("<2I", data[:8])[1]
	print(crc_db1 == crc_db)
	crc = crc32_jx2(c)
	#if crc < 0: crc = 0xffffffff + crc + 1
	print(hex(crc_db))
	print(hex(crc))
	print(crc_db == crc)