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


bl_info = {
    "name": "Wall Creator",
    "description": "Wall Creator",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0, 5),
    "blender": (2, 93, 0),
    "location": "Left Toolbar > WallCreator",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"
}

import bpy
import random
from .fabrickbrick import FabrickBrick
from bpy.utils import register_class, unregister_class
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import IntProperty, FloatProperty, BoolProperty


def UpdatedFunction(self, context):
    bpy.context.window_manager.zwc.first_time = False

    ###########################################################
    # Elimino solo los ladrillos anteriores y los orphan data #
    ###########################################################
    bpy.ops.object.select_all(action='DESELECT')

    for ob in bpy.context.scene.objects:
        if ob.name.startswith('ZWC_brick_'):
            ob.select_set(True)
            bpy.context.view_layer.objects.active = ob

    bpy.ops.object.delete(use_global=False)

    for mesh in bpy.data.meshes:
        if mesh.name.startswith('ZWC_brick_') and mesh.users == 0:
            bpy.data.meshes.remove(mesh, do_unlink=True, do_id_user=True)

    ###########################################################

    # pongo blender en metros:
    bpy.context.scene.unit_settings.system = 'METRIC'

    centimetros = bpy.context.window_manager.zwc.centimetros
    boundary = bpy.context.window_manager.zwc.fill_boundaryes
    muro_ancho = bpy.context.window_manager.zwc.muro_ancho
    muro_alto = bpy.context.window_manager.zwc.muro_alto
    # objects = bpy.data.objects
    randomdepth = bpy.context.window_manager.zwc.randomdepth
    amountrand = bpy.context.window_manager.zwc.amountrand
    cementb = bpy.context.window_manager.zwc.cementb

    if centimetros:
        ladrillo_alto = bpy.context.window_manager.zwc.ladrillo_alto/2/100
        ladrillo_ancho = bpy.context.window_manager.zwc.ladrillo_ancho/2/100
        ladrillo_profundo = bpy.context.window_manager.zwc.ladrillo_profundo/2/100
        if cementb:
            cemento = bpy.context.window_manager.zwc.cemento/2/100
        else:
            cemento = 0
    else:
        ladrillo_alto = bpy.context.window_manager.zwc.ladrillo_alto/2
        ladrillo_ancho = bpy.context.window_manager.zwc.ladrillo_ancho/2
        ladrillo_profundo = bpy.context.window_manager.zwc.ladrillo_profundo/2
        if cementb:
            cemento = bpy.context.window_manager.zwc.cemento/2
        else:
            cemento = 0

    brick = FabrickBrick()
    mitad_ladri_ancho = (ladrillo_ancho/2)
    mitad_ladri_alto = (ladrillo_alto/2)
    # J es X
    # I es Y
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
                brick.create("ZWC_brick_row_"+str(i)+"_col_"+str(j),
                             ladrillo_ancho,
                             ladrillo_profundo,
                             ladrillo_alto,
                             (j*(ladrillo_ancho+cemento))+ladrillo_ancho,
                             0+nr,
                             (i*(ladrillo_alto+cemento))+mitad_ladri_alto
                             )

                # creando los medios ladrillos para el final o a la derecha:
                if boundary: # si hay que hacer medios ladrillos para los bordes:
                    if j == muro_ancho-1 and i < muro_alto-1: # si estamos en el ultimo creamos el medio ladrillo:
                        brick.create("ZWC_brick_right_boundary_"+str(i),
                                     mitad_ladri_ancho-cemento,
                                     ladrillo_profundo,
                                     ladrillo_alto,
                                     (j*(ladrillo_ancho+cemento))+ladrillo_ancho+(mitad_ladri_ancho/2)+(cemento/2),
                                     0+nr,
                                     ((i*(ladrillo_alto+cemento))+ladrillo_alto+mitad_ladri_alto+cemento)
                                     )

            else: # para los impares los desplazo:
                if boundary: # si hay que hacer medios ladrillos para los bordes:
                    # print("i ", i)
                    # print("j ", j)
                    if j == 0: # si estamos en los pares en el principio o a la izquierda creamos solo ese lado
                        brick.create("ZWC_brick_left_boundary_"+str(i),
                                     mitad_ladri_ancho-cemento,
                                     ladrillo_profundo,
                                     ladrillo_alto,
                                     j+(mitad_ladri_ancho/2)-(cemento/2),
                                     0+nr,
                                     ((i*(ladrillo_alto+cemento))-mitad_ladri_alto-cemento)
                                     )
                    # me faltaba con la altura total en numeor impar me faltaba el ladrillo del boudary izquierdo de arrib del todo
                    # por eso he creado esta otra regla extra:
                    if i+2 == muro_alto and j == 0:
                        brick.create("ZWC_brick_left_boundary_"+str(i),
                                     mitad_ladri_ancho-cemento,
                                     ladrillo_profundo,
                                     ladrillo_alto,
                                     j+(mitad_ladri_ancho/2)-(cemento/2),
                                     0+nr,
                                     ((i*(ladrillo_alto+cemento))-mitad_ladri_alto+cemento+(ladrillo_alto*2))
                                     )
                # los impares enteros con desplazamiento:
                brick.create("ZWC_brick_row_"+str(i)+"_col_"+str(j),
                             ladrillo_ancho,
                             ladrillo_profundo,
                             ladrillo_alto,
                             (j*(ladrillo_ancho+cemento)+mitad_ladri_ancho),
                             0+nr,
                             ((i*(ladrillo_alto+cemento)))+mitad_ladri_alto
                             )

    bpy.ops.object.select_all(action='DESELECT')


