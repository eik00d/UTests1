import sqlite3
import sys

class HelloUser:
	cmd=''
	params=[]
	current_role=-1
	db=None
	conn=None
	lastError=None
	
	def __init__(self):
		self.conn = sqlite3.connect(":memory:")
		self.db = self.conn.cursor()
		# Create table users -> name:password:role
		self.db.execute("CREATE TABLE users (name text, password text, role integer)")
		self.db.execute("INSERT INTO users VALUES ('admin','passw0rd',0)")

		self.conn.commit()
			
	def editUser(self):
		if self.current_role==0:
			
			try:
				self.params[2]=int(self.params[2])
			except:
				print "Role is not INT"
			else:
				strSQL="SELECT name FROM users WHERE name=?"
				role=self.db.execute(strSQL, [self.params[0]])
				res=role.fetchone()
				if not res:
					
					res=self.db.execute("INSERT INTO users VALUES (?,?,?)", [self.params[0],self.params[1],self.params[2]])
					
					self.conn.commit()
				else:
					
					res=self.db.execute("UPDATE users SET password=?, role=? WHERE name=?",[self.params[1],self.params[2],self.params[0]])
					
					self.conn.commit()
			
				
		elif self.current_role<0:
			print "ACCESS DENIED"
		else:
			strSQL="SELECT role FROM users WHERE name=?"
			role=self.db.execute(strSQL, [self.params[0]])
			res=role.fetchone()
			
			if res:
				if self.current_role==res[0]:
					self.db.execute("UPDATE users SET password=? WHERE name=?",[self.params[1],self.params[0]])
					self.conn.commit()
				else:
					print "AUTH ERROR"
			else:
				print "ERROR"
		
		
	def login(self):
	
		strSQL="SELECT role FROM users WHERE name=? AND password=?"
		role=self.db.execute(strSQL, [self.params[0],self.params[1]])
		res=role.fetchone()
		
		
		if res:
			self.current_role=res[0]
		else:
			self.current_role=-2

	def help(self):
		print "\nLogin: \t login <username> <password>"
		print "Edit/Add user (for adm): \t edit <username> <password> <role>"

	def parse(self,input):
		# Command
		self.cmd=input.split(" ")[0] 
		# Parametrs
		self.params=filter(None, input.split(" ")[1:])
		
		if self.cmd=='login':
			try:
				self.login()
				self.lastError=None
			except:
				print "AUTH ERROR!"
				self.lastError=sys.exc_info()[0]
			print "Logged in with ROLE: "+str(self.current_role)
			
		elif self.cmd=='help':
			self.help()
		elif self.cmd=='edit':
			try:
				self.editUser()
				self.lastError=None
			except:
				print "EDIT ERROR!"
				self.lastError=sys.exc_info()[0]
		else:
			self.help()
	
def main():
	User=HelloUser();
	
	while(1):
		input = raw_input("CMD: ")
		if input=='quit':
			break
		User.parse(input)
		
if __name__ == '__main__':
    main()
