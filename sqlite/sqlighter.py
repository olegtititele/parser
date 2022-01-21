import mysql.connector
from datetime import datetime, timedelta

# self.db = ['localhost','root', '1916Nikita565.']
# 		"""Подключаемся к БД"""
# 		self.adv_mydb = mysql.connector.connect(
# 			host=self.db[0],
# 			# port=self.db[1],
# 			user=self.db[1],
# 			passwd=self.db[2],
# 			database='testdb',
# 			)
# 		self.adv_cursor = self.adv_mydb.cursor(buffered=True)
# 		self.user_mydb = mysql.connector.connect(
# 			host=self.db[0],
# 			# port=self.db[1],
# 			user=self.db[1],
# 			passwd=self.db[2],
# 			database='users',
# 			)
# 		self.user_cursor = self.user_mydb.cursor(buffered=True)
# 		self.hash_mydb = mysql.connector.connect(
# 			host=self.db[0],
# 			# port=self.db[1],
# 			user=self.db[1],
# 			passwd=self.db[2],
# 			database='hash',
# 			)
# 		self.hash_cursor = self.hash_mydb.cursor(buffered=True)
# 		self.countriessub_mydb = mysql.connector.connect(
# 			host=self.db[0],
# 			# port=self.db[1],
# 			user=self.db[1],
# 			passwd=self.db[2],
# 			database='countries_subscribers',
# 			)
# 		self.countriessub_cursor = self.countriessub_mydb.cursor(buffered=True)
class SQLighter:

	def __init__(self):
		self.db = ['92.53.88.82', '6033', 'bluefasick', 'QUq8oHutp2Qk']
		self.adv_mydb = mysql.connector.connect(
			host=self.db[0],
			port=self.db[1],
			user=self.db[2],
			passwd=self.db[3],
			database='parsdb',
			)
		self.adv_cursor = self.adv_mydb.cursor(buffered=True)
		self.user_mydb = mysql.connector.connect(
			host=self.db[0],
			port=self.db[1],
			user=self.db[2],
			passwd=self.db[3],
			database='usersdb',
			)
		self.user_cursor = self.user_mydb.cursor(buffered=True)
		self.hash_mydb = mysql.connector.connect(
			host=self.db[0],
			port=self.db[1],
			user=self.db[2],
			passwd=self.db[3],
			database='hashdb',
			)
		self.hash_cursor = self.hash_mydb.cursor(buffered=True)
		self.countriessub_mydb = mysql.connector.connect(
			host=self.db[0],
			port=self.db[1],
			user=self.db[2],
			passwd=self.db[3],
			database='subscriptions',
			)
		self.countriessub_cursor = self.countriessub_mydb.cursor(buffered=True)

# """Действия с бд юзеров"""


	def add_user(self, user_id, username):
		try:
			sql = "INSERT INTO `users` (`user_id`, `username`) VALUES (%s,%s)"
			val = user_id, username
			self.user_cursor.execute(sql, val)
			self.user_mydb.commit()
			return
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.user_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='usersdb',
					)
				self.user_cursor = self.user_mydb.cursor(buffered=True)
				return self.add_user(user_id, username)
			raise e

	def check_user(self, user_id):
		try:
			self.user_cursor.execute("SELECT * FROM users WHERE `user_id` = %s", (user_id, ))
			data = self.user_cursor.fetchone()
			return data
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.user_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='usersdb',
					)
				self.user_cursor = self.user_mydb.cursor(buffered=True)
				return self.check_user(user_id)
			raise e



	def get_users_data(self):
		try:
			sql = "SELECT * FROM users"
			self.user_cursor.execute(sql)
			return self.user_cursor.fetchall()
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.user_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='usersdb',
					)
				self.user_cursor = self.user_mydb.cursor(buffered=True)
				return self.get_users_data()
			raise e



	def get_users_length(self):
		try:
			sql = "SELECT * FROM users"
			self.user_cursor.execute(sql)
			length = len(self.user_cursor.fetchall())
			return length
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.user_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='usersdb',
					)
				self.user_cursor = self.user_mydb.cursor(buffered=True)
				return self.get_users_length()
			raise e


	# def clear_users_table(self, user_id):
	# 	sql = "TRUNCATE TABLE `{}`".format(user_id)
	# 	self.user_cursor.execute(sql)
	# 	return