class zwc_properties(PropertyGroup):
    muro_alto: IntProperty(name="alto", min=0, max=100, default=10, update=UpdatedFunction)
    muro_ancho: IntProperty(name="ancho", min=0, max=100, default=6, update=UpdatedFunction)
    ladrillo_alto: FloatProperty(name="ladrillo_alto", min=0, max=100, default=5, update=UpdatedFunction)
    ladrillo_profundo: FloatProperty(name="ladrillo_ancho", min=0, max=100, default=11.1, update=UpdatedFunction)
    ladrillo_ancho: FloatProperty(name="ladrillo_largo", min=0, max=100, default=24, update=UpdatedFunction)
    cementb: BoolProperty(name="cementb", default=False, update=UpdatedFunction)
    cemento: FloatProperty(name="cemento", min=0, max=5, default=1.6, update=UpdatedFunction)
    centimetros: BoolProperty(name="centimetros", default=True, update=UpdatedFunction)
    randomdepth: BoolProperty(name="random_depth", default=False, update=UpdatedFunction)
    amountrand: FloatProperty(name="amountrand", min=0, max=15, default=1, update=UpdatedFunction)
    fill_boundaryes: BoolProperty(name="fill_boundaryes", default=True, update=UpdatedFunction)
    first_time: BoolProperty(name="first_time", default=True)
    bevel: BoolProperty(name="bevel", default=False, update=UpdatedFunction)
    bevel_amount: FloatProperty(name="bevel_amount", min=0.000, max=1.0, default=0.002, precision=3, update=UpdatedFunction)


class MAIN_OT_operator(Operator):
    bl_idname = "main.operator"
    bl_label = "Wall Bricks Creator v05"
    bl_category = "WallCreator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def execute(self, context):
        UpdatedFunction(self, context)
        return {'FINISHED'}


class MAIN_PT_panel(Panel):
    bl_idname = "main.panel"
    bl_label = "Wall Bricks Creator v04"
    bl_category = "WallCreator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.use_property_split = True
        layout.use_property_decorate = False
        flow = layout.grid_flow(align=True)
        col = flow.column()

        if bpy.context.window_manager.zwc.first_time:
            col.operator("main.operator", text='Start')
        else:
            col.label(text="Wall Settings:")
            col.prop(bpy.context.window_manager.zwc, "muro_alto", text='Height')
            col.prop(bpy.context.window_manager.zwc, "muro_ancho", text='Width')
            col.label(text="Brick Settings:")
            col.prop(bpy.context.window_manager.zwc, "ladrillo_alto", text='Height')
            col.prop(bpy.context.window_manager.zwc, "ladrillo_ancho", text='Width')
            col.prop(bpy.context.window_manager.zwc, "ladrillo_profundo", text='Depth')
            col.prop(bpy.context.window_manager.zwc, "randomdepth", text='Random pos in Depth')
            col.prop(bpy.context.window_manager.zwc, "amountrand", text='Amount RandDepth')
            col.prop(bpy.context.window_manager.zwc, "bevel", text='Bevel')
            col.prop(bpy.context.window_manager.zwc, "bevel_amount", text='Bevel Amount')
            col.label(text="Cement Settings:")
            col.prop(bpy.context.window_manager.zwc, "cementb", text='Enable Cement')
            col.prop(bpy.context.window_manager.zwc, "cemento", text='Cement')
            col.label(text="Units Settings:")
            col.prop(bpy.context.window_manager.zwc, "centimetros", text='centimeters' )
            col.label(text="Fill Settings:")
            col.prop(bpy.context.window_manager.zwc, "fill_boundaryes", text='fill empty holes at the ends' )


all_classes = [
    zwc_properties,
    MAIN_OT_operator,
    MAIN_PT_panel,
]


def register():
    for cls in all_classes:
        register_class(cls)

    bpy.types.WindowManager.zwc = bpy.props.PointerProperty(type=zwc_properties)


def unregister():
    for cls in reversed(all_classes):
        unregister_class(cls)

    del bpy.types.WindowManager.zwc


if __name__ == "__main__":
    register()
