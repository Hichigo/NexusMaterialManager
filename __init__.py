bl_info = {
	"name": "Nexus Material Manager",
	"author": "Nexus Studio",
	"version": (0, 2, 5),
	"blender": (2, 79, 0),
	"location": "Properties > Material",
	"description": "Append material",
	"warning": "",
	"wiki_url": "https://github.com/Hichigo/NexusMaterialManager",
	"category": "Material",
}


import bpy
import os
from bpy.props import *
import bpy.utils.previews
from bpy.types import WindowManager

class MaterialPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__

	path_to_material = bpy.types.Scene.path_to_material = StringProperty(
		name="Path",
		default=os.path.join(os.path.dirname(__file__), "Resource"),
		description="The path to your materials",
		subtype="DIR_PATH",
	)

	def draw(self, context):
		layout = self.layout

		col = layout.column(align=True)
		col.prop(self, "path_to_material")


def make_enum(path):

	dirs = os.listdir(path)
	i = 0
	mode_options = []

	for dir in dirs:
		if os.path.isdir(os.path.join(path, dir)):
			item = (dir, dir, '', i)
			mode_options.append(item)
			i += 1

	return mode_options

############################ Library ##########################
def enum_library_mat(self, context):
	resource_dir = bpy.context.window_manager.resource_dir
	path_material = os.path.join(resource_dir, "Materials")

	return make_enum(path_material)



############################ Material ##########################
def enum_type_mat(self, context):
	resource_dir = bpy.context.window_manager.resource_dir
	category = bpy.context.window_manager.library_mat
	path_category = os.path.join(resource_dir, "Materials", category)

	return make_enum(path_category)




def enum_previews_material_items(self, context):
	enum_items = []

	category = bpy.data.window_managers['WinMan'].type_mat
	path_material = bpy.data.window_managers['WinMan'].resource_dir
	directory = os.path.join(path_material, category)
	image_extensions = (".jpg", ".JPG", ".png", ".jpeg")

	if context is None:
		return enum_items

	wm = context.window_manager

	pcoll = material_collections["main"]

	if directory == pcoll.material_previews_dir:
		return pcoll.material_previews

	if directory and os.path.exists(directory):
		image_paths = []
		for fn in os.listdir(directory):
			if fn.endswith(image_extensions):
				image_paths.append(fn)

		for i, name in enumerate(image_paths):
			filepath = os.path.join(directory, name)

			if filepath in pcoll:
				enum_items.append((name, name, "", pcoll[filepath].icon_id, i))
			else:
				thumb = pcoll.load(filepath, filepath, 'IMAGE')
				enum_items.append((name, name, "", thumb.icon_id, i))
	enum_items.sort()

	pcoll.material_previews = enum_items
	pcoll.material_previews_dir = directory
	return pcoll.material_previews
	return

material_collections = {}

class MaterialPreviewsPanel(bpy.types.Panel):

	bl_label = "Nexus Material Manager"
	bl_idname = "nexus_mat_manager"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'material'


	@classmethod
	def poll(cls, context):
		return context.scene.render.engine == 'CYCLES' and context.active_object.material_slots.data.active_material

	def draw(self, context):
		material_prev = bpy.data.window_managers["WinMan"].material_previews
		layout = self.layout
		wm = context.window_manager


############## Material Panel ##############

		col = layout.column()
		col.prop(wm, "resource_dir")

		box = layout.box()
		box.label(text="MATERIAL")
####### Library
		row = box.row()
		row.label("Library")
		row.prop(wm, "library_mat", text="")
####### Type material
		row = box.row()
		row.label("Type")
		row.prop(wm, "type_mat", text="")
####### Previews
		row = box.row()
		row.scale_y = 1.5
		row.template_icon_view(wm, "material_previews", show_labels=True)
####### Model Name
		row = box.row()
		row.alignment = 'CENTER'
		row.scale_y = 0.5
		row.label(os.path.splitext(material_prev)[0])
####### Add Button
		row = box.row()
		row.operator("add.material", icon="ZOOMIN", text="Add Material")

class OBJECT_OT_AddMaterial(bpy.types.Operator):
	bl_idname = "add.material"
	bl_label = "Add Material"

	def execute(self, context):
		mat_name = os.path.splitext(bpy.data.window_managers["WinMan"].material_previews)[0]
		category = bpy.data.window_managers['WinMan'].type_mat
		path_material = bpy.data.window_managers['WinMan'].resource_dir
		filepath = os.path.join(path_material, category + ".blend")
		filepath_mat_section = filepath + "\\Material\\"
		key = True

		with bpy.data.libraries.load(filepath) as (data_from, data_to):
			mat_list = [mat for mat in data_from.materials]

		for mat in bpy.data.materials:
			if key == False:
				break
			for name in mat_list:
				if mat.name == mat_name:
					key = False
					break

		if key == True:
			bpy.ops.wm.append(filepath=filepath, filename=mat_name, directory=filepath_mat_section)
			context.active_object.material_slots[0].material = bpy.data.materials[mat_name]


		return{'FINISHED'}

class NexusMaterialManager_WM_Properties(bpy.types.PropertyGroup):

	material_category = EnumProperty(
		items=enum_type_mat
	)

	material_previews = EnumProperty(
		items=enum_previews_material_items
	)

def register():
	# WindowManager.nexus_material_manager = bpy.props.PointerProperty(type=NexusMaterialManager_WM_Properties)
	bpy.utils.register_class(MaterialPreferences)
	bpy.utils.register_module(__name__)


	user_preferences = bpy.context.user_preferences
	addon_prefs = user_preferences.addons[__name__].preferences

	WindowManager.resource_dir = StringProperty(
		name="Folder Path",
		subtype="DIR_PATH",
		default=addon_prefs.path_to_material
	)

	WindowManager.library_mat = EnumProperty(
		name="Library",
		items=enum_library_mat
	)

	WindowManager.type_mat = EnumProperty(
		name="Type",
		items=enum_type_mat
	)

	WindowManager.material_previews = EnumProperty(
		items=enum_previews_material_items
	)

	pcoll = bpy.utils.previews.new()
	pcoll.material_previews_dir = ""
	pcoll.material_previews = ()

	material_collections["main"] = pcoll


def unregister():
	bpy.utils.unregister_class(MaterialPreferences)
	bpy.utils.unregister_module(__name__)

	for pcoll in material_collections.values():
		bpy.utils.previews.remove(pcoll)
	material_collections.clear()

	# del WindowManager.nexus_material_manager.resource_dir
	del WindowManager.resource_dir
	del WindowManager.material_previews
	del WindowManager.type_mat



if __name__ == "__main__":
	register()
