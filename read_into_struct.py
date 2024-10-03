from ctypes import Structure as struct, c_uint as i4, c_ushort as i2, c_char as i1, sizeof
from io import BytesIO

class DataHeader(struct):
	_pack_ = 1
	_fields_ = [
		("Size", i4),
		("CRC", i4),
		("Version", i2)
	]
_fields = lambda type: lambda arr: list((name, type) for name in arr)

i4_fields = lambda arr: _fields(i4)(arr)
i2_fields = lambda arr: _fields(i2)(arr)
i1_fields = lambda arr: _fields(i1)(arr)

class DataOffset(struct):
	_pack_ = 1
	_fields_ = i4_fields(
		["BaseInfo", "FSkill", "LSkill", "Task", "Item", "Quick", "Event", "Trigger", "StallInfo", "Recipe", "CustomData"]
	) + [("reserved", i1 * 20)]

class BaseInfo(struct):
	_pack_ = 1
	_fields_ = [
		("ServiceID", i4), 
		("Name", i1 * 32), 
		("RolePrimKindNo", i1), 
		("UseRevive", i1),
		("TongName", i1 * 32),
		("AccName", i1 * 32),
	] + i1_fields(
		["LastSect", "FightMode", "BoxPageCount", "Genre"]
	) + i4_fields(
		["IBBuyIndex", "SectRole", "RevivalID", "RevivalX", "RevivalY", "EnterGameID", "EnterGameX", "EnterGameY", "PartnerTemplateID", "PartnerExp", "PartnerRandSeed"]
	) + [
		("PartnerName", i1 * 16),
		("PartnerLevel", i1),
		("PartnerType", i1),
		("PartnerCode", i1*2),
		("SaveMoney", i4),
		("Money", i4),
		("FightLevel", i2),
		("TransLife", i2)
	] + i4_fields(
		["FightExp", "Power", "Agility", "Outer", "Inside", "Observe", "Prop", "MaxLife", "MaxStamina", "MaxInner", "CurLife", "CurStamina", "CurInner", "OuterWound", "InnerWound", "PKValue", "FinishGame", "TongID", "Repute", "OfflineLiveLeftTime", "LastLoginTime"]
	) + i2_fields(
		["HeadImage", "ReLiveTime"]
	) + i4_fields(
		["LastDayBeginTime", "GainRepute", "LastHour", "WorldStat", "CreateTime"]
	) + [
		("Titles", i4 * 8),
		("CurTitle", i4),
		("MoodPhrase", i1 * 32)
	] + i4_fields(
		["ExercisePKCount", "ExercisePKWinCount", "Popur"]
	) + i2_fields(
		["CapType", "ArmorType", "LowBodyType", "MaskType", "ClothType", "OutfootType", "WeaponType", "HorseType"]
	) + i4_fields(
		["DoubleExpTime", "DoubleExpCount", "RoleSpecialFlag"]
	) + [
		("KillNpcCount", i2),
		("ConErrorCount", i1),
		("EatDoubleTimes", i1),
		("DoubleWeakBeginTime", i4)
	] + i2_fields(
		["LittleYinPiao", "BigYinPiao", "LittleYinPiaoIncoming", "LittleYinPiaoOutgoing", "BigYinPiaoIncoming", "BigYinPiaoOutgoing", "PunishTime"]
	) + [
		("LikeUsePluginNum", i1),
		("PrisonLeftTime", i2),
		("BePrisonedNum", i1),
		("FightExpHigh", i2)
	]

class SkillData(struct):
	_fields_ = i2_fields(
		["SkillID", "SkillLevel"]
	)

class TaskData(struct):
	_fields_ = i4_fields(
		["TaskID", "TaskValue"]
	)

class LSkillData(struct):
	_pack_ = 1
	_fields_ = i1_fields(
		["Gene", "SkillID", "CurLevel", "MaxLevel"]
	) + [
		("CurExp", i4),
		("IsMainSkill", i1),
		("reserved", i1 * 5)
	]

