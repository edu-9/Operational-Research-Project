#Trabalho Realizado pelo grupo composto por Eduardo Dias, Tomás Santos,
#Mariana Lopes, Maria Cardoso e Mariana Rodrigues
#1/2/3 b)
import gurobipy as gp
from gurobipy import GRB

import random
import math

import networkx as nx
import matplotlib.pyplot as plt


def getData(num_aluno,n,m,p):
    
    ''' 
    Recebe:
    n - número de potenciais localizações para veículos
    m - número de localizações onde podem ocorrer ignições
    p - número de veículos
            
    Retorna:
    coord - coordenadas de cada localização, indíces <n de veículos, índices >=n e <m ignições
    d - distancia entre cada par de potenciais localizações para veículos e ignições 
    r - risco de cada local

            
    '''
    assert n>0
    assert m>0
    assert p>0
    
    random.seed(num_aluno)
         
    ####################################
    #random.seed(num_aluno)
    ####################################
    
    ####################################
    # Coordenadas 
    ####################################
    '''
    Os primeiros n locais (índices de 0 a n-1) dizem respeito a veículos.
    Os úlitmos m locais (índices de n a n+m-1) dizem respeito a ignições.
    '''
    coord={}
    for k in range(n+m):
        coord[k]=(random.random(),random.random())


    ####################################
    # distâncias entre todos os pares
    ####################################
    d = {}
    for i in range(n):
        for j in range(m):
            d[(i,n+j)] = math.sqrt((coord[i][0]-coord[n+j][0])**2 + (coord[i][1]-coord[n+j][1])**2)

    ####################################
    # risco (questão 3)
    ####################################
    
    r=[random.randrange(5)+1 for i in range (m)]
        
    return coord, d, r
           

    ####################################
    #
    # Visualização da Solução
    #
    ####################################
    
def visualizeSolution(aSelectedLocations, aNonSelectedLocations, aCoveredPoints, 
                      aNonCoveredPoints, aAssignment, aPos):
    '''
    aSelectedLocations - índices das instalações seleccionadas
    aNonSelectedLocations - índices das instalações não seleccionadas
    aCoveredPoints - índices dos pontos seleccionados
    aNonCoveredPoints - índices dos pontos não seleccionados
    aAssignment - lista dos pares (i,j) em que i é uma localização seleccionada e j um ponto por ela coberto.
    aPos  - coordenadas dos locais como retornadas pela função getData()
    '''
    
    plt.figure()
    G = nx.Graph()
    G.add_nodes_from(aSelectedLocations)
    G.add_nodes_from(aNonSelectedLocations)
    for (i,j) in aAssignment: G.add_edge(i,j)
    
       
    nx.draw_networkx_nodes(G, aPos, node_color='green', nodelist=aSelectedLocations, node_size=100)
    nx.draw_networkx_nodes(G, aPos, node_color='grey', nodelist=aNonSelectedLocations, node_size=50)
    nx.draw_networkx_nodes(G, aPos, node_color='blue', nodelist=aCoveredPoints, node_size=10)
    nx.draw_networkx_nodes(G, aPos, node_color='red', nodelist=aNonCoveredPoints, node_size=50)
    nx.draw_networkx_edges(G, aPos, edgelist=aAssignment)

   
    plt.title("Localização", size=10)
    plt.axis("off")
    plt.savefig("figure.jpg", dpi=300)
    plt.show()


    ####################################
    #
    # Main
    #
    ####################################