# """Действия с основной бд"""

	def create_advertisement_table(self, user_id):
		try:
			self.adv_cursor.execute("CREATE TABLE `%s` (`Площадка` VARCHAR(255), `Название объявления` VARCHAR(255), `Цена объявления` VARCHAR(255), `Дата создания объявления` VARCHAR(255), `Ссылка на объявление` VARCHAR(255), `Местоположение` VARCHAR(255), `Ссылка на изображение` VARCHAR(255), `Имя продавца` VARCHAR(255), `Номер продавца` VARCHAR(255), `Количество объявлений продавца` VARCHAR(255), `Дата регистрации` VARCHAR(255) DEFAULT NULL, `Бизнесс аккаунт` VARCHAR(255) DEFAULT NULL)", (user_id))
			return
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='parsdb',
					)
				self.adv_cursor = self.adv_mydb.cursor(buffered=True)
				return self.create_advertisement_table(user_id)
			raise e



	def add_advertisement(self, user_id, platform, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business):
		try:
			sql = "INSERT INTO `%s` (`Площадка`, `Название объявления`, `Цена объявления`, `Дата создания объявления`, `Ссылка на объявление`, `Местоположение`, `Ссылка на изображение`, `Имя продавца`, `Номер продавца`, `Количество объявлений продавца`, `Дата регистрации`, `Бизнесс аккаунт`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			val = user_id, platform, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business
			self.adv_cursor.execute(sql, val)
			self.adv_mydb.commit()
			return
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='parsdb',
					)
				self.adv_cursor = self.adv_mydb.cursor(buffered=True)
				return self.add_advertisement(user_id, platform, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business)
			raise e
	


	def get_len_previously_platfrom(self, user_id, platform):
		try:
			sql = "SELECT * FROM `%s` WHERE `Площадка`=%s"
			adr = (user_id, platform, )
			self.adv_cursor.execute(sql, adr)
			length = len(self.adv_cursor.fetchall())
			return length
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='parsdb',
					)
				self.adv_cursor = self.adv_mydb.cursor(buffered=True)
				return self.get_len_previously_platfrom(user_id, platform)
			raise e
	

	def get_previously_adv(self, user_id, platform):
		try:
			sql = "SELECT * FROM `%s` WHERE `Площадка`=%s"
			adr = (user_id, platform, )
			self.adv_cursor.execute(sql, adr)
			data = self.adv_cursor.fetchall()
			return data
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='parsdb',
					)
				self.adv_cursor = self.adv_mydb.cursor(buffered=True)
				return self.get_previously_adv(user_id, platform)
			raise e


	def delete_previously_adv(self, user_id, platform):
		try:
			sql = "DELETE FROM `%s` WHERE `Площадка`=%s"
			adr = (user_id, platform, )
			self.adv_cursor.execute(sql, adr)
			self.adv_mydb.commit()
			return
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='parsdb',
					)
				self.adv_cursor = self.adv_mydb.cursor(buffered=True)
				return self.delete_previously_adv(user_id, platform)
			raise e
	
		


	def len_advertisement_data(self, user_id):
		try:
			self.adv_cursor.execute("SELECT * FROM `%s`", (user_id,))
			length = len(self.adv_cursor.fetchall())
			print(length)
			return length
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='parsdb',
					)
				self.adv_cursor = self.adv_mydb.cursor(buffered=True)
				return self.len_advertisement_data(user_id)
			raise e



	def check_advestisement(self, user_id, adv_url):
		try:
			sql = "SELECT * FROM `%s` WHERE `Ссылка на объявление`=%s"
			adr = (user_id, adv_url, )
			self.adv_cursor.execute(sql, adr)
			data = self.adv_cursor.fetchone()
			return data
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='parsdb',
					)
				self.adv_cursor = self.adv_mydb.cursor(buffered=True)
				return self.check_advestisement(user_id, adv_url)
			raise e


	def get_tel_num(self, user_id, telnum):
		try:
			sql = "SELECT * FROM `%s` WHERE `Номер продавца`=%s"
			adr = (user_id, telnum, )
			self.adv_cursor.execute(sql, adr)
			data = self.adv_cursor.fetchone()
			return data
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='parsdb',
					)
				self.adv_cursor = self.adv_mydb.cursor(buffered=True)
				return self.get_tel_num(user_id, telnum)
			raise e


	def clear_advestisement(self, user_id):
		try:
			return self.adv_cursor.execute("TRUNCATE TABLE `%s`", (user_id,))
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='parsdb',
					)
				self.adv_cursor = self.adv_mydb.cursor(buffered=True)
				return self.clear_advestisement(user_id)
			raise e



