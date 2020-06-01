#Original code transcript from Alasdair Turner
#https://www.openprocessing.org/sketch/3101#
#Code developed and tested in Grasshopper Python Script by Alex Berd

import rhinoscriptsyntax as rs
import scriptcontext as sc
import random


if (Reset):
    class Genotype:
      def __init__(self):
        # these genes use floating point numbers rather than
        # binary strings
        self.NumberOfGenes=len(sc.sticky["inputs"])
        self.m_genes = [];
        for g in range(self.NumberOfGenes):
            self.m_genes.append(0)
    
      def createGenes(self):
        self.m_genes = [];
        for i in range(self.NumberOfGenes):
            min=sc.sticky["inputs"][i][0]
            max=sc.sticky["inputs"][i][1]
            gene=random.uniform(min,max)
            gene=round(gene, sc.sticky["inputs"][i][2])
            self.m_genes.append(gene)
        print("genes: "+str(self.m_genes))
      
      def mutate(self):
        # 5% mutation rate
        for i in range(self.NumberOfGenes):
          #FULL-DOMAIN
          if (random.uniform(0,1) < 0.05):
            min=sc.sticky["inputs"][i][0]
            max=sc.sticky["inputs"][i][1]
            gene = random.uniform(min,max)
            gene = round(gene, sc.sticky["inputs"][i][2])
            self.m_genes[i] = gene
          #MICRO-DOMAIN
          elif (random.uniform(0,1) < 0.05):
            min=sc.sticky["inputs"][i][0]
            max=sc.sticky["inputs"][i][1]
            percentage=(max-min)/100
            gene = self.m_genes[i]+random.uniform(-percentage,percentage)
            gene = round(gene, sc.sticky["inputs"][i][2])
            self.m_genes[i] = gene
    
    def crossover(a, b): #Import Genotypes
      # uniform crossover switches at any location
      # between genes in the genotype
      c = Genotype();
      for i in range(len(c.m_genes)):
        if (random.uniform(0,1) < 0.5):
          c.m_genes[i] = a.m_genes[i]
        
        else:
          c.m_genes[i] = b.m_genes[i]
      return c
    
    # Phenotype -- the external expression of the genotype can be evaluated
    
    width = 10
    height=10
    
    class Phenotype:
      
      def __init__(self,g):
          donothing=0
      
      def evaluate(self):
        self.fitness = 0.0;
        self.fitness += (self.m_width + self.m_height + self.m_depth)**2
        self.fitness -= self.m_width * self.m_height * self.m_depth
        return self.fitness
    
    # An individual has both a genotype and a phenotype
    
    class Individual:
      
      def __init__(self):
      
        self.m_genotype = Genotype()
        self.m_genotype.createGenes()
        self.m_fitness = 0.0
        self.evaluated = False
      
      def m_fitness():
        return self.m_fitness
    
      def evaluate(self):
        self.m_fitness = self.m_phenotype.evaluate()
    
    def breed_(a, b):
      c = Individual()
      c.m_genotype = crossover(a.m_genotype,b.m_genotype)
      c.m_genotype.mutate()
      return c
    
    def compareGenes(a,b):
        result = True
        for g in range(len(a)):
            if a[g]!=b[g]:
                result=False
        return result
    
    class PopulationClass:
    
      def __init__(self,p):
        self.NumberOfIndividuals=p
        self.m_pop = []
        print("self.NumberOfIndividuals: "+str(self.NumberOfIndividuals))
        
        for i in range(self.NumberOfIndividuals):
          self.m_pop.append(Individual())
        self.m_pop.sort(key = lambda x: x.m_fitness)
        donothing=0
        
      def select(self):
        import math
        # Selection requires some form of bias to fitter individuals,
        which = int(math.floor((self.NumberOfIndividuals - 1e-6) * (1.0 - (random.uniform(0,1))**2)))
        print("individual no: "+ str(which) +" selected")
        return self.m_pop[which]
    
      def breed(self):
        print("breed starts")
        a = self.select()
        b = self.select()
        x=a
        count=0
        while self.individualExist(x) and count<200: # try 200 times for creating a new breed which is different from existing individual - This is currently limited for debuggin purposed just in case it throw an exception
            count+=1
            x = breed_(a,b)
            print("count :"+str(count))
        if (self.individualExist(x) and count>1):
            for p in self.m_pop:
                print(p.m_genotype.m_genes)
            print("------")
            print(x.m_genotype.m_genes)
            print("asdf"+3)
        self.m_pop[0] = x
        return x
    
      def sort(self):
        self.m_pop.sort(key = lambda x: x.m_fitness)
    
      def evolve_old(self):
        a = self.select()
        b = self.select()
        x = breed(a,b)
        self.m_pop[0] = x
        self.m_pop.sort(key = lambda x: x.m_fitness)
    
      def individualExist(self, i):
        result=False
        for p in self.m_pop:
            if compareGenes(p.m_genotype.m_genes,i.m_genotype.m_genes):
                result=True
                break
        return result
        
      def shrinkPopulation(self, i):
          self.NumberOfIndividuals=i
          del self.m_pop[:len(self.m_pop)-i]
    
    def checkGenes():
        Component = ghenv.Component
        GhDef = None
        if Component:
            GhDef = Component.OnPingDocument()
        objects=[]
        for o in range(len(GhDef.Objects)):
            if GhDef.Objects[o].NickName=="input":
                print(GhDef.Objects[o].NickName)
                object=(GhDef.Objects[o])
                objects.append(object)
        print(objects)
        sc.sticky["inputs"]=[] # Array of Input Minimum, Maximum and DecimalPlaces
        for object in objects:
            sc.sticky["inputs"].append([object.Slider.Minimum,object.Slider.Maximum,object.Slider.DecimalPlaces])
    
    #STICKY PARAMETERS
    sc.sticky["GenotypeClass"] = Genotype
    sc.sticky["PhenotypeClass"] = Phenotype
    sc.sticky["IndividualClass"] = Individual
    #sc.sticky["PopulationClass"] = PopulationClass
    sc.sticky["PopulationNum"] = int(Population)*int(InitialBoost)
    
    sc.sticky["Iteration"]=0
    sc.sticky["Iteration"]=-1

    sc.sticky["resetRelease"]=False
    print("1")
    checkGenes()
    pop = PopulationClass(sc.sticky["PopulationNum"])
    sc.sticky["Population"]=pop
    