#1 c)
try:

    num_aluno=97169
    
    n=10 # número de potenciais localizações para veículos
    m=30 # número de localizações onde podem ocorrer ignições
    p=4 # número de veiculos
    
    # coord - coordenadas de cada local 
    # d - distancia entre cada par de potenciais localizações para veículos e ignições 
    # r - risco de cada local
    
    coord, d, r = getData(num_aluno, n,m,p)
    
    model=gp.Model('trabIO')
         
    # model.addVars
    y = model.addVars(n, vtype=GRB.BINARY, name='y')
    x = model.addVars(n, m, vtype = GRB.BINARY, name='x')   
    # model.setObjective
    model.setObjective(sum(d[i,n+j]*x[i,j] for i in range(n) for j in range(m)), GRB.MINIMIZE)
    # model.addConstrs
    model.addConstr(((sum(y[i] for i in range(n))) == p))
    model.addConstrs((sum(x[i,j] for i in range(n))==1) for j in range(m))
    model.addConstrs((x[i,j] <= y[i]) for i in range(n) for j in range (m))
    
    model.setParam('TimeLimit', 10) # in seconds
    model.setParam('MIPGap', 1e-4) # default 1e-4 
      
    model.update()
    
    model.write("modelo.lp")
    
    model.optimize()
    
    print(model.Status) #2-optimal
    
    aSelectedLocations = [i for i in y if y[i].x == 1]
    aNonSelectedLocations = [i for i in y if i not in aSelectedLocations]
    aCoveredPoints = [j+n for j in range(m) if sum(x[i,j].x for i in range(n)) == 1]
    aNonCoveredPoints = [j+n for j in range(m) if j+n not in aCoveredPoints]
    aAssignment = [(i,j+n) for (i,j) in x if x[i,j].x == 1]   
    aPos = coord               
    visualizeSolution(aSelectedLocations, aNonSelectedLocations, aCoveredPoints, aNonCoveredPoints, aAssignment, aPos)
        
    print("Optimal value=", model.ObjVal)
    print("Selected facilities:", aSelectedLocations)
    print("Assigment:", aAssignment)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
    


#1 d) 
try:

    num_aluno=97169
    
    n=100 # número de potenciais localizações para veículos
    m=2000 # número de localizações onde podem ocorrer ignições
    p=40 # número de veiculos
    
    # coord - coordenadas de cada local 
    # d - distancia entre cada par de potenciais localizações para veículos e ignições 
    # r - risco de cada local
    
    coord, d, r = getData(num_aluno, n,m,p)
    
    model=gp.Model('trabIO')
         
    # model.addVars
    y = model.addVars(n, vtype=GRB.BINARY, name='y')
    x = model.addVars(n, m, vtype = GRB.BINARY, name='x')   
    # model.setObjective
    model.setObjective(sum(d[i,n+j]*x[i,j] for i in range(n) for j in range(m)), GRB.MINIMIZE)
    # model.addConstrs
    model.addConstrs(((sum(y[i] for i in range(n))) == p) for j in range(m))
    model.addConstrs((sum(x[i,j] for i in range(n))==1) for j in range(m))
    model.addConstrs((x[i,j] <= y[i]) for i in range(n) for j in range (m))
    
    model.setParam('TimeLimit', 30) # in seconds
    model.setParam('MIPGap', 1e-4) # default 1e-4 
      
    model.update()
    
    model.write("modelo.lp")
    
    model.optimize()

    print(model.Status) #2-optimal
    
    aSelectedLocations = [i for i in y if y[i].x == 1]
    aNonSelectedLocations = [i for i in y if i not in aSelectedLocations]
    aCoveredPoints = [j+n for j in range(m) if sum(x[i,j].x for i in range(n)) == 1]
    aNonCoveredPoints = [j+n for j in range(m) if j+n not in aCoveredPoints]
    aAssignment = [(i,j+n) for (i,j) in x if x[i,j].x == 1]   
    aPos = coord               
    visualizeSolution(aSelectedLocations, aNonSelectedLocations, aCoveredPoints, aNonCoveredPoints, aAssignment, aPos)
        
    print("Optimal value=", model.ObjVal)
    print("Selected facilities:", aSelectedLocations)
    print("Assigment:", aAssignment)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
    


