#select loop and run

import bpy
import bmesh

def getOrder():
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    selEdges = [edge for edge in bm.edges if edge.select]
    #lista de vertices y edges 
    connections = {}
    for edge in selEdges:
        for vert in edge.verts:
            connections.setdefault(vert.index,[]).append(edge.index)
    #creo vertice inicial de punta
    for vert, edgelist in connections.items():
        if len(edgelist) == 1:
            startVert = vert
            break
    order = [startVert]
    for i in range(len(selEdges)):
        tempVal = connections[startVert][0]
        connections.pop(startVert)
        for vert, edgelist in connections.items():
            if tempVal in edgelist:        
                order.append(vert)
                startVert = vert
                connections[vert].remove(tempVal)
                break    
    bm.select_flush_mode()                
    return(order)            

# mesh     
LoopOrder = getOrder()
bm = bmesh.from_edit_mesh(bpy.context.object.data)
percents = []
total = 0
difTipEnd = bm.verts[LoopOrder[-1]].co - bm.verts[LoopOrder[0]].co

prevPercent = 0
for segment in range(len(LoopOrder)-1):
    dif = (bm.verts[LoopOrder[segment+1]].co - bm.verts[LoopOrder[segment]].co).length
    percent = dif  /difTipEnd.length 
    bm.verts[LoopOrder[segment+1]].co = difTipEnd * (percent+prevPercent) + bm.verts[LoopOrder[0]].co
    prevPercent += percent


bmesh.update_edit_mesh(bpy.context.object.data)
