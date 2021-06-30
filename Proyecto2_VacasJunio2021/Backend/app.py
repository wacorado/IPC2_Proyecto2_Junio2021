from tkinter import Listbox
from flask import *
import xml.etree.ElementTree as ET
from flask.wrappers import Request
from jinja2.utils import evalcontextfunction
from werkzeug.wrappers import Response
from datetime import date
from xml.dom import minidom
import requests as rqt


strBkpReturn=''
str_Archivo=''
xml_Reportesfinal=''


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hola Mundo'
#Se procesara el XML

@app.route('/clientes-xml', methods = ['POST'])
def post_ClientesXML():
    global strBkpReturn,xml_Reportesfinal
    listaclientes=[]
    listaMejoresClientes=[]
    listaJuegos=[]
    listaJuegosMasVendidos=[]
    # cantidadGastada=0
    str_Archivo= request.data.decode('UTF-8')
    strBkpReturn=request.data.decode('UTF-8')

    #------------- Aqui Desarmo el XML Recibido --------------------------
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
                    elif(datosJuego.tag=="Stock"):
                        print(datosJuego.text)
                        stockJuego=datosJuego.text
                print("Juego Registrado Exitosamente")
                listaJuegos.append([nombreJuego,plataformaJuego,añoLanzamientoJuego,clacificacionJuego,stockJuego])
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
    listaMejoresClientesReporteFinalOrdenada=list(reversed(tempListRepoMejoresClientes))

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
    listaClasificacionesReporteOrdenada=list(reversed(listaClasificacionesReporte))

    #Aqui se Generan los Datos para Reporte de Cumpleaños

    listaReporteCumpleañeros=[]
    for x in range(len(listaclientes)):
        listaReporteCumpleañeros.append([(str(listaclientes[x][0]+" "+str(listaclientes[x][1]))),str(listaclientes[x][3])])
    tempFechas=sorted(listaReporteCumpleañeros, key = lambda x:  str(x[1]))
    listaReporteCumpleañerosOrdenada=list(reversed(tempFechas))

    #---------- Aqui se Genera el Reporte de Juegos ---------------
    listaReporteJuegos=[]
    for x in range(len(listaJuegos)):
        listaReporteJuegos.append([str(listaJuegos[x][0]),str(listaJuegos[x][4])])
    tempListaRepJuegos=sorted(listaReporteJuegos, key = lambda x:  int(x[1]))
    listaReporteJuegosOrdenada=list(reversed(tempListaRepJuegos))


    




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
    
    print("\n------------ Datos Repo Cumpleaños ---------------\n")    
    for i in listaReporteCumpleañerosOrdenada:
        print(i)
    
    print("\n------------ Datos Repo Juegos ---------------\n")    
    for i in listaReporteJuegosOrdenada:
        print(i)
    
    #Incio Escritura de XML Reportes
    document=minidom.Document()
    root=document.createElement('Reportes')
    #Aqui Escribo los Datos del XML para Mejores Clientes
    repoMejoresClientes=document.createElement('ReporteMejoresClientes')
    root.appendChild(repoMejoresClientes)
    for x in range(len(listaMejoresClientesReporteFinalOrdenada)):
        mejorCliente=document.createElement("MejorCliente")
        repoMejoresClientes.appendChild(mejorCliente)
        for y in range(len(listaMejoresClientesReporteFinalOrdenada[x])):
            if(y==0):
                nombreMejorClienteReporte=document.createElement("Nombre")
                nombreMejorClienteReporte.appendChild(document.createTextNode(str(listaMejoresClientesReporteFinalOrdenada[x][y])))
                mejorCliente.appendChild(nombreMejorClienteReporte)
            if(y==1):
                cantidadGastadaClienteReporte=document.createElement("CantidadGastada")
                cantidadGastadaClienteReporte.appendChild(document.createTextNode(str(listaMejoresClientesReporteFinalOrdenada[x][y])))
                mejorCliente.appendChild(cantidadGastadaClienteReporte)
    #Aqui Escribo los Datos del XML para Juegos Mas Vendidos
    reporteJuegosMasVendidos=document.createElement('ReporteJuegosMasVendidos')
    root.appendChild(reporteJuegosMasVendidos)
    for x in range(len(listaReporteJuegoMasVendido)):
        juegosMasVendido=document.createElement("JuegoMasVendido")
        reporteJuegosMasVendidos.appendChild(juegosMasVendido)
        for y in range(len(listaReporteJuegoMasVendido[x])):
            if(y==0):
                nombreJuegoMasVendidoReporte=document.createElement("Nombre")
                nombreJuegoMasVendidoReporte.appendChild(document.createTextNode(str(listaReporteJuegoMasVendido[x][y])))
                juegosMasVendido.appendChild(nombreJuegoMasVendidoReporte)
            elif(y==1):
                añoLanzamientoJuegoMasVendidoReporte=document.createElement("AñoLanzamiento")
                añoLanzamientoJuegoMasVendidoReporte.appendChild(document.createTextNode(str(listaReporteJuegoMasVendido[x][y])))
                juegosMasVendido.appendChild(añoLanzamientoJuegoMasVendidoReporte)
            elif(y==2):
                copiasVendidasJuegoMasVendidoReporte=document.createElement("CopiasVendidas")
                copiasVendidasJuegoMasVendidoReporte.appendChild(document.createTextNode(str(listaReporteJuegoMasVendido[x][y])))
                juegosMasVendido.appendChild(copiasVendidasJuegoMasVendidoReporte)
    #Aqui Escribo los datos del XML para Clasificacion
    reporteClasificacion=document.createElement('ReporteClasificaciónes')
    root.appendChild(reporteClasificacion)
    for x in range(len(listaClasificacionesReporteOrdenada)):
        clasificacionRepo=document.createElement("Clacificación")
        reporteClasificacion.appendChild(clasificacionRepo)
        for y in range(len(listaClasificacionesReporteOrdenada[x])):
            if(y==0):
                tipoClasificacion=document.createElement("TipoClasificación")
                tipoClasificacion.appendChild(document.createTextNode(str(listaClasificacionesReporteOrdenada[x][y])))
                clasificacionRepo.appendChild(tipoClasificacion)
            elif(y==1):
                cantidadTipoClasificacion=document.createElement("Cantidad")
                cantidadTipoClasificacion.appendChild(document.createTextNode(str(listaClasificacionesReporteOrdenada[x][y])))
                clasificacionRepo.appendChild(cantidadTipoClasificacion)
    #Aqui Escribo los Datos para Reporte Cumpleañeros
    reporteCumpleañeors=document.createElement('ReporteCumpleañeros')
    root.appendChild(reporteCumpleañeors)
    for x in range(len(listaReporteCumpleañerosOrdenada)):
        cumpleañeroReporte=document.createElement("ClienteCumpleaños")
        reporteCumpleañeors.appendChild(cumpleañeroReporte)
        for y in range(len(listaReporteCumpleañerosOrdenada[x])):
            if(y==0):
                nombreCumpleañero=document.createElement("Nombre")
                nombreCumpleañero.appendChild(document.createTextNode(str(listaReporteCumpleañerosOrdenada[x][y])))
                cumpleañeroReporte.appendChild(nombreCumpleañero)
            elif(y==1):
                fechaCumpleañero=document.createElement("FechaNacimiento")
                fechaCumpleañero.appendChild(document.createTextNode(str(listaReporteCumpleañerosOrdenada[x][y])))
                cumpleañeroReporte.appendChild(fechaCumpleañero)
    #Aqui escribo el reporte de  Listado de Juegos
    reporteListadoJuegos=document.createElement("ReporteJuegos")
    root.appendChild(reporteListadoJuegos)
    for x in range(len(listaReporteJuegosOrdenada)):
        juegoReporte=document.createElement("Juego")
        reporteListadoJuegos .appendChild(juegoReporte)
        for y in range(len(listaReporteJuegosOrdenada[x])):
            if(y==0):
                nombreJuegoReporte=document.createElement("Nombre")
                nombreJuegoReporte.appendChild(document.createTextNode(str(listaReporteJuegosOrdenada[x][y])))
                juegoReporte.appendChild(nombreJuegoReporte)
            elif(y==1):
                stockJuegoReporte=document.createElement("Stock")
                stockJuegoReporte.appendChild(document.createTextNode(str(listaReporteJuegosOrdenada[x][y])))
                juegoReporte.appendChild(stockJuegoReporte)

    

    xml_Reportes = root.toprettyxml(indent='\t', encoding='utf-8')
    str_Reporte=(bytes(xml_Reportes)).decode('utf-8') 
    xml_Reportesfinal=str_Reporte 
    #str_Reportes=(xml_Reportes).encode('utf-8')
    print (str_Reporte) 

    #rqt.post('http://localhost:8000/Reportes',xml_Reportes)
    return Response(status=200)
   
@app.route('/returnXMLCompleto', methods = ['GET'])
def return_XML():
    global strBkpReturn
    #print(str(strBkpReturn))    
    return strBkpReturn

@app.route('/returnXMLReporte', methods = ['GET'])
def return_XMLReporte():
    global xml_Reportesfinal
    #print(str(strBkpReturn))    
    return xml_Reportesfinal

if __name__ == '__main__':
    app.run(debug=True)
