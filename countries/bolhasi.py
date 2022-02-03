import sys
import os
from sqlite.sqlighter import SQLighter
import requests
import traceback
from bs4 import BeautifulSoup as BS
from string import whitespace
import urllib
from requests.auth import HTTPProxyAuth
import datetime as dt
import threading, time, sys
from threading import *


class BolhaSI(object):
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
		self.page = page
		self.ann_cnd = 0
		self.err_num = 0
		self.loopflag = True
		self.non_image = "https://upload.wikimedia.org/wikipedia/commons/9/9a/%D0%9D%D0%B5%D1%82_%D1%84%D0%BE%D1%82%D0%BE.png"
		self.db = SQLighter()

	def generate_link(self):
		print(f"{self.user_id} запустил парсер bolha.com")
		while True:
			if self.err_num >= 3:
				self.loopflag = False
				return False
			if "https://www.bolha.com/" in self.link:
				page_link = self.link + '?page=' + str(self.page)
				self.page += 1
				self.err_num += 1
				self.start_pars(page_link)
			else:
				page_link = "https://www.bolha.com/?ctl=search_ads&keywords=" +self.link+ '&page=' + str(self.page)
				self.page += 1
				self.err_num += 1
				self.start_pars(page_link)

	def start_pars(self, page_link):
		try:
			r = requests.get(page_link)
			html = BS(r.content, 'lxml')
			ads_link_block = html.find_all("h3", class_="entity-title")
			self.err_num = 0
			for ads in ads_link_block:
				adv_url = "https://www.bolha.com" + ads.find("a", class_="link")['href']
				if self.ann_cnd < (int(self.announ_count)):
					if(not self.db.check_advestisement(self.user_id, adv_url)):
						self.start_pars2(adv_url)
					else:
						pass
				else:
					self.loopflag = False
					return False


		except IndexError as e :
			self.generate_link()


	def start_pars2(self, adv_url):
		try:
			
			r = requests.get(adv_url)
			html = BS(r.content, 'lxml')
			try:
				# Местоположение
				try:
					location = html.find_all("span", class_="ClassifiedDetailBasicDetails-textWrapContainer")[3].text
				except Exception as e:
					location = "Не указано"
					
				# Название объявления	
				adv_title = html.find("h1", class_="ClassifiedDetailSummary-title").text
	
				# Цена объявления
				try:
					adv_price = html.find("dd", class_="ClassifiedDetailSummary-priceDomestic").text.translate(dict.fromkeys(map(ord, whitespace)))
				except Exception as e:
					adv_price = "Не указана"
					
				# Изображение	
				adv_image_block = html.find("figure", class_="ClassifiedDetailGallery-figure")
				if adv_image_block:
					try:
						adv_image = adv_image_block.find("img")['src']
					except Exception as e:
						adv_image = self.non_image	
				else:
					pass
				# Дата создания объявления
				adv_reg = html.find_all("dd", class_="ClassifiedDetailSystemDetails-listData")[0].text.split("ob")[0].translate(dict.fromkeys(map(ord, whitespace)))[:-1]
				adv_data = dt.datetime.strptime(adv_reg, '%d.%m.%Y')
				profile = html.find("a", class_="link-standard")['href']
				if self.adv_reg_data.lower() == "нет":
					self.get_profile_url(profile, adv_url, location, adv_title, adv_price, adv_image, adv_reg)
				else:
					inpt_date_reg_adv = dt.datetime.strptime(self.adv_reg_data, '%d.%m.%Y')
					if inpt_date_reg_adv <= adv_data:
						self.get_profile_url(profile, adv_url, location, adv_title, adv_price, adv_image, adv_reg)
					else:
						pass
			except Exception:
				# Местоположение
				location_block = html.find_all("tr")
				if location_block:
					for lb in location_block:
						try:
							if "Lokacija:" in lb.text:
								location = lb.text.split("Lokacija:")[1].replace("\n","")
						except Exception as e:
							location = "Не указано"
				else:
					location = "Не указано"	
				# Название объявления
				adv_title = html.find("h1", class_="entity-title").text
				
				# Цена объявления
				try:
					adv_price = html.find("strong", class_="price price--hrk").text.translate(dict.fromkeys(map(ord, whitespace)))
				except Exception as e :
					adv_price = "Не указана"
				# Изображение	
				adv_image_block = html.find("div", class_="FlexImage")
				if adv_image_block:
					adv_image = "https:" + adv_image_block.find_all("img")[1]['src']
				else:
					adv_image = self.non_image
				# Дата создания объявления	
				adv_reg = html.find("time", class_="value").text.split(" ")[0]
				adv_data = dt.datetime.strptime(adv_reg, '%d.%m.%Y')
				profile_block = html.find("div", class_="Profile-wrapUsername")
				profile = profile_block.find("a")['href']

				
				if self.adv_reg_data.lower() == "нет":
					self.get_profile_url(profile, adv_url, location, adv_title, adv_price, adv_image, adv_reg)
				else:
					inpt_date_reg_adv = dt.datetime.strptime(self.adv_reg_data, '%d.%m.%Y')
					if inpt_date_reg_adv <= adv_data:
						self.get_profile_url(profile, adv_url, location, adv_title, adv_price, adv_image, adv_reg)
					else:
						pass

		except Exception as e:
			print(traceback.format_exc(), self.user_id, adv_url)
			pass	



	def get_profile_url(self, profile, adv_url, location, adv_title, adv_price, adv_image, adv_reg):
		try:
			if "https://www.bolha.com" in profile:
				self.profile_pars(profile, adv_url, location, adv_title, adv_price, adv_image, adv_reg)
			else:
				profile_url = "https://www.bolha.com" + profile
				self.profile_pars(profile_url, adv_url, location, adv_title, adv_price, adv_image, adv_reg)
		except Exception as e:
			pass

	def profile_pars(self, profile, adv_url, location, adv_title, adv_price, adv_image, adv_reg):
		try:
			r = requests.get(profile)
			html = BS(r.content, 'lxml')
			seller_name = html.find("h1", class_="UserProfileDetails-title").text.translate(dict.fromkeys(map(ord, whitespace)))
			seller_reg_data = html.find("p", class_="UserProfileDetails-subtitle").text.translate(dict.fromkeys(map(ord, whitespace))).split(':')[-1][:-1]
			sellreg_dt = dt.datetime.strptime(seller_reg_data, '%d.%m.%Y')
			tel_number_block = html.find("li", class_="UserProfileDetailsContactInfo-contactEntry--tel")
			if not tel_number_block:
				pass
			else:
				tel_number = tel_number_block.find("a")['data-display']
			check_business_acc = html.find("p", class_="UserProfileDetails-subtitle").text
			seller_ads_count = html.find("strong", class_="entities-count").text.translate(dict.fromkeys(map(ord, whitespace)))

			if self.seller_reg_data.lower() == "нет":
				self.check_business(adv_url, location, adv_title, adv_price, adv_image, adv_reg, seller_name, seller_reg_data, tel_number, seller_ads_count, check_business_acc)
			else:
				inpt_date_reg_seller = dt.datetime.strptime(self.seller_reg_data, '%d.%m.%Y')
				if inpt_date_reg_seller <= sellreg_dt:
					self.check_business(adv_url, location, adv_title, adv_price, adv_image, adv_reg, seller_name, seller_reg_data, tel_number, seller_ads_count, check_business_acc)
				else:
					pass
		except Exception as e:
			pass



	def check_business(self, adv_url, location, adv_title, adv_price, adv_image, adv_reg, seller_name, seller_reg_data, tel_number, seller_ads_count, check_business_acc):
		try:
			if self.business.lower() == "нет":
				if 'Trgovina' in check_business_acc:
					business = "Бизнесс аккаунт"
					self.display_results(adv_url, location, adv_title, adv_price, adv_image, adv_reg, seller_name, seller_reg_data, tel_number, seller_ads_count, business)
				else:
					business = "Частное лицо"
					self.display_results(adv_url, location, adv_title, adv_price, adv_image, adv_reg, seller_name, seller_reg_data, tel_number, seller_ads_count, business)
			elif self.business.lower() == "да":
				if 'Trgovina' in check_business_acc:
					pass
				else:
					business = "Частное лицо"
					self.display_results(adv_url, location, adv_title, adv_price, adv_image, adv_reg, seller_name, seller_reg_data, tel_number, seller_ads_count, business)
		except Exception as e:
			pass




	def display_results(self, adv_url, location, adv_title, adv_price, adv_image, adv_reg, seller_name, seller_reg_data, tel_number, seller_ads_count, buiss):
		if self.seller_adv_count.lower() == 'нет':
			self.check_repeated_number(adv_url, location, adv_title, adv_price, adv_image, adv_reg, seller_name, seller_reg_data, tel_number, seller_ads_count, buiss)


		elif int(seller_ads_count) <= int(self.seller_adv_count):
			self.check_repeated_number(adv_url, location, adv_title, adv_price, adv_image, adv_reg, seller_name, seller_reg_data, tel_number, seller_ads_count, buiss)

		else:
			pass


	def check_repeated_number(self, adv_url, location, adv_title, adv_price, adv_image, adv_reg, seller_name, seller_reg_data, tel_number, seller_ads_count, buiss):
		if self.repeated_number.lower() == 'да':
			self.ann_cnd += 1
			self.db.add_advertisement(self.user_id, self.platform, adv_title, adv_price, adv_reg, adv_url, location, adv_image, seller_name, tel_number, seller_ads_count, seller_reg_data, buiss)
			self.db.add_hash_advertisement(self.user_id, self.platform, adv_title, adv_price, adv_reg, adv_url, location, adv_image, seller_name, tel_number, seller_ads_count, seller_reg_data, buiss)
		elif self.repeated_number.lower() == 'нет':
			if(not self.db.get_tel_num(self.user_id, tel_number)):
				self.ann_cnd += 1
				self.db.add_advertisement(self.user_id, self.platform, adv_title, adv_price, adv_reg, adv_url, location, adv_image, seller_name, tel_number, seller_ads_count, seller_reg_data, buiss)
				self.db.add_hash_advertisement(self.user_id, self.platform, adv_title, adv_price, adv_reg, adv_url, location, adv_image, seller_name, tel_number, seller_ads_count, seller_reg_data, buiss)
			else:
				pass
		else:
			pass	