elif sc.sticky["resetRelease"]==False:
    print("2")
    sc.sticky["resetRelease"]=True
    ghenv.Component.Params.Input[0].Sources[0].ExpireSolution(True) #Just not to stack when pressing the reset button
else:
    print("3")
    
    import scriptcontext as sc

    pop = sc.sticky["Population"]
    i=0
    
    objects=[]
    
    if Run==True:
        
        Component = ghenv.Component
        GhDef = None
        if Component:
            GhDef = Component.OnPingDocument()
        for o in range(len(GhDef.Objects)):
            if GhDef.Objects[o].NickName=="input":
                objects.append(GhDef.Objects[o])
        print(objects)
        
        
        
        print(str(sc.sticky["Iteration"])+" ? "+str(sc.sticky["PopulationNum"]-1))
        
        if int(sc.sticky["Iteration"])==int(sc.sticky["PopulationNum"]-1):#Runs only the last individual_storing evaluation and start breeding
            #Store previous Phenotype
            print("STORE FITNESS")
            #print((sc.sticky["Population"].m_pop)[int(sc.sticky["Iteration"])].m_fitness)
            (sc.sticky["Population"].m_pop)[int(sc.sticky["Iteration"])].m_fitness=Fitness
            (sc.sticky["Population"].m_pop)[int(sc.sticky["Iteration"])].evaluated=True
            
            sc.sticky["Iteration"]=int(sc.sticky["Iteration"])+1
            
            #SHRINK POPULATION
            sc.sticky["PopulationNum"] = int(Population)
            sc.sticky["Population"].shrinkPopulation(sc.sticky["PopulationNum"])
            
            
            print("CREATE FIRST BREED")
            #print(sc.sticky["Population"])
            
            breed=sc.sticky["Population"].m_pop[0]
            count=0
            breed=sc.sticky["Population"].breed()
            for g in range (len(sc.sticky["inputs"])):
                nextGene=breed.m_genotype.m_genes[g]
                print(nextGene)
                objects[g].Slider.Value = float(nextGene)
                objects[g].ExpireSolution(True)
            
            
        
        elif int(sc.sticky["Iteration"])>int(sc.sticky["PopulationNum"]-1): #Storing new breed and create more breeding
            
            print("STORE BREED FITNESS")
            #print((sc.sticky["Population"].m_pop)[0].m_fitness)
            #print("Genotype: "+(rs.sticky["Population"].m_pop)[int(rs.sticky["Iteration"])].m_fitness)
            (sc.sticky["Population"].m_pop)[0].m_fitness=Fitness
            (sc.sticky["Population"].m_pop)[0].evaluated=True
            
            sc.sticky["Iteration"]=int(sc.sticky["Iteration"])+1
            
            print("SORT the POPULATION")
            sc.sticky["Population"].sort()
            
            print("CREATE MORE BREEDS")
            breed=sc.sticky["Population"].breed()
            for g in range(len(sc.sticky["inputs"])):
                nextGene=breed.m_genotype.m_genes[g]
                print(nextGene)
                objects[g].Slider.Value = float(nextGene)
                objects[g].ExpireSolution(True)
            
        else: #Evaluating and storing entire Population (apart from storing the last individual evaluation)
            
            print("STORE FITNESS")
            if sc.sticky["Iteration"]!=-1:
                (sc.sticky["Population"].m_pop)[int(sc.sticky["Iteration"])].m_fitness=Fitness
                (sc.sticky["Population"].m_pop)[int(sc.sticky["Iteration"])].evaluated=True
                
            sc.sticky["Iteration"]=int(sc.sticky["Iteration"])+1
            for g in range(len(sc.sticky["inputs"])):
                
                nextGene=(sc.sticky["Population"].m_pop)[int(sc.sticky["Iteration"])].m_genotype.m_genes[g]
                print(nextGene)
                
                objects[g].Slider.Value = float(nextGene)
                objects[g].ExpireSolution(True)
            
output=("Population: "+str(sc.sticky["PopulationNum"])+" \nIteration: "+str(sc.sticky["Iteration"])+" \nFitness: "+str(Fitness))
pop=sc.sticky["Population"].m_pop
population=[]
for p in range(len(pop)):
    genotypes=""
    for g in range(len(sc.sticky["inputs"])):
        if g==0:
            genotypes=" ("+str(pop[p].m_genotype.m_genes[g])
        else:
            genotypes=genotypes+","+str(pop[p].m_genotype.m_genes[g])
    genotypes=genotypes+")"
    if pop[p].evaluated:
        population.append(str(pop[p].m_fitness)+genotypes)
    else:
        population.append("---"+genotypes)
