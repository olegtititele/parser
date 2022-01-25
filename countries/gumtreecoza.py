import sys
import os
import re
from sqlite.sqlighter import SQLighter
import requests
import time
import datetime as dt
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from string import whitespace
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class GumtreeCoZa(object):
	def __init__(self, user_id, platform, link, announ_count, seller_adv_count, adv_reg_data, seller_reg_data, business, repeated_number):
		self.user_id = user_id
		self.platform = platform
		self.link = link
		self.announ_count = announ_count
		self.seller_adv_count = seller_adv_count
		self.adv_reg_data = adv_reg_data
		self.seller_reg_data = seller_reg_data
		self.business = business
		self.repeated_number = repeated_number
		self.db = SQLighter()
		self.non_image = "https://upload.wikimedia.org/wikipedia/commons/9/9a/%D0%9D%D0%B5%D1%82_%D1%84%D0%BE%D1%82%D0%BE.png"
		self.ann_cnd = 0
		self.num_err = 0
		self.page = 0
		self.loopflag = True
		self.index = -1
		self.options = webdriver.ChromeOptions()
		self.options.add_argument("--headless")
		self.options.add_argument("--no-sandbox")
		self.options.add_argument("--disable-dev-shm-usage")
		self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.driver = webdriver.Chrome(options=self.options, executable_path="chromedriver")


	def generate_link(self):
		while True:
			if self.link[self.index].isdigit():
				self.index -= 1
			elif not self.link[-1].isdigit():
				return False
			else:
				page_link = self.link[:self.index]
				self.start_pars(page_link)
				return False

	def start_pars(self, page_link):
		while self.loopflag:
			self.page += 1
			gen_link = page_link + "p" + str(self.page)
			try:
				r = requests.get(gen_link)
				html = BS(r.content, 'lxml')
				adv_link_block = html.find_all("a", class_="related-ad-title")
				for alb in adv_link_block:
					adv_link = "https://www.gumtree.co.za" + alb['href']
					print(adv_link)
					if self.num_err >= 3:
						self.loopflag = False
						return False
					elif self.ann_cnd < (int(self.announ_count)):
						if(not self.db.check_advestisement(self.user_id, adv_link)):
							print("tyt")
							self.driver.get(adv_link)
							print("Неа")
							self.check_number(adv_link)
						else:
							pass	

			except IndexError as e :
				print(e)
				self.num_err += 1
				self.start_pars(page_link)


	def check_number(self, adv_link):
		try:
			self.driver.find_element(By.XPATH, '//*[@id="reply-form"]/div/div[2]/div[1]/div/span[3]').click()
			phone_number = "+27" + self.driver.find_element(By.XPATH, '//*[@id="reply-form"]/div/div[2]/div[1]/div/span[2]').text.replace("-", "")
			if self.repeated_number.lower() == 'да':
				self.pars_adv_info(adv_link, phone_number)
			elif self.repeated_number.lower() == 'нет':
				if(not self.db.get_tel_num(self.user_id, phone_number)):
					print(phone_number)
					self.pars_adv_info(adv_link, phone_number)
				else:
					pass

		except Exception as e:
			pass

	
	def pars_adv_info(self, adv_link, phone_number):
		try:
			print("dada")
			self.num_err = 0
			r = requests.get(adv_link)
			html = BS(r.content, 'lxml')
			# Название объявления
			adv_title = html.find("div", class_="title").text

			# Цена объявления
			adv_price = html.find("span", class_="ad-price").text.translate(dict.fromkeys(map(ord, whitespace)))

			# Изображение
			try:
				adv_image = html.find("img", class_="lazyloaded")['src']
			except Exception as e:
				adv_image = self.non_image
			adv_general_details = html.find_all("div", class_="attribute")

			# Имя продавца
			seller_name = html.find("div", class_="seller-name").text

			# Количество объявлений продавца
			seller_total_ads = html.find("span", class_="active-ad").text.split(" ")[-1]

			# Дата регистрации продавца
			seller_reg_block = html.find("span", class_="seller-year").text
			seller_reg = self.get_data(seller_reg_block)

			# Дата регистрации объявления
			adv_reg_data_block = html.find("span", class_="creation-date").text
			adv_reg = self.get_data(adv_reg_data_block)

			# Местоположение и тип объявления
			for agd in adv_general_details:
				if "Location:" in agd.text:
					try:
						adv_location = agd.text.split("Location:")[1]
					except Exception as e:
						adv_location = "Не указана"

				elif "For Sale By:" in agd.text:
					try:
						adv_business = agd.text.split("For Sale By:")[1]
						if adv_business == "Dealer":
							adv_business = "Бизнесс аккаунт"
						else:
							adv_business = "Частное лицо"
					except Exception as e:
						adv_business = "Не указано"

			if self.business.lower() == "нет":
				if adv_business == "Бизнесс аккаунт" or adv_business == "Не указано":
					self.check_seller_adv_count(adv_link, adv_title, adv_price, adv_reg, adv_image, adv_location, adv_business, phone_number, seller_name, seller_total_ads, seller_reg)
				else:
					self.check_seller_adv_count(adv_link, adv_title, adv_price, adv_reg, adv_image, adv_location, adv_business, phone_number, seller_name, seller_total_ads, seller_reg)
			elif self.business.lower() == "да":
				if adv_business == "Частное лицо":
					self.check_seller_adv_count(adv_link, adv_title, adv_price, adv_reg, adv_image, adv_location, adv_business, phone_number, seller_name, seller_total_ads, seller_reg)
				else:
					pass
			
		except Exception as e:
			print(e)
			pass	

	def get_data(self, reg_data_block):
		reg_data_digit = int(re.sub("[^0-9]", "", reg_data_block))
		if "day" in reg_data_block:
			reg_data_full = dt.datetime.now() - dt.timedelta(days=reg_data_digit)
			reg_data = reg_data_full.strftime('%d.%m.%Y')
		elif "month" in reg_data_block:
			reg_data_full = dt.datetime.now() - dt.timedelta(days=reg_data_digit*30)
			reg_data = reg_data_full.strftime('%d.%m.%Y')
		elif "year" in reg_data_block:
			reg_data_full = dt.datetime.now() - dt.timedelta(days=reg_data_digit*365)
			reg_data = reg_data_full.strftime('%d.%m.%Y')
		else:
			reg_data_full = dt.datetime.now()
			reg_data = reg_data_full.strftime('%d.%m.%Y')
		return reg_data


	def check_seller_adv_count(self, adv_link, adv_title, adv_price, adv_reg, adv_image, adv_location, adv_business, phone_number, seller_name, seller_total_ads, seller_reg):
		if self.seller_adv_count.lower() == "нет":
			self.check_adv_reg_data(adv_link, adv_title, adv_price, adv_reg, adv_image, adv_location, adv_business, phone_number, seller_name, seller_total_ads, seller_reg)
		elif int(seller_total_ads) <= int(self.seller_adv_count):
			self.check_adv_reg_data(adv_link, adv_title, adv_price, adv_reg, adv_image, adv_location, adv_business, phone_number, seller_name, seller_total_ads, seller_reg)
		else:
			pass

	def check_adv_reg_data(self, adv_link, adv_title, adv_price, adv_reg, adv_image, adv_location, adv_business, phone_number, seller_name, seller_total_ads, seller_reg):
		if self.adv_reg_data.lower() == "нет":
			self.check_seller_reg(adv_link, adv_title, adv_price, adv_reg, adv_image, adv_location, adv_business, phone_number, seller_name, seller_total_ads, seller_reg)
		else:
			inpt_date_reg_adv = dt.datetime.strptime(self.adv_reg_data, '%d.%m.%Y')
			reg_adv_block = dt.datetime.strptime(adv_reg, '%d.%m.%Y')
			if inpt_date_reg_adv <= reg_adv_block:
				self.check_seller_reg(adv_link, adv_title, adv_price, adv_reg, adv_image, adv_location, adv_business, phone_number, seller_name, seller_total_ads, seller_reg)
			else:
				pass
	def check_seller_reg(self, adv_link, adv_title, adv_price, adv_reg, adv_image, adv_location, adv_business, phone_number, seller_name, seller_total_ads, seller_reg):
		if self.seller_reg_data.lower() == "нет":
			self.ann_cnd += 1
			self.db.add_advertisement(self.user_id, self.platform, adv_title, adv_price, adv_reg, adv_link, adv_location, adv_image, seller_name, phone_number, seller_total_ads, seller_reg, adv_business)
			self.db.add_hash_advertisement(self.user_id, self.platform, adv_title, adv_price, adv_reg, adv_link, adv_location, adv_image, seller_name, phone_number, seller_total_ads, seller_reg, adv_business)
		else:
			inpt_seller_reg = dt.datetime.strptime(self.seller_reg_data, '%d.%m.%Y')
			seller_reg_block = dt.datetime.strptime(seller_reg, '%d.%m.%Y')
			if inpt_seller_reg <= seller_reg_block:
				self.ann_cnd += 1
				self.db.add_advertisement(self.user_id, self.platform, adv_title, adv_price, adv_reg, adv_link, adv_location, adv_image, seller_name, phone_number, seller_total_ads, seller_reg, adv_business)
				self.db.add_hash_advertisement(self.user_id, self.platform, adv_title, adv_price, adv_reg, adv_link, adv_location, adv_image, seller_name, phone_number, seller_total_ads, seller_reg, adv_business)
			else:
				pass
