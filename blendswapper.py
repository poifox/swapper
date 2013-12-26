
bl_info = {
	"name": "Blend Swapper",
	"author": "Jonathan Acosta",
	"blender": (2, 69, 0),
	"location": "File > Import-Export",
	"description": "Upload current blend file to Blend Swap",
	"warning": "",
	"wiki_url": "https://github.com/poifox/swapper/wiki",
	"tracker_url": "",
	"support": "",
	"category": "Import-Export"
}

from blendswap_auth import *
from blendswap_upload import *

out_of_blender = False

addon_version = "0.01"
addon_status = "DEV"

try:
	import bpy
except ImportError:
	out_of_blender = True

class Swapper():
	"""A plugin to upload ans share directly to Blend Swap"""
	
	bl_idname = "blendswap.upload"
	bl_label = "Upload to Blend Swap"
	bl_options = {"REGISTER", "UNDO"}
	
	def __init__(self):
		"""Construct and setup the instance"""
		self.bauth = BlendSwapAuth()
		self.bupload = BlendSwapUpload(self.bauth)
		if not self.bauth.isLoggedIn():
			print "You are not loggeed into Blend Swap."
	
	def execute(self, context):
		"""Used by the Blender Addon API"""
		# TODO basically everything
		return {"FINISHED"}
		
def register():
	# bpy.utils.register_class(Swapper)
	# Add UI here
	return False
	
def unregister():
	# bpy.utils.unregister_class(Swapper)
	# Remove UI here
	return False

if ( out_of_blender ):
	swapper = Swapper()
else:
	if __name__ == "__main__":
		register()
