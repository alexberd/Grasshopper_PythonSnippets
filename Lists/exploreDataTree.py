#From Rhino Developer Docs
#https://developer.rhino3d.com/guides/rhinopython/grasshopper-datatrees-and-python/

output = []

for i in range(input.BranchCount):
    branchList = input.Branch(i)
    branchPath = input.Path(i)
    
    for j in range(branchList.Count):
        s = str(branchPath) + "[" + str(j) + "] "
        s += type(branchList[j]).__name__ + ": "
        s += str(branchList[j])
        
        output.append(s)
