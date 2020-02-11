import math
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

""" -------------------------------------------------
Clase que optimiza un problema por Busqueda Local
------------------------------------------------- """
class Optimizador():

    #Clase que tiene las Funciones Objetivo
    global funcionesObj
    global grafi
    

    def busquedaLocal(self):
        
        solucionActual = self.darSolInicial()

        solActFO = self.calcularFO(solucionActual)

        terminar = False
        i=0
        self.grafi.graficarIteracion3D(solucionActual, solActFO)
        
        while (not terminar):
            vecinos = self.calcVecinos(solucionActual)

            encontroMejorVecino = False

            for veci in vecinos:
                foVeci = self.calcularFO(veci)
                if(foVeci<=solActFO):
                    solucionActual = veci
                    solActFO = foVeci
                    encontroMejorVecino = True
            
            if(encontroMejorVecino):
                self.grafi.graficarIteracion3D(solucionActual, solActFO)
            else:
                terminar = True
            

        self.grafi.graficarPuntoOptimo(solucionActual, solActFO)

    def simulatedAnnealing(self):
        
        act = self.darSolInicial()
        solActFO = self.calcularFO(act)

        T = 100
        tope = 10
        t=0

        
        self.grafi.graficarIteracion3D(act, solActFO)
        
        while (T>0.1):
            est = act
            foEst = self.calcularFO(est)
            it = 0

            while it<tope:

                sig=self.calcSucesorAleatorio(est)
                foSig = self.calcularFO(sig)
                deltaE = foSig - foEst
                if deltaE<0 :
                    est = sig
                    foEst = foSig
                    self.grafi.graficarIteracion3D(est, foEst)
                else:
                    q=min(1,math.exp(-deltaE/T))
                    if(random.random() < q):
                        est = sig
                        foEst = foSig
                        self.grafi.graficarIteracion3D(est, foEst)
                        print("Toma malo")
                it=it+1

            
            act = est
            solActFO = foEst
            T = 0.6*T
            print("Temp",T)
            

        self.grafi.graficarPuntoOptimo(act, solActFO)


    def darSolInicial(self):

        x = random.random()*10 - 5
        y = random.random()*10 - 5

        act = Individuo2D(x,y)
        return act

    def calcSucesorAleatorio(self, indiv):
        return indiv.darVecinoAleatorio()


    def calcVecinos(self, indiv):
        listaVecinos = indiv.darVecindario()
        for i in range(0,5):
            vecinoC = indiv.darVecinoAleatorio()
            listaVecinos.append(vecinoC)

        return listaVecinos


    def calcularFO(self, indiv):
        x = indiv.valX
        y = indiv.valY
        z=self.funcionesObj.funcion2Variables(x,y)
        
        return z
        
    #Método que inicializa el optimizador y ejecuta la optimización
    def __init__(self):

        #Inicializa la clase que contiene las funciones objetivo
        self.funcionesObj = FuncionesObjetivo()

        #Inicializa la clase que grafica funciones univariadas
        self.grafi = GraficadorUnivariado(self.funcionesObj)

        self.simulatedAnnealing()

""" -------------------------------------------------
Clase que representa una solucion (Individuo)
------------------------------------------------- """
class Individuo2D():

    global valX  
    global valY  
    global FO  

    def darVecinoAleatorio(self):

        xNuevo = self.valX + random.random()*2-1
        yNuevo = self.valY + random.random()*2-1
        vecino=Individuo2D(xNuevo,yNuevo)

        return vecino

    def darVecindario(self):
        lista=[]
        lista.append(Individuo2D(self.valX+0.25,self.valY+0.25))
        lista.append(Individuo2D(self.valX+0.25,self.valY))
        lista.append(Individuo2D(self.valX+0.25,self.valY-0.25))
        lista.append(Individuo2D(self.valX,self.valY+0.25))
        lista.append(Individuo2D(self.valX,self.valY-0.25))
        lista.append(Individuo2D(self.valX-0.25,self.valY+0.25))
        lista.append(Individuo2D(self.valX-0.25,self.valY))
        lista.append(Individuo2D(self.valX-0.25,self.valY-0.25))

        return lista

    def __init__(self, x, y):
        self.valX=x
        self.valY=y

    def __str__(self):
        return "x="+str(self.valX)+", y="+str(self.valY)

