from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton
import config.config as cf
from aiogram import types

# Кнопка назад🔙
back_btn = InlineKeyboardButton('🔙 Вернуться в меню', callback_data='back_to_menu')
back_kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
back_kb.add(back_btn)


# Стартовая клавиатура
start_pars_btn = InlineKeyboardButton('🤖 Начать парсинг', callback_data='parser_sites')
previously_pars_btn = InlineKeyboardButton('♻️ Ранее просмотренные объявления', callback_data='previously_pars')
popup_balance_btn = InlineKeyboardButton("💵 Пополнить баланс", callback_data='popup_balance')
settings_btn = InlineKeyboardButton("⚙️ Настройки", callback_data='settings')
info_btn = InlineKeyboardButton("ℹ️ Обратная связь", callback_data='info')
main_kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_kb.add(start_pars_btn, previously_pars_btn)
main_kb.add(popup_balance_btn)
main_kb.add(settings_btn, info_btn)

# Клавиатура кэша
show_hash_btn = InlineKeyboardButton('✈️​​ Показать объявления 📃', callback_data='show_hash')
clear_hash_btn = InlineKeyboardButton("🗑 Очистить кэш", callback_data='clear_hash')

hash_kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
hash_kb.add(show_hash_btn, clear_hash_btn)
hash_kb.add(back_btn)

just_parsed_kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
just_parsed_kb.add(show_hash_btn)

show_countries_kb = types.InlineKeyboardMarkup(resize_keyboard=True)
for key in cf.COUNTRIES_SITES:
	item = types.InlineKeyboardButton(key, callback_data=key)
	show_countries_kb.add(item)
show_countries_kb.add(back_btn)

no_btn = KeyboardButton('Нет')
seller_adv_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
seller_adv_kb.row(no_btn)

yes_btn = KeyboardButton('Да')
business_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
business_kb.row(yes_btn, no_btn)

start_pars_btn = InlineKeyboardButton('🕔 Начать парсинг', callback_data='start_pars')
start_pa = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_pa.row(start_pars_btn)
