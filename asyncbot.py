import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


from sqlite.sqlighter import SQLighter
import config.config as cf
from countries.bolhasi import BolhaSI
from countries.bazarlu import BazarLu
from keyboards import *

from datetime import datetime, timedelta
import threading, time, sys
from threading import *
from create_bot import dp, bot
from handlers.dynamicload import DynamicLoading
logging.basicConfig(level=logging.INFO)

# bot = Bot(token=cf.BOT_TOKEN)
# dp = Dispatcher(bot, storage=MemoryStorage())

db = SQLighter()

class Timer:
	stop = False

	async def start(self):
		ii = 0
		while not self.stop:
			ii += 1
			print(ii)
			time.sleep(1)
		return ii

# States
class Form(StatesGroup):
	country = State()
	link = State()
	adv_count = State()
	seller_adv = State()
	business = State()
	adv_reg_data = State()
	reg_seller_data = State()
	repeated_number = State()


from handlers import client, admin, other

client.register_handlers_client(dp)
other.register_handlers_other(dp)


@dp.message_handler(state='*', commands='exit')
@dp.message_handler(Text(equals='exit', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
	"""
	Allow user to cancel any action
	"""
	current_state = await state.get_state()
	if current_state is None:
		return

	logging.info('Cancelling state %r', current_state)
	# Cancel state and inform user about it
	await state.finish()
	# And remove keyboard (just in case)
	username = f'<a href="https://t.me/+{message.from_user.username}">{message.from_user.first_name}</a>'
	await bot.send_message(message.chat.id, "<b>"+username+" , Вы вернулись в меню</b>", parse_mode=types.ParseMode.HTML, reply_markup=start_pars_kb,disable_web_page_preview=True)


# Ссылка
@dp.message_handler(lambda message: message.text.isdigit(), state=Form.link)
async def process_link_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Введите ссылку корректно.</b>", parse_mode="HTML")

@dp.message_handler(state=Form.link)
async def process_link(message: types.Message, state: FSMContext):
	link = message.text
	async with state.proxy() as data:
		platform = data['country']
	if platform in link:
		async with state.proxy() as data:	
			data['link'] = link
		await Form.next()
		await bot.send_message(message.chat.id, "<b>📌 Введите кол-во товара:</b>\n\nПример: <i>100</i>\n\n<i>Чтобы вернуться в меню введите</i> /exit", parse_mode="HTML")
	else:
		await process_link_invalid(message)	


# Количество объявлений
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.adv_count)
async def process_adv_count_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Должно быть цифрой. Введите повторно.</b>", parse_mode="HTML")

@dp.message_handler(lambda message: message.text.isdigit(), state=Form.adv_count)
async def process_adv_count(message: types.Message, state: FSMContext):
	await Form.next()
	await state.update_data(adv_count=int(message.text))
	return await bot.send_message(message.chat.id, "<b>🔷 Введите число кол-ва объявлений продавца</b>\n\nПример: 10 <i>(парсер будет искать продавцов у которых кол-во объявлений не будет превышать 10)\n\nЧтобы отключить этот фильтр нажмите</i> <b>'Нет'</b>\n\n<i>Чтобы вернуться в меню введите</i> /exit", parse_mode=types.ParseMode.HTML, reply_markup=seller_adv_kb, disable_web_page_preview=True)

# Количество объявлений продавца
@dp.message_handler(lambda message: not message.text.isdigit() and message.text not in ["Нет", "нет"], state=Form.seller_adv)
async def process_seller_adv_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Должно быть цифрой или 'Нет'. Введите повторно.</b>", parse_mode="HTML")

@dp.message_handler(state=Form.seller_adv)
async def process_seller_adv(message: types.Message, state: FSMContext):

	async with state.proxy() as data:
		data['seller_adv'] = message.text

	await Form.next()
	await bot.send_message(message.chat.id, "<b>👨🏻‍💻 Убрать бизнес аккаунты?</b>\n\n<i>Если вы хотите включить этот фильтр нажмите</i> <b>'Да'</b>\n\n<i>Если вы не хотите включать этот фильтр нажмите</i> <b>'Нет'</b>\n\n<i>Чтобы вернуться в меню введите</i> /exit", parse_mode=types.ParseMode.HTML, reply_markup=business_kb, disable_web_page_preview=True)


# Проверка бизнесс аккаунта
@dp.message_handler(lambda message: message.text.isdigit() or message.text not in ["Нет", "нет", "Да", "да"], state=Form.business)
async def process_business_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Можно ввести только 'Да' или 'Нет'.</b>", parse_mode="HTML")

@dp.message_handler(state=Form.business)
async def process_business(message: types.Message, state: FSMContext):

	async with state.proxy() as data:
		data['business'] = message.text

	await Form.next()
	# await bot.send_message(message.chat.id, data['link']+data['seller_adv']+data['business'])
	await bot.send_message(message.chat.id, "🗓<b> Укажите дату создания объявления\n\n</b><i>✅Пример: 01.01.2022 (парсер будет искать объявления, которые были созданы с 01.01.2022 по текущую дату)</i>\n\n<b>Чтобы отключить этот фильтр нажмите 'Нет'</b>\n\n<i>Чтобы вернуться в меню введите</i> /exit", parse_mode=types.ParseMode.HTML, reply_markup=seller_adv_kb, disable_web_page_preview=True)


# Дата регистрации объявления
@dp.message_handler(lambda message: message.text.isdigit(), state=Form.adv_reg_data)
async def process_adv_reg_data_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Дата должна быть строго формата 'ДД.ММ.ГГГГ' или 'Нет'\n\nВведите дату создания объявления повторно.</b>", parse_mode="HTML")

async def process_adv_next_step(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['adv_reg_data'] = message.text
		await Form.next()
		await bot.send_message(message.chat.id, "🗓<b> Укажите дату регистрации продавца\n\n</b><i>✅Пример: 01.01.2022 (парсер будет искать продавцов, которые зарегистрировались с 01.01.2022 по текущую дату)</i>\n\n<b>Чтобы отключить этот фильтр нажмите 'Нет'</b>\n\n<i>Чтобы вернуться в меню введите</i> /exit", parse_mode=types.ParseMode.HTML, reply_markup=seller_adv_kb, disable_web_page_preview=True)

@dp.message_handler(state=Form.adv_reg_data)
async def process_adv_reg_data(message: types.Message, state: FSMContext):
	try:
		if message.text in ["Нет", "нет", "Да", "да"]:
			await process_adv_next_step(message, state)
		else:
			datetime.strptime(message.text, '%d.%m.%Y')
			await process_adv_next_step(message, state)
		
	except Exception as e:
		print(repr(e))
		await process_adv_reg_data_invalid(message)

# Дата регистрации продавца
@dp.message_handler(lambda message: message.text.isdigit(), state=Form.reg_seller_data)
async def process_seller_reg_data_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Дата должна быть строго формата 'ДД.ММ.ГГГГ' или 'Нет'\n\nВведите дату создания объявления повторно.</b>", parse_mode="HTML")

async def process_seller_next_step(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['reg_seller_data'] = message.text
		await Form.next()
		await bot.send_message(message.chat.id, "🗓<b> Показывать объявления с повторяющимся номером?</b>\n\n<i>Если вы нажмете </i><b>'Да'</b><i>, то бот сможет парсить другие объявления продавца.\n\n Чтобы отключить этот фильтр нажмите </i><b>'Нет'</b>\n\n<i>Чтобы вернуться в меню введите</i> /exit", parse_mode=types.ParseMode.HTML, reply_markup=business_kb, disable_web_page_preview=True)

@dp.message_handler(state=Form.reg_seller_data)
async def process_seller_reg_data(message: types.Message, state: FSMContext):
	try:
		if message.text in ["Нет", "нет", "Да", "да"]:
			await process_seller_next_step(message, state)
		else:
			datetime.strptime(message.text, '%d.%m.%Y')
			await process_seller_next_step(message, state)
		
	except Exception as e:
		print(repr(e))
		await process_seller_reg_data_invalid(message)

# Проверка повторяющегося номера
@dp.message_handler(lambda message: message.text.isdigit() or message.text not in ["Нет", "нет", "Да", "да"], state=Form.repeated_number)
async def process_repeated_number_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Можно ввести только 'Да' или 'Нет'.</b>", parse_mode="HTML")

@dp.message_handler(state=Form.repeated_number)
async def process_repeated_number(message: types.Message, state: FSMContext):

	async with state.proxy() as data:
		data['repeated_number'] = message.text

	business_kb = types.ReplyKeyboardRemove()
	await bot.send_message(message.chat.id, f"📤 <b>Ваши параметры для парсинга: </b>\n\n<b>Площадка: </b><code>{data['country']}</code>\n\n<b>Ссылка: </b><code>{data['link']}</code>\n\n<b>Количество товара: </b><code>{data['adv_count']}</code>\n\n<b>Количество объявлений продавца: </b><code>{data['seller_adv']}</code>\n\n<b>Бизнесс аккаунт: </b><code>{data['business']}</code>\n\n<b>Дата создания объявления: </b><code>{data['adv_reg_data']}</code>\n\n<b>Дата регистрации продавца: </b><code>{data['reg_seller_data']}</code>\n\n<b>Повторять номера: </b><code>{data['repeated_number']}</code>\n\n<b>Чтобы вернуться в меню введите </b>/exit", parse_mode=types.ParseMode.HTML, reply_markup=start_pa)


@dp.callback_query_handler()
async def process_callback_button1(call: types.CallbackQuery, state: FSMContext):

	for key in cf.COUNTRIES_SITES:
		if call.data == key:
			for cnt in cf.COUNTRIES_SITES[key]:
				show_sites_kb = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
				item = types.InlineKeyboardButton(cnt, callback_data=cnt)
				show_sites_kb.add(item)
				await call.message.edit_text(text="<b>🌐 Выберите площадку, где вы хотите найти объявления.</b>", parse_mode=types.ParseMode.HTML, reply_markup=show_sites_kb)

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
						await call.message.edit_text(text=await choose_user_link(call, cnt), parse_mode=types.ParseMode.HTML, disable_web_page_preview = True)
						async with state.proxy() as data:
							data['country'] = cnt
						await Form.link.set()

	for key in cf.COUNTRIES_SITES:
		for cnt in cf.COUNTRIES_SITES[key]:
			for pr in cf.PRICES:
				if call.data == cnt + str(cf.PRICES[pr]):
					new_date = db.get_subscriber_time(cnt, call.from_user.id) + timedelta(days=cf.PRICES[pr])
					db.update_subsc_time(call.from_user.id, new_date, cnt)
					if cf.PRICES[pr] == 1:
						line = '<b>🔑 Вы преобрели подписку на </b><b>'+ str(cf.PRICES[pr]) +'</b> <b>день.</b>'
					elif cf.PRICES[pr] == 3:
						line = '<b>🔑 Вы преобрели подписку на </b><b>'+ str(cf.PRICES[pr]) +'</b> <b>дня.</b>'
					elif cf.PRICES[pr] == 7 or cf.PRICES[pr] == 30:
						line = '<b>🔑 Вы преобрели подписку на </b><b>'+ str(cf.PRICES[pr]) +'</b> <b>дней.</b>'
					await call.message.edit_text(text=line, parse_mode=types.ParseMode.HTML)

	for key in cf.COUNTRIES_SITES:
		for cnt in cf.COUNTRIES_SITES[key]:
			if call.data == "previously"+cnt:
				callshow = cnt+'show_data'
				callclear = cnt+'clear_data'
				show_data_btn = InlineKeyboardButton('✈️​​ Показать объявления 📃', callback_data=callshow)
				clear_data_btn = InlineKeyboardButton("🗑 Удалить объявления", callback_data=callclear)
				data_kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
				data_kb.add(show_data_btn, clear_data_btn)
				await call.message.edit_text(text="<b>‼️ Выберите то, что хотите сделать с объявлениями</b>", parse_mode=types.ParseMode.HTML, disable_web_page_preview = True, reply_markup=data_kb)

	for key in cf.COUNTRIES_SITES:
		for cnt in cf.COUNTRIES_SITES[key]:
			if call.data == cnt+'show_data':
				for usl in db.get_previously_adv(call.from_user.id, cnt):
					whatsapp_number = usl[8].replace(' ', '')
					if usl[0] == "bolha.com":
						whatsapp = f'<a href="https://api.whatsapp.com/send?phone={whatsapp_number}&text=Živjo, to želim kupiti. V dobrem stanju? {usl[4]}">🟢 WhatsApp</a>'
					elif usl[0] == "bazar.lu":
						whatsapp = f'<a href="https://api.whatsapp.com/send?phone={whatsapp_number}&text=Hallo,%20ich%20möchte%20das%20kaufen.%20In%20guter%20Kondition?%20{usl[4]}">🟢 WhatsApp</a>'
					viber_number = usl[8].split("+")[1].replace(' ', '')
					adv_link = f'<a href="{usl[4]}">🔑 Ссылка на объявление</a>'
					image_link = f'<a href="{usl[6]}">🗾 Ссылка на изображение</a>'
					viber = f'<a href="https://viber.click/{viber_number}">🟣 Viber</a>'
					await bot.send_photo(call.message.chat.id, usl[6], caption="<b>📦 Название объявления: </b><code>"+usl[1]+"</code>\n<b>💳 Цена товара: </b><code>"+usl[2]+"</code>\n<b>🌏 Местоположение: </b><code>"+usl[5]+"</code>\n<b>📅 Дата создания объявления: </b><code>"+usl[3]+"</code>\n\n"+adv_link+"\n"+image_link+"\n\n<b>🙎🏻‍♂️ Имя продавца: </b><code>"+usl[7]+"</code>\n<b>📞 Номер продавца:</b> <code>"+usl[8]+"</code>\n\n"+whatsapp+"\n"+viber+"\n\n<b>📝 Количество объявлений продавца: </b><code>"+usl[9]+"</code>\n<b>📆 Дата регистрации продавца: </b><code>"+usl[10]+"</code>\n<b>📃 Бизнесс аккаунт: </b><code>"+usl[11]+"</code>", parse_mode="HTML")
					time.sleep(0.5)
			elif call.data == cnt+"clear_data":
				db.delete_previously_adv(call.from_user.id, cnt)
				await call.message.edit_text(text="<b>🚬 Ранее добавленные объявления с площадки </b><code>"+cnt+"</code><b> удалены</b>", parse_mode=types.ParseMode.HTML, disable_web_page_preview = True)

	if call.data == 'show_hash':
		for usl in db.get_hash_data(call.from_user.id):
			whatsapp_number = usl[8].replace(' ', '')
			if usl[0] == "bolha.com":
				whatsapp = f'<a href="https://api.whatsapp.com/send?phone={whatsapp_number}&text=Živjo, to želim kupiti. V dobrem stanju? {usl[4]}">🟢 WhatsApp</a>'
			elif usl[0] == "bazar.lu":
				whatsapp = f'<a href="https://api.whatsapp.com/send?phone={whatsapp_number}&text=Hallo,%20ich%20möchte%20das%20kaufen.%20In%20guter%20Kondition?%20{usl[4]}">🟢 WhatsApp</a>'
			viber_number = usl[8].split("+")[1].replace(' ', '')
			adv_link = f'<a href="{usl[4]}">🔑 Ссылка на объявление</a>'
			image_link = f'<a href="{usl[6]}">🗾 Ссылка на изображение</a>'
			viber = f'<a href="https://viber.click/{viber_number}">🟣 Viber</a>'
			await bot.send_photo(call.message.chat.id, usl[6], caption="<b>📦 Название объявления: </b><code>"+usl[1]+"</code>\n<b>💳 Цена товара: </b><code>"+usl[2]+"</code>\n<b>🌏 Местоположение: </b><code>"+usl[5]+"</code>\n<b>📅 Дата создания объявления: </b><code>"+usl[3]+"</code>\n\n"+adv_link+"\n"+image_link+"\n\n<b>🙎🏻‍♂️ Имя продавца: </b><code>"+usl[7]+"</code>\n<b>📞 Номер продавца:</b> <code>"+usl[8]+"</code>\n\n"+whatsapp+"\n"+viber+"\n\n<b>📝 Количество объявлений продавца: </b><code>"+usl[9]+"</code>\n<b>📆 Дата регистрации продавца: </b><code>"+usl[10]+"</code>\n<b>📃 Бизнесс аккаунт: </b><code>"+usl[11]+"</code>", parse_mode="HTML")
			time.sleep(0.5)
		
		await bot.send_message(call.message.chat.id, "🟢 Парсинг успешно завершен", parse_mode="HTML", reply_markup=start_pars_kb)
		db.clear_hash_data(call.from_user.id)


	elif call.data == "clear_hash":
		db.clear_hash_data(call.from_user.id)
		await call.message.edit_text(
			text="🚬 Кэш очищен")	



			


@dp.callback_query_handler(state=Form.repeated_number)
async def start_pars_button1(call: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		platform = data['country']
		link = data['link']
		adv_count = data['adv_count']
		seller_adv = data['seller_adv']
		adv_reg_data = data['adv_reg_data']
		reg_seller_data = data['reg_seller_data']
		business = data['business']
		repeated_number = data['repeated_number']

# BOLHA.COM
	if platform == "bolha.com":
# 		bolha = BolhaSI(call.from_user.id, platform, link, adv_count, seller_adv, adv_reg_data, reg_seller_data, business, repeated_number)
		dyn_load = DynamicLoading()
# 		thread_pars = Thread(target=bolha.generate_link)
# 		thread_pars = Thread(target=await dyn_load.start_loop(call, state))
		if call.data == 'start_pars':
			await call.message.edit_text(text="⌛️ Поиск объявлений начался. Это займет несколько минут.", parse_mode=types.ParseMode.HTML)
# 			thread_pars.start()
			await dyn_load.start_loop(call, state)

		elif call.data == "stop_parser":
			print("Вышел")
# 			dyn_load.loopflag = False
# 			return
# 			await call.message.edit_text(text="⌛️ dddddddddd", parse_mode=types.ParseMode.HTML)
# 			bolha.stop_pars()
			await dyn_load.stop_loop(call, state)	


# BAZAR.LU
# 	elif platform == "bazar.lu":
# 		bazar = BazarLu(call.from_user.id, platform, link, adv_count, seller_adv, adv_reg_data, reg_seller_data, business, repeated_number)
# 		dyn_load = DynamicLoading(call.from_user.id)
# # 		thread_pars = Thread(target=bazar.get_parameters)

# 		if call.data == 'start_pars':
# 			await call.message.edit_text(text="⌛️ Поиск объявлений начался. Это займет несколько минут.", parse_mode=types.ParseMode.HTML)
# # 			thread_pars.start()
# 			await dyn_load.start_loop(call, state)

# 		elif call.data == "stop_parser":
# 			print("Вышел")
# # 			return
# 			bazar.stop_pars()
# # 			await dyn_load.stop_loop(call, state)

# async def loop_test(call):
# 	while True:
# 		print(call.from_user.id)
# 		time.sleep(1)

async def create_price_keyboard(call, platform):
	show_prices_kb = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	for key in cf.PRICES:
		callback_data = platform + str(cf.PRICES[key])
		item = types.InlineKeyboardButton(key, callback_data=callback_data)
		show_prices_kb.add(item)
	await call.message.edit_text(text="🔴 <b>У вас нет доступа\n\n🔵 Площадка: </b><code>"+platform+"</code>\n\n🔵 <b>Твой id - </b><code>"+str(call.from_user.id)+"</code>\n\n🟡 <b>Цена 4500₽ (30 дней)</b>\n🟡 <b>Цена 1500₽ (7 дней)</b>\n🟡 <b>Цена 700₽ (3 дня)</b>\n🟡 <b>Цена 350₽ (1 день)</b>", parse_mode=types.ParseMode.HTML, reply_markup=show_prices_kb)	


async def choose_user_link(call, platform):
	if platform == "bolha.com":
		country_url = 'https://www.bolha.com/avdio-in-video'
		line = "🖌<b>Введите вашу ссылку с категорией или ключевое слово</b>\n"+"\n<i>Пример ссылки: </i>"+country_url+"\n\n<i>Пример слова:</i> <b>apple</b>\n\n<i>Чтобы вернуться в меню введите</i> /exit"
		return line
	elif platform == "bazar.lu":
		country_url = 'https://www.bazar.lu/Scripts/sql.exe?SqlDB=bazar&Sql=Search.phs&category=30'
		line = "🖌<b>Введите вашу ссылку с категорией</b>\n"+"\n<i>Пример ссылки: </i>"+country_url+"\n\n<i>Чтобы вернуться в меню введите</i> /exit"
		return line


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
