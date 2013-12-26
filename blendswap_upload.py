
import requests

class BlendSwapUpload:
	
	def __init__(self, BAuth=None):
		if BAuth == None:
			return False
		self.bauth = BAuth
		return True
	
	def upload(self, filename=None, payload=None ):
		"""Sends file to server"""
		if filename == None or payload == None:
			return False
		return False