#2 c)
try:
    num_aluno=97169
    
    n=10 # número de potenciais localizações para veículos
    m=30 # número de localizações onde podem ocorrer ignições
    p=4 # número de veiculos
    
    # coord - coordenadas de cada local 
    # d - distancia entre cada par de potenciais localizações para veículos e ignições 
    # r - risco de cada local
    
    coord, d, r = getData(num_aluno, n,m,p)
    
    model=gp.Model('trabIO')
         
    # model.addVars
    y = model.addVars(n, vtype=GRB.BINARY, name='y')
    x = model.addVars(n, m, vtype = GRB.BINARY, name='x') 
    z = model.addVar(vtype = GRB.CONTINUOUS, name='z')    
    # model.setObjective
    model.setObjective(z, GRB.MINIMIZE)
    # model.addConstrs
    model.addConstr(((sum(y[i] for i in range(n))) == p))
    model.addConstrs((sum(x[i,j] for i in range(n))==1) for j in range(m))
    model.addConstrs((x[i,j] <= y[i]) for i in range(n) for j in range (m))
    model.addConstrs((z >= d[i,n+j]*x[i,j]) for i in range(n) for j in range(m))
       
    model.setParam('TimeLimit', 10) # in seconds
    model.setParam('MIPGap', 1e-4) # default 1e-4 
      
    model.update()
    
    model.write("modelo.lp")
    
    model.optimize()

    print(model.Status) #2-optimal
    
    aSelectedLocations = [i for i in y if y[i].x == 1]
    aNonSelectedLocations = [i for i in y if i not in aSelectedLocations]
    aCoveredPoints = [j+n for j in range(m) if sum(x[i,j].x for i in range(n)) == 1]
    aNonCoveredPoints = [j+n for j in range(m) if j+n not in aCoveredPoints]
    aAssignment = [(i,j+n) for (i,j) in x if x[i,j].x == 1]   
    aPos = coord               
    visualizeSolution(aSelectedLocations, aNonSelectedLocations, aCoveredPoints, aNonCoveredPoints, aAssignment, aPos)
        
    print("Optimal value=", model.ObjVal)
    print("Selected facilities:", aSelectedLocations)
    print("Assigment:", aAssignment)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
        
#2 d)   
try: 

    num_aluno=97169
    
    n=100 # número de potenciais localizações para veículos
    m=2000 # número de localizações onde podem ocorrer ignições
    p=40 # número de veiculos
    
    # coord - coordenadas de cada local 
    # d - distancia entre cada par de potenciais localizações para veículos e ignições 
    # r - risco de cada local
    
    coord, d, r = getData(num_aluno, n,m,p)
    
    model=gp.Model('trabIO')
         
    # model.addVars
    y = model.addVars(n, vtype=GRB.BINARY, name='y')
    x = model.addVars(n, m, vtype = GRB.BINARY, name='x') 
    z = model.addVar(vtype = GRB.CONTINUOUS, name='z')    
    # model.setObjective
    model.setObjective(z, GRB.MINIMIZE)
    # model.addConstrs
    model.addConstr(((sum(y[i] for i in range(n))) == p))
    model.addConstrs((sum(x[i,j] for i in range(n))==1) for j in range(m))
    model.addConstrs((x[i,j] <= y[i]) for i in range(n) for j in range (m))
    model.addConstrs((z >= d[i,n+j]*x[i,j]) for i in range(n) for j in range(m))
    
    model.setParam('TimeLimit', 10000) # in seconds
    model.setParam('MIPGap', 1e-4) # default 1e-4 
      
    model.update()
    
    model.write("modelo.lp")
    
    model.optimize()

    print(model.Status) #2-optimal
    
    aSelectedLocations = [i for i in y if y[i].x == 1]
    aNonSelectedLocations = [i for i in y if i not in aSelectedLocations]
    aCoveredPoints = [j+n for j in range(m) if sum(x[i,j].x for i in range(n)) == 1]
    aNonCoveredPoints = [j+n for j in range(m) if j+n not in aCoveredPoints]
    aAssignment = [(i,j+n) for (i,j) in x if x[i,j].x == 1]   
    aPos = coord               
    visualizeSolution(aSelectedLocations, aNonSelectedLocations, aCoveredPoints, aNonCoveredPoints, aAssignment, aPos)
        
    print("Optimal value=", model.ObjVal)
    print("Selected facilities:", aSelectedLocations)
    print("Assigment:", aAssignment)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
        
        
    

#3 c)

