
import requests
import json

class BlendSwapAuth:
	
	cookie = ""
	
	is_logged_in = False
	
	config_file = "config.json"
	
	server = "http://blendswap.dev"
	
	auth_path = "/users/apilogin.json"
	
	config = {
		"username": "",
		"password": "",
		"user_id": 0,
		"api_key": "",
		"cookie" : "",
		}
	
	def __init__(self):
		"""Init instance"""
		if not self.readConfig():
			print "Creating config.json..."
			self.createConfig()
		if not self.isSetup():
			self.setup()
		if not self.isLoggedIn():
			self.login()
	
	def readConfig(self):
		"""Load the config file and parse it to a local object"""
		config_string = ""
		
		try:
			CF = open(self.config_file,"r")
			config_string = CF.read()
		except IOError:
			print "File not found, creating a new one..."
		except ValueError:
			print "File is empty, creating a new one..."
		if not config_string:
			return False
		
		self.config = self.parseJson(config_string)
		return True
	
	
	def createConfig(self):
		"""Creates a new config file when it's absent"""
		return self.saveConfig()
	
	
	def isSetup(self):
		"""Check and see if config is ready for auth requests"""
		# TODO Add API KEY validation
		if (
				not self.config["username"] or 
				not self.config["password"] or
				not self.config["cookie"]):
			print "Auth module is not setup, setting up now..."
			return False
		return (
			len(self.config["username"]) > 0 and 
			len(self.config["password"]) > 0 and
			len(self.config["cookie"]) > 0 )
	
	
	def isLoggedIn(self):
		"""Return current login status"""
		if not self.isSetup():
			return False
		if not self.config["cookie"]:
			print "Logging into Blend Swap"
			self.login()
		return self.validateSession()
	
		
	def validateSession(self):
		"""Log in to Server"""
		url = self.server + self.auth_path
		headers = {"Cookie": self.config["cookie"]}
		req = requests.get(url,headers=headers)
		response = self.parseJson(req.text)
		return 1 == response["isLoggedIn"]
		
	
	def parseJson(self,body):
		"""Parse content and responses from JSON to objects"""
		result = json.loads(body)
		if "response" in result:
			return result["response"]
		return result
	
	
	def login(self):
		"""Send POST request to server so plugin is authorized
		This will also refresh the auth cookie. """
		url = self.server + self.auth_path
		data = {
			"User[username]": self.config["username"],
			"User[password]": self.config["password"],
		}
		req = requests.post(url,data=data)
		response = self.parseJson(req.text)
		if 1 == response["isLoggedIn"]:
			cookie = self.getCookie(req.headers)
			self.setConfig(key="cookie",value=cookie)
			self.config["user_id"] = response["user_id"]
			return self.saveConfig()
		return False
	
	
	def getCookie(self,headers=None):
		"""Gets the auth cookie from headers[set-cookie]"""
		if None == headers:
			return None
		startCookie = headers["set-cookie"].rindex("blend_swap")
		endCookie = len(headers["set-cookie"])
		return headers["set-cookie"][startCookie:endCookie]
	
	
	def saveConfig(self):
		"""Saves the current config to config.json"""
		try:
			CF = open(self.config_file,"w+")
			config_string = json.dumps(self.config,sort_keys=False)
			CF.write(config_string)
			CF.close()
		except IOError:
			print "An IO error happened when creating the config file!"
			return False
		except Exception:
			print "An unknown error happened when creatign the config file!"
			return False
		return True
	
	
	def setup(self):
		"""Setup auth module
		Get user input from keyboard or from blender fields."""
		keys = ("username","password","api_key")
		if not self.isSetup():
			print "Setting up auth module, please enter the values:"
		for k in keys:
			while not self.config[ k ]:
				self.setConfig( k )
		self.saveConfig()
		return self.isSetup()
	
	
	def setConfig(self,key,value=None):
		"""Set one key in config"""
		if not value:
			value = raw_input(key.title() + ": ")
		self.config[ key ] = value
		return value
