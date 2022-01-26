from sqlite.sqlighter import SQLighter
import config.config as cf
from create_bot import dp, bot

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards import *

photo = open('mainmenu.jpg', 'rb')

def check_sub_channel(chat_member):
	if chat_member['status'] != 'left':
		return True
	else:
		return False

async def echo(call: types.CallbackQuery):
	if call.data == "parser_sites":
		await bot.edit_message_caption(
			chat_id=call.message.chat.id,
			caption="<b>🌍 Выберите страну, где вы хотите найти объявления.</b>",
			parse_mode=types.ParseMode.HTML, 
			reply_markup=show_countries_kb
			)
# 	if check_sub_channel(await bot.get_chat_member(chat_id=cf.CHANNEL_CHAT_ID, user_id=message.from_user.id)):
# 		db = SQLighter()
# 		if call.data == "parser_sites":
# 			if db.len_hash_data(message.from_user.id) > 0:
# 				await bot.send_message(
# 					chat_id=message.from_user.id,
# 					text="‼️<b>У вас есть непросмотренные объявлния. Нажмите на соответсвующую кнопку, чтобы посмотреть или удалить их.</b>",
# 					parse_mode=types.ParseMode.HTML, 
# 					reply_markup=hash_kb)
# 			else:
# 				await bot.send_message(
# 					chat_id=message.from_user.id,
# 					text="<b>🌍 Выберите страну, где вы хотите найти объявления.</b>",
# 					parse_mode=types.ParseMode.HTML, 
# 					reply_markup=show_countries_kb)
# 		elif message.text == "♻️ Ранее просмотренные объявления":
# 			if db.len_advertisement_data(message.from_user.id) > 0:
# 				# Ранее добавленные
# 				previously_added_kb = types.InlineKeyboardMarkup(resize_keyboard=True)
# 				for key in cf.COUNTRIES_SITES:
# 					for cnt in cf.COUNTRIES_SITES[key]:
# 						callback_data = "previously"+cnt
# 						db = SQLighter()
# 						length = str(db.get_len_previously_platfrom(message.from_user.id, cnt))
# 						if int(length) > 0:
# 							if length[-1] == "1" and length != "11":
# 								button = key[0:2] + cnt + " — " + length + " объявление"
# 							elif length[-1] in ("2", "3", "4") and length != "12" and length != "13" and length != "14":
# 								button = key[0:2] + cnt + " — " + length + " объявления"
# 							elif length[-1] in ("0","5", "6", "7", "8", "9") or length == "11" or length == "12" or length == "14":
# 								button = key[0:2] + cnt + " — " + length + " объявлений"
# 							item = types.InlineKeyboardButton(button, callback_data=callback_data)
# 							previously_added_kb.add(item)
# 						else:
# 							pass	

# 				await bot.send_message(
# 					chat_id=message.from_user.id,
# 					text="<b>Выберите площадку на которой хотите посмотреть ранее добавленные объявления.</b>",
# 					parse_mode=types.ParseMode.HTML, 
# 					reply_markup=previously_added_kb)
# 			else:
# 				await bot.send_message(
# 					chat_id=message.from_user.id,
# 					text="<b>Вы пока не добавили ни одного объявления.</b>",
# 					parse_mode=types.ParseMode.HTML,)

# 	else:
# 		news_channel = f'<a href="{cf.CHANNEL}">новостей</a>'
# 		await bot.send_message(
# 				chat_id=message.from_user.id,
# 				text="🆘 <b>Вас нет в канале "+news_channel+". Вступите, чтобы пользоваться ботом.</b>",
# 				parse_mode=types.ParseMode.HTML,
# 				reply_markup=start_pars_kb)




def register_handlers_other(dp : Dispatcher):
	dp.register_callback_query_handler(echo, lambda callback_query: True)
	
			