try:
    num_aluno=97169
    
    n=10 # número de potenciais localizações para veículos
    m=30 # número de localizações onde podem ocorrer ignições
    p=4 # número de veiculos
    
    # coord - coordenadas de cada local 
    # d - distancia entre cada par de potenciais localizações para veículos e ignições 
    # r - risco de cada local
    
    coord, d, r = getData(num_aluno, n,m,p)
    
    model=gp.Model('trabIO')
         
    # model.addVars
    y = model.addVars(n, vtype=GRB.BINARY, name='y')
    x = model.addVars(n, m, vtype = GRB.BINARY, name='x')     
    # model.setObjective
    model.setObjective(sum(x[i,j]*r[j] for i in range(n) for j in range(m)), GRB.MAXIMIZE)
    # model.addConstrs
    model.addConstr(((sum(y[i] for i in range(n))) == p))
    model.addConstrs((sum(x[i,j] for i in range(n))<=1) for j in range(m))
    model.addConstrs((x[i,j] <= y[i]) for i in range(n) for j in range (m))
    model.addConstrs((d[i,n+j]*x[i,j]<=0.3) for i in range(n) for j in range(m))
        
    model.setParam('TimeLimit', 10) # in seconds
    model.setParam('MIPGap', 1e-4) # default 1e-4 
      
    model.update()
    
    model.write("modelo.lp")
    
    model.optimize()
       
    print(model.Status) #2-optimal
    
    aSelectedLocations = [i for i in y if y[i].x == 1]
    aNonSelectedLocations = [i for i in y if i not in aSelectedLocations]
    aCoveredPoints = [j+n for j in range(m) if sum(x[i,j].x for i in range(n)) == 1]
    aNonCoveredPoints = [j+n for j in range(m) if j+n not in aCoveredPoints]
    aAssignment = [(i,j+n) for (i,j) in x if x[i,j].x == 1]   
    aPos = coord               
    visualizeSolution(aSelectedLocations, aNonSelectedLocations, aCoveredPoints, aNonCoveredPoints, aAssignment, aPos)
    
    print("Valor da soma dos indices de risco se todos os locais de potencial ignição se encontrassem cobertos", sum(r))    
    print("Optimal value=", model.ObjVal)
    print("Selected facilities:", aSelectedLocations)
    print("Assigment:", aAssignment)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')    
    
    
#3 d)     
try:

    num_aluno=97169
     
    n=100 # número de potenciais localizações para veículos
    m=2000 # número de localizações onde podem ocorrer ignições
    p=40 # número de veiculos
     
    # coord - coordenadas de cada local 
    # d - distancia entre cada par de potenciais localizações para veículos e ignições 
    # r - risco de cada local
     
    coord, d, r = getData(num_aluno, n,m,p)
     
    model=gp.Model('trabIO')
          
    # model.addVars
    y = model.addVars(n, vtype=GRB.BINARY, name='y')
    x = model.addVars(n, m, vtype = GRB.BINARY, name='x') 
     
    # model.setObjective
    model.setObjective(sum(x[i,j]*r[j] for i in range(n) for j in range(m)), GRB.MAXIMIZE)
    # model.addConstrs
    model.addConstr(((sum(y[i] for i in range(n))) == p))
    model.addConstrs((sum(x[i,j] for i in range(n))<=1) for j in range(m))
    model.addConstrs((x[i,j] <= y[i]) for i in range(n) for j in range (m))
    model.addConstrs((d[i,n+j]*x[i,j]<=0.3) for i in range(n) for j in range(m))
          
    model.setParam('TimeLimit', 20) # in seconds
    model.setParam('MIPGap', 1e-4) # default 1e-4 
       
    model.update()
     
    model.write("modelo.lp")
     
    model.optimize()
     
    print(model.Status) #2-optimal
     
    aSelectedLocations = [i for i in y if y[i].x == 1]
    aNonSelectedLocations = [i for i in y if i not in aSelectedLocations]
    aCoveredPoints = [j+n for j in range(m) if sum(x[i,j].x for i in range(n)) == 1]
    aNonCoveredPoints = [j+n for j in range(m) if j+n not in aCoveredPoints]
    aAssignment = [(i,j+n) for (i,j) in x if x[i,j].x == 1]   
    aPos = coord               
    visualizeSolution(aSelectedLocations, aNonSelectedLocations, aCoveredPoints, aNonCoveredPoints, aAssignment, aPos)
    
    print("Valor da soma dos indices de risco se todos os locais de potencial ignição se encontrassem cobertos", sum(r))     
    print("Optimal value=", model.ObjVal)
    print("Selected facilities:", aSelectedLocations)
    print("Assigment:", aAssignment)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')      
    

