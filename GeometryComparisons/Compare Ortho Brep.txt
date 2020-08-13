__author__ = "alexberd"
__version__ = "2020.08.13"

import rhinoscriptsyntax as rs

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

def moveToOrigin(listInput):
    listOutput=[]
    for input in listInput:
        x=[]
        y=[]
        z=[]
        
        for i in input:
            x.append(i.X)
            y.append(i.Y)
            z.append(i.Z)
        
        output=[]
        for i in input:
            output.append(rs.CreatePoint(i.X-min(x),i.Y-min(y),i.Z-min(z)))
        listOutput.append(output)
    return(listOutput)

def dist_from_origin(i):
    return int(100*(i.X**2+i.Y**2+i.Z**2)**0.5)

def sortPoints(listInput):
    listOutput=[]
    for input in listInput:
        dist=[]
        listOutput.append(sorted(input, key=dist_from_origin))
    return listOutput
    
def comparePoints(input1, input2):
    similar=True

zeroPoint=rs.CreatePoint(0,0,0)
rotationAxis=rs.CreateVector(0, 0, 1)

import math

def rotate(input):
    result=[]
    for ii in [0,90,180,270]:
        list=[]
        for i in input:
            v=rs.CreateVector(i)
            v.Rotate(math.radians(int(ii)),rotationAxis)
            list.append(v)
        result.append(list)
    return result

import math

def selectRotation(input,rotation):
    result=[]
    return input[rotation]

a = []
tolerance=float(tolerance)

group=[]
group_points=[]
input_group_key=[]

direction=[]

debug=[]

for i in range(input.BranchCount):
    print(i)

    P=rotate(input.Branch(i)) #0,90,180,270
    
    P=moveToOrigin(P)
    P=sortPoints(P)
    debug.append(P)
    if len(group_points)==0:
        print("create group"+str(len(selectRotation(P,0))))
        group_points.append(selectRotation(P,0))
        direction.append(0)
        print("group "+str(len(group_points)-1)+" is created")
        group.append(str(len(group_points)-1))
    else:
        for ii in range(len(group_points)):
            print(len(selectRotation(P,0)))
            print(str(len(selectRotation(P,0)))+" "+str(len(group_points[ii])))
            if len(selectRotation(P,0))==len(group_points[ii]):
                for d in range(4):
                    print("direction: "+str(d))
                    Similar=True
                    for iii in range(len(group_points[ii])):
                        if(group_points[ii][iii].DistanceTo(selectRotation(P,d)[iii]))>tolerance:
                            Similar=False
                    if Similar:
                        break
                if Similar:
                    print("group"+str(i)+"is named: "+str(ii)+" - direction "+str(d))
                    group.append(str(ii))
                    direction.append(d)
                    break
        else:
            Similar=False
        
        if Similar==False:
            group_points.append(selectRotation(P,0))
            print("group "+str(len(group_points)-1)+" is created"+" - direction 0")
            group.append(str(len(group_points)-1))
            direction.append(0)

output=group
debug=list_to_tree(debug)
