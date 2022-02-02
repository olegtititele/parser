from sqlite.sqlighter import SQLighter
import config.config as cf
from create_bot import dp, bot
from keyboards import *
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile

from datetime import datetime, timedelta
import time

file_path = "mainmenu.jpg"



class Form(StatesGroup):
	country = State()
	link = State()
	adv_count = State()
	seller_adv = State()
	business = State()
	adv_reg_data = State()
	reg_seller_data = State()
	repeated_number = State()

class Filters(StatesGroup)	:
	whatsapp_text = State()
	page_start = State()

def check_sub_channel(chat_member):
	if chat_member['status'] != 'left':
		return True
	else:
		return False
	
# @dp.message_handler()
async def back_button(message: types.Message):
	file = InputFile(file_path)
	if message.text == "🔙 Вернуться в меню":
		await bot.send_photo(chat_id=message.from_user.id, photo=file, caption=f"🆔 <b>Ваш ид:</b> <code>{message.from_user.id}</code>", parse_mode=types.ParseMode.HTML, reply_markup=main_kb)

async def echo(call: types.CallbackQuery, state: FSMContext):
	file = InputFile(file_path)
	db = SQLighter()
	if check_sub_channel(await bot.get_chat_member(chat_id=cf.CHANNEL_CHAT_ID, user_id=call.from_user.id)):
		for key in cf.COUNTRIES_SITES:
			if call.data == key:
				for cnt in cf.COUNTRIES_SITES[key]:
					show_sites_kb = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
					item = types.InlineKeyboardButton(cnt, callback_data=cnt)
					show_sites_kb.add(item)
				show_sites_kb.add(back_btn)	
				await bot.edit_message_caption(
							chat_id=call.message.chat.id,
							message_id = call.message.message_id,
							caption="<b>🌐 Выберите площадку, где вы хотите найти объявления.</b>",
							parse_mode=types.ParseMode.HTML, 
							reply_markup=show_sites_kb
							)

		for key in cf.COUNTRIES_SITES:
			for cnt in cf.COUNTRIES_SITES[key]:
				if call.data == cnt:
					if(not db.check_subscriber(cnt, call.from_user.id)):
						db.add_subscriber(cnt, call.from_user.id)
						await create_price_keyboard(call, cnt)
					else:
						if db.get_subscriber_time(cnt, call.from_user.id) <= datetime.now():
							await create_price_keyboard(call, cnt)
						else:
							await bot.edit_message_caption(
							chat_id=call.message.chat.id,
							message_id = call.message.message_id,
							caption=await choose_user_link(call, cnt),
							parse_mode=types.ParseMode.HTML,
							)
							async with state.proxy() as data:
								data['country'] = cnt
							await Form.link.set()

		for key in cf.COUNTRIES_SITES:
			for cnt in cf.COUNTRIES_SITES[key]:
				for pr in cf.PRICES:
					if call.data == cnt + str(cf.PRICES[pr]):
						new_date = datetime.now() + timedelta(days=cf.PRICES[pr])
						db.update_subsc_time(call.from_user.id, new_date, cnt)
						if cf.PRICES[pr] == 1:
							line = '<b>🔑 Вы преобрели подписку на </b><b>'+ str(cf.PRICES[pr]) +'</b> <b>день.</b>'
						elif cf.PRICES[pr] == 3:
							line = '<b>🔑 Вы преобрели подписку на </b><b>'+ str(cf.PRICES[pr]) +'</b> <b>дня.</b>'
						elif cf.PRICES[pr] == 7 or cf.PRICES[pr] == 30:
							line = '<b>🔑 Вы преобрели подписку на </b><b>'+ str(cf.PRICES[pr]) +'</b> <b>дней.</b>'
						await bot.edit_message_caption(
							chat_id=call.message.chat.id,
							message_id = call.message.message_id,
							caption=line,
							reply_markup = back_kb,
							parse_mode=types.ParseMode.HTML
							)

		for key in cf.COUNTRIES_SITES:
			for cnt in cf.COUNTRIES_SITES[key]:
				if call.data == "previously"+cnt:
					callshow = cnt+'show_data'
					callclear = cnt+'clear_data'
					show_data_btn = InlineKeyboardButton('✈️​​ Показать объявления 📃', callback_data=callshow)
					clear_data_btn = InlineKeyboardButton("🗑 Удалить объявления", callback_data=callclear)
					data_kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
					data_kb.add(show_data_btn, clear_data_btn)
					data_kb.add(back_btn)
					await bot.edit_message_caption(
						chat_id=call.message.chat.id,
						message_id = call.message.message_id,
						caption="<b>‼️ Выберите то, что хотите сделать с объявлениями</b>",
						parse_mode=types.ParseMode.HTML, reply_markup=data_kb)

		for key in cf.COUNTRIES_SITES:
			for cnt in cf.COUNTRIES_SITES[key]:
				if call.data == cnt+'show_data':
					whatsapp_text = db.get_text_and_page(call.from_user.id)[2]
					length_data = db.len_advertisement_data(call.from_user.id)
					counter = 1
					for usl in db.get_previously_adv(call.from_user.id, cnt):
						try:
							whatsapp_number = usl[8]
							whatsapp = f'<a href="https://api.whatsapp.com/send?phone={whatsapp_number}&text={whatsapp_text} {usl[4]}">🟢 WhatsApp</a>'
							viber_number = usl[8].split("+")[1]
							adv_link = f'<a href="{usl[4]}">🔑 Ссылка на объявление</a>'
							image_link = f'<a href="{usl[6]}">🗾 Ссылка на изображение</a>'
							viber = f'<a href="https://viber.click/{viber_number}">🟣 Viber</a>'
							await bot.send_photo(call.message.chat.id, usl[6], caption=f"<b>📦 Название объявления: </b><code>{usl[1]}</code>\n<b>💳 Цена товара: </b><code>{usl[2]}</code>\n<b>🌏 Местоположение: </b><code>{usl[5]}</code>\n<b>📅 Дата создания объявления: </b><code>{usl[3]}</code>\n\n{adv_link}\n{image_link}\n\n<b>🙎🏻‍♂️ Имя продавца: </b><code>{usl[7]}</code>\n<b>📞 Номер продавца:</b> <code>{usl[8]}</code>\n\n{whatsapp}\n{viber}\n\n<b>📝 Количество объявлений продавца: </b><code>{usl[9]}</code>\n<b>📆 Дата регистрации продавца: </b><code>{usl[10]}</code>\n<b>📃 Бизнесс аккаунт: </b><code>{usl[11]}</code>\n\nОбъявление {counter}/{length_data}", parse_mode=types.ParseMode.HTML, reply_markup=back_key_kb)
							counter +=1
							time.sleep(1)
						except Exception as e:
							print(e)
							pass

		if call.data == "back_to_menu":
			await bot.edit_message_caption(
				chat_id=call.message.chat.id,
				message_id = call.message.message_id,
				caption=f"🆔 <b>Ваш ид:</b> <code>{call.from_user.id}</code>", 
				parse_mode=types.ParseMode.HTML, 
				reply_markup=main_kb)
			
		elif call.data == "back_from_pars":
			file = InputFile(file_path)
			await bot.send_photo(chat_id=call.from_user.id, photo=file, caption=f"🆔 <b>Ваш ид:</b> <code>{call.from_user.id}</code>", parse_mode=types.ParseMode.HTML, reply_markup=main_kb)




		elif call.data == "parser_sites":
			if db.len_hash_data(call.from_user.id) > 0:
				await bot.edit_message_caption(
					chat_id=call.message.chat.id,
					message_id = call.message.message_id,
					caption="‼️<b>У вас есть непросмотренные объявлния. Нажмите на соответсвующую кнопку, чтобы посмотреть или удалить их.</b>",
					parse_mode=types.ParseMode.HTML, 
					reply_markup=hash_kb)
			else:	
				await bot.edit_message_caption(
					chat_id=call.message.chat.id,
					message_id = call.message.message_id,
					caption="<b>🌍 Выберите страну, где вы хотите найти объявления.</b>",
					parse_mode=types.ParseMode.HTML,
					reply_markup=show_countries_kb
					)


		elif call.data == "info":
			username = f'<a href="https://t.me/{call.from_user.username}">{call.from_user.first_name}</a>'
			news_channel = f'<a href="{cf.CHANNEL}">GzuzPars News</a>'
			await bot.edit_message_caption(
					chat_id=call.message.chat.id,
					message_id = call.message.message_id,
					caption=f"Контакты: {username}\n\nНовостной канал: {news_channel}",
					parse_mode=types.ParseMode.HTML, 
					reply_markup=back_kb)
			
		elif call.data == "settings":
			await bot.edit_message_caption(
					chat_id=call.message.chat.id,
					message_id = call.message.message_id,
					caption="Выберите пункт: ",
					parse_mode=types.ParseMode.HTML, 
					reply_markup=settings_kb)

		elif call.data == "log_creator":
			await bot.edit_message_caption(
				chat_id=call.message.chat.id,
				message_id = call.message.message_id,
				caption="Конфигуратор лога: ",
				parse_mode=types.ParseMode.HTML, 
				reply_markup=configure_logs_kb)

		elif call.data == "filters":
			db = SQLighter()
			user_filters = db.get_text_and_page(call.from_user.id)
			await bot.edit_message_caption(
				chat_id=call.message.chat.id,
				message_id = call.message.message_id,
				caption=f"🖋 Фильтры:\n\n<b>Текст для WhatsApp:</b> <code>{user_filters[2]}</code>\n<b>Стартовая страница:</b> <code>{user_filters[3]}</code>",
				parse_mode=types.ParseMode.HTML, 
				reply_markup=filters_kb)

		elif call.data == "whatsapp_text":
			await bot.edit_message_caption(
				chat_id=call.message.chat.id,
				message_id = call.message.message_id,
				caption="Введите текст для WhatsApp:",
				parse_mode=types.ParseMode.HTML)
			await Filters.whatsapp_text.set()
			
		elif call.data == "starter_page":
			await bot.edit_message_caption(
				chat_id=call.message.chat.id,
				message_id = call.message.message_id,
				caption="Введите стартовую страницу:",
				parse_mode=types.ParseMode.HTML)
			await Filters.page_start.set()
			
				
				

		elif call.data == "previously_pars":
			db = SQLighter()
			if db.len_advertisement_data(call.from_user.id) > 0:
				# Ранее добавленные
				previously_added_kb = types.InlineKeyboardMarkup(resize_keyboard=True)
				for key in cf.COUNTRIES_SITES:
					for cnt in cf.COUNTRIES_SITES[key]:
						callback_data = "previously"+cnt
						length = str(db.get_len_previously_platfrom(call.from_user.id, cnt))
						if int(length) > 0:
							if length[-1] == "1" and length != "11":
								button = key[0:2] + cnt + " — " + length + " объявление"
							elif length[-1] in ("2", "3", "4") and length != "12" and length != "13" and length != "14":
								button = key[0:2] + cnt + " — " + length + " объявления"
							elif length[-1] in ("0","5", "6", "7", "8", "9") or length == "11" or length == "12" or length == "14":
								button = key[0:2] + cnt + " — " + length + " объявлений"
							item = types.InlineKeyboardButton(button, callback_data=callback_data)
							previously_added_kb.add(item)
						else:
							pass	
				previously_added_kb.add(back_btn)
				await bot.edit_message_caption(
					chat_id=call.message.chat.id,
					message_id = call.message.message_id,
					caption="<b>Выберите площадку на которой хотите посмотреть ранее добавленные объявления.</b>",
					parse_mode=types.ParseMode.HTML, 
					reply_markup=previously_added_kb)
			else:
				await bot.edit_message_caption(
					chat_id=call.message.chat.id,
					message_id = call.message.message_id,
					caption="<b>Вы пока не добавили ни одного объявления.</b>",
					parse_mode=types.ParseMode.HTML,
					reply_markup=back_kb)



		elif call.data == 'show_hash':
			whatsapp_text = db.get_text_and_page(call.from_user.id)[2]
			length_hash = len(db.get_hash_data(call.from_user.id))
			counter = 1
			for usl in db.get_hash_data(call.from_user.id):
				try:
					whatsapp_number = usl[8]
					whatsapp = f'<a href="https://api.whatsapp.com/send?phone={whatsapp_number}&text={whatsapp_text} {usl[4]}">🟢 WhatsApp</a>'
					viber_number = usl[8].split("+")[1]
					adv_link = f'<a href="{usl[4]}">🔑 Ссылка на объявление</a>'
					image_link = f'<a href="{usl[6]}">🗾 Ссылка на изображение</a>'
					viber = f'<a href="https://viber.click/{viber_number}">🟣 Viber</a>'
					await bot.send_photo(call.message.chat.id, usl[6], caption=f"<b>📦 Название объявления: </b><code>{usl[1]}</code>\n<b>💳 Цена товара: </b><code>{usl[2]}</code>\n<b>🌏 Местоположение: </b><code>{usl[5]}</code>\n<b>📅 Дата создания объявления: </b><code>{usl[3]}</code>\n\n{adv_link}\n{image_link}\n\n<b>🙎🏻‍♂️ Имя продавца: </b><code>{usl[7]}</code>\n<b>📞 Номер продавца:</b> <code>{usl[8]}</code>\n\n{whatsapp}\n{viber}\n\n<b>📝 Количество объявлений продавца: </b><code>{usl[9]}</code>\n<b>📆 Дата регистрации продавца: </b><code>{usl[10]}</code>\n<b>📃 Бизнесс аккаунт: </b><code>{usl[11]}</code>\n\nОбъявление {counter}/{length_hash}", parse_mode=types.ParseMode.HTML,)
					counter +=1
					time.sleep(1)
				except Exception as e:
					print(e)
					pass

			await bot.send_message(call.message.chat.id, "🟢 Парсинг успешно завершен", parse_mode="HTML", reply_markup=back_key_kb)
			db.clear_hash_data(call.from_user.id)


		elif call.data == "clear_hash":
			db.clear_hash_data(call.from_user.id)
			await bot.edit_message_caption(
				chat_id=call.message.chat.id,
				message_id = call.message.message_id,
				caption="🚬 Кэш очищен",
				reply_markup=back_kb)

		elif call.data == cnt+"clear_data":
			db.delete_previously_adv(call.from_user.id, cnt)
			await bot.edit_message_caption(
				chat_id=call.message.chat.id,
				message_id = call.message.message_id,
				caption="<b>🚬 Ранее добавленные объявления с площадки </b><code>"+cnt+"</code><b> удалены</b>", parse_mode=types.ParseMode.HTML, reply_markup=back_kb)


	else:
		news_channel = f'<a href="{cf.CHANNEL}">новостей</a>'
		await bot.send_message(
			chat_id=message.from_user.id,
			text="🆘 <b>Вас нет в канале "+news_channel+". Вступите, чтобы пользоваться ботом.</b>",
			parse_mode=types.ParseMode.HTML,
			reply_markup=start_pars_kb)


