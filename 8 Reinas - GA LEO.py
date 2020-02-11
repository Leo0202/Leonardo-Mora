import math
import os
import random


""" -------------------------------------------------
Clase que optimiza un problema por Busqueda Local
------------------------------------------------- """
class Optimizador():

    global nombreArchivo
    global duraciones
    global tamPoblacion
    global poblacion
    global numSujTorneo
    global probaMutar
    global maxGeneraciones
    global numReinas
    global mejor
    global peor
    global mejorFO
    global peorFO
    
    def algoritmoGenetico(self):
        self.inicializarPoblacion()
        self.calcularFOpoblacion()

        terminado = False
        numGeneracion = 0
        self.actualizaMejor()
        self.actualizaPeor()
        print("Mejor it"+str(numGeneracion),self.mejor.toString())
        print("Peor it "+str(numGeneracion),self.peor.toString())
            
        while (not terminado):
            nuevaPoblacion = []
            
            for k in range(0,int(self.tamPoblacion/2)):
                padre = self.seleccionarPadre()
                madre = self.seleccionarPadre()

                hijo1, hijo2 = self.reproducirPadres(padre,madre)
                
                probaMutaH1 = random.random()
                if(probaMutaH1<self.probaMutar):
                    hijo1=self.mutar(hijo1)

                probaMutaH2 = random.random()
                if(probaMutaH2<self.probaMutar):
                    hijo2=self.mutar(hijo2)
                
                self.calcularFOindi(hijo1)
                self.calcularFOindi(hijo2)


                sobr1, sobr2 = self.seleccionaSobrevivientes(padre, madre, hijo1, hijo2)

                nuevaPoblacion.append(sobr1)
                nuevaPoblacion.append(sobr2)

            self.poblacion = nuevaPoblacion
            numGeneracion = numGeneracion +1
            
            self.actualizaMejor()
            self.actualizaPeor()
            
            print("Mejor it"+str(numGeneracion),self.mejor)
            print("Peor it "+str(numGeneracion),self.peor)
                
            if(numGeneracion==self.maxGeneraciones):
                terminado = True

            


    def seleccionarPadre(self):
        #Saca numSujTorneo individuos aleatorios de la poblacion
        indiTorneo = []
        for i in range(0,self.numSujTorneo):
            idIndiAleatorio = random.randint(0,self.tamPoblacion-1)
            indiTorneo.append(self.poblacion[idIndiAleatorio])

        #Encuentra cuál es el mejor de los individuos en el torneo
        mejorIndi = None
        mejorFO = None

        for temp in indiTorneo:
            tempFO = temp.FO
            if(mejorFO == None or tempFO < mejorFO):
                mejorFO = tempFO
                mejorIndi = temp

        return mejorIndi


    def reproducirPadres(self,mama,papa):
        
        aleat = random.randint(0,self.numReinas)
        genoMama = mama.genotipo
        genoPapa = papa.genotipo
       

        
        genoHijo1 = [None for j in range(self.numReinas)]

        genoHijo2 = [None for j in range(self.numReinas)]

        for i in range(0, aleat):
            genoHijo1[i] = genoMama[i]
            genoHijo2[i] = genoPapa[i]


        for i in range(aleat, self.numReinas):
            genoHijo1[i] = genoMama[i]
            genoHijo2[i] = genoPapa[i]


        
        hijo1 = Individuo(genoHijo1)
        hijo2 = Individuo(genoHijo2)
        
        #------------------------------------------------------
        # modifique el metodo reproducirPadres()
        # Especificaciones:
        #   Debe crear 2 hijos (hijo1, hijo2) con una parte de los genes del papa y una parte de los genes de la mama
        # Recomendaciones:
        #   Cree un numero aleatorio entero (aleat) que indique hasta que posicion toma los genes del papa. El numero aleatorio puede tomar valores desde 0 hasta self.numReinas
        #   Cree un nuevo vector vacio, que sera el genotipo del Hijo1 (genoHijo1)
        #   Agregue al vector (genoHijo1) los genes del papa hasta la posicion (aleat)
        #   Agregue al vector (genoHijo1) los genes de la mama desde la posicion (aleat) hasta el final
        #   Cree en la variable (hijo1) un nuevo Individuo con el vector (genoHijo1) como genotipo
        #
        #   Repita el procedimiento para el (hijo2) cambiando los roles del papa y la mama
        #------------------------------------------------------


        return hijo1,hijo2


    def mutar(self,individuo):
        aleat = random.randint(0,self.numReinas-1)

        nuevoValor = random.randint(0,self.numReinas-1)


        vectorTemp = individuo.genotipo
        vectorTemp[aleat] = nuevoValor
        individuo.genotipo = vectorTemp
        
        return individuo
        #------------------------------------------------------
        # modifique el metodo mutar()
        # Especificaciones:
        #   Debe mutar el genotipo del individuo y guardarlo de nuevo en (individuo.genotipo)
        # Recomendaciones:
        #   Cree un numero aleatorio entero (aleat) que indique el gen a mutar. El numero aleatorio puede tomar valores enteros desde 0 hasta self.numReinas
        #   Cree un numero aleatorio entero (nuevoValor) que indique el nuevo valor del gen a mutar. El numero aleatorio puede tomar valores enteros desde 0 hasta self.numReinas
        #   Guarde en un nuevo vector (vectorTemp) el genotipo del individuo (individuo.genotipo)
        #   Modifique la posicion (aleat) del vector (vectorTemp) y asigne el valor generado (nuevoVal)
        #   Asigne a (individuo.genotipo) el nuevo vector (vectorTemp)
        #
        #------------------------------------------------------

    def seleccionaSobrevivientes(self,mama,papa,hijo1,hijo2):        

        lista= [mama,papa,hijo1,hijo2]
        listaFOs = [mama.FO,papa.FO,hijo1.FO,hijo2.FO]

        
        listaFOs.sort()

       
        mejor = None
        for indi in lista:
            if(indi.FO == listaFOs[0]):
                mejor = indi

      
        segundo=None
        for indi in lista:
            if(indi.FO == listaFOs[1]):
                segundo = indi

        return mejor, segundo
        

    def inicializarPoblacion(self):
        self.poblacion = []

        for i in range(0,self.tamPoblacion):
            ind = Individuo(self.darInividuoAleatorio())

            self.poblacion.append(ind)
        
    def darInividuoAleatorio(self):
        #------------------------------------------------------
        # modifique el metodo darInividuoAleatorio()
        # Especificaciones:
        #   Debe generar un Individuo con Genotipo aleatorio.
        # Recomendaciones:
        #   Cree un nuevo vector (genoTemp) vacio
        #   En un ciclo que itere desde 0 hasta self.numReinas realice: 
        #      Cree un numero aleatorio entero (aleat) que indique la posicion donde se ubicara la reina. El numero aleatorio puede tomar valores enteros desde 0 hasta (self.numReinas)
        #      Agregue el numero aleatorio (aleat) en el vector (genoTemp)
        #
        #   Terminado el ciclo, cree en la variable (indiv1) un nuevo Individuo, usando el vector (genoTemp) como genotipo
        #------------------------------------------------------

        genoTemp = []
        
        for i in range(self.numReinas):
            aleat = random.randint(0,(self.numReinas-1))    
            genoTemp.append(aleat)
           #indiv1.append(genoTemp)
                

        return genoTemp

    def calcularFOpoblacion(self):
        for indi in self.poblacion:
            self.calcularFOindi(indi)

    def calcularFOindi(self, individuo):
        genotipo = individuo.genotipo

        matriz = [[0 for j in range(self.numReinas)] for i in range(self.numReinas)]    
        
        for i in range(self.numReinas):
            matriz[genotipo[i]][i] = 1
           
        #   Calcule cuantos cruces hay verticalmente (crucesVer) segun el genotipo almacenado en (individuo.genotipo)

        crucesVer = 0
        crucesHor = 0
        
        for i in range(self.numReinas):
            if genotipo.count(i)>1:
                crucesHor += genotipo.count(i)-1 

        #   Calcule cuantos cruces hay en las diagonales crecientes (crucesDiagCrec) segun el genotipo almacenado en (individuo.genotipo)

        crucesDiagCrec = 0 

        for i in range(self.numReinas):
            cruceDiag = 0 
            for j in range(i+1):
                if matriz[i-j][j] == 1:
                    cruceDiag +=1
            if cruceDiag > 1:
                crucesDiagCrec +=cruceDiag-1
            
            cruceDiag = 0 
            for j in range (7-i):
                if matriz[7-j][i+j+1] == 1:
                    cruceDiag +=1
            if cruceDiag > 1:
                crucesDiagCrec +=cruceDiag-1    

        #   Calcule cuantos cruces hay en las diagonales decrecientes (crucesDiagDecr) segun el genotipo almacenado en (individuo.genotipo)
        crucesDiagDecr = 0

        for i in range((self.numReinas-1),0,-1):
            cruceDiag = 0
            for j in range(self.numReinas-i):
                if matriz[i+j][j] == 1:
                    cruceDiag +=1
            if cruceDiag > 1:
                crucesDiagDecr += (cruceDiag-1)
        
        for i in range(self.numReinas):
            cruceDiag = 0
            for j in range(self.numReinas-i):
                if matriz[j][i+j] == 1:
                    cruceDiag +=1
            if cruceDiag > 1:
                crucesDiagDecr +=cruceDiag-1
        
        #   Sume los cruces totales y asigne a (individuo.FO) el total
      
        individuo.FO = crucesVer+crucesHor+crucesDiagCrec+crucesDiagDecr
        
    def actualizaMejor(self):
        self.mejor = None
        self.mejorFO = None
        for indiv in self.poblacion:
            indiFo = indiv.FO
            if(self.mejorFO == None or indiFo < self.mejorFO):
                self.mejorFO = indiFo
                self.mejor = indiv

    def actualizaPeor(self):
        self.peor = None
        self.peorFO = None
        for indiv in self.poblacion:
            indiFo = indiv.FO
            if(self.peorFO == None or indiFo > self.peorFO):
                self.peorFO = indiFo
                self.peor = indiv
        

    
        
    #Método que inicializa el optimizador y ejecuta la optimización
                
    def __init__(self):
        
        self.tamPoblacion = 1000  # con self.poblacion <<  1000 surgen algunos errores
        self.numSujTorneo = 2
        self.probaMutar = 0.8
        self.maxGeneraciones = 100
        self.numReinas = 8
              
        self.mejor = None
        self.mejorFO = None
        self.peor = None
        self.peorFO = None

        #------------------------------------------------------
        # Punto 1: modifique el metodo darInividuoAleatorio()
        # Especificaciones:
        #   Debe generar un Individuo con Genotipo aleatorio.
        # Validacion
        # indiTemp = self.darInividuoAleatorio()
        # print(indiTemp.genotipo) # Debe dar un vector aleatorio de 8 posiciones. Por ejemplo: [5, 2, 3, 3, 5, 5, 0, 7]
        # print(len(indiTemp.genotipo)) # Debe dar como resultado: 8
        # print(len([x for x in indiTemp.genotipo if (x < 0 or x > 7)])) # Cuenta los elementos fuera de rango. Debe dar como resultado: 0
        #------------------------------------------------------

        #------------------------------------------------------
        # Punto 2: modifique el metodo calcularFOindi()
        # Especificaciones:
        #   Debe calcular el numero de cruces de reinas en el genotipo
        # Validacion
        # indiTemp = Individuo([1, 6, 2, 5, 7, 4, 0, 3])
        # self.calcularFOindi(indiTemp)
        # print(indiTemp.FO) # Debe dar como resultado: 0
        #
        # indiTemp = Individuo([3, 1, 7, 2, 4, 0, 5, 3])
        # self.calcularFOindi(indiTemp)
        # print(indiTemp.FO) # Debe dar como resultado: 4
        #------------------------------------------------------
        

        #------------------------------------------------------
        # Punto 3: modifique el metodo reproducirPadres()
        #------------------------------------------------------

        #------------------------------------------------------
        # Punto 4: modifique el metodo mutar()
        #------------------------------------------------------
        
        
        #------------------------------------------------------
        # Punto Final: 
        # Especificaciones:
        #   Quite el comentario de la linea self.algoritmoGenetico()
        #------------------------------------------------------

        self.algoritmoGenetico()

""" -------------------------------------------------
Clase que representa una solucion (Individuo)
------------------------------------------------- """
class Individuo():

    global genotipo
    global FO
    global matrizInicios


    def __init__(self, geno):
        self.genotipo=geno
        self.FO=99999999
        self.matrizInicios = []

    def toString(self):
        linea = ""
        for i in self.matrizInicios:
            linea+=str(i)+"\n"
            
        return "x("+str(int(self.FO))+")="+str(self.genotipo)+"\n"+linea

    def __str__(self):
        linea = ""
        for i in self.matrizInicios:
            linea+=str(i)+"\n"
            
        return "x("+str(int(self.FO))+")="+str(self.genotipo)+"\n"+linea




        
  

opti=Optimizador()


