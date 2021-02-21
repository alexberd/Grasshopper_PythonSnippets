#coding=utf-8
import Rhino
from Rhino import *
from Rhino.DocObjects import *
from Rhino.Commands import *
from Rhino.Geometry import *
from scriptcontext import doc

# function written by Giulio Piacentino, giulio@mcneel.com
def tree_to_list(input, retrieve_base = lambda x: x[0]):
    """Returns a list representation of a Grasshopper DataTree"""
    def extend_at(path, index, simple_input, rest_list):
        target = path[index]
        if len(rest_list) <= target: rest_list.extend([None]*(target-len(rest_list)+1))
        if index == path.Length - 1:
            rest_list[target] = list(simple_input)
        else:
            if rest_list[target] is None: rest_list[target] = []
            extend_at(path, index+1, simple_input, rest_list[target])
    all = []
    for i in range(input.BranchCount):
        path = input.Path(i)
        extend_at(path, 0, input.Branch(path), all)
    return retrieve_base(all)

# function written by Giulio Piacentino, giulio@mcneel.com
def list_to_tree(input, none_and_holes=True, source=[0]):
    """Transforms nestings of lists or tuples to a Grasshopper DataTree"""
    from Grasshopper import DataTree as Tree
    from Grasshopper.Kernel.Data import GH_Path as Path
    from System import Array
    def proc(input,tree,track):
        path = Path(Array[int](track))
        if len(input) == 0 and none_and_holes: tree.EnsurePath(path); return
        for i,item in enumerate(input):
            if hasattr(item, '__iter__'): #if list or tuple
                track.append(i); proc(item,tree,track); track.pop()
            else:
                if none_and_holes: tree.Insert(item,path,i)
                elif item is not None: tree.Add(item,path)
    if input is not None: t=Tree[object]();proc(input,t,source[:]);return t

LayerName=Rhino.RhinoDoc.ActiveDoc.Layers

output_Brep=(Rhino.RhinoDoc.ActiveDoc.Objects.GetObjectList(ObjectType.Brep))
output_Curve=(Rhino.RhinoDoc.ActiveDoc.Objects.GetObjectList(ObjectType.Curve))
output=(Rhino.RhinoDoc.ActiveDoc.Objects)

output_Brep_=[]
for i in output_Brep:
    output_Brep_.append(i)

output_Curve_=[]
for i in output_Curve:
    output_Curve_.append(i)

count=0

BrepElements=[]

for l in range (len(Rhino.RhinoDoc.ActiveDoc.Layers)):
    count=0
    print("l: "+str(l))
    elementByLayerBrep=[]
    for i in output_Brep_:
         print(count)
         if str(i.Attributes.LayerIndex)==str(l):
            elementByLayerBrep.append(i.Geometry)
         count+=1
    BrepElements.append(elementByLayerBrep)
Brep=list_to_tree(BrepElements)

CurveElements=[]
for l in range (len(Rhino.RhinoDoc.ActiveDoc.Layers)):
    elementByLayerCurve=[]
    for i in output_Curve_:
        if str(i.Attributes.LayerIndex)==str(l):
            elementByLayerCurve.append(i.Geometry)
    CurveElements.append(elementByLayerCurve)
Curve=list_to_tree(CurveElements)

ProjectName=Rhino.RhinoDoc.ActiveDoc.Name[:-4]