@dp.message_handler(state=Filters.whatsapp_text)
async def process_text(message: types.Message, state: FSMContext):
	db = SQLighter()
	whats_text = message.text
	db.update_whatsapp_text(message.from_user.id, whats_text)
	await state.finish()
	await bot.send_message(message.chat.id, "<b>Успешно!</b>", parse_mode="HTML", reply_markup=back_key_kb)

@dp.message_handler(lambda message:not message.text.isdigit(), state=Filters.page_start)
async def process_page_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Должно быть цифрой.</b>", parse_mode="HTML")	

@dp.message_handler(state=Filters.page_start)
async def process_page(message: types.Message, state: FSMContext):
	db = SQLighter()
	page_pars = message.text
	db.update_user_page(message.from_user.id, page_pars)
	await state.finish()
	await bot.send_message(message.chat.id, "<b>Успешно!</b>", parse_mode="HTML", reply_markup=back_key_kb)	


async def create_price_keyboard(call, platform):
	show_prices_kb = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	for key in cf.PRICES:
		callback_data = platform + str(cf.PRICES[key])
		item = types.InlineKeyboardButton(key, callback_data=callback_data)
		show_prices_kb.add(item)
	await bot.edit_message_caption(
		chat_id=call.message.chat.id,
		message_id = call.message.message_id,
		caption="🔴 <b>У вас нет доступа\n\n🔵 Площадка: </b><code>"+platform+"</code>\n\n🔵 <b>Твой id - </b><code>"+str(call.from_user.id)+"</code>\n\n🟡 <b>Цена 4500₽ (30 дней)</b>\n🟡 <b>Цена 1500₽ (7 дней)</b>\n🟡 <b>Цена 700₽ (3 дня)</b>\n🟡 <b>Цена 350₽ (1 день)</b>",
		parse_mode=types.ParseMode.HTML, 
		reply_markup=show_prices_kb
		)


async def choose_user_link(call, platform):
	if platform == "bolha.com":
		country_url = 'https://www.bolha.com/avdio-in-video'
		line = "🖌<b>Введите вашу ссылку с категорией или ключевое слово</b>\n"+"\n<i>Пример ссылки: </i>"+country_url+"\n\n<i>Пример слова:</i> <b>apple</b>"
	elif platform == "bazar.lu":
		country_url = 'https://www.bazar.lu/Scripts/sql.exe?SqlDB=bazar&Sql=Search.phs&category=30'
		line = "🖌<b>Введите вашу ссылку с категорией</b>\n"+"\n<i>Пример ссылки: </i>"+country_url
	elif platform == "gumtree.co.za":
		country_url = 'https://www.gumtree.co.za/s-iphone/v1c9420p1'
		line = f"🖌<b>Введите вашу ссылку с категорией или ключевое слово.</b>\n\nПример ссылки: {country_url}\n\nПример слова: iphone"
	return line	


def register_handlers_other(dp : Dispatcher):
	dp.register_message_handler(back_button)
	dp.register_callback_query_handler(echo, lambda callback_query: True)
	
		