#3 e)  
#comparação com a alinea c)
try:

    num_aluno=97169
    
    n=10 # número de potenciais localizações para veículos
    m=30 # número de localizações onde podem ocorrer ignições
    p=4 # número de veiculos
    
    # coord - coordenadas de cada local 
    # d - distancia entre cada par de potenciais localizações para veículos e ignições 
    # r - risco de cada local
    
    coord, d, r = getData(num_aluno, n,m,p)
    
    model=gp.Model('trabIO')
         
    # model.addVars
    y = model.addVars(n, vtype=GRB.BINARY, name='y')
    x = model.addVars(n, m, vtype = GRB.BINARY, name='x') 
    
    # model.setObjective
    model.setObjective(sum(x[i,j]*r[j] for i in range(n) for j in range(m)), GRB.MAXIMIZE)
    # model.addConstrs
    model.addConstr(((sum(y[i] for i in range(n))) == p))
    model.addConstrs((sum(x[i,j] for i in range(n))<=1) for j in range(m))
    model.addConstrs((x[i,j] <= y[i]) for i in range(n) for j in range (m))
    model.addConstrs((d[i,n+j]*x[i,j]<=0.2) for i in range(n) for j in range(m))
        
    model.setParam('TimeLimit', 10) # in seconds
    model.setParam('MIPGap', 1e-4) # default 1e-4 
      
    model.update()
    
    model.write("modelo.lp")
    
    model.optimize()

    print(model.Status) #2-optimal
    
    aSelectedLocations = [i for i in y if y[i].x == 1]
    aNonSelectedLocations = [i for i in y if i not in aSelectedLocations]
    aCoveredPoints = [j+n for j in range(m) if sum(x[i,j].x for i in range(n)) == 1]
    aNonCoveredPoints = [j+n for j in range(m) if j+n not in aCoveredPoints]
    aAssignment = [(i,j+n) for (i,j) in x if x[i,j].x == 1]   
    aPos = coord               
    visualizeSolution(aSelectedLocations, aNonSelectedLocations, aCoveredPoints, aNonCoveredPoints, aAssignment, aPos)
    
    print("Valor da soma dos indices de risco se todos os locais de potencial ignição se encontrassem cobertos", sum(r))    
    print("Optimal value=", model.ObjVal)
    print("Selected facilities:", aSelectedLocations)
    print("Assigment:", aAssignment)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')    
    
try:

    num_aluno=97169
    
    n=10 # número de potenciais localizações para veículos
    m=30 # número de localizações onde podem ocorrer ignições
    p=4 # número de veiculos
    
    # coord - coordenadas de cada local 
    # d - distancia entre cada par de potenciais localizações para veículos e ignições 
    # r - risco de cada local
    
    coord, d, r = getData(num_aluno, n,m,p)
    
    model=gp.Model('trabIO')
         
    # model.addVars
    y = model.addVars(n, vtype=GRB.BINARY, name='y')
    x = model.addVars(n, m, vtype = GRB.BINARY, name='x') 
    
    # model.setObjective
    model.setObjective(sum(x[i,j]*r[j] for i in range(n) for j in range(m)), GRB.MAXIMIZE)
    # model.addConstrs
    model.addConstr(((sum(y[i] for i in range(n))) == p))
    model.addConstrs((sum(x[i,j] for i in range(n))<=1) for j in range(m))
    model.addConstrs((x[i,j] <= y[i]) for i in range(n) for j in range (m))
    model.addConstrs((d[i,n+j]*x[i,j]<=0.4) for i in range(n) for j in range(m))
        
    model.setParam('TimeLimit', 10) # in seconds
    model.setParam('MIPGap', 1e-4) # default 1e-4 
      
    model.update()
    
    model.write("modelo.lp")
    
    model.optimize()
    
    print(model.Status) #2-optimal
    
    aSelectedLocations = [i for i in y if y[i].x == 1]
    aNonSelectedLocations = [i for i in y if i not in aSelectedLocations]
    aCoveredPoints = [j+n for j in range(m) if sum(x[i,j].x for i in range(n)) == 1]
    aNonCoveredPoints = [j+n for j in range(m) if j+n not in aCoveredPoints]
    aAssignment = [(i,j+n) for (i,j) in x if x[i,j].x == 1]   
    aPos = coord               
    visualizeSolution(aSelectedLocations, aNonSelectedLocations, aCoveredPoints, aNonCoveredPoints, aAssignment, aPos)
    
    print("Valor da soma dos indices de risco se todos os locais de potencial ignição se encontrassem cobertos", sum(r))    
    print("Optimal value=", model.ObjVal)
    print("Selected facilities:", aSelectedLocations)
    print("Assigment:", aAssignment)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')    
    

