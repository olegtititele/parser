from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import *
from sqlite.sqlighter import SQLighter
from create_bot import dp, bot
import time

class DynamicLoading(object):
	def __init__(self):
# 		self.user_id = user_id
		self.loopflag = True
# 		self.iy = 0
		
	async def stop_loop(self, call, state: FSMContext):
# 		global loopflag
# 		loopflag = 'False'+str(call.from_user.id)
		self.a.append(call.from_user.id)
		global iy
		iy = 20
# 		async with state.proxy() as data:
# 			total_adv = data['adv_count']
# 		db = SQLighter()
# 		length = str(db.len_hash_data(call.from_user.id))	
# 		if length[-1] == "1" and length != "11":
# 			line = "✅<b>Поиск объявлений завершен. Получено "+length+ " объявление из "+ str(total_adv) + "</b>"
# 		elif length[-1] in ("2", "3", "4") and length != "12" and length != "13" and length != "14":
# 			line = "✅<b>Поиск объявлений завершен. Получено "+length+ " объявления из "+ str(total_adv) + "</b>"
# 		elif length[-1] in ("0","5", "6", "7", "8", "9") or length == "11" or length == "12" or length == "14":
# 			line = "✅<b>Поиск объявлений завершен. Получено "+length+ " объявлений из "+ str(total_adv) + "</b>"
# 		await call.message.edit_text(text=line, parse_mode=types.ParseMode.HTML, reply_markup=just_parsed_kb)
# 		await state.finish()

	async def start_loop(self, call, state: FSMContext):
# 		global loopflag
# 		loopflag = 'True'+str(call.from_user.id)
		async with state.proxy() as data:
			total_adv = data['adv_count']
		stop_btn = "stop_parser"+str(call.from_user.id)
		stop_kb = InlineKeyboardMarkup()
		stop_kb.add(InlineKeyboardButton(text="❌ Остановить парсер", callback_data=stop_btn))
		coursor = '🌕🌖🌗🌘🌑🌒🌓🌔'
		global iy
		iy = 0
		while self.loopflag:	
			for i in coursor:
				db = SQLighter()
				length = str(db.len_hash_data(call.from_user.id))
				if int(length) == total_adv or iy == 20:
					if length[-1] == "1" and length != "11":
						line = "✅<b>Поиск объявлений завершен. Получено "+length+ " объявление из "+ str(total_adv) + "</b>"
					elif length[-1] in ("2", "3", "4") and length != "12" and length != "13" and length != "14":
						line = "✅<b>Поиск объявлений завершен. Получено "+length+ " объявления из "+ str(total_adv) + "</b>"
					elif length[-1] in ("0","5", "6", "7", "8", "9") or length == "11" or length == "12" or length == "14":
						line = "✅<b>Поиск объявлений завершен. Получено "+length+ " объявлений из "+ str(total_adv) + "</b>"
					await state.finish()
					return await call.message.edit_text(text=line, parse_mode=types.ParseMode.HTML, reply_markup=just_parsed_kb)
# 					self.loopflag == False
# 					break
				else:
					load = "<b>" + i + " Поиск объявлений в процессе</b>"
					if length[-1] == "1" and length != "11":
						line = "<b>Получено "+length+ " объявление из "+ str(total_adv) + "</b>"
					elif length[-1] in ("2", "3", "4") and length != "12" and length != "13" and length != "14":
						line = "<b>Получено "+length+ " объявления из "+ str(total_adv) + "</b>"
					elif length[-1] in ("0","5", "6", "7", "8", "9") or length == "11" or length == "12" or length == "14":
						line = "<b>Получено "+length+ " объявлений из "+ str(total_adv) + "</b>"
					await call.message.edit_text(text=load+"\n\n"+line, parse_mode=types.ParseMode.HTML, reply_markup=stop_kb)
					time.sleep(0.5)