# """Действия с временной бд"""

	def create_hash_table(self, tb_name):
		try:
			self.hash_cursor.execute("CREATE TABLE `%s` (`Площадка` VARCHAR(255), `Название объявления` VARCHAR(255), `Цена объявления` VARCHAR(255), `Дата создания объявления` VARCHAR(255), `Ссылка на объявление` VARCHAR(255), `Местоположение` VARCHAR(255), `Ссылка на изображение` VARCHAR(255), `Имя продавца` VARCHAR(255), `Номер продавца` VARCHAR(255), `Количество объявлений продавца` VARCHAR(255), `Дата регистрации` VARCHAR(255) DEFAULT NULL, `Бизнесс аккаунт` VARCHAR(255) DEFAULT NULL)", (tb_name, ))
			return
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='hashdb',
					)
				self.hash_cursor = self.hash_mydb.cursor(buffered=True)
				return self.create_hash_table(tb_name)
			raise e



	def add_hash_advertisement(self, user_id, platform, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business):
		try:
			sql = "INSERT INTO `%s` (`Площадка`, `Название объявления`, `Цена объявления`, `Дата создания объявления`, `Ссылка на объявление`, `Местоположение`, `Ссылка на изображение`, `Имя продавца`, `Номер продавца`, `Количество объявлений продавца`, `Дата регистрации`, `Бизнесс аккаунт`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			val = user_id, platform, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business
			self.hash_cursor.execute(sql, val)
			return self.hash_mydb.commit()
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='hashdb',
					)
				self.hash_cursor = self.hash_mydb.cursor(buffered=True)
				return self.add_hash_advertisement(user_id, platform, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business)
			raise e


	def get_hash_data(self, user_id):
	# """Получаем все элементы ВРЕМЕННОЙ бд"""
		try:
			self.hash_cursor.execute("SELECT * FROM `%s`", (user_id, ))
			return self.hash_cursor.fetchall()
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='hashdb',
					)
				self.hash_cursor = self.hash_mydb.cursor(buffered=True)
				return self.get_hash_data(user_id)
			raise e

	def clear_hash_data(self, tb_name):
		try:
			return self.hash_cursor.execute("TRUNCATE TABLE `%s`", (tb_name, ))
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='hashdb',
					)
				self.hash_cursor = self.hash_mydb.cursor(buffered=True)
				return self.clear_hash_data(tb_name)
			raise e


	def len_hash_data(self, user_id):
	# """Получаем длину ВРЕМЕННОЙ бд"""
		try:
			self.hash_cursor.execute("SELECT * FROM `%s`", (user_id, ))
			length = len(self.hash_cursor.fetchall())
			return length
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='hashdb',
					)
				self.hash_cursor = self.hash_mydb.cursor(buffered=True)
				return self.len_hash_data(user_id)
			raise e


	# def delete_table(self, tb_name):
	# 	try:
	# 		return self.adv_cursor.execute("DROP TABLE `%s`", (tb_name, ))
	# 	except Exception as e:
	# 		return		

	# def delete_hash_table(self, tb_name):
	# 	try:
	# 		return self.hash_cursor.execute("DROP TABLE `%s`", (tb_name, ))
	# 	except Exception as e:
	# 		return	

	# def delete_temporary_params_table(self, tb_name):
	# 	sql = "DROP TABLE `{}`".format(tb_name)
	# 	return self.temporaryparams_cursor.execute(sql)

	# def delete_users_table(self, tb_name):
	# 	try:
	# 		sql = "DROP TABLE `%s`"
	# 		return self.user_cursor.execute(sql, tb_name)
	# 	except Exception as e:
	# 		return	

	# def delete_users_subsc_database(self, country):
	# 	try:
	# 		sql = "DROP DATABASE `{}`".format(country)
	# 		return self.adv_cursor.execute(sql)
	# 	except Exception as e:
	# 		return	


