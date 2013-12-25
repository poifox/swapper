
bl_info = {
	"name": "Blend Swapper",
	"author": "Campbell Barton",
	"blender": (2, 69, 0),
	"location": "File > Import-Export",
	"description": "Upload current blend file to Blend Swap",
	"warning": "",
	"wiki_url": "https://github.com/poifox/swapper/wiki",
	"tracker_url": "",
	"support": "",
	"category": "Import-Export"
}

# import sys
import string
import random
import base64
import urllib2
import httplib2
import mimetypes

is_testing = False

addon_version = "0.01"
addon_status = "DEV"
BOUNDARY_CHARS = string.digits + string.ascii_letters

try:
	import bpy
except ImportError:
	is_testing = True
	
try:
	import json
except ImportError:
	import simplejson as json

def esc_quote(s):
	return s.replace('"','\\"')

class BlendSwapper():
	"""A plugin to upload ans share directly to Blend Swap"""
	
	bl_idname = "blendswap.upload"
	bl_label = "Upload to Blend Swap"
	bl_options = {"REGISTER", "UNDO"}
	
	config = {}
	config_name = "config.json"
	config = {
		"user_id"  : 0,
		"username" : "",
		"password" : "",
		"api_key"  : "",
		"cookie"   : "",
	}
	
	is_logged_in = False
	
	
	server = "http://blendswap.dev"
	auth_path = "/users/apilogin.json"
	add_path = "/blends/apiadd.json"
	
	def __init__(self):
		"""Construct and setup the instance"""
		try:
			self.config_file = open(self.config_name,"r")
			settings_string = self.config_file.read()
			self.config = json.loads(settings_string)
		except IOError as e:
			print "Config file was not found, a new one will be created"
		except ValueError:
			print "Config file was empty, a new one will be created"
		self.saveConfig();
	
	def setupPlugin(self):
		"""Setup instance"""
		if self.isSetup():
			print "The plugin is setup, loging into services"
		else:
			print "We need your credentials, enter them now:"
			self.config["username"] = raw_input("Username: ")
			self.config["password"] = raw_input("Password: ")
			# self.config["api_key"] = raw_input("API Key: ")
		self.saveConfig()
	
	def isSetup(self):
		"""Confir if setup is good"""
		# TODO add API KEY validation
		return len(self.config["username"]) >= 2 and len(self.config["password"]) >= 1
		
	def saveConfig(self):
		"""Saves current configuration to config.json"""
		self.config_file = open(self.config_name,"w+")
		json_config = json.dumps(self.config)
		self.config_file.write(json_config)
		return None == self.config_file.close()
	
	def isLoggedIn(self):
		"""Check if user is already logged in"""
		if None == self.config['cookie']:
			return self.login()
		elif len(self.config['cookie']) < 50:
			return False
		elif not self.isSetup():
			return False
		else:
			return self.askLogin()
		return False
	
	def askLogin(self):
		"""Ask the server if user is logged in"""
		adapter = httplib2.Http(".cache")
		url = self.server + self.auth_path
		headers = {"Cookie": self.config["cookie"]}
		resp, content = adapter.request(url,"GET",headers=headers)
		response = self.parseResponse(content)
		self.saveConfig()
		if response['isLoggedIn'] == 0:
			self.login()
		else:
			print "You are logged in already :)"
		return response["isLoggedIn"] == 1
	
	def parseResponse(self,content):
		"""Parses the json response from the Blend Swap API"""
		parsed = json.loads(content)
		return parsed["response"]
	
	def getAuthCookie(self, resp):
		"""Splits the set-cookie to get the useful part of it so it can be saved to config.json"""
		startCookie = resp["set-cookie"].rindex("blend_swap")
		endCookie = len(resp["set-cookie"])
		return resp["set-cookie"][startCookie:endCookie]
	
	def login(self):
		"""Logs in to server and saves the cookie returned by the server for subsequent transactions"""
		url = self.server + self.auth_path
		body = {"User[username]": self.config["username"], "User[password]": self.config["password"]}
		headers = {"Content-type": "application/x-www-form-urlencoded"}
		adapter = httplib2.Http(".cache")
		resp, content = adapter.request(url,"POST",headers=headers,body=urllib2.urlencode(body))
		# print resp, content
		response = self.parseResponse(content)
		if response["user_id"] > 0:
			self.config["user_id"] = response["user_id"]
			self.config["cookie"] = self.getAuthCookie(resp)
			print "You are now logged into Blend Swap"
		else:
			print "There was an error logging in to Blend Swap"
		self.saveConfig()
		return response['isLoggedIn'] == 1
		
	def sendFile(self,filename=""):
		"""Send a file to BlendSwap"""
		if "" == filename:
			return False
		print "Sending " + filename
		form_data = {
			"body": "This is the description of the blend",
			"tags": "taggy, tagger, tagaru",
			"title": "Test title",
			"user_id": self.config["user_id"],
			"fan_art": 1,
			"blender_version": 268 }
		upload_file = {
			"File[blend_file]": {
				"filename": filename, 
				"content": open(filename,"rb").read()
				}
			}
		headers, body = self.encode_multipart(form_data,upload_file)
		url = self.server + self.add_path
		# print url
		adapter = httplib2.Http('.cache')
		resp, content = adapter.request(url,"POST",headers=headers,body=body)
		print resp, content
		return False
	
	def encode_multipart(self,fields, files):
		BOUNDARY = ''.join(random.choice(BOUNDARY_CHARS) for i in range(8))
		lines = []
		for name, value in fields.items():
			lines.extend((
				"--{0}".format(BOUNDARY),
				'Content-Disposition: form-data; name="Blend[{0}]"'.format(esc_quote(name)),
				'',
				str(value)
				))
		# THIS IS NOT WORKING YET
		# for name, value in files.items():
		# 	filename = value['filename']
		# 	mimetype = mimetypes.guess_type(filename,strict=False)[0] or "application/octet-stream"
		# 	lines.extend((
		# 		'--{0}'.format(BOUNDARY),
		# 		'Content-Disposition: file; filename="{1}"'.format(
		# 			esc_quote(name),esc_quote(filename)
		# 			),
		# 			'Content-Type: {0}'.format(mimetype),
		# 			'Content-Transfer-Encoding: binary',
		# 			'',
		# 			value['content']
		# 		))
		lines.extend((
			"--{0}--".format(BOUNDARY),
			'',
			))
		body = "\r\n".join(lines)
		print body
		headers = {
			'Content-Type': 'multipart/form-data; boundary={0}'.format(BOUNDARY),
			'Content-Length': str(len(body)),
			'Cookie': self.config["cookie"]
		}
		return (headers, body)
	
		
	def execute(self, context):
		"""Used by the Blender Addon API"""
		# TODO basically everything
		return {"FINISHED"}
		
def register():
	# bpy.utils.register_class(BlendSwapper)
	# Add UI here
	return False
	
def unregister():
	# bpy.utils.unregister_class(BlendSwapper)
	# Remove UI here
	return False

if ( is_testing ):
	blendswapper = BlendSwapper()
	blendswapper.setupPlugin()
	if not blendswapper.isLoggedIn():
		blendswapper.login()
	blendswapper.sendFile("test.blend")
else:
	if __name__ == "__main__":
		register()
