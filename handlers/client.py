from sqlite.sqlighter import SQLighter
import config.config as cf
from create_bot import dp, bot
from aiogram import executor, types, Dispatcher
from keyboards import *
from datetime import datetime, timedelta
from aiogram.types import InputFile

db = SQLighter()
file_path = "mainmenu.jpg"


def check_sub_channel(chat_member):
	if chat_member['status'] != 'left':
		return True
	else:
		return False

async def start_bot(message: types.Message):
	file = InputFile(file_path)
	if check_sub_channel(await bot.get_chat_member(chat_id=cf.CHANNEL_CHAT_ID, user_id=message.from_user.id)):
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
			await bot.send_photo(chat_id=message.from_user.id, photo=file, caption=f"🆔 <b>Ваш ид:</b> <code>{message.from_user.id}</code>", parse_mode=types.ParseMode.HTML, reply_markup=main_kb)
		else:
			await bot.send_photo(chat_id=message.from_user.id, photo=file, caption=f"🆔 <b>Ваш ид:</b> <code>{message.from_user.id}</code>", parse_mode=types.ParseMode.HTML, reply_markup=main_kb)
	else:
		news_channel = f'<a href="{cf.CHANNEL}">новостей</a>'
		await bot.send_message(
				chat_id=message.from_user.id,
				text="🆘 <b>Вас нет в канале "+news_channel+". Вступите, чтобы пользоваться ботом.</b>",
				parse_mode=types.ParseMode.HTML)

# /help
async def help_command(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id=cf.ADMIN_LOGS_CHAT_ID, user_id=message.from_user.id)):
		commands_text = ''
		for key in cf.ADMIN_COMMANDS:
			commands_text += "\n\n" + key + ' - ' + cf.ADMIN_COMMANDS[key]
		await bot.send_message(
			chat_id=cf.ADMIN_LOGS_CHAT_ID,
			text="<b>🚀 Команды управления проектом: </b>"+commands_text,
			parse_mode=types.ParseMode.HTML)
	else:
		pass


# Получить количество пользователей бота
async def get_users_length(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id=cf.ADMIN_LOGS_CHAT_ID, user_id=message.from_user.id)):
		await bot.send_message(
			chat_id=cf.ADMIN_LOGS_CHAT_ID,
			text="Количество пользователей бота: " +str(db.get_users_length()),
			parse_mode=types.ParseMode.HTML)
	else:
		pass


# Обновить время подписки 
async def update_subscriber_time(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id=cf.ADMIN_LOGS_CHAT_ID, user_id=message.from_user.id)):
		try:
			arguments = message.get_args()
			if arguments:
				user_id = arguments.split(":")[0]
				new_date = arguments.split(":")[1]
				date = new_date.split(".")
				new_datetime = datetime(int(date[2]), int(date[1]), int(date[0]))
				country = arguments.split(":")[2]
				db.update_subsc_time(user_id, new_datetime, country)
				await bot.send_message(
						chat_id=cf.ADMIN_LOGS_CHAT_ID,
						text=f"<b>✨Подписка обновлена\n\nID пользователя: </b><code>{user_id}</code>\n\n<b>Страна: </b><code>{country}</code>\n\n<b>До: </b><code>{new_date}</code>",
						parse_mode=types.ParseMode.HTML)
			else:
				await bot.send_message(
					chat_id=cf.ADMIN_LOGS_CHAT_ID,
					text="♻️<b>Введите команду корректно</b>",
					parse_mode=types.ParseMode.HTML)
		except Exception as e:
			await bot.send_message(
					chat_id=cf.ADMIN_LOGS_CHAT_ID,
					text="♻️<b>Введите команду корректно</b>",
					parse_mode=types.ParseMode.HTML)
	else:
		pass		

# Получить ID пользователя
async def get_user_id(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id=cf.ADMIN_LOGS_CHAT_ID, user_id=message.from_user.id)):
		try:
			username = message.get_args().split("@")[1]
			print(username)
			if username:
				user_id = db.get_user_id(username)
				await bot.send_message(
					chat_id=cf.ADMIN_LOGS_CHAT_ID,
					text=f"<b>🔑 ID пользователя @</b>{username}<b> — </b><code>{user_id}</code>",
					parse_mode=types.ParseMode.HTML)
			else:
				await bot.send_message(
					chat_id=cf.ADMIN_LOGS_CHAT_ID,
					text="♻️<b>Введите команду корректно</b>",
					parse_mode=types.ParseMode.HTML)
		except Exception as e:
			await bot.send_message(
					chat_id=cf.ADMIN_LOGS_CHAT_ID,
					text="♻️<b>Введите команду корректно</b>",
					parse_mode=types.ParseMode.HTML)
	else:
		pass
	
# Сообщение всем
async def alert_all(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id=cf.ADMIN_LOGS_CHAT_ID, user_id=message.from_user.id)):
		errors_count = 0
		try:
			msg = message.get_args()
			if msg:
				users = db.get_all_users_id()
				for user in users:
					user_id = int(user[0])
					try:
						await bot.send_message(
							chat_id=user_id,
							text=msg,
							parse_mode=types.ParseMode.HTML)
						errors_count += 1
					except:
						pass
					
				await bot.send_message(
					chat_id=cf.ADMIN_LOGS_CHAT_ID,
					text=f"Cообщение отправлено {errors_count} юзерам",
					parse_mode=types.ParseMode.HTML)	
			else:	
				await bot.send_message(
					chat_id=cf.ADMIN_LOGS_CHAT_ID,
					text="♻️<b>Введите команду корректно</b>",
					parse_mode=types.ParseMode.HTML)
		except Exception as e:
			import traceback
			print(traceback.format_exc())
			await bot.send_message(
					chat_id=cf.ADMIN_LOGS_CHAT_ID,
					text="♻️<b>Введите команду корректно</b>",
					parse_mode=types.ParseMode.HTML)
	else:
		pass		

	
def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(start_bot, commands=['start'])
	dp.register_message_handler(help_command, commands=['help'])
	dp.register_message_handler(get_users_length, commands=['get_users_length'])
	dp.register_message_handler(update_subscriber_time, commands=['update_subscriber_time'])
	dp.register_message_handler(get_user_id, commands=['get_user_id'])
	dp.register_message_handler(alert_all, commands=['alert'])
