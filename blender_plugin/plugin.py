bl_info = {
    "name": "Custom Transform Panel",
    "blender": (2, 90, 0),
    "category": "Object",
}

import bpy
import requests

# PropertyGroup for selecting the server function (transform, translation, rotation, scale)
class TransformServerSelection(bpy.types.PropertyGroup):
    endpoint: bpy.props.EnumProperty(
        name="Server Function",
        items=[("translation", "Translation", "Send position data to the server"),
               ("rotation", "Rotation", "Send rotation data to the server"),
               ("scale", "Scale", "Send scale data to the server"),
               ("transform", "Transform", "Send all transform data to the server")],
        default="translation"
    )

# Operator to send transform data (position, rotation, or scale) to the Flask server
class MYOBJECT_OT_send_position(bpy.types.Operator):
    bl_idname = "object.send_position"
    bl_label = "Send Position"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        transform_type = context.scene.transform_server.endpoint  # Get selected server function

        if transform_type == "translation":
            data = {"x": obj.location.x, "y": obj.location.y, "z": obj.location.z}
            endpoint = "/translation"
        elif transform_type == "rotation":
            data = {"x": obj.rotation_euler.x, "y": obj.rotation_euler.y, "z": obj.rotation_euler.z}
            endpoint = "/rotation"
        elif transform_type == "scale":
            data = {"x": obj.scale.x, "y": obj.scale.y, "z": obj.scale.z}
            endpoint = "/scale"
        else:  # default to /transform
            data = {
                "location": {"x": obj.location.x, "y": obj.location.y, "z": obj.location.z},
                "rotation": {"x": obj.rotation_euler.x, "y": obj.rotation_euler.y, "z": obj.rotation_euler.z},
                "scale": {"x": obj.scale.x, "y": obj.scale.y, "z": obj.scale.z},
            }
            endpoint = "/transform"

        try:
            # Send POST request to Flask server with the selected data
            response = requests.post(f"http://localhost:5000{endpoint}", json=data)
            if response.status_code == 200:
                self.report({'INFO'}, f"{transform_type.capitalize()} sent successfully")
            else:
                self.report({'ERROR'}, f"Failed to send {transform_type}")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
        return {'FINISHED'}

# Panel for displaying the object transform controls and sending data
class MYOBJECT_PT_transform(bpy.types.Panel):
    bl_label = "Custom Transformation Panel"
    bl_idname = "MYOBJECT_PT_transform"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Transform'

    def draw(self, context):
        layout = self.layout
        obj = context.object

        # Display object name and transformation controls
        layout.label(text="Object Name: {}".format(obj.name))
        layout.prop(obj, "location")
        layout.prop(obj, "rotation_euler")
        layout.prop(obj, "scale")

        # Dropdown to select the server function (transform, translation, rotation, scale)
        layout.prop(context.scene, "transform_server")

        # Button to send the selected transformation data to the server
        layout.operator("object.send_position", text="Send Transform Data")

# Registration and Unregistration
def register():
    bpy.utils.register_class(TransformServerSelection)
    bpy.utils.register_class(MYOBJECT_OT_send_position)
    bpy.utils.register_class(MYOBJECT_PT_transform)
    bpy.types.Scene.transform_server = bpy.props.PointerProperty(type=TransformServerSelection)

def unregister():
    bpy.utils.unregister_class(TransformServerSelection)
    bpy.utils.unregister_class(MYOBJECT_OT_send_position)
    bpy.utils.unregister_class(MYOBJECT_PT_transform)
    del bpy.types.Scene.transform_server

if __name__ == "__main__":
    register()
