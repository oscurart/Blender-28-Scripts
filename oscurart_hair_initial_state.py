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
# Usage: set the frame in the initial state and run. Then scrub the timeline.
# Author: Eugenio Pignataro (Oscurart) www.oscurart.com.ar


import bpy

obj = bpy.context.object
bpy.context.scene.render.engine = 'CYCLES'

psys = obj.modifiers["hair"] # CAMBIAR NOMBRE

# Connect and disconnect (needed, but why?)
bpy.ops.particle.disconnect_hair(all=True)
bpy.ops.particle.connect_hair(all=True)

""" https://developer.blender.org/T58792 """
#https://docs.blender.org/api/blender2.8/bpy.types.Depsgraph.html  <--- relevant?
depsgraph = bpy.context.evaluated_depsgraph_get()
object_eval = obj.evaluated_get(depsgraph)
psys_eval = object_eval.particle_systems[0]

psys = psys_eval

hd = { particle: [hk.co[:] for hk in particle.hair_keys] for i,particle in enumerate(psys.particles)}

psys.particles[0].hair_keys[-1].co

psys.use_hair_dynamics = False
bpy.context.scene.frame_set(frame=1)

for particle,list in hd.items():
    for hk,hkr in zip(list,particle.hair_keys):
        hkr.co = hk

     