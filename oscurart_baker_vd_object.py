#usage
#select the model with multires with the sculpt levels on top


import bpy

lr = bpy.context.object.copy()
lrd = bpy.context.object.data.copy()
hr = bpy.context.object.copy()
hrd = bpy.context.object.data.copy()
vl = bpy.context.object.modifiers[0].levels
bpy.context.collection.objects.link(lr)
bpy.context.collection.objects.link(hr)
lr.data = lrd
hr.data = hrd

for mod in lr.modifiers:
    lr.modifiers.remove(mod)

#pongo subdivision    
lrMod = lr.modifiers.new("subsurf", "SUBSURF")   
#seteo levels al lr
lrMod.levels = vl
lrMod.render_levels  = vl
#cambio nombre
lr.name = "LR"
hr.name = "HR"
#saco materiales
lr.data.materials.clear()
hr.data.materials.clear()

#creo materiales temps
hrMat = bpy.data.materials.new("hrTemp")
lrMat = bpy.data.materials.new("lrTemp")

#sumo materiales
lrd.materials.append(lrMat)
hrd.materials.append(hrMat)

#seteo lrMat
lrMat.use_nodes = True
lrImg = bpy.data.images.new("lrTemp", 2048,2048,alpha=False, float_buffer=True)
imgNodeLR = lrMat.node_tree.nodes.new("ShaderNodeTexImage")
geoNode = lrMat.node_tree.nodes.new("ShaderNodeNewGeometry")
imgNodeLR.image = lrImg
lrMat.node_tree.links.new(lrMat.node_tree.nodes['Material Output'].inputs['Surface'], geoNode.outputs['Position'])

#seteo hrMat
hrMat.use_nodes = True
hrImg = bpy.data.images.new("hrTemp", 2048,2048,alpha=False, float_buffer=True)
imgNodeHR = hrMat.node_tree.nodes.new("ShaderNodeTexImage")
geoNode = hrMat.node_tree.nodes.new("ShaderNodeNewGeometry")
imgNodeHR.image = hrImg
hrMat.node_tree.links.new(hrMat.node_tree.nodes['Material Output'].inputs['Surface'], geoNode.outputs['Position'])

#bake hr y lr
bpy.ops.object.select_all(action="DESELECT")
lr.select_set(True)
bpy.context.view_layer.objects.active = lr # usar este
bpy.ops.object.bake(type="EMIT")
bpy.ops.object.select_all(action="DESELECT")
hr.select_set(True)
bpy.context.view_layer.objects.active = hr # usar este
bpy.ops.object.bake(type="EMIT")

#se restan las imagenes
bpy.context.view_layer.objects.active = lr # usar este
hrRestaNode = lrMat.node_tree.nodes.new("ShaderNodeTexImage")
hrRestaNode.image = hrImg
restaImg = bpy.data.images.new("restaTemp", 2048,2048,alpha=False, float_buffer=True)
mixNode = lrMat.node_tree.nodes.new("ShaderNodeMixRGB")
mixNode.blend_type="SUBTRACT"
lrMat.node_tree.links.new(lrMat.node_tree.nodes['Material Output'].inputs['Surface'],mixNode.outputs['Color'])
lrMat.node_tree.links.new(mixNode.inputs[2], imgNodeLR.outputs[0])
lrMat.node_tree.links.new(mixNode.inputs[1], hrRestaNode.outputs[0])
mixNode.inputs['Fac'].default_value = 1

bpy.ops.object.select_all(action="DESELECT")
lr.select_set(True)
bakerNode = lrMat.node_tree.nodes.new("ShaderNodeTexImage")
bakerNode.image = restaImg
lrMat.node_tree.nodes.active = bakerNode
bakerNode.select=1

#bake diferencial
bpy.context.view_layer.objects.active = lr # usar este
bpy.ops.object.bake(type="EMIT")

#purga
"""
bpy.context.collection.objects.unlink(hr)
bpy.data.images.remove(lrImg)
bpy.data.images.remove(hrImg)
bpy.data.materials.remove(lrMat)
bpy.data.materials.remove(hrMat)
"""