import config.config as cf
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import *


from create_bot import dp, bot
# States
# class Form(StatesGroup):
# 	country = State()
# 	link = State()
# 	adv_count = State()
# 	seller_adv = State()
# 	business = State()
# 	adv_reg_data = State()
# 	reg_seller_data = State()
# 	repeated_number = State()




# @dp.message_handler(state='*', commands='exit')
# @dp.message_handler(Text(equals='exit', ignore_case=True), state='*')
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
# @dp.message_handler(lambda message: message.text.isdigit(), state=Form.link)
async def process_link_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Введите ссылку корректно.</b>", parse_mode="HTML")

# @dp.message_handler(state=Form.link)
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
# @dp.message_handler(lambda message: not message.text.isdigit(), state=Form.adv_count)
async def process_adv_count_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Должно быть цифрой. Введите повторно.</b>", parse_mode="HTML")

# @dp.message_handler(lambda message: message.text.isdigit(), state=Form.adv_count)
async def process_adv_count(message: types.Message, state: FSMContext):
	await Form.next()
	await state.update_data(adv_count=int(message.text))
	return await bot.send_message(message.chat.id, "<b>🔷 Введите число кол-ва объявлений продавца</b>\n\nПример: 10 <i>(парсер будет искать продавцов у которых кол-во объявлений не будет превышать 10)\n\nЧтобы отключить этот фильтр нажмите</i> <b>'Нет'</b>\n\n<i>Чтобы вернуться в меню введите</i> /exit", parse_mode=types.ParseMode.HTML, reply_markup=seller_adv_kb, disable_web_page_preview=True)

# Количество объявлений продавца
# @dp.message_handler(lambda message: not message.text.isdigit() and message.text not in ["Нет", "нет"], state=Form.seller_adv)
async def process_seller_adv_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Должно быть цифрой или 'Нет'. Введите повторно.</b>", parse_mode="HTML")

# @dp.message_handler(state=Form.seller_adv)
async def process_seller_adv(message: types.Message, state: FSMContext):

	async with state.proxy() as data:
		data['seller_adv'] = message.text

	await Form.next()
	await bot.send_message(message.chat.id, "<b>👨🏻‍💻 Убрать бизнес аккаунты?</b>\n\n<i>Если вы хотите включить этот фильтр нажмите</i> <b>'Да'</b>\n\n<i>Если вы не хотите включать этот фильтр нажмите</i> <b>'Нет'</b>\n\n<i>Чтобы вернуться в меню введите</i> /exit", parse_mode=types.ParseMode.HTML, reply_markup=business_kb, disable_web_page_preview=True)


# Проверка бизнесс аккаунта
# @dp.message_handler(lambda message: message.text.isdigit() or message.text not in ["Нет", "нет", "Да", "да"], state=Form.business)
async def process_business_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Можно ввести только 'Да' или 'Нет'.</b>", parse_mode="HTML")

# @dp.message_handler(state=Form.business)
async def process_business(message: types.Message, state: FSMContext):

	async with state.proxy() as data:
		data['business'] = message.text

	await Form.next()
	# await bot.send_message(message.chat.id, data['link']+data['seller_adv']+data['business'])
	await bot.send_message(message.chat.id, "🗓<b> Укажите дату создания объявления\n\n</b><i>✅Пример: 01.01.2022 (парсер будет искать объявления, которые были созданы с 01.01.2022 по текущую дату)</i>\n\n<b>Чтобы отключить этот фильтр нажмите 'Нет'</b>\n\n<i>Чтобы вернуться в меню введите</i> /exit", parse_mode=types.ParseMode.HTML, reply_markup=seller_adv_kb, disable_web_page_preview=True)