# bolhasi
	# def create_countries_sub(self):
	# 	db = "CREATE DATABASE `{}`".format('countries_subscribers')
	# 	return self.adv_cursor.execute(db)

	def create_countries_sub_table(self, country):
		try:
			return self.countriessub_cursor.execute("CREATE TABLE `%s` (`ID` INT AUTO_INCREMENT PRIMARY KEY, `user_id` VARCHAR(255), `time_until` VARCHAR(255))", (country, ))
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='subscriptions',
					)
				self.countriessub_cursor = self.countriessub_mydb.cursor(buffered=True)
				return self.create_countries_sub_table(country)
			raise e


	def add_subscriber(self, country, user_id, time_until = datetime.now()):
		try:
			self.countriessub_cursor.execute("INSERT INTO `%s` (`user_id`, `time_until`) VALUES (%s,%s)", (country, user_id, time_until,))
			return self.countriessub_mydb.commit()
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='subscriptions',
					)
				self.countriessub_cursor = self.countriessub_mydb.cursor(buffered=True)
				return self.add_subscriber(country, user_id, time_until = datetime.now())
			raise e	

	def check_subscriber(self, country, user_id):
		try:
			sql = "SELECT * FROM `%s` WHERE `user_id` = %s"
			adr = (country, user_id,)
			self.countriessub_cursor.execute(sql, adr)
			data = self.countriessub_cursor.fetchone()
			return data
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='subscriptions',
					)
				self.countriessub_cursor = self.countriessub_mydb.cursor(buffered=True)
				return self.check_subscriber(country, user_id)
			raise e

	def get_subscriber_time(self, country, user_id):
		try:
			self.countriessub_cursor.execute("SELECT time_until FROM `%s` WHERE `user_id` = %s", (country, user_id,))
			sub_time = self.countriessub_cursor.fetchone()
			a = sub_time[0]
			b = a.split("-")
			c = b[2].split(" ")
			d = c[1].split(":")
			k = d[2].split(".")
			return datetime(int(b[0]), int(b[1]), int(c[0]), int(d[0]), int(d[1]), int(k[0]), int(k[1]))
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='subscriptions',
					)
				self.countriessub_cursor = self.countriessub_mydb.cursor(buffered=True)
				return self.get_subscriber_time(country, user_id)
			raise e


	def update_subsc_time(self, user_id, time_until, country):
		try:
			self.countriessub_cursor.execute("UPDATE `%s` SET `time_until` = %s WHERE `user_id` = %s", (country, time_until, user_id,))
			self.countriessub_mydb.commit()
		except Exception as e:
			if e.errno == 2055 or e.errno == 2013:
				print("popa4ka")
				self.adv_mydb = mysql.connector.connect(
					host=self.db[0],
					port=self.db[1],
					user=self.db[2],
					passwd=self.db[3],
					database='subscriptions',
					)
				self.countriessub_cursor = self.countriessub_mydb.cursor(buffered=True)
				return self.update_subsc_time(user_id, time_until, country)
			raise e

