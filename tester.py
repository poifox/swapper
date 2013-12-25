
import urllib
import httplib2

plugin_version = 0.1

class BlendSwapper:
	""" Base class for Swapper Plugin"""
	
	name = "Blend Swapper"
	
	version = plugin_version
	
	add_path = "/blends/apiadd.json"
	
	dev_server = "http://blendswap.dev"
	
	live_server = "http://www.blendswap.com"
	
	auth_path = "/users/apilogin.json"
	
	def __init_(self):
		self.server = self.dev_server
		self.client = httplib2.Http(".cache")
		if ( self.authenticate() ):
			print self.authCookie
			print "\n"
			self.headers = { 'Cookie': self.authCookie }
			self.response, self.content = self.client.request("http://blendswap.dev"+self.add_path,"POST",headers=self.headers)
			# print self.response, 
			print self.content
			return False
		else:
			print('Authentication error on ' + self.server)
	
	
	def authenticate(self):
		url = self.server + self.auth_path
		body = {'User[username]': 'poifox', 'User[password]': 'aEternal.45'}
		headers = {'Content-type': 'application/x-www-form-urlencoded'}
		self.authClient = httplib2.Http()
		response, content = self.authClient.request(url,"POST",headers=headers, body=urllib.urlencode(body))
		startCookie = response['set-cookie'].rindex('blend_swap')
		endCookie = len(response['set-cookie'])
		self.authCookie = response['set-cookie'][startCookie:endCookie]
		html_file = open("result.json","w")
		html_file.write(self.authCookie)
		html_file.close()
		return '200' == response['status']

swapper = BlendSwapper()
