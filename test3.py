#!/usr/bin/python2

#import "platform_audit"
import web3 as proto

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
if __name__ == '__main__':
	unittest.main()
