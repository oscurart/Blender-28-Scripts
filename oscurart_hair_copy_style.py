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
# Usage: seleccionar destino y fuente. El destino no debe tener edicion. una vez corrido dar un pincelazo
# al aire para freezar
# Author: Eugenio Pignataro (Oscurart) www.oscurart.com.ar


import bpy

source = bpy.context.object
selObjs = bpy.context.selected_objects 
target = [o for o in selObjs if o != source][0]

print("source"+source.name)
print("target"+target.name)

psys = source.modifiers.active
selpsys = target.modifiers.active


depsgraph = bpy.context.evaluated_depsgraph_get()
source_eval = source.evaluated_get(depsgraph)
psys_source = source_eval.particle_systems[0]
target_eval = target.evaluated_get(depsgraph)
psys_target = target_eval.particle_systems[0]

for sourcePart,targetPart in zip(psys_source.particles,psys_target.particles):
    for sourceHK,targetHK in zip(sourcePart.hair_keys,targetPart.hair_keys):
        targetHK.co = sourceHK.co

bpy.ops.particle.disconnect_hair(all=True)
bpy.ops.particle.connect_hair(all=True)