# Дата регистрации объявления
# @dp.message_handler(lambda message: message.text.isdigit(), state=Form.adv_reg_data)
async def process_adv_reg_data_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Дата должна быть строго формата 'ДД.ММ.ГГГГ' или 'Нет'\n\nВведите дату создания объявления повторно.</b>", parse_mode="HTML")
# @dp.message_handler(lambda message: message.text.isdigit(), state=Form.adv_reg_data)
async def process_adv_next_step(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['adv_reg_data'] = message.text
		await Form.next()
		await bot.send_message(message.chat.id, "🗓<b> Укажите дату регистрации продавца\n\n</b><i>✅Пример: 01.01.2022 (парсер будет искать продавцов, которые зарегистрировались с 01.01.2022 по текущую дату)</i>\n\n<b>Чтобы отключить этот фильтр нажмите 'Нет'</b>\n\n<i>Чтобы вернуться в меню введите</i> /exit", parse_mode=types.ParseMode.HTML, reply_markup=seller_adv_kb, disable_web_page_preview=True)

# @dp.message_handler(state=Form.adv_reg_data)
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
# @dp.message_handler(lambda message: message.text.isdigit(), state=Form.reg_seller_data)
async def process_seller_reg_data_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Дата должна быть строго формата 'ДД.ММ.ГГГГ' или 'Нет'\n\nВведите дату создания объявления повторно.</b>", parse_mode="HTML")

async def process_seller_next_step(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['reg_seller_data'] = message.text
		await Form.next()
		await bot.send_message(message.chat.id, "🗓<b> Показывать объявления с повторяющимся номером?</b>\n\n<i>Если вы нажмете </i><b>'Да'</b><i>, то бот сможет парсить другие объявления продавца.\n\n Чтобы отключить этот фильтр нажмите </i><b>'Нет'</b>\n\n<i>Чтобы вернуться в меню введите</i> /exit", parse_mode=types.ParseMode.HTML, reply_markup=business_kb, disable_web_page_preview=True)

# @dp.message_handler(state=Form.reg_seller_data)
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
# @dp.message_handler(lambda message: message.text.isdigit() or message.text not in ["Нет", "нет", "Да", "да"], state=Form.repeated_number)
async def process_repeated_number_invalid(message: types.Message):
	return await bot.send_message(message.chat.id, "<b>❗️ Можно ввести только 'Да' или 'Нет'.</b>", parse_mode="HTML")

# @dp.message_handler(state=Form.repeated_number)
async def process_repeated_number(message: types.Message, state: FSMContext):

	async with state.proxy() as data:
		data['repeated_number'] = message.text

	business_kb = types.ReplyKeyboardRemove()
	await bot.send_message(message.chat.id, f"📤 <b>Ваши параметры для парсинга: </b>\n\n<b>Площадка: </b><code>{data['country']}</code>\n\n<b>Ссылка: </b><code>{data['link']}</code>\n\n<b>Количество товара: </b><code>{data['adv_count']}</code>\n\n<b>Количество объявлений продавца: </b><code>{data['seller_adv']}</code>\n\n<b>Бизнесс аккаунт: </b><code>{data['business']}</code>\n\n<b>Дата создания объявления: </b><code>{data['adv_reg_data']}</code>\n\n<b>Дата регистрации продавца: </b><code>{data['reg_seller_data']}</code>\n\n<b>Повторять номера: </b><code>{data['repeated_number']}</code>\n\n<b>Чтобы вернуться в меню введите </b>/exit", parse_mode=types.ParseMode.HTML, reply_markup=start_pa)


def register_handler_admin(dp : Dispatcher):
	dp.register_message_handler(cancel_handler, commands=['exit'], state="*")

	dp.register_message_handler(process_link_invalid, state=Form.link)
	dp.register_message_handler(process_link, state=Form.link)

	dp.register_message_handler(process_adv_count_invalid, state=Form.adv_count)
	dp.register_message_handler(process_adv_count, state=Form.adv_count)

	dp.register_message_handler(process_seller_adv_invalid, state=Form.seller_adv)
	dp.register_message_handler(process_seller_adv, state=Form.seller_adv)

	dp.register_message_handler(process_business_invalid, state=Form.business)
	dp.register_message_handler(process_business, state=Form.business)

	dp.register_message_handler(process_adv_reg_data_invalid, state=Form.adv_reg_data)
	dp.register_message_handler(process_adv_next_step, state=Form.adv_reg_data)
	dp.register_message_handler(process_adv_reg_data, state=Form.adv_reg_data)

	dp.register_message_handler(process_seller_reg_data_invalid, state=Form.reg_seller_data)
	dp.register_message_handler(process_seller_next_step, state=Form.reg_seller_data)
	dp.register_message_handler(process_seller_reg_data, state=Form.reg_seller_data)

	dp.register_message_handler(process_repeated_number_invalid, state=Form.repeated_number)
	dp.register_message_handler(process_repeated_number, state=Form.repeated_number)
