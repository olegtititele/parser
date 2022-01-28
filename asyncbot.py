import logging
import asyncio
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
from countries.gumtreecoza import GumtreeCoZa
from keyboards import *

from datetime import datetime, timedelta
import threading, time, sys
from threading import *
from multiprocessing import Process
from create_bot import dp, bot
from handlers.dynamicload import DynamicLoading
logging.basicConfig(level=logging.INFO)

db = SQLighter()
photo = open('mainmenu.jpg', 'rb')


from handlers import client, admin, other
from handlers.other import Form

client.register_handlers_client(dp)
other.register_handlers_other(dp)

# @dp.callback_query_handler(state='*')
# async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
# 	if call.data == 'close_state':
# 		current_state = await state.get_state()
# 		if current_state is None:
# 			return

# 		logging.info('Cancelling state %r', current_state)
# 		await state.finish()
# 		await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=f"🆔 <b>Ваш ид:</b> <code>{call.from_user.id}</code>", parse_mode=types.ParseMode.HTML, reply_markup=main_kb)

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
@dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) > 100, state=Form.adv_count)
async def process_adv_count_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Должно быть цифрой и не должно превышать 100. Введите повторно.</b>", parse_mode="HTML")

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
	await bot.send_message(message.chat.id, f"📤 <b>Ваши параметры для парсинга: </b>\n\n<b>Площадка: </b><code>{data['country']}</code>\n\n<b>Ссылка: </b><code>{data['link']}</code>\n\n<b>Количество товара: </b><code>{data['adv_count']}</code>\n\n<b>Количество объявлений продавца: </b><code>{data['seller_adv']}</code>\n\n<b>Бизнесс аккаунт: </b><code>{data['business']}</code>\n\n<b>Дата создания объявления: </b><code>{data['adv_reg_data']}</code>\n\n<b>Дата регистрации продавца: </b><code>{data['reg_seller_data']}</code>\n\n<b>Повторять номера: </b><code>{data['repeated_number']}</code>", parse_mode=types.ParseMode.HTML, reply_markup=start_pa)
	


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
		
	if call.data == 'close_state':
		current_state = await state.get_state()
		if current_state is None:
			return

		logging.info('Cancelling state %r', current_state)
		await state.finish()
		await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=f"🆔 <b>Ваш ид:</b> <code>{call.from_user.id}</code>", parse_mode=types.ParseMode.HTML, reply_markup=main_kb)	

# BOLHA.COM
	if platform == "bolha.com":
		dyn_load = DynamicLoading()
		bolha = BolhaSI(call.from_user.id, platform, link, adv_count, seller_adv, adv_reg_data, reg_seller_data, business, repeated_number)
		thread_pars = Thread(target=bolha.generate_link)
		if call.data == 'start_pars':
			thread_pars.start()
			await dyn_load.start_loop(bolha, call, state)
			thread_pars.join()


# BAZAR.LU
	elif platform == "bazar.lu":
		dyn_load = DynamicLoading()
		bazar = BazarLu(call.from_user.id, platform, link, adv_count, seller_adv, adv_reg_data, reg_seller_data, business, repeated_number)
		thread_pars = Thread(target=bazar.get_parameters)
		if call.data == 'start_pars':
			thread_pars.start()
			await dyn_load.start_loop(bazar, call, state)
			thread_pars.join()

# GUMTREE.CO.ZA
	elif platform == "gumtree.co.za":
		dyn_load = DynamicLoading()
		gumtreecoza = GumtreeCoZa(call.from_user.id, platform, link, adv_count, seller_adv, adv_reg_data, reg_seller_data, business, repeated_number)
		thread_pars = Thread(target=gumtreecoza.generate_link)
		if call.data == 'start_pars':
			thread_pars.start()
			await dyn_load.start_loop(gumtreecoza, call, state)
			thread_pars.join()			



if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