#comparação com a alinea d)      
try:

    num_aluno=97169
      
    n=100 # número de potenciais localizações para veículos
    m=2000 # número de localizações onde podem ocorrer ignições
    p=40 # número de veiculos
      
    # coord - coordenadas de cada local 
    # d - distancia entre cada par de potenciais localizações para veículos e ignições 
    # r - risco de cada local
      
    coord, d, r = getData(num_aluno, n,m,p)
      
    model=gp.Model('trabIO')
           
    # model.addVars
    y = model.addVars(n, vtype=GRB.BINARY, name='y')
    x = model.addVars(n, m, vtype = GRB.BINARY, name='x') 
      
    # model.setObjective
    model.setObjective(sum(x[i,j]*r[j] for i in range(n) for j in range(m)), GRB.MAXIMIZE)
    # model.addConstrs
    model.addConstr(((sum(y[i] for i in range(n))) == p))
    model.addConstrs((sum(x[i,j] for i in range(n))<=1) for j in range(m))
    model.addConstrs((x[i,j] <= y[i]) for i in range(n) for j in range (m))
    model.addConstrs((d[i,n+j]*x[i,j]<=0.2) for i in range(n) for j in range(m))   
      
    model.setParam('TimeLimit', 20) # in seconds
    model.setParam('MIPGap', 1e-4) # default 1e-4 
        
    model.update()
      
    model.write("modelo.lp")
      
    model.optimize()
      
    print(model.Status) #2-optimal
      
    aSelectedLocations = [i for i in y if y[i].x == 1]
    aNonSelectedLocations = [i for i in y if i not in aSelectedLocations]
    aCoveredPoints = [j+n for j in range(m) if sum(x[i,j].x for i in range(n)) == 1]
    aNonCoveredPoints = [j+n for j in range(m) if j+n not in aCoveredPoints]
    aAssignment = [(i,j+n) for (i,j) in x if x[i,j].x == 1]   
    aPos = coord               
    visualizeSolution(aSelectedLocations, aNonSelectedLocations, aCoveredPoints, aNonCoveredPoints, aAssignment, aPos)
    
    print("Valor da soma dos indices de risco se todos os locais de potencial ignição se encontrassem cobertos", sum(r))
    print("Optimal value=", model.ObjVal)
    print("Selected facilities:", aSelectedLocations)
    print("Assigment:", aAssignment)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')      
     

try:

     num_aluno=97169
       
     n=100 # número de potenciais localizações para veículos
     m=2000 # número de localizações onde podem ocorrer ignições
     p=40 # número de veiculos
       
     # coord - coordenadas de cada local 
     # d - distancia entre cada par de potenciais localizações para veículos e ignições 
     # r - risco de cada local
       
     coord, d, r = getData(num_aluno, n,m,p)
       
     model=gp.Model('trabIO')
            
     # model.addVars
     y = model.addVars(n, vtype=GRB.BINARY, name='y')
     x = model.addVars(n, m, vtype = GRB.BINARY, name='x') 
       
     # model.setObjective
     model.setObjective(sum(x[i,j]*r[j] for i in range(n) for j in range(m)), GRB.MAXIMIZE)
     # model.addConstrs
     model.addConstr(((sum(y[i] for i in range(n))) == p))
     model.addConstrs((sum(x[i,j] for i in range(n))<=1) for j in range(m))
     model.addConstrs((x[i,j] <= y[i]) for i in range(n) for j in range (m))
     model.addConstrs((d[i,n+j]*x[i,j]<=0.4) for i in range(n) for j in range(m))
           
     model.setParam('TimeLimit', 20) # in seconds
     model.setParam('MIPGap', 1e-4) # default 1e-4 
         
     model.update()
       
     model.write("modelo.lp")
       
     model.optimize()
       
     print(model.Status) #2-optimal
       
     aSelectedLocations = [i for i in y if y[i].x == 1]
     aNonSelectedLocations = [i for i in y if i not in aSelectedLocations]
     aCoveredPoints = [j+n for j in range(m) if sum(x[i,j].x for i in range(n)) == 1]
     aNonCoveredPoints = [j+n for j in range(m) if j+n not in aCoveredPoints]
     aAssignment = [(i,j+n) for (i,j) in x if x[i,j].x == 1]   
     aPos = coord               
     visualizeSolution(aSelectedLocations, aNonSelectedLocations, aCoveredPoints, aNonCoveredPoints, aAssignment, aPos)
     
     print("Valor da soma dos indices de risco se todos os locais de potencial ignição se encontrassem cobertos", sum(r))
     print("Optimal value=", model.ObjVal)
     print("Selected facilities:", aSelectedLocations)
     print("Assigment:", aAssignment)

except gp.GurobiError as e:
     print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
     print('Encountered an attribute error')      
      

             
    
    
    
  
    