###############################################
# LICENSE GPL
###############################################
'''
Copyright (c) 2012 Jorge Hernandez - Melendez
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

###############################################
# ADDON DATA
###############################################
bl_info = {
    "name": "Wall Creator",
    "description": "Wall Creator",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0, 3),
    "blender": (2, 93, 0),
    "location": "Left Toolbar > WallCreator",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"
}

###############################################
# Imports
###############################################
if "bpy" in locals():
    # si ya se hizo un import bpy entonces
    # se da por hecho que ya se cargo entonces se hace reload
    import imp # importamos imp para acceder a los internals de import
    #imp.reload(basics)    
    imp.reload(fabrickbrick)
else:
    # sino se hace el primer import
    # importando archivos en el mismo directorio que el __init__.py
    #from .basics import *
    from .fabrickbrick import *

import bpy
from bpy.props import *
import random

from bpy.utils import register_class
from bpy.utils import unregister_class

###############################################
# para tener un boton que recarga el addon
###############################################
import addon_utils
###############################################
addon_utils.enable("__init__", default_set=False, persistent=False, handle_error=None)
addon_utils.disable("__init__", default_set=False, handle_error=None)
class ReloadMyAdoon(bpy.types.Operator):
    bl_idname = "object.zebus_dialog2"
    bl_label = "Reset addon"
    def execute(self,context):
        addon_utils.disable("wallcreator")
        addon_utils.enable("wallcreator")
        return {'FINISHED'}
###############################################
        
class DialogOperator(bpy.types.Operator):
    bl_idname = "object.zebus_dialog"
    bl_label = "Wall Bricks Creator v03"
    ###############################################
    # Defaults:
    ###############################################
    muro_alto: IntProperty(name="alto", min=0, max=100, default=10)
    muro_ancho: IntProperty(name="ancho", min=0, max=100, default=6)
    ###############################################
    ladrillo_alto: FloatProperty(name="ladrillo_alto", min=0, max=100, default=5)
    ladrillo_profundo: FloatProperty(name="ladrillo_ancho", min=0, max=100, default=11.1)
    ladrillo_ancho: FloatProperty(name="ladrillo_largo", min=0, max=100, default=24)
    cementb: BoolProperty(name="cementb", default=False)
    cemento: FloatProperty(name="cemento", min=0, max=5, default=1.6)
    ###############################################
    centimetros: BoolProperty(name="centimetros", default=True)
    randomdepth: BoolProperty(name="random_depth", default=True)
    amountrand: FloatProperty(name="amountrand", min=1, max=15, default=1)
    fill_boundaryes: BoolProperty(name="fill_boundaryes", default=True)
    ###############################################
    
    def execute(self,context):
        ###############################################
        # MAIN
        ###############################################
        # Elimino solo los ladrillos anteriores:
        objects = bpy.context.scene.objects
        if objects:
            for ob in  objects:
                if ob.name.startswith('WC_ladrillo_'):
                    ob.select_set(True)
                    bpy.context.view_layer.objects.active = ob
                    bpy.ops.object.delete(use_global=False)


        # pongo blender en metros:
        bpy.context.scene.unit_settings.system = 'METRIC'

        centimetros = self.centimetros
        boundary = self.fill_boundaryes
        muro_ancho = self.muro_ancho
        muro_alto = self.muro_alto
        objects = bpy.data.objects
        randomdepth = self.randomdepth
        amountrand = self.amountrand
        cementb = self.cementb

        if centimetros:
            ladrillo_alto = self.ladrillo_alto/2/100
            ladrillo_ancho = self.ladrillo_ancho/2/100
            ladrillo_profundo = self.ladrillo_profundo/2/100
            if cementb:
                cemento = self.cemento/2/100
            else:
                cemento = 0
        else:
            ladrillo_alto = self.ladrillo_alto/2
            ladrillo_ancho = self.ladrillo_ancho/2
            ladrillo_profundo = self.ladrillo_profundo/2
            if cementb:
                cemento = self.cemento/2
            else:
                cemento = 0

        brick = FabrickBrick()
        mitad_ladri_ancho = (ladrillo_ancho/2)
        mitad_ladri_alto = (ladrillo_alto/2)
        for i in range(muro_alto):
            for j in range(muro_ancho):

                if randomdepth:
                    if centimetros:
                        # lo divido con 1000 para que sea un valor muy bajo y asi la funcion no sea inversa
                        nr = (0.0 + random.randint(1, 10))/1000*amountrand # numero random entre 0 y 2
                    else: # si esta en metros, para que el valor introducido por el usuario, guarde la proporcion y asi que no tenga q introducir otro valor
                        nr = (0.0 + random.randint(1, 10))/1000*amountrand*100 # y asi que no tenga q volver introducir otro nuevo valor
                else:
                    nr = 0

                if i%2 == 0: # para los pares:
                    brick.create("WC_ladrillo_"+str(i), \
                    ladrillo_ancho, \
                    ladrillo_profundo, \
                    ladrillo_alto, \
                    (j*(ladrillo_ancho+cemento))+ladrillo_ancho, \
                    0+nr, \
                    (i*(ladrillo_alto+cemento))+mitad_ladri_alto \
                    )
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                    # creando los medios ladrillos para el final o a la derecha:
                    if boundary: # si hay que hacer medios ladrillos para los bordes:                    
                        if j == muro_ancho-1: # si estamos en el ultimo creamos el medio ladrillo:
                            brick.create("WC_ladrillo_"+str(i), \
                            mitad_ladri_ancho-cemento, \
                            ladrillo_profundo, \
                            ladrillo_alto, \
                            (j*(ladrillo_ancho+cemento))+ladrillo_ancho+(mitad_ladri_ancho/2)+(cemento/2), \
                            0+nr, \
                            ((i*(ladrillo_alto+cemento))+ladrillo_alto+mitad_ladri_alto+cemento) \
                            )
                            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

                else: # para los impares los desplazo:
                    if boundary: # si hay que hacer medios ladrillos para los bordes:
                        if j == 0: # si estamos en los pares en el principio o a la izquierda creamos solo ese lado
                            brick.create("WC_ladrillo_"+str(i), \
                            mitad_ladri_ancho-cemento, \
                            ladrillo_profundo, \
                            ladrillo_alto, \
                            j+(mitad_ladri_ancho/2)-(cemento/2), \
                            0+nr, \
                            ((i*(ladrillo_alto+cemento))-mitad_ladri_alto-cemento) \
                            )
                            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                    # los impares enteros con desplazamiento:
                    brick.create("WC_ladrillo_"+str(i), \
                    ladrillo_ancho, \
                    ladrillo_profundo, \
                    ladrillo_alto, \
                    (j*(ladrillo_ancho+cemento)+mitad_ladri_ancho), \
                    0+nr, \
                    ((i*(ladrillo_alto+cemento)))+mitad_ladri_alto \
                    )
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)


        bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}
        ###############################################  

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=200)

    def draw(self, context):
        ###############################################
        # GUI Float WINDOW
        ###############################################
        layout = self.layout
        box = layout.box()
        col = box.column()
        ###############################################        
        col.label(text="Wall Settings:")
        rowsub0 = col.row()
        rowsub0.prop(self, "muro_alto", text='Height')
        rowsub0.prop(self, "muro_ancho", text='Width')
        ###############################################
        col.label(text="Brick Settings:")
        col.prop(self, "ladrillo_alto", text='Height')
        col.prop(self, "ladrillo_ancho", text='Width')
        col.prop(self, "ladrillo_profundo", text='Depth')
        col.prop(self, "randomdepth", text='Random pos in Depth')
        col.prop(self, "amountrand", text='Amount RandDepth')
        col.label(text="Cement Settings:")
        col.prop(self, "cementb", text='Enable Cement')
        col.prop(self, "cemento", text='Cement')
        ###############################################
        col.label(text="Units Settings:")
        col = box.column()
        col.prop(self, "centimetros", text='centimeters' )
        ###############################################
        col.label(text="Fill Settings:")
        col.prop(self, "fill_boundaryes", text='fill empty holes at the ends' )
        ###############################################

      
###############################################
# GUI TAB and BUTTON
###############################################
class DialogPanel(bpy.types.Panel):
    bl_label = "Buttons:"
    bl_category = "WallCreator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
 
    def draw(self, context):
        layout = self.layout
        context = bpy.context
        scn = context.scene
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'
        col.operator("object.zebus_dialog")
        ###############################################
        # para tener un boton que recarga el addon
        ###############################################
        # col.operator("object.zebus_dialog2")
        ###############################################


all_classes = [
    DialogOperator,
    ReloadMyAdoon,
    DialogPanel
]


###############################################       
#   Registration
###############################################
def register():
     for cls in all_classes:
        register_class(cls)
    

def unregister():
    for cls in reversed(all_classes):
        unregister_class(cls)
        
###############################################
# Register main
###############################################
if __name__ == "__main__":
    register()
###############################################