""" -------------------------------------------------
Clase que contiene Múltiples Funciones Univariadas
------------------------------------------------- """
class FuncionesObjetivo():

    #Variables que definen los rangos de la variable de decisión
    global rangoFOUnivariable1
    global rangoFOUnivariable2
    
    rangoFOUnivariable1 = [-10,10]    
    rangoFOUnivariable2 = [-10,10]
    
    #Función que calcula la primera función univariada
    def funcionUnivariable1(self, x):
        y=math.sin((x/3)**2)-((x-2)/10)**2
        return y

    #Función que calcula la segunda función Univariada
    def funcionUnivariable2(self, x):
        y=-(x-2)**2
        return y

    #Funcion que calcula la funcion de dos variables
    def funcion2Variables(self, x, y):
        z = (x**2) + (y**2) + 25*((np.sin(x))**2+(np.sin(y))**2)
        return z

    def darRangoFOUni1(self):
        return rangoFOUnivariable1

    

""" -------------------------------------------------
Clase que realiza gráficas de una función univariada
------------------------------------------------- """
class GraficadorUnivariado():

    ax = None
    list_x=np.array([])
    list_y=np.array([])
    list_z=np.array([])

    #Función que grafica la primera función Univariada
    def graficarFuncionUnivariable1(self, fo):
        

        vectorX=[]
        vectorY=[]
        intervalos=100
        num1 = fo.darRangoFOUni1()[1]
        num2 = fo.darRangoFOUni1()[0]
        
        tamInterv = (num1-num2)/intervalos
        
        for i in range(0,intervalos+1):
            x=num2+tamInterv*i
            y=fo.funcionUnivariable1(x)
            vectorX.append(x)
            vectorY.append(y)

        plt.axis([-10,10,-2.5,1.5])
        plt.ion()
        plt.show()
        plt.plot(vectorX, vectorY)
        plt.draw()
        plt.pause(0.001)

    #Función que grafica la segunda función Univariada
    def graficarFuncionUnivariable2(self, fo):

        vectorX=[]
        vectorY=[]
        intervalos=100

        num1 = fo.darRangoFOUni1()[1]
        num2 = fo.darRangoFOUni1()[0]
        
        tamInterv = (num1-num2)/intervalos
        
        for i in range(0,intervalos+1):
            x=num2+tamInterv*i
            y=fo.funcionUnivariable2(x)
            vectorX.append(x)
            vectorY.append(y)

        
        plt.axis([-10,10,-150,10])
        plt.ion()
        plt.show()
        plt.plot(vectorX, vectorY)
        plt.draw()
        plt.pause(0.001)

    def f(self, x, y):
        return np.sin(np.sqrt(x ** 2 + y ** 2))
    
    #Función que grafica una iteracion (dibuja un vector verde en la solucion actual)
    def graficarIteracion3D(self,indiv,fo):

        theta = 2 * np.pi * np.random.random(1000)
        r = 6 * np.random.random(1000)
        self.list_x= np.append(self.list_x,[indiv.valX])
        self.list_y= np.append(self.list_y,[indiv.valY])
        
        self.list_z=((self.list_x**2) + (self.list_y**2) + 25*((np.sin(self.list_x))**2+(np.sin(self.list_y))**2))+5

        self.ax.plot(self.list_x,self.list_y,self.list_z,color="b")

        #self.ax.scatter(self.list_x, self.list_y, self.list_z, color="r", linewidth=2);
        #self.ax.contour3D(self.list_x, self.list_y, self.list_z, 50, cmap='binary')

        plt.draw()
        plt.pause(0.001)
        zMod=(self.list_x**1)*0
        self.ax.plot(self.list_x,self.list_y,zMod,color="g")

        self.ax.scatter([indiv.valX], [indiv.valY], [0], color="g", linewidth=2);
        self.ax.scatter([indiv.valX], [indiv.valY], [fo], color="b", linewidth=2);


    def graficarVecinos(self,listaXY):
        lista =[]
        for coord in listaXY:
            x=coord[0]
            y=coord[1]
            p1, = plt.plot(x,y,"xb")
            lista.append(p1)
            plt.draw()
            plt.pause(0.001)
        input("Press [enter] to continue.")

        for li in lista:
            li.remove()

        
        
    #Función que grafica el punto optimo
    def graficarPuntoOptimo(self,indiv,fo):
        self.ax.scatter([indiv.valX], [indiv.valY], [0], color="r", linewidth=2)
        self.ax.scatter([indiv.valX], [indiv.valY], [fo], color="r", linewidth=2)

    def graficar3D(self, fo):
        x = np.linspace(-5, 5, 30)
        y = np.linspace(-5, 5, 30)

        X, Y = np.meshgrid(x, y)
        Z = fo.funcion2Variables(X, Y)

        plt.ion()
        plt.show()

        fig = plt.figure()
        self.ax = plt.gca(projection='3d')
        self.ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                        cmap='Greys', edgecolor='none', color='b')
        self.ax.set_title('surface');
        
        plt.draw()
        plt.pause(0.001)
        
        
        
    #Función que inicia la grafica
    def __init__(self, fo):
        #self.graficarFuncionUnivariable1(fo)
        self.graficar3D(fo)





opti=Optimizador()

