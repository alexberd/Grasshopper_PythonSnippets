import Rhino
from Rhino import *

s=Rhino.DocObjects.ObjectEnumeratorSettings()
s.HiddenObjects = True       
s.LockedObjects = True

#Define your translation vector
xf = Rhino.Geometry.Transform.Translation(10000,10000,0)    

#get the Active Document
doc = RhinoDoc.ActiveDoc
    
#Select All Elements in Document
allElements=(Rhino.RhinoDoc.ActiveDoc.Objects.GetObjectList(s))

#Iterate elements
for input in allElements:
    
    #Apply the transform
    doc.Objects.Transform(input, xf, True);
    
    #Redraw Active Document
    doc.Views.Redraw();
