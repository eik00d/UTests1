import sqlite3
import sys

class HelloUser:
	cmd=''
	params=[]
	current_role=-1
	db=None
	lastError=None
	
	def __init__(self):
		conn = sqlite3.connect(":memory:")
		c = conn.cursor()
		# Create table users -> name:password:role
		c.execute("CREATE TABLE users (name text, password text, role integer)")
		c.execute("INSERT INTO users VALUES ('admin','passw0rd',0)")
		conn.commit()
		self.db=c
		
	def login(self):
	
		strSQL="SELECT role FROM users WHERE name='%s' AND password='%s'" 
		role=self.db.execute(strSQL % (self.params[0],self.params[1]))
		res=role.fetchone()
		
		
		if res:
			self.current_role=res[0]
		else:
			self.current_role=-2
			
	def help(self):
		print "\nUSE: \t login <username> <password>"
		
	def parse(self,input):
		# Command
		self.cmd=input.split(" ")[0] 
		# Parametrs
		self.params=filter(None, input.split(" ")[1:])
		
		if self.cmd=='login':
			#try:
			self.login()
			self.lastError=None
			#except:
			#print "AUTH ERROR!"
			#self.lastError=sys.exc_info()[0]
				
			print "Logged in with ROLE: "+str(self.current_role)
			
		elif self.cmd=='help':
			self.help()
			
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
