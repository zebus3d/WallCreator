import bpy
class FabrickBrick(object):
    def create(self, name, sizex, sizey, sizez, coordx=0, coordy=0, coordz=0):
        bpy.ops.mesh.primitive_cube_add(size=1, align='WORLD', enter_editmode=False, location=(coordx, coordy, coordz))
        ob = bpy.context.object
        ob.name = name
        ob.scale.x = sizex
        ob.scale.y = sizey
        ob.scale.z = sizez
