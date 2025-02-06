bl_info = {
    "name": "Transform Data Sender",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import requests
import os

# Custom Panel to Select Object and Transformation Type
class OBJECT_PT_custom_transform(bpy.types.Panel):
    bl_label = "Transform"
    bl_idname = "OBJECT_PT_custom_transform"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Transform'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "selected_object")
        
        if scene.selected_object:
            obj = bpy.data.objects.get(scene.selected_object)
            if obj:
                layout.label(text="Modify Transformations:")
                
                # Dropdown to select transformation type
                layout.prop(scene, "transform_type", text="Transformation Type")
                
                # Show transformation values based on the selected transformation type
                if scene.transform_type == "transform":
                    layout.label(text="Location: X={:.2f}, Y={:.2f}, Z={:.2f}".format(obj.location.x, obj.location.y, obj.location.z))
                    layout.label(text="Rotation: X={:.2f}, Y={:.2f}, Z={:.2f}".format(obj.rotation_euler.x, obj.rotation_euler.y, obj.rotation_euler.z))
                    layout.label(text="Scale: X={:.2f}, Y={:.2f}, Z={:.2f}".format(obj.scale.x, obj.scale.y, obj.scale.z))
                    layout.operator("object.submit_transform", text="Submit All Transforms")
                elif scene.transform_type == "translation":
                    layout.prop(obj, "location")
                    layout.operator("object.submit_transform", text="Submit Translation")
                elif scene.transform_type == "rotation":
                    layout.prop(obj, "rotation_euler", text="Rotation")
                    layout.operator("object.submit_transform", text="Submit Rotation")
                elif scene.transform_type == "scale":
                    layout.prop(obj, "scale")
                    layout.operator("object.submit_transform", text="Submit Scale")
                elif scene.transform_type == "file-path":
                    layout.operator("object.submit_transform", text="Submit File Path")

# Operator to Submit Transform Data
class OBJECT_OT_submit_transform(bpy.types.Operator):
    bl_idname = "object.submit_transform"
    bl_label = "Submit Transform Data"

    def execute(self, context):
        scene = context.scene
        obj_name = scene.selected_object
        obj = bpy.data.objects.get(obj_name)

        # Get the file path of the current Blender file
        file_path = bpy.data.filepath if bpy.data.is_saved else "Unsaved File"
        
        if scene.transform_type == "transform":
            if obj:
                data = {
                    "object_name": obj.name,
                    "file_path": file_path,
                    "changes": {
                        "location": {"x": obj.location.x, "y": obj.location.y, "z": obj.location.z},
                        "rotation": {"x": obj.rotation_euler.x, "y": obj.rotation_euler.y, "z": obj.rotation_euler.z},
                        "scale": {"x": obj.scale.x, "y": obj.scale.y, "z": obj.scale.z},
                    }
                }
                url = "http://localhost:5000/transform"
        elif scene.transform_type == "translation":
            if obj:
                data = {
                    "object_name": obj.name,
                    "translation": {"x": obj.location.x, "y": obj.location.y, "z": obj.location.z}
                }
                url = "http://localhost:5000/translation"
        elif scene.transform_type == "rotation":
            if obj:
                data = {
                    "object_name": obj.name,
                    "rotation": {"x": obj.rotation_euler.x, "y": obj.rotation_euler.y, "z": obj.rotation_euler.z}
                }
                url = "http://localhost:5000/rotation"
        elif scene.transform_type == "scale":
            if obj:
                data = {
                    "object_name": obj.name,
                    "scale": {"x": obj.scale.x, "y": obj.scale.y, "z": obj.scale.z}
                }
                url = "http://localhost:5000/scale"
        elif scene.transform_type == "file-path":
            data = {
                "file_path": file_path
            }
            url = "http://localhost:5000/file-path"

        # Send the data to the server
        try:
            response = requests.post(url, json=data)
            self.report({'INFO'}, f"Response: {response.text}")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")

        return {'FINISHED'}

# Update the object list when objects are added or removed
def update_object_list(self, context):
    items = [(obj.name, obj.name, "") for obj in bpy.data.objects]
    return items

# Register and Unregister Functions
def register():
    bpy.utils.register_class(OBJECT_PT_custom_transform)
    bpy.utils.register_class(OBJECT_OT_submit_transform)
    bpy.types.Scene.selected_object = bpy.props.EnumProperty(
        name="Select Object",
        description="Choose an object to modify",
        items=update_object_list
    )
    bpy.types.Scene.transform_type = bpy.props.EnumProperty(
        name="Transform Type",
        description="Select the transformation to modify",
        items=[
            ('transform', 'All Transforms', ""),
            ('translation', 'Position', ""),
            ('rotation', 'Rotation', ""),
            ('scale', 'Scale', ""),
            ('file-path', 'File Path', "")
        ]
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_custom_transform)
    bpy.utils.unregister_class(OBJECT_OT_submit_transform)
    del bpy.types.Scene.selected_object
    del bpy.types.Scene.transform_type

if __name__ == "__main__":
    register()
