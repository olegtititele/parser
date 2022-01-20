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
		sql = "INSERT INTO `users` (`user_id`, `username`) VALUES (%s,%s)"
		val = user_id, username
		self.user_cursor.execute(sql, val)
		self.user_mydb.commit()
		return

	def check_user(self, user_id):
		self.user_cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id, ))
		data = self.user_cursor.fetchone()
		return data


	def get_users_data(self):
		sql = "SELECT * FROM users"
		self.user_cursor.execute(sql)
		return self.user_cursor.fetchall()


	def get_users_length(self):
		sql = "SELECT * FROM users"
		self.user_cursor.execute(sql)
		length = len(self.user_cursor.fetchall())
		return length

	# def clear_users_table(self, user_id):
	# 	sql = "TRUNCATE TABLE `{}`".format(user_id)
	# 	self.user_cursor.execute(sql)
	# 	return



# """Действия с основной бд"""

	def create_advertisement_table(self, user_id):
		self.adv_cursor.execute("CREATE TABLE `%s` (`Площадка` VARCHAR(255), `Название объявления` VARCHAR(255), `Цена объявления` VARCHAR(255), `Дата создания объявления` VARCHAR(255), `Ссылка на объявление` VARCHAR(255), `Местоположение` VARCHAR(255), `Ссылка на изображение` VARCHAR(255), `Имя продавца` VARCHAR(255), `Номер продавца` VARCHAR(255), `Количество объявлений продавца` VARCHAR(255), `Дата регистрации` VARCHAR(255) DEFAULT NULL, `Бизнесс аккаунт` VARCHAR(255) DEFAULT NULL)", (user_id))
		return


	def add_advertisement(self, user_id, platform, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business):
		sql = "INSERT INTO `%s` (`Площадка`, `Название объявления`, `Цена объявления`, `Дата создания объявления`, `Ссылка на объявление`, `Местоположение`, `Ссылка на изображение`, `Имя продавца`, `Номер продавца`, `Количество объявлений продавца`, `Дата регистрации`, `Бизнесс аккаунт`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		val = user_id, platform, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business
		self.adv_cursor.execute(sql, val)
		self.adv_mydb.commit()
		return


	def get_len_previously_platfrom(self, user_id, platform):
		sql = "SELECT * FROM `%s` WHERE `Площадка`=%s"
		adr = (user_id, platform, )
		self.adv_cursor.execute(sql, adr)
		length = len(self.adv_cursor.fetchall())
		return length

	def get_previously_adv(self, user_id, platform):
		sql = "SELECT * FROM `%s` WHERE `Площадка`=%s"
		adr = (user_id, platform, )
		self.adv_cursor.execute(sql, adr)
		data = self.adv_cursor.fetchall()
		return data

	def delete_previously_adv(self, user_id, platform):
		sql = "DELETE FROM `%s` WHERE `Площадка`=%s"
		adr = (user_id, platform, )
		self.adv_cursor.execute(sql, adr)
		self.adv_mydb.commit()
		return 
		


	def len_advertisement_data(self, user_id):
		self.adv_cursor.execute("SELECT * FROM `%s`", (user_id,))
		length = len(self.adv_cursor.fetchall())
		print(length)
		return length


	def check_advestisement(self, user_id, adv_url):
		sql = "SELECT * FROM `%s` WHERE `Ссылка на объявление`=%s"
		adr = (user_id, adv_url, )
		self.adv_cursor.execute(sql, adr)
		data = self.adv_cursor.fetchone()
		return data

	def get_tel_num(self, user_id, telnum):
		sql = "SELECT * FROM `%s` WHERE `Номер продавца`=%s"
		adr = (user_id, telnum, )
		self.adv_cursor.execute(sql, adr)
		data = self.adv_cursor.fetchone()
		return data	

	def clear_advestisement(self, user_id):
		return self.adv_cursor.execute("TRUNCATE TABLE `%s`", (user_id,))


