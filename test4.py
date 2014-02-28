#!/usr/bin/python2

#import "platform_audit"
import web4 as proto

import unittest


'''Синтксис ввода: login <username> <passw> '''
class LoginTest(unittest.TestCase):
		TestUser=None
		
		def setUp(self):
			print "SETUP"
			self.TestUser=proto.HelloUser()
		def tearDown(self):
			print "CLEAR"
			self.TestUser=None
			reload(proto)
			
		'''По умолчанию не аутентифицированы'''
		def test_Auth0(self):
			self.assertTrue(self.TestUser.current_role<0, "По умолчанию роль должна быть отрицательной")
			
		'''Пробуем не правильный пароль'''
		def test_Auth1(self):
			self.TestUser.parse("login admin not_exist")
			self.assertTrue(self.TestUser.current_role<0,"Удалось получить роль без правильного пароля")  
			
		'''Пробуем не правильный логин и пароль'''
		def test_Auth2(self):
			self.TestUser.parse("login not_admin not_exist")
			self.assertTrue(self.TestUser.current_role<0,"Удалось получить роль без существующего логина")
			
		'''Пробуем не правильный логин и правельный пароль'''
		def test_Auth3(self):
			self.TestUser.parse("login not_admin passw0rd")
			self.assertFalse(self.TestUser.current_role==0,"Удалось получить роль без существующего логина")
			
		'''Пробуем  правильный логин и пароль'''
		def test_Auth4(self):
			self.TestUser.parse("login admin passw0rd")
			self.assertTrue(self.TestUser.current_role==0,"Должны получить нулевую роль")
			
		def test_Auth5(self):
			self.TestUser.parse("log1in admin aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
			self.assertTrue(self.TestUser.current_role<0,"Значение роли долэно быть отрицательным") 
			

'''Синтксис ввода: login <username> <passw> '''
class LoginSecurityTest(unittest.TestCase):
	def setUp(self):
		print "SETUP"
		self.TestUser=proto.HelloUser()
	def tearDown(self):
		print "CLEAR"
		self.TestUser=None
		reload(proto)
		
	'''LDAP Injection 1'''
	def test_LDAP1(self):
		self.TestUser.parse("login * *")
		self.assertFalse(self.TestUser.current_role==0, "LDAP Injection 1")
		
	'''LDAP Injection 2'''
	def test_LDAP2(self):
		self.TestUser.parse("login admin *")
		self.assertFalse(self.TestUser.current_role==0, "LDAP Injection 2")
		
	'''LDAP Injection 3'''
	def test_LDAP3(self):
		self.TestUser.parse("login admin)(&)) *")
		self.assertFalse(self.TestUser.current_role==0, "LDAP Injection 3")
		
	'''SQL Injection'''
	def test_SQL1(self):
		self.TestUser.parse("login admin' aaa")
		self.assertFalse(self.TestUser.current_role==0, "SQL Injection 1")
		
	'''SQL Injection 2'''
	def test_SQL2(self):
		self.TestUser.parse("login admin'-- aaa")
		self.assertFalse(self.TestUser.current_role==0, "SQL Injection 2")
		
	'''SQL Injection 3'''
	def test_SQL3(self):
		self.TestUser.parse("login admin aaa'or'1'like'1")
		self.assertFalse(self.TestUser.current_role==0, "SQL Injection 3")
		
	'''SQL Injection 4'''
	def test_SQL4(self):
		self.TestUser.parse("login admin '-0=0-'")
		self.assertFalse(self.TestUser.current_role==0, "SQL Injection 3")
		
	'''SQL Injection 5'''
	def test_SQL5(self):
		self.TestUser.parse("login admin 1'='2")
		self.assertFalse(self.TestUser.current_role==0, "SQL Injection 5")
		
	'''Input validation 1'''
	def test_SQL5(self):
		self.TestUser.parse("login'$%^&*\">< admin admin")
		self.assertFalse(self.TestUser.current_role==0, "Input validation 1")
		
	'''Input validation 2'''
	def test_SQL5(self):
		self.TestUser.parse("login admin'$%^&*\">< admin'$%^&*\"><")
		self.assertFalse(self.TestUser.current_role==0, "Input validation 2")
		

'''Синтксис ввода: edit <username> <passw> <role>'''
class EditTest(unittest.TestCase):
	def setUp(self):
		print "SETUP"
		self.TestUser=proto.HelloUser()
	def tearDown(self):
		print "CLEAR"
		self.TestUser=None
		reload(proto)
	'''По умолчанию не аутентифицированы'''
	def test_Edit1(self):
		self.TestUser.parse("edit admin passw0rd2 0")
		self.TestUser.parse("login admin passw0rd2")
		self.assertFalse(self.TestUser.current_role==0, "Без аутентифкации нельзя поменять пароль")
	'''Меняем себе пароль и роль'''
	def test_Edit2(self):
		self.TestUser.parse("login admin passw0rd")
		self.TestUser.parse("edit admin passw0rd2 1")
		self.TestUser.parse("login admin passw0rd")
		self.assertTrue(self.TestUser.current_role<0, "Меняем себе пароль и роль")
	'''Меняем себе пароль и роль'''
	def test_Edit3(self):
		self.TestUser.parse("login admin passw0rd")
		self.TestUser.parse("edit admin passw0rd2 1")
		self.TestUser.parse("login admin passw0rd2")
		self.assertTrue(self.TestUser.current_role==1, "Меняем себе пароль и роль")
	'''Добавляем пользователя'''
	def test_Edit4(self):
		self.TestUser.parse("login admin passw0rd")
		self.TestUser.parse("edit test test 1")
		self.TestUser.parse("login test test")
		self.assertTrue(self.TestUser.current_role==1, "Добавляем пользователя")
	'''Добавляем пользователя c ролью 0'''
	def test_Edit5(self):
		self.TestUser.parse("login admin passw0rd")
		self.TestUser.parse("edit test test 0")
		self.TestUser.parse("login test test")
		self.assertTrue(self.TestUser.current_role==0, "Добавляем пользователя 0")
	'''Пользователь 0 добавляет пользователя'''
	def test_Edit6(self):
		self.TestUser.parse("login admin passw0rd")
		self.TestUser.parse("edit test test 0")
		self.TestUser.parse("login test test")
		self.TestUser.parse("edit test2 test2 1")
		self.TestUser.parse("login test2 test2")
		self.assertTrue(self.TestUser.current_role==1, "Добавляем пользователя и еще")
	'''Пользователь 1 добавляет пользователя'''
	def test_Edit7(self):
		self.TestUser.parse("login admin passw0rd")
		self.TestUser.parse("edit test test 1")
		self.TestUser.parse("login test test")
		self.TestUser.parse("edit test2 test2 1")
		self.TestUser.parse("login test2 test2")
		self.assertTrue(self.TestUser.current_role<0, "Пользователь 1 добавляет пользователя")
	'''Пользователь 1 меняет себе пароль и роль'''
	def test_Edit8(self):
		self.TestUser.parse("login admin passw0rd")
		self.TestUser.parse("edit test test 1")
		self.TestUser.parse("login test test")
		self.TestUser.parse("edit test test2 3")
		self.TestUser.parse("login test test2")
		self.assertTrue(self.TestUser.current_role==1, "Добавляем пользователя 1 и роль")
	'''Пользователь 1 меняет пароль не себе'''
	def test_Edit9(self):
		self.TestUser.parse("login admin passw0rd")
		self.TestUser.parse("edit test test 1")
		self.TestUser.parse("edit test2 test2 2")
		self.TestUser.parse("login test test")
		self.TestUser.parse("edit test2 test3 3")
		self.TestUser.parse("login test2 test3")
		self.assertTrue(self.TestUser.current_role<0, "Пользователь 1 меняет пароль не себе")
		self.TestUser.parse("login test2 test2")
		self.assertTrue(self.TestUser.current_role==2, "Пользователь 1 меняет пароль не себе")
	'''Админ меняет пароль и роль'''
	def test_Edit10(self):
		self.TestUser.parse("login admin passw0rd")
		self.TestUser.parse("edit test test 1")
		self.TestUser.parse("edit test test2 2")
		self.TestUser.parse("login test test1")
		self.assertTrue(self.TestUser.current_role<0, "Админ меняет пароль и роль")
		self.TestUser.parse("login test test2")
		self.assertTrue(self.TestUser.current_role==2, "Админ меняет пароль и роль")

class EditSecurityTest(unittest.TestCase):
	def setUp(self):
		print "SETUP"
		self.TestUser=proto.HelloUser()
		self.TestUser.parse("login admin passw0rd")
		self.TestUser.parse("edit test1 test1 1")
		self.TestUser.parse("edit test2 test2 2")
	def tearDown(self):
		print "CLEAR"
		self.TestUser=None
		reload(proto)
	'''Валидация ввода'''
	def test_inputValidation(self):
		self.TestUser.parse("edit test'*&&<>56 test'$%><\" 5-3'%^&*()")
		
	'''SQLi 1'''
	def test_inputValidation2(self):
		self.TestUser.parse("edit test' test' 5-3")
		
		self.TestUser.parse("login test' test'")
		self.assertFalse(self.TestUser.current_role==2, "SQli")
		self.assertTrue(self.TestUser.current_role<0, "Validation error 2")

if __name__ == '__main__':
	unittest.main()
