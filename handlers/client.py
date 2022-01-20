from sqlite.sqlighter import SQLighter
import config.config as cf
from create_bot import dp, bot
from aiogram import executor, types, Dispatcher
from keyboards import *


db = SQLighter()

def check_sub_channel(chat_member):
	print(chat_member['status'])
	if chat_member['status'] != 'left':
		return True
	else:
		return False

async def start_bot(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id=cf.CHANNEL_CHAT_ID, user_id=message.from_user.id))
		usname = f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>'
		if(not db.check_user(message.from_user.id)):
			db.create_advertisement_table(message.from_user.id)
			db.create_hash_table(message.from_user.id)
			db.add_user(message.from_user.id, message.from_user.username)
			await bot.send_message(
				chat_id=cf.ADMIN_LOGS_CHAT_ID,
				text="<b>Пользоватеть "+ usname +" запустил бота. </b>",
				parse_mode=types.ParseMode.HTML,
				disable_web_page_preview=True)
			await bot.send_message(
				chat_id=message.from_user.id,
				text="<b>Добро пожаловать, </b>"+usname,
				parse_mode=types.ParseMode.HTML, 
				reply_markup=start_pars_kb,
				disable_web_page_preview=True)
		else:
			await bot.send_message(
				chat_id=message.from_user.id,
				text="<b>Добро пожаловать, </b>"+usname,
				parse_mode=types.ParseMode.HTML, 
				reply_markup=start_pars_kb,
				disable_web_page_preview=True)
	else:
		news_channel = f'<a href="{cf.CHANNEL}">новостей</a>'
		await bot.send_message(
				chat_id=message.from_user.id,
				text="🆘 <b>Вас нет в канале "+news_channel+". Вступите, чтобы пользоваться ботом.</b>",
				parse_mode=types.ParseMode.HTML,
				reply_markup=start_pars_kb)


async def help_command(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id=cf.ADMIN_LOGS_CHAT_ID, user_id=message.from_user.id)):
		commands_text = ''
		for key in cf.ADMIN_COMMANDS:
			commands_text += "\n\n" + key + ' - ' + cf.ADMIN_COMMANDS[key]
		await bot.send_message(
			chat_id=message.from_user.id,
			text="<b>🚀 Команды управления проектом: </b>"+commands_text,
			parse_mode=types.ParseMode.HTML)
	else:
		pass

async def get_users_length(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id=cf.ADMIN_LOGS_CHAT_ID, user_id=message.from_user.id)):
		await bot.send_message(
			chat_id=message.from_user.id,
			text="Количество пользователей бота: " +str(db.get_users_length()),
			parse_mode=types.ParseMode.HTML)
	else:
		pass

def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(start_bot, commands=['start'])
	dp.help_command(help_command, commands=['help'])
	dp.get_users_length(get_users_length, commands=['get_users_length'])
