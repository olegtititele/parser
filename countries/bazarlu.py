import sys
import os
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

class BazarLu(object):
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
		self.lubuiss = "Не указано"
		self.sell_reg = "Не указана"
		self.ann_cnd = 0
		self.page = 1
		self.err_num = 0
		self.loopflag = True
		self.db = SQLighter()
		self.options = webdriver.ChromeOptions()
		self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.driver = webdriver.Chrome(options=self.options, executable_path="chromedriver")
		

	def get_parameters(self):
		self.ann_cnd = 0
		self.page = 1
		while self.loopflag:
			self.driver.get(self.link)
			element = self.driver.find_elements(By.CLASS_NAME, "annonces_entry_link")
			self.start_pars(element)

	def start_pars(self, element):
		try:
			for el in element:
				if self.err_num >= 3:
					self.loopflag = False
					return self.loopflag
				if self.ann_cnd < (int(self.announ_count)):
					self.err_num = 0
					adv_link = el.get_attribute("href")
					print(adv_link)
					if(not self.db.check_advestisement(self.user_id, adv_link)):
						# print(self.db.check_advestisement(self.user_id, adv_link))
						r = requests.get(adv_link)
						html = BS(r.content, 'lxml')
						phone_number_block = html.find("div", id="annonce_phone")
						phone_number_id = phone_number_block['onclick'].split("(")[1].split(")")[0]
						phone_link = "https://www.bazar.lu/Scripts/sql.exe?SqlDB=bazar&Sql=Phone.phs&site=0&item=" + phone_number_id
						r = requests.get(phone_link)
						phone_html = BS(r.content, 'lxml')
						phone_number = phone_html.find("body").text.translate(dict.fromkeys(map(ord, whitespace)))

						if phone_number == "pasdisponible":
							continue
						elif "+33" not in phone_number:
							phone_number = "+33"+phone_number					

						adv_name = html.find("div", class_="annonce_entry_top_title").text
						if not adv_name:
							adv_name = "Не указано"

						adv_reg_time = html.find("div", class_="annonce_entry_top_date").text.split(" ")[0].translate(dict.fromkeys(map(ord, whitespace))).replace("/",".")
						adv_data = dt.datetime.strptime(adv_reg_time, '%d.%m.%Y')
						image_link_block = html.find("img", id="annonce_entry_image_pic_image")['src']

						if image_link_block:
							image = "https://www.bazar.lu"+image_link_block
						else:
							continue

						price_block = html.find("span", id="annonce_price_highlight").text.split('"')[0].split(" ")

						if price_block:
							price = price_block[1]+" "+price_block[0]
						else:
							price = "Не указана"

						seller_name = html.find("div", id="annonce_user_name").text

						if not seller_name:
							seller_name = "Не указано"

						location = html.find("div", id="annonce_address_country").text

						if not location:
							location = "Не указано"


						
						seller_adv_count_block = html.find("div", class_="annonces-right-container")
						seller_link_block = seller_adv_count_block.find("a")['href']
						seller_link = "https://www.bazar.lu/Scripts/"+seller_link_block
						r = requests.get(seller_link)
						adv_count_html = BS(r.content, 'lxml')
						seller_adv = adv_count_html.find("span", id="bazarBandeau_results_nbr").text

						if not seller_adv:
							seller_adv = "Не указано"
				
						if self.seller_adv_count.lower() == "нет":
							self.check_seller_ads(adv_name, price, adv_reg_time, adv_link, location, image, seller_name, phone_number, seller_adv)
						else:
							
							inpt_date_reg_adv = dt.datetime.strptime(adv_reg_data, '%d.%m.%Y')
							if inpt_date_reg_adv <= adv_data:
								self.check_seller_ads(adv_name, price, adv_reg_time, adv_link, location, image, seller_name, phone_number, seller_adv)
							else:
								pass
					else:
						pass		
				else:
					self.loopflag = False
					return False

		except IndexError as e:
			print(repr(e))
			pass
		
		if self.ann_cnd < (int(self.announ_count)):
			try:
				self.next_page()
			except Exception:
				self.err_num +=1
		else:
			self.loopflag = False
			return False


	def check_seller_ads(self, adv_name, price, adv_reg_time, adv_link, location, image, seller_name, phone_number, seller_adv):
		if self.seller_adv_count.lower() == 'нет':
			if self.repeated_number.lower() == "да":
				self.ann_cnd += 1
				self.db.add_advertisement(self.user_id, self.platform, adv_name, price, adv_reg_time, adv_link, location, image, seller_name, phone_number, seller_adv, self.lubuiss, self.sell_reg)
				self.db.add_hash_advertisement(self.user_id, self.platform, adv_name, price, adv_reg_time, adv_link, location, image, seller_name, phone_number, seller_adv, self.lubuiss, self.sell_reg)
			elif self.repeated_number.lower() == "нет":
				if(not self.db.get_tel_num(self.user_id, phone_number)):
					self.ann_cnd += 1
					self.db.add_advertisement(self.user_id, self.platform, adv_name, price, adv_reg_time, adv_link, location, image, seller_name, phone_number, seller_adv, self.lubuiss, self.sell_reg)
					self.db.add_hash_advertisement(self.user_id, self.platform, adv_name, price, adv_reg_time, adv_link, location, image, seller_name, phone_number, seller_adv, self.lubuiss, self.sell_reg)
				else:
					pass	
		elif int(self.seller_adv_count) >= int(seller_adv):
			if self.repeated_number.lower() == "да":
				self.ann_cnd += 1
				self.db.add_advertisement(self.user_id, self.platform, adv_name, price, adv_reg_time, adv_link, location, image, seller_name, phone_number, seller_adv, self.lubuiss, self.sell_reg)
				self.db.add_hash_advertisement(self.user_id, self.platform, adv_name, price, adv_reg_time, adv_link, location, image, seller_name, phone_number, seller_adv, self.lubuiss, self.sell_reg)

			elif self.repeated_number.lower() == "нет":
				if(not self.db.get_tel_num(self.user_id, phone_number)):
					self.ann_cnd += 1
					self.db.add_advertisement(self.user_id, self.platform, adv_name, price, adv_reg_time, adv_link, location, image, seller_name, phone_number, seller_adv, self.lubuiss, self.sell_reg)
					self.db.add_hash_advertisement(self.user_id, self.platform, adv_name, price, adv_reg_time, adv_link, location, image, seller_name, phone_number, seller_adv, self.lubuiss, self.sell_reg)
				else:
					pass
			
		else:
			pass


	def next_page(self):
		try:
			self.page += 1	
			button = self.driver.find_element(By.XPATH, f'//div[@onclick="goTo({self.page})"]').click()
			element = self.driver.find_elements(By.CLASS_NAME, "annonces_entry_link")
			self.start_pars(element)
		except Exception:
			self.loopflag = False
			return False
