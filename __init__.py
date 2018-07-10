bl_info = {
	"name": "Nexus Material Manager",
	"author": "Nexus Studio",
	"version": (0, 0, 2),
	"blender": (2, 79, 0),
	"location": "Properties > Material",
	"description": "Append materials",
	"warning": "",
	"wiki_url": "",
	"category": "Material",
}


import bpy
import os
from bpy.props import *
import bpy.utils.previews
from bpy.types import WindowManager

class MaterialPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__

	path_to_materials = bpy.types.Scene.path_to_materials = StringProperty(
		name="Path",
		default=os.path.join(os.path.dirname(__file__), "Materials"),
		description="The path to your materials",
		subtype="DIR_PATH",
	)

	def draw(self, context):
		layout = self.layout

		col = layout.column(align=True)
		col.prop(self, "path_to_materials")


def make_materials_category(path):

	dirs = os.listdir(path)
	print(dirs)
	i = 0
	mode_options = []

	for dir in dirs:
		if os.path.isdir(os.path.join(path, dir)):
			item = (dir, dir, '', i)
			mode_options.append(item)
			i += 1

	return mode_options

############################ Materials ##########################
def enum_materials_category(self, context):
	path_materials = bpy.context.window_manager.materials_dir

	return make_materials_category(path_materials)


# def enum_previews_material_items(self, context):

class MaterialsPreviewsPanel(bpy.types.Panel):

	bl_label = "Nexus Material Manager"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Nexus Material Manager"

	def draw(self, context):
		# furniture_prev = bpy.data.window_managers["WinMan"].furniture_previews
		# accessorie_prev = bpy.data.window_managers["WinMan"].accessorie_previews
		# detail_prev = bpy.data.window_managers["WinMan"].detail_previews
		layout = self.layout
		wm = context.window_manager


############## Furniture Panel ##############

		col = layout.column()
		col.prop(wm, "materials_dir")

		box = layout.box()
		box.label(text="MATERIALS")
####### Drop Down Menu
		row = box.row()
		row.prop(wm, "materials_category", text="")
####### Previews
# 		row = box.row()
# 		row.scale_y = 1.5
# 		row.template_icon_view(wm, "furniture_previews", show_labels=True)
# ####### Model Name
# 		row = box.row()
# 		row.alignment = 'CENTER'
# 		row.scale_y = 0.5
# 		row.label(os.path.splitext(furniture_prev)[0])
# ####### Add Button
# 		row = box.row()
# 		row.operator("add.furniture", icon="ZOOMIN", text="Add Furniture Model")


def test():
	blendfile = "C:\\Users\\hichi\\Desktop\\materials.blend"
	section = "\\Material\\"
	mat_name = "wood"
	key = True

	mat_path  = blendfile + section + mat_name
	directory = blendfile + section

	with bpy.data.libraries.load(blendfile) as (data_from, data_to):
		mat_list = [mat for mat in data_from.materials]
		#data_to.objects = data_from.objects
		#if data_from.groups:
				#data_to.groups = data_from.groups

	for mat in bpy.data.materials:
		if key == False:
			break
		for name in mat_list:
			if mat.name == mat_name:
				key = False
				break

	if key == True:
		bpy.ops.wm.append(filepath=mat_path, filename=mat_name, directory=directory)


def register():
	bpy.utils.register_class(MaterialPreferences)
	bpy.utils.register_module(__name__)


	user_preferences = bpy.context.user_preferences
	addon_prefs = user_preferences.addons[__name__].preferences

	WindowManager.materials_dir = StringProperty(
		name="Folder Path",
		subtype="DIR_PATH",
		default=addon_prefs.path_to_materials
		)

	# WindowManager.material_previews = EnumProperty(
	# 	items=enum_previews_material_items
	# 	)

	WindowManager.materials_category = EnumProperty(
		items=enum_materials_category
		)



def unregister():
	bpy.utils.unregister_class(MaterialPreferences)
	bpy.utils.unregister_module(__name__)

	del WindowManager.materials_dir
	del WindowManager.material_previews
	del WindowManager.materials_category



if __name__ == "__main__":
	register()
