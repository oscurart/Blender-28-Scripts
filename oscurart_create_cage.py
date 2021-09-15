# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

#Usage: select object in object mode and run
#This addon create a new cage from bake settings

import bpy

ce = bpy.context.scene.render.bake.cage_extrusion

selObMatrix = bpy.context.object.matrix_world.copy()

depsgraph = bpy.context.evaluated_depsgraph_get()
object_eval = bpy.context.object.evaluated_get(depsgraph)
nMesh = bpy.data.meshes.new_from_object(object_eval)

actCollection = bpy.context.view_layer.active_layer_collection.collection

cageObj = bpy.data.objects.new("Cage", nMesh)

actCollection.objects.link(cageObj)

for vert in cageObj.data.vertices:
    vert.co = vert.co + (vert.normal*ce)
    
bpy.context.scene.render.bake.cage_object = cageObj 
cageObj.matrix_world = selObMatrix

