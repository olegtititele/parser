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
from selenium.common.exceptions import NoSuchElementException

class GumtreeCoZa(object):
	def __init__(self, page, user_id, platform, link, announ_count, seller_adv_count, adv_reg_data, seller_reg_data, business, repeated_number):
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
		self.page = page
		self.loopflag = True
		self.index = -1
		self.options = webdriver.ChromeOptions()
		self.options.add_argument("--window-size=1200,600")
		self.options.add_argument("--headless")
		self.options.add_argument('--no-sandbox')
		self.options.add_argument("--disable-extensions")
		self.options.add_argument("--disable-dev-shm-usage")
		self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
		
		self.driver = webdriver.Chrome(options=self.options, executable_path="chromedriver")

	def generate_link(self):
		if "https://www.gumtree.co.za/" in self.link:
			first_link = self.link.split("/")[-1]
			second_link = first_link.split("p")[0]
			page_link = self.link.split(second_link)[0] + second_link + "p" + str(self.page)
			return page_link
		else:
			page_link = "https://www.gumtree.co.za/s-all-the-ads/v1b0p" + str(self.page) + "?q=" + self.link
			return page_link


	def start_pars(self):
		page_link = self.generate_link()
		self.driver.get(page_link)
		
		
		get_all_pages = self.driver.find_element(By.XPATH, '//span[@class="sudo-link last"]').click()
		url = self.driver.current_url
		last_page_block = url.split("/")
		for lpb in last_page_block:
			if "page" in lpb:
				last_page = int(re.sub("[^0-9]", "", lpb))
		for i in range(int(last_page)):
			page_link = self.generate_link()
			self.page += 1
			r = requests.get(page_link)
			html = BS(r.content, 'lxml')
			advertisements = html.find_all("a", class_="related-ad-title")
			# self.driver.get(page_link)
			# advertisements = self.driver.find_elements(By.XPATH, '//div[@class="title title-mult-lines"]//a[@class="related-ad-title"]')
			for adv in advertisements:
				adv_link = "https://www.gumtree.co.za" + adv['href']
				# adv_link = adv.get_attribute("href")
				if self.ann_cnd < (int(self.announ_count)):
					self.driver.get(adv_link)
					try:
						element = self.driver.find_element(By.XPATH, '//*[@id="reply-form"]/div/div[2]/div[1]/div/span[3]')
						element.click()
						phone_number_block = "+27" + self.driver.find_element(By.XPATH, '//*[@id="reply-form"]/div/div[2]/div[1]/div').text
						phone_number = phone_number_block.replace("-", "")
						if(not self.db.check_advestisement(self.user_id, adv_link)):
							self.check_number(adv_link, phone_number)
						else:
							pass
					except NoSuchElementException:
						pass
				else:
					self.driver.close()
					self.driver.quit()
					return False
		self.driver.close()
		self.driver.quit()
		return False		

	def check_number(self, adv_link, phone_number):
		try:
			if self.repeated_number.lower() == 'да':
				self.pars_adv_info(adv_link, phone_number)
			elif self.repeated_number.lower() == 'нет':
				if(not self.db.get_tel_num(self.user_id, phone_number)):
					self.pars_adv_info(adv_link, phone_number)
				else:
					pass

		except Exception as e:
			pass

	
	def pars_adv_info(self, adv_link, phone_number):
		try:
			# Название объявления
			try:
				adv_title = self.driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[1]/div[3]/div[1]/div/div[1]/div[1]/h1').text
			except NoSuchElementException:
				adv_title = "Не указано"
			# Цена объявления
			adv_price = self.driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[1]/div[3]/div[1]/div/div[1]/div[2]/h3/span').text

			# Изображение
			try:
				adv_image = self.driver.find_element(By.XPATH, '//*[@id="vip-gallery"]/div[1]/div/div[1]/div[1]/div/picture/img').get_attribute("src")
			except Exception as e:
				adv_image = self.non_image

			# Имя продавца
			try:
				seller_name = self.driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[1]/div[3]/div[2]/div[1]/div[1]/div').text
			except NoSuchElementException:
				seller_name = "Не указано"
				
			# Количество объявлений продавца
			try:
				seller_total_ads = self.driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[1]/div[3]/div[2]/div[1]/div[1]/span[2]/span/span').text
			except NoSuchElementException:
				seller_name = "Не указано"
				
			# Дата регистрации продавца
			seller_reg_block = self.driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[1]/div[3]/div[2]/div[1]/div[1]/span[1]').text
			seller_reg = self.get_data(seller_reg_block)

			# Дата регистрации объявления
			adv_reg_data_block = self.driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[1]/div[3]/div[1]/div/div[3]/div[1]/span[2]').text
			adv_reg = self.get_data(adv_reg_data_block)

			adv_business = "Не указано"
			adv_location = "Не указана"

			# Местоположение и тип объявления
			adv_general_details = self.driver.find_elements(By.XPATH, '//*[@class="attribute"]')

			for agd in adv_general_details:
				try:
					if "Location:" in agd.text:
						adv_location = agd.text.split("Location:")[1].replace("\n", "")
					elif "For Sale By:" in agd.text:
						adv_business = agd.text.split("For Sale By:")[1]
						if adv_business == "Dealer" or adv_business == "Agency":
							adv_business = "Бизнесс аккаунт"
						else:
							adv_business = "Частное лицо"
				except Exception as e:
					continue
					
			if self.business.lower() == "нет":
				if adv_business == "Бизнесс аккаунт" or adv_business == "Не указано":
					self.check_seller_adv_count(adv_link, adv_title, adv_price, adv_reg, adv_image, adv_location, adv_business, phone_number, seller_name, seller_total_ads, seller_reg)
				else:
					self.check_seller_adv_count(adv_link, adv_title, adv_price, adv_reg, adv_image, adv_location, adv_business, phone_number, seller_name, seller_total_ads, seller_reg)
			elif self.business.lower() == "да":
				if adv_business == "Частное лицо" or adv_business == "Не указано":
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
		if not self.seller_adv_count.isdigit() or seller_total_ads == "Не указано":
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

