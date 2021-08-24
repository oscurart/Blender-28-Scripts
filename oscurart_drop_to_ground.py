import bpy

C = bpy.context
for ob in bpy.context.selected_objects:
    #mesh creation
    ob.matrix_world.copy()
    dg = C.evaluated_depsgraph_get()
    ob_eval = ob.evaluated_get(dg)
    nm = bpy.data.meshes.new_from_object(ob_eval)
    nm.transform(ob.matrix_world)
    #evaluate
    vl = min([vert.co[-1] for vert in nm.vertices])
    ob.location[2] -= vl
