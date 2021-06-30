from tkinter import Listbox
from flask import *
import xml.etree.ElementTree as ET
from flask.wrappers import Request
from jinja2.utils import evalcontextfunction
from werkzeug.wrappers import Response

strBkpReturn=''
str_Archivo=''


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hola Mundo'
#Se procesara el XML

@app.route('/clientes-xml', methods = ['POST'])
def post_ClientesXML():
    global strBkpReturn
    listaclientes=[]
    listaMejoresClientes=[]
    listaJuegos=[]
    listaJuegosMasVendidos=[]
    # cantidadGastada=0
    str_Archivo= request.data.decode('UTF-8')
    strBkpReturn=request.data.decode('UTF-8')
    raiz = ET.fromstring(str_Archivo)
    for elemento in raiz:
        print("-----------------------"+elemento.tag+"---------------------")
        if(elemento.tag=="Clientes"):
            for clientes in elemento:
                print("-------------------"+clientes.tag+"-------------------------")
                for datosCliente in clientes:
                    if(datosCliente.tag=="Nombre"):
                        print(datosCliente.text)
                        nombre=datosCliente.text
                    elif(datosCliente.tag=="Apellido"):
                        print(datosCliente.text)
                        apellido=datosCliente.text
                    elif(datosCliente.tag=="Edad"):
                        print(datosCliente.text)
                        edad=datosCliente.text
                    elif(datosCliente.tag=="FechaCumpleaños"):
                        print(datosCliente.text)
                        fechaCumple=datosCliente.text
                    elif(datosCliente.tag=="FechaPrimeraCompra"):
                        print(datosCliente.text)
                        fechaPrimeraCompra=datosCliente.text
                print("Cliente Guardado Correctamente")
                listaclientes.append([nombre,apellido,edad,fechaCumple,fechaPrimeraCompra])
        elif(elemento.tag=="MejoresClientes"):
            for mejoresClientes in elemento:
                print("-----------------"+mejoresClientes.tag+"------------------------")
                for datosMejorCliente in mejoresClientes:
                    if(datosMejorCliente.tag=="Nombre"):
                        print(datosMejorCliente.text)
                        nombreMejorCliente=datosMejorCliente.text
                    elif(datosMejorCliente.tag=="FechaUltimaCompra"):
                        print(datosMejorCliente.text)
                        fechaUltimaCompraMejorCliente=datosMejorCliente.text
                    elif(datosMejorCliente.tag=="CantidadComprada"):
                        print(datosMejorCliente.text)
                        cantidadComprada=datosMejorCliente.text
                    elif(datosMejorCliente.tag=="CantidadGastada"):
                        print(datosMejorCliente.text)
                        cantidadGastada=datosMejorCliente.text
                print("Mejor Cliente Guardado Exitosamente")
                listaMejoresClientes.append([nombreMejorCliente,fechaUltimaCompraMejorCliente,cantidadComprada,cantidadGastada])
        elif(elemento.tag=="Juegos"):
            for juegos in elemento:
                print("-----------------"+juegos.tag+"-------------------")
                for datosJuego in juegos:
                    if(datosJuego.tag=="Nombre"):
                        print(datosJuego.text)
                        nombreJuego=datosJuego.text
                    elif(datosJuego.tag=="Plataforma"):
                        print(datosJuego.text)
                        plataformaJuego=datosJuego.text
                    elif(datosJuego.tag=="AñoLanzamiento"):
                        print(datosJuego.text)
                        añoLanzamientoJuego=datosJuego.text
                    elif(datosJuego.tag=="Clasificacion"):
                        print(datosJuego.text)
                        clacificacionJuego=datosJuego.text
                print("Juego Registrado Exitosamente")
                listaJuegos.append([nombreJuego,plataformaJuego,añoLanzamientoJuego,clacificacionJuego])
        elif(elemento.tag=="JuegosMasVendidos"):
            for juegosMasVendidos in elemento:
                print("-----------------"+juegosMasVendidos.tag+"----------------")
                for datoJuegoMasVendido in juegosMasVendidos:
                    if(datoJuegoMasVendido.tag=="Nombre"):
                        print(datoJuegoMasVendido.text)
                        nombreJuegoMasVendido=datoJuegoMasVendido.text
                    elif(datoJuegoMasVendido.tag=="FechaUltimaCompra"):
                        print(datoJuegoMasVendido.text)
                        fechaUitimaCompraJuegoMasVendido=datoJuegoMasVendido.text
                    elif(datoJuegoMasVendido.tag=="CopiasVendidas"):
                        print(datoJuegoMasVendido.text)
                        copiasVendidasJuegosMasVendido=datoJuegoMasVendido.text
                    elif(datoJuegoMasVendido.tag=="Stock"):
                        print(datoJuegoMasVendido.tag)
                        stockJuegoMasVendido=datoJuegoMasVendido.text
                print("Juego Mas Vendido Registrado Exitosamente")
                listaJuegosMasVendidos.append([nombreJuegoMasVendido,fechaUitimaCompraJuegoMasVendido,copiasVendidasJuegosMasVendido,stockJuegoMasVendido])

    print("\n ---------- Data Almacenada en las Listas Principales ------------\n")
    print("\n###### Lista Clienetes######\n")
    for i in listaclientes:
        print(i)
    print("\n###### Lista Mejores Clienetes######\n")
    for i in listaMejoresClientes:
        print(i)
    print("\n###### Lista Juegos######\n")
    for i in listaJuegos:
        print(i)
    print("\n###### Lista Juegos Mas Vendidos######\n")
    for i in listaJuegosMasVendidos:
        print(i)
    
    

    print("\n---------Data para los Reportes a partir de aqui --------\n")

    #--------- Aqui valido el reporte Juegos Mas Vendidos
    listaReporteJuegoMasVendido=[]
    añoLanzamientoJuegoReporte=''
    for x in range(len(listaJuegosMasVendidos)):
        for y in range(len(listaJuegosMasVendidos[x])):
            if(y==0):
                nombreJuegoMasVendidoRepo=str(listaJuegosMasVendidos[x][y])
                for x1 in range(len(listaJuegos)):
                    for y1 in range(len(listaJuegos[x1])):
                        if (y1==0):
                            if(nombreJuegoMasVendidoRepo==str(listaJuegos[x1][y1])):
                                print("Juego: "+nombreJuegoMasVendidoRepo+" igual a: "+str(listaJuegos[x1][y1]))
                                #print("Juego Mas vendido si se Encuentra dentro de Juegos Mas Vendidos")
                                print("Año Lanzamiento: "+str(listaJuegos[x1][2]))
                                añoLanzamientoJuegoReporte=str(listaJuegos[x1][2])
                                cantidadVendidaReporte=str(listaJuegosMasVendidos[x][2])
                                listaReporteJuegoMasVendido.append([nombreJuegoMasVendidoRepo,añoLanzamientoJuegoReporte,cantidadVendidaReporte])
                            else:
                                print("Juego: "+nombreJuegoMasVendidoRepo+" No igual a: "+str(listaJuegos[x1][y1]))
    
   
    #---------------- Aqui genero el reporte mejores Clientes
    listaMejoresClientesReporte=[]
    listaPosRepetidas=[]
    for x in range(len(listaMejoresClientes)):
        for y in range(len(listaMejoresClientes[x])):
            if(y==0):
                nombreMejorClienteReporte=str(listaMejoresClientes[x][y])
                montoGastadoMejorCliente=float(listaMejoresClientes[x][3])
                for x1 in range(len(listaMejoresClientes)):
                    for y1 in range(len(listaMejoresClientes[x1])):
                        if(y1==0):
                            if(x1==x):
                                print("Se esta Comparando el Mismo registro por lo cual se Salta")
                            else:
                                if(nombreMejorClienteReporte==str(listaMejoresClientes[x1][0])):
                                    print("Existe Coincidencia en Datos")
                                    montoGastadoMejorCliente=montoGastadoMejorCliente+float(listaMejoresClientes[x1][3])
                                    listaPosRepetidas.append(x1)
                                    #listaMejoresClientesReporte.append([nombreMejorClienteReporte,MontoTotal])
                                else:
                                    print("No se Genero Coincidencia")
                listaMejoresClientesReporte.append([nombreMejorClienteReporte,str(montoGastadoMejorCliente)])
    
    listaMejoresClientesReporteFinal=[]
    for i in listaMejoresClientesReporte:
        if i not in listaMejoresClientesReporteFinal:
            listaMejoresClientesReporteFinal.append(i)
    tempListRepoMejoresClientes=sorted(listaMejoresClientesReporteFinal, key = lambda x:  float(x[1]))
    listaMejoresClientesReporteFinalOrdenada=reversed(tempListRepoMejoresClientes)

    #Aqui genero la data para el reporte Clasificacion
    listaClasificaciones=[]
    listaClasificacionesReporte=[]
    listaTempClasificaciones=[]
    tempOrdenadorCalificaciones=[]
    for x in range(len(listaJuegos)):
        for y in range(len(listaJuegos[x])):
            listaTempClasificaciones.append(str(listaJuegos[x][3]))
    listaClasificaciones=set(listaTempClasificaciones)
    for i in listaClasificaciones:
        print(i)
    for i in listaClasificaciones:
        contador=0
        for x in range(len(listaJuegos)):
            if (str(i)==str(listaJuegos[x][3])):
                contador = contador+1
        tempOrdenadorCalificaciones.append([str(i),str(contador)])
    listaClasificacionesReporte=sorted(tempOrdenadorCalificaciones, key = lambda x:  int(x[1]))
    listaClasificacionesReporteOrdenada=reversed(listaClasificacionesReporte)


    




    print("\n-------------- Data Reportes Graficas ---------------\n")

    print("\n-------------- Data Juegos Mas Vendidos --------------\n")
    for i in listaReporteJuegoMasVendido:
        print(i)
    
    print("\n------------ Datos Mejores Clientes ---------------\n")
    for i in listaMejoresClientesReporteFinalOrdenada:
        print(i)

    print("\n------------ Datos Repo Clasificacion ---------------\n")    
    for i in listaClasificacionesReporteOrdenada:
        print(i)

    return Response(status=200)

    

@app.route('/returnXMLCompleto', methods = ['GET'])
def return_XML():
    global strBkpReturn
    #print(str(strBkpReturn))    
    return strBkpReturn

if __name__ == '__main__':
    app.run(debug=True)