# """Действия с временной бд"""

	def create_hash_table(self, tb_name):
		self.hash_cursor.execute("CREATE TABLE `%s` (`Площадка` VARCHAR(255), `Название объявления` VARCHAR(255), `Цена объявления` VARCHAR(255), `Дата создания объявления` VARCHAR(255), `Ссылка на объявление` VARCHAR(255), `Местоположение` VARCHAR(255), `Ссылка на изображение` VARCHAR(255), `Имя продавца` VARCHAR(255), `Номер продавца` VARCHAR(255), `Количество объявлений продавца` VARCHAR(255), `Дата регистрации` VARCHAR(255) DEFAULT NULL, `Бизнесс аккаунт` VARCHAR(255) DEFAULT NULL)", (tb_name, ))
		return


	def add_hash_advertisement(self, user_id, platform, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business):
		sql = "INSERT INTO `%s` (`Площадка`, `Название объявления`, `Цена объявления`, `Дата создания объявления`, `Ссылка на объявление`, `Местоположение`, `Ссылка на изображение`, `Имя продавца`, `Номер продавца`, `Количество объявлений продавца`, `Дата регистрации`, `Бизнесс аккаунт`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		val = user_id, platform, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business
		self.hash_cursor.execute(sql, val)
		return self.hash_mydb.commit()


	def get_hash_data(self, user_id):
	# """Получаем все элементы ВРЕМЕННОЙ бд"""
		self.hash_cursor.execute("SELECT * FROM `%s`", (user_id, ))
		return self.hash_cursor.fetchall()

	def clear_hash_data(self, tb_name):
		return self.hash_cursor.execute("TRUNCATE TABLE `%s`", (tb_name, ))


	def len_hash_data(self, user_id):
	# """Получаем длину ВРЕМЕННОЙ бд"""
		self.hash_cursor.execute("SELECT * FROM `%s`", (user_id, ))
		length = len(self.hash_cursor.fetchall())
		return length


	def delete_table(self, tb_name):
		return self.adv_cursor.execute("DROP TABLE `%s`", (tb_name, ))

	def delete_hash_table(self, tb_name):
		return self.hash_cursor.execute("DROP TABLE `%s`", (tb_name, ))

	# def delete_temporary_params_table(self, tb_name):
	# 	sql = "DROP TABLE `{}`".format(tb_name)
	# 	return self.temporaryparams_cursor.execute(sql)

	def delete_users_table(self, tb_name):
		sql = "DROP TABLE `%s`"
		return self.user_cursor.execute(sql, tb_name)

	def delete_users_subsc_database(self, country):
		sql = "DROP DATABASE `{}`".format(country)
		return self.adv_cursor.execute(sql)	


# bolhasi
	# def create_countries_sub(self):
	# 	db = "CREATE DATABASE `{}`".format('countries_subscribers')
	# 	return self.adv_cursor.execute(db)

	def create_countries_sub_table(self, country):
		return self.countriessub_cursor.execute("CREATE TABLE `%s` (`ID` INT AUTO_INCREMENT PRIMARY KEY, `user_id` VARCHAR(255), `time_until` VARCHAR(255))", (country, ))

	def add_subscriber(self, country, user_id, time_until = datetime.now()):
		sql = "INSERT INTO `%s` (`user_id`, `time_until`) VALUES (%s,%s)"
		val = country, user_id, time_until
		self.countriessub_cursor.execute(sql, val)
		return self.countriessub_mydb.commit()

	def check_subscriber(self, country, user_id):
		adr = (country, user_id,)
		self.countriessub_cursor.execute("SELECT * FROM `%s` WHERE user_id = %s", adr)
		data = self.countriessub_cursor.fetchone()
		return data

	def get_subscriber_time(self, country, user_id):
		self.countriessub_cursor.execute("SELECT time_until FROM `%s` WHERE user_id = %s", (country, user_id,))
		sub_time = self.countriessub_cursor.fetchone()
		a = sub_time[0]
		b = a.split("-")
		c = b[2].split(" ")
		d = c[1].split(":")
		k = d[2].split(".")
		return datetime(int(b[0]), int(b[1]), int(c[0]), int(d[0]), int(d[1]), int(k[0]), int(k[1]))


	def update_subsc_time(self, user_id, time_until, country):
		sql = "UPDATE `%s` SET time_until = %s WHERE user_id = %s"
		val = (country, time_until, user_id)
		self.countriessub_cursor.execute(sql, val)
		self.countriessub_mydb.commit()


	# def clear_sub_data(self, country):
	# 	sql = "TRUNCATE TABLE `{}`".format(country)
	# 	return self.countriessub_cursor.execute(sql)


if __name__ == '__main__':
	sq = SQLighter()
	# sq.create_users_db()
	# sq.delete_users_subsc_database()
	# sq.clear_sub_data("bazar.lu")
	# sq.create_countries_sub()
	# sq.create_countries_sub_table("bolha.com")
	# sq.create_countries_sub_table("bazar.lu")
	# sq.delete_users_subsc_database('countri1es_subscribers')
	# sq.create_countries_sub_table("bazar.lu")
	# sq.delete_users_table('users')
	# sq.create_users_table()
	# sq.clear_hash_data(2029023685)
	# sq.clear_advestisement(2029023685)
	# sq.add_temporary_params(2029023685, "bolha.si", 'https://www.bolha.com/index.php?ctl=search_ads&keywords=apple', '25', 'нет', '21.03.2015', 'нет', 'нет')
	# sq.create_temporary_params_table(2029023685)
	# sq.delete_users_table('usersdb')
	# sq.delete_table(2029023685)
	# sq.delete_hash_table(2029023685)
	# sq.delete_temporary_params_table(2029023685)
	# sq.create_users_table()
	sq.get_advertisement_data(2029023685, "bolha.com")
	# for i in sq.get_advertisement_data(2029023685):
	# 	if i[0] == "bolha.com":

