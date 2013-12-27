
import bpy

bl_info = {
    "name": "Upload to Blend Swap",
    "author": "Jonathan Acosta",
    "blender": (2, 69, 0),
    "location": "File > Import-Export",
    "description": "Upload your blend directly to blend Swap",
    "warning": "Such dangerous. Very pre-alfa. wow",
    "support": "TESTING",
    "category": "Import-Export",
    }

import bpy
from bpy.props import (BoolProperty,
                       EnumProperty,
                       StringProperty
                       )
from bpy_extras.io_utils import ExportHelper

class Swapper(bpy.types.Operator, ExportHelper):
    """Manage uploads to Blend dSwap"""
    
    bl_idname = "blendswap.upload"
    bl_label = "Upload to Blend Swap"
    bl_options = {}
    
    filename_ext = ".blend"
    
    def execute(self, context):
        return {"FINISHED"}

def menu_func_export(self,context):
    self.layout.operator(Swapper.bl_idname,text="Upload to Blend Swap")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