class ItemData(struct):
	_pack_ = 1
	_fields_ = i1_fields(
		["DataSize", "EquipClassCode", "Local", "X", "Y", "Identify", "DetailType", "Level"]
	) + [
		("ParticularType", i2),
		("Socket", i2 * 3),
		("SocketInfo", i2 * 3),
		("MaxDurability", i2),
		("Durability", i2),
		("GenTime", i4),
		("Version", i2),
		("BitStatus", i2),
		("Param1", i4),
		("Param2", i4),
		("CurLingqi", i2),
		("MaxLingqi", i2),
		("BelongPlayerName", i1 * 17)
	]

class CustomDataHeader(struct):
	_fields_ = i2_fields(["Signature", "Size"])

class StallDataHeader(struct):
	_pack_ = 1
	_fields_ = [
		("HeaderSize", i4),
		("Version", i1),
		("StallAdv", i1 * 32),
		("StallItemSize", i2),
		("StallItemCount", i1)
	]

class StallItemData(struct):
	_pack_ = 1
	_fields_ = [
		("X", i1),
		("Y", i1),
		("Price", i4)
	]

class Data:
	def __init__(self, data):
		self.header = DataHeader()
		header_data = data[:10]
		with BytesIO(header_data) as f:
			sz = f.readinto(self.header)

		self.offsets = DataOffset()
		body_data = data[10:]
		with BytesIO(body_data) as f:
			sz = f.readinto(self.offsets)
		
		self.base_info = BaseInfo()
		base_info_data = data[self.offsets.BaseInfo:]
		with BytesIO(base_info_data) as f:
			sz = f.readinto(self.base_info)

		fskill_info_data = data[self.offsets.FSkill:]
		fskill_count = i4()
		with BytesIO(fskill_info_data) as f:
			sz = f.readinto(fskill_count)
		self.fskills = []
		for i in range(fskill_count.value):
			self.fskills.append(SkillData())
			fskill_info_data = fskill_info_data[sz:]
			with BytesIO(fskill_info_data) as f:
				sz = f.readinto(self.fskills[-1])

		lskill_info_data = data[self.offsets.LSkill:]
		lskill_count = i4()
		with BytesIO(lskill_info_data) as f:
			sz = f.readinto(lskill_count)
		self.lskills = []
		for i in range(lskill_count.value):
			self.lskills.append(LSkillData())
			lskill_info_data = lskill_info_data[sz:]
			with BytesIO(lskill_info_data) as f:
				sz = f.readinto(self.lskills[-1])


		task_data = data[self.offsets.Task:]
		task_count = i4()
		with BytesIO(task_data) as f:
			sz = f.readinto(task_count)
		self.tasks = []
		for i in range(task_count.value):
			self.tasks.append(TaskData())
			task_data = task_data[sz:]
			with BytesIO(task_data) as f:
				sz = f.readinto(self.tasks[-1])

		item_data = data[self.offsets.Item:]
		item_count = i4()
		with BytesIO(item_data) as f:
			sz = f.readinto(item_count)
		self.items = []
		for i in range(item_count.value):
			self.items.append(ItemData())
			item_data = item_data[sz:]
			with BytesIO(item_data) as f:
				sz = f.readinto(self.items[-1])

		recipe_data = data[self.offsets.Recipe:]
		recipe_count = i4()
		with BytesIO(recipe_data) as f:
			sz = f.readinto(recipe_count)
		self.recipes = []
		for i in range(recipe_count.value):
			self.recipes.append(i4())
			recipe_data = recipe_data[sz:]
			with BytesIO(recipe_data) as f:
				sz = f.readinto(self.recipes[-1])

		custom_data = data[self.offsets.CustomData:]
		self.custom_data = []
		while True:
			custom_header = CustomDataHeader()
			with BytesIO(custom_data) as f:
				sz = f.readinto(custom_header)
			
			if custom_header.Signature == 0 or custom_header.Size == 0:
				break
			d = []
			for i in range(custom_header.Size):
				with BytesIO(custom_data[i:]) as f:
					t = i1()
					f.readinto(t)
					d.append(t)
			custom_data = custom_data[custom_header.Size:]
			self.custom_data.append({
				"header": custom_header,
				"data": d
			})

player = None
with open("AnalyzeJx2Role.dat", "rb") as f:
	#record = DataHeader()
	#f.readinto(record)
	data = f.read()
	player = Data(data)

