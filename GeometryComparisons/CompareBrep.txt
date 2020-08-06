__author__ = "alexberd"
__version__ = "03"

import rhinoscriptsyntax as rs

def moveToOrigin(input):
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
    return(output)

def dist_from_origin(i):
    return int(100*(i.X**2+i.Y**2+i.Z**2)**0.5)

def sortPoints(input):
    dist=[]
    
    return sorted(input, key=dist_from_origin)
    

def comparePoints(input1, input2):
    similar=True

a = []
tolerance=float(tolerance)

group=[]
group_points=[]
input_group_key=[]

for i in range(input.BranchCount):
    print(i)
    P=moveToOrigin(input.Branch(i))
    P=sortPoints(P)
    
    if len(group_points)==0:
        group_points.append(P)
        print("group "+str(len(group_points)-1)+" is created")
        group.append(str(len(group_points)-1))
    else:
        print(group_points[0])
        Similar=False
        for ii in range(len(group_points)):
            print(str(len(P))+" "+str(len(group_points[ii])))
            if len(P)==len(group_points[ii]):
                Similar=True
                for iii in range(len(group_points[ii])):
                    if(group_points[ii][iii].DistanceTo(P[iii]))>tolerance:
                        Similar=False
                if Similar:
                    print("group"+str(i)+"is named: "+str(ii))
                    group.append(str(ii))
                    break
        else:
            Similar=False
        
        if Similar==False:
            group_points.append(P)
            print("group "+str(len(group_points)-1)+" is created")
            group.append(str(len(group_points)-1))
            
output=group
