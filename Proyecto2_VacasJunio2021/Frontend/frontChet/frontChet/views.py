from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests as rqt
import csv
import re
from xml.dom import minidom
import xml.etree.ElementTree as ET

class listaClientes:
    def __init__(self):
        self.listaClientes=[]
    def addCliente(self,cliente):
        self.listaClientes.append(cliente)
    def returnClientes(self):
        return self.listaClientes

class Cliente:
    def __init__(self,nombre,apellido,edad,fechaNac,fechaPrimeraCompra):
        self.nombre=nombre
        self.apellido=apellido
        self.edad=edad
        self.fechaNac=fechaNac
        self.fechaPrimeraCompra=fechaPrimeraCompra

listaClientesCsv=listaClientes()
xml_ReportesFrontend=''
    
def Saludo(request):
    return HttpResponse("Hola Mundo Prueba Cruel")

def principal(request):
    xml_return=rqt.get('http://localhost:5000/returnXMLCompleto')
    xml_returnSTR=xml_return.text
    context={'xmlTotal':xml_returnSTR}
    #context={'xmlTotal':rqt.get('http://localhost:5000/returnXMLCompleto').text}
    return render(request,'index.html',context)
    #return render(request,'index.html')

def procesarCSVClientes(request):
    lista1Clientes=[]
    listaPosErrores=[]
    listaMejoresClientes=[]
    listaPosErroresMejoresClientes=[]
    listaJuegos=[]
    listaposErroresJuegos=[]
    listaJuegosMasVendidos=[]
    lisaPosErroresJuegosMasVendidos=[]
    if request.method=='POST':

        print("si entro al post de los archivos")
        # ------------------------ Proceso el archivo Clientes.csv desde aqui ---------------------------
        file = open ("ReporteEroresWEBClientes.txt","w")
        urlCsvClientes=request.FILES['clientes'].read().decode('utf-8').splitlines()
        print("------------------------------- Clientes ----------------------------------------")
        #print(urlCsvClientes)
        reader = csv.reader(urlCsvClientes, delimiter=';')
        #print("-------- Comprobar Lectura de CSV ------------")
        for i in reader:
            listaClientesCsv.addCliente(Cliente(i[0],i[1],i[2],i[3],i[4]))
            lista1Clientes.append(i)
            #print(i)
        lista1Clientes.pop(0)

        for i in lista1Clientes:
            print(i)

        for x in range(len(lista1Clientes)):
            for y in range(len(lista1Clientes[x])):
                if(y==0):
                    nombre=str(lista1Clientes[x][y])
                    nombreValid=re.search(r'[^a-zA-Z\s\á\é\í\ó\ú]+?', nombre)
                    if(nombreValid):
                        print("Error en Nombre de Cliente")
                        file.write("Error en Nombre: "+nombre+ " Registro #: "+str(x+1)+"\n")
                        listaPosErrores.append(int(x))
                    else:
                        print("Nombre de Cliente Valido")
                if(y==1):
                    apellido=str(lista1Clientes[x][y])
                    apellidoValid=re.search(r'[^a-zA-Z\s\á\é\í\ó\ú]+?',apellido)
                    if(apellidoValid):
                        print("Error en apellido del Cliente")
                        file.write("Error en Apellido: "+apellido+ " Registro #: "+str(x+1)+"\n")
                        listaPosErrores.append(int(x))
                    else:
                        print("Apellido de Cliente Valido")
                if(y==2):
                    edad=str(lista1Clientes[x][y])
                    edadValid=re.search(r'[^0-9\s]+?',edad)
                    if(edadValid):
                        print("Error en edad del Cliente")
                        file.write("Error en edad: "+edad+ " Registro #: "+str(x+1)+"\n")
                        listaPosErrores.append(int(x))
                    else:
                        print("edad de Cliente Valido")
                if(y==3):
                    fechaNac=str(lista1Clientes[x][y])
                    fechaNacValid=re.search(r'^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$',fechaNac)
                    if(fechaNacValid):
                        print("Fecha de Nacimiento Valida")
                    else:
                        print("Error en Formato Fecha de Nacimiento")
                        file.write("Error en formato Fecha: "+fechaNac+" Registro #: "+str(x+1)+"\n")
                        listaPosErrores.append(int(x))
                if(y==4):
                    fechaUltCompra=str(lista1Clientes[x][y])
                    fechaUltCompraValid=re.search(r'^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$',fechaUltCompra)
                    if(fechaUltCompraValid):
                        print("Fecha de Ultima Compra Valida")
                    else:
                        print("Error en Formato Fecha de Ultima Compra")
                        file.write("Error en formato Fecha: "+fechaNac+" Registro #: "+str(x+1)+"\n")
                        listaPosErrores.append(int(x))
        listaPosErroresOrdenada=sorted(listaPosErrores)
        for i in listaPosErroresOrdenada:
            print(i)
        listTemp=set(listaPosErroresOrdenada)
        listaBorradorClientes=sorted(listTemp)
        contadorBorradorClientes=0
        print("Validador de Numeros Correctos")
        for i in listaBorradorClientes:
            lista1Clientes.pop(int(i)-contadorBorradorClientes)
            contadorBorradorClientes=contadorBorradorClientes+1
            print(i)   
        file.close()        
        print("\n --------------- DepuraCion de Archivo Clientes -------------------------\n")

        for i in lista1Clientes:
            print(i)

        #------------------ a partir de aqui proceso el de Mejores Clientes -------------------------------------------
        file = open ("ReporteEroresWEBMejoresClientes.txt","w")
        urlCsvMejoresClientes=request.FILES['mejoresClientes'].read().decode('utf-8').splitlines()
        print("-------------------- Mejores Clientes --------------------------------------")
        #print(urlCsvMejoresClientes)
        readerMejoresClientes = csv.reader(urlCsvMejoresClientes,delimiter=";")
        for i in readerMejoresClientes:
            listaMejoresClientes.append(i)
        listaMejoresClientes.pop(0)
        for i in listaMejoresClientes:
            print(i)
        
        for x in range(len(listaMejoresClientes)):
            for y in range(len(listaMejoresClientes[x])):
                if(y==0):
                    nombreMejorCliente=str(listaMejoresClientes[x][y])
                    nombreMejorClienteValid=re.search(r'[^a-zA-Z\s\á\é\í\ó\ú]+?',nombreMejorCliente)
                    if(nombreMejorClienteValid):
                        print("Error en Nombre de Cliente")
                        file.write("Error en Nombre Mejor Cliente: "+nombre+ " Registro #: "+str(x+1)+"\n")
                        listaPosErroresMejoresClientes.append(x)
                    else:
                        print("Nombre de Mejor Cliente Valido")
                if(y==1):
                    fechaUltCompra=str(listaMejoresClientes[x][y])
                    fechaUltCompraValid=re.search(r'^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$',fechaUltCompra)
                    if(fechaUltCompraValid):
                        print("Fecha de Ultima Compra Valida")
                    else:
                        print("Error en Formato Fecha Ultima Compra")
                        file.write("Error en formato Fecha Ultima Compra: "+fechaUltCompra+" Registro #: "+str(x+1)+"\n")
                        listaPosErroresMejoresClientes.append(x)
                if(y==2):
                    cantidad=str(listaMejoresClientes[x][y])
                    cantidadValid=re.search(r'[^0-9\s]+?',cantidad)
                    if(cantidadValid):
                        print("Error en Cantidad Juegos del Cliente")
                        file.write("Error en Cantidad: "+cantidad+ " Registro #: "+str(x+1)+"\n")
                        listaPosErroresMejoresClientes.append(x)
                    else:
                        print("edad de Cliente Valido")
                if(y==3):
                    montoGastado=str(listaMejoresClientes[x][y])
                    montoGastadoValid=re.search(r'[^0-9\.\s]',montoGastado)
                    if(montoGastadoValid):
                        print("Error en monto Gastado")
                        file.write("Error en Formato de Monto Gastado: "+montoGastado+" Registro #: "+str(x+1)+"\n")
                        listaPosErroresMejoresClientes.append(x)
                    else:
                        montoGastadoPunto=str(listaMejoresClientes[x][y])
                        montoGastadoPuntoValid=re.search(r'[\.]',montoGastadoPunto)
                        if(montoGastadoPuntoValid):
                            print("Monto Gastado es Valido")
                        else:
                            listaMejoresClientes[x][y]=str(listaMejoresClientes[x][y])+".00"
                            print("Monto Gastado Corregido")
        listaPosErroresMejoresClientesOrdenada=sorted(listaPosErroresMejoresClientes)
        listTemp2=set(listaPosErroresMejoresClientesOrdenada)
        listaBorradorMejoresClientes=sorted(listTemp2)
        contadorBorradorMejoresClientes=0
        print("Validador de Numeros Correctos")
        for i in listaBorradorMejoresClientes:
            listaMejoresClientes.pop(int(i)-contadorBorradorMejoresClientes)
            contadorBorradorMejoresClientes=contadorBorradorMejoresClientes+1
            print(i)   
        file.close()        
        print("\n --------------- Depuracion de Archivo MejoresClientes -------------------------\n")

        for i in listaMejoresClientes:
            print(i)

        # --------------------------- a partir de aqui proceso archivo Juegos -------------------------------------------
        file=open("ReporteEroresWEBJuegos.txt","w")
        urlCsvJuegos=request.FILES['juegos'].read().decode('utf-8').splitlines()
        print("-------------------- Juegos --------------------------------------")
        readerJuegos = csv.reader(urlCsvJuegos,delimiter=";")
        for i in readerJuegos:
            listaJuegos.append(i)
        listaJuegos.pop(0)
        for i in listaJuegos:
            print(i)
        for x in range(len((listaJuegos))):
            for y in range(len(listaJuegos[x])):
                if(y==0):
                    nombreJuego=str(listaJuegos[x][y])
                    nombreJuegoValid=re.search(r'[^a-zA-Z0-9\s\á\é\í\ó\ú\-\:\ñ\Ñ]+?',nombreJuego)
                    if(nombreJuegoValid):
                        print("Error en Nombre de Juego")
                        file.write("Error en Nombre de Juego: "+nombreJuego+ " Registro #: "+str(x+1)+"\n")
                        listaposErroresJuegos.append(x)
                    else:
                        print("Nombre de Juego Valido")
                if(y==1):
                    plataformaJuego=str(listaJuegos[x][y])
                    plataformaJuegoValid=re.search(r'[^a-zA-Z0-9\s\á\é\í\ó\ú\-]+?',plataformaJuego)
                    if(plataformaJuegoValid):
                        print("Error en Plataforma de Juego")
                        file.write("Error en Plataforma de Juego: "+plataformaJuego+ " Registro #: "+str(x+1)+"\n")
                        listaposErroresJuegos.append(x)
                    else:
                        print("Plataforma de Juego Valida")
                if(y==2):
                    añoLanzamiento=str(listaJuegos[x][y])
                    añoLanzamientoValid=re.search(r'[^0-9\s]+?',añoLanzamiento)
                    if(añoLanzamientoValid):
                        print("Error en Año de Lanzamiento de Juego")
                        file.write("Error en Año de Lanzamiento de Juego: "+añoLanzamiento+ " Registro #: "+str(x+1)+"\n")
                        listaposErroresJuegos.append(x)
                    else:
                        print("Año de Lanzamiento Valido")
                if(y==3):
                    clasificacionJuego=str(listaJuegos[x][y])
                    clasificacionJuegoValid=re.search(r'[^A-Z]{1}?',clasificacionJuego)
                    if(clasificacionJuegoValid):
                        print("Error en Clasificacion de Juego")
                        file.write("Error en Clasificacion de Juego: "+clasificacionJuego+ " Registro #: "+str(x+1)+"\n")
                        listaposErroresJuegos.append(x)
                    else:
                        print("Clasificacion de Juego Valida")
                if(y==4):
                    stock=str(listaJuegos[x][y])
                    stockValid=re.search(r'[^0-9\s]+?',stock)
                    if(stockValid):
                        print("Error en Stock de Juego")
                        file.write("Error en Stok de Juego: "+stock+ " Registro #: "+str(x+1)+"\n")
                        listaposErroresJuegos.append(x)
                    else:
                        print("Stock de Juego Valida")

        listaposErroresJuegosOrdenada=sorted(listaposErroresJuegos)
        listTemp3=set(listaposErroresJuegosOrdenada)
        listaBorradorJuegos=sorted(listTemp3)
        contadorBorradorJuegos=0
        print("Validador de Numeros a Borrar en Juegos")
        for i in listaBorradorJuegos:
            listaJuegos.pop(int(i)-contadorBorradorJuegos)
            contadorBorradorJuegos=contadorBorradorJuegos+1
            print(i)
        file.close()
        print("\n --------------- Depuracion de Archivo Juegos -------------------------\n")
        for i in listaJuegos:
            print(i)

        #---------------- a partir de aqui proceso el Archivo JuegosmasVendidos --------------------------------------------
        file=open("ReporteErroresWEBJuegosMasVendidos.txt","w")
        urlCsvJuegosMasVendidos=request.FILES['juegosMasVendidos'].read().decode('utf-8').splitlines()
        print("----------------------- Juegos Mas Vendidos ----------------------------")
        readerJuegosMasVendidos=csv.reader(urlCsvJuegosMasVendidos, delimiter=";")
        for i in readerJuegosMasVendidos:
            listaJuegosMasVendidos.append(i)
        listaJuegosMasVendidos.pop(0)
        for i in listaJuegosMasVendidos:
            print(i)
        for x in range(len(listaJuegosMasVendidos)):
            for y in range(len(listaJuegosMasVendidos[x])):
                if(y==0):
                    nombreJuegoMasVendido=str(listaJuegosMasVendidos[x][y])
                    nombreJuegoMasVendidoValid=re.search(r'[^a-zA-Z0-9\s\á\é\í\ó\ú\-\.]+?',nombreJuegoMasVendido)
                    if(nombreJuegoMasVendidoValid):
                        print("Error en Nombre de Juego Mas Vendido")
                        file.write("Error en Nombre de Juego Mas Vendido : "+nombreJuegoMasVendido+ " Registro #: "+str(x+1)+"\n")
                        lisaPosErroresJuegosMasVendidos.append(x)
                    else:
                        print("Nombre de Juego Mas Vendido Valido")
                elif(y==1):
                    fechaUltimaCompraMasVendido=str(listaJuegosMasVendidos[x][y])
                    fechaUltimaCompraMasVendidoValid=re.search(r'^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$',fechaUltimaCompraMasVendido)
                    if(fechaUltimaCompraMasVendidoValid):
                         print("Fecha de Ultima Compra Valida")
                    else:
                        print("Error en Formato Fecha de Ultima Compra")
                        file.write("Error en formato Fecha Ultima COmpra: "+fechaUltimaCompraMasVendido+" Registro #: "+str(x+1)+"\n")
                        lisaPosErroresJuegosMasVendidos.append(int(x))
                elif(y==2):
                    copiasVendidas=str(listaJuegosMasVendidos[x][y])
                    copiasVendidasValid=re.search(r'[^0-9\s]+?',copiasVendidas)
                    if(copiasVendidasValid):
                        print("Error en Cantidad de Copias Vendidas")
                        file.write("Error en Cantidad de Copias Vendidas: "+copiasVendidas+ " Registro #: "+str(x+1)+"\n")
                        lisaPosErroresJuegosMasVendidos.append(int(x))
                    else:
                        print("Cantidad de Copias Vendidas Validas")
                elif(y==3):
                    stockMasVendido=str(listaJuegosMasVendidos[x][y])
                    stockMasVendidoValid=re.search(r'[^0-9\s]+?',stockMasVendido)
                    if(stockMasVendidoValid):
                        print("Error en Estok de Ventas")
                        file.write("Error en Estock de Ventas: "+stockMasVendido+ " Registro #: "+str(x+1)+"\n")
                        lisaPosErroresJuegosMasVendidos.append(int(x))
                    else:
                        print("Cantidad Stock Valida")
        listaPosErroresJuegosMasVendidosOrdenada=sorted(lisaPosErroresJuegosMasVendidos)
        listaTemp4=set(listaPosErroresJuegosMasVendidosOrdenada)
        listaBorradorJuegosMasVendidos=sorted(listaTemp4)
        contadorBorradorJuegosMasVendidos=0
        print("Validador Nuemreos a Borrar en Juegos Mas Vendidos")
        for i in listaBorradorJuegosMasVendidos:
            listaJuegosMasVendidos.pop(int(i)-contadorBorradorJuegosMasVendidos)
            contadorBorradorJuegosMasVendidos=contadorBorradorJuegosMasVendidos+1
            print(i)
        file.close()
        print("\n --------------- Depuracion de  Juegos Mas Vendidos -------------------------\n")
        for i in listaJuegosMasVendidos:
            print(i)

       
        #Escribo la parte de Clientes en el XML
        #Escribo el XML los Clientes
        document=minidom.Document()
        root=document.createElement('Chet')
        #Escribo los Clientes ya Validados
        clientesXML=document.createElement('Clientes')
        root.appendChild(clientesXML)
        for x in range(len(lista1Clientes)):
            clienteXML= document.createElement("Cliente")
            clientesXML.appendChild(clienteXML)
            for y in range(len(lista1Clientes[x])):
                if(y==0):
                    nombreCliente=document.createElement("Nombre")
                    nombreCliente.appendChild(document.createTextNode(str(lista1Clientes[x][y])))
                    clienteXML.appendChild(nombreCliente)
                elif(y==1):
                    apellidoCliente=document.createElement("Apellido")
                    apellidoCliente.appendChild(document.createTextNode(str(lista1Clientes[x][y])))
                    clienteXML.appendChild(apellidoCliente)
                elif(y==2):
                    edadCliente=document.createElement("Edad")
                    edadCliente.appendChild(document.createTextNode(str(lista1Clientes[x][y])))
                    clienteXML.appendChild(edadCliente)
                elif(y==3):
                    fechaNacCliente=document.createElement("FechaCumpleaños")
                    fechaNacCliente.appendChild(document.createTextNode(str(lista1Clientes[x][y])))
                    clienteXML.appendChild(fechaNacCliente)
                elif(y==4):
                    fechaPrimCompra=document.createElement("FechaPrimeraCompra")
                    fechaPrimCompra.appendChild(document.createTextNode(str(lista1Clientes[x][y])))
                    clienteXML.appendChild(fechaPrimCompra)
        #Escribo los MejoresClientes ya Validados
        mejoresClientesXML=document.createElement('MejoresClientes')
        root.appendChild(mejoresClientesXML)
        for x in range(len(listaMejoresClientes)):
            mejorClienteXML=document.createElement('MejorCliente')
            mejoresClientesXML.appendChild(mejorClienteXML)
            for y in range(len(listaMejoresClientes[x])):
                if(y==0):
                    nombreCliente=document.createElement("Nombre")
                    nombreCliente.appendChild(document.createTextNode(str(listaMejoresClientes[x][y])))
                    mejorClienteXML.appendChild(nombreCliente)
                if(y==1):
                    fechaUltimaCompra=document.createElement("FechaUltimaCompra")
                    fechaUltimaCompra.appendChild(document.createTextNode(str(listaMejoresClientes[x][y])))
                    mejorClienteXML.appendChild(fechaUltimaCompra)
                if(y==2):
                    cantidadComprada=document.createElement("CantidadComprada")
                    cantidadComprada.appendChild(document.createTextNode(str(listaMejoresClientes[x][y])))
                    mejorClienteXML.appendChild(cantidadComprada)
                if(y==3):
                    cantidadGastada=document.createElement("CantidadGastada")
                    cantidadGastada.appendChild(document.createTextNode(str(listaMejoresClientes[x][y])))
                    mejorClienteXML.appendChild(cantidadGastada)
        #Escribo los Juegos ya Validados
        juegosXML=document.createElement('Juegos')
        root.appendChild(juegosXML)
        for x in range(len(listaJuegos)):
            juegoXML=document.createElement('Juego')
            juegosXML.appendChild(juegoXML)
            for y in range(len(listaJuegos[x])):
                if(y==0):
                    nombreJuego=document.createElement("Nombre")
                    nombreJuego.appendChild(document.createTextNode(str(listaJuegos[x][y])))
                    juegoXML.appendChild(nombreJuego)
                elif(y==1):
                    plataformaJuego=document.createElement("Plataforma")
                    plataformaJuego.appendChild(document.createTextNode(str(listaJuegos[x][y])))
                    juegoXML.appendChild(plataformaJuego)
                elif(y==2):
                    añoJuego=document.createElement("AñoLanzamiento")
                    añoJuego.appendChild(document.createTextNode(str(listaJuegos[x][y])))
                    juegoXML.appendChild(añoJuego)
                elif(y==3):
                    clasificJuego=document.createElement("Clasificacion")
                    clasificJuego.appendChild(document.createTextNode(str(listaJuegos[x][y])))
                    juegoXML.appendChild(clasificJuego)
                elif(y==4):
                    stockJuego=document.createElement("Stock")
                    stockJuego.appendChild(document.createTextNode(str(listaJuegos[x][y])))
                    juegoXML.appendChild(stockJuego)
        #Escribo los Juegos Mas Vendidos ya Validados
        juegosMasVendidos=document.createElement("JuegosMasVendidos")
        root.appendChild(juegosMasVendidos)
        for x in range(len(listaJuegosMasVendidos)):
            juegoMasVendidoXML=document.createElement("JuegoMasVendido")
            juegosMasVendidos.appendChild(juegoMasVendidoXML)
            for y in range(len(listaJuegosMasVendidos[x])):
                if(y==0):
                    nombreJuegoMasVendido=document.createElement("Nombre")
                    nombreJuegoMasVendido.appendChild(document.createTextNode(str(listaJuegosMasVendidos[x][y])))
                    juegoMasVendidoXML.appendChild(nombreJuegoMasVendido)
                elif(y==1):
                    fechaUltimaCompraJuegoMasVendido=document.createElement("FechaUltimaCompra")
                    fechaUltimaCompraJuegoMasVendido.appendChild(document.createTextNode(str(listaJuegosMasVendidos[x][y])))
                    juegoMasVendidoXML.appendChild(fechaUltimaCompraJuegoMasVendido)
                elif(y==2):
                    copiasVendidasJuegoMasVendido=document.createElement("CopiasVendidas")
                    copiasVendidasJuegoMasVendido.appendChild(document.createTextNode(str(listaJuegosMasVendidos[x][y])))
                    juegoMasVendidoXML.appendChild(copiasVendidasJuegoMasVendido)
                elif(y==3):
                    stock=document.createElement("Stock")
                    stock.appendChild(document.createTextNode(str(listaJuegosMasVendidos[x][y])))
                    juegoMasVendidoXML.appendChild(stock)

        
        xml_file = root.toprettyxml(indent='\t', encoding='utf-8')
        print(xml_file)
        rqt.post('http://localhost:5000/clientes-xml',xml_file)
    return redirect('principal')

def Reportes(request):
    global xml_ReportesFrontend
    listaMejoresClientesRepo=[]
    listaJuegosMasVendidoRepo=[]
    listaClasificacionRepo=[]
    listaCumpleañerosRepo=[]
    listaJuegosRepo=[]
    xml_ReportesFrontend=rqt.get('http://localhost:5000/returnXMLReporte')
    print(xml_ReportesFrontend)
    strxml_ReportesFrontend=xml_ReportesFrontend.text
    raiz = ET.fromstring(strxml_ReportesFrontend)
    for elemento in raiz:
        print("-----------------------"+elemento.tag+"---------------------")
        if(elemento.tag=="ReporteMejoresClientes"):
            for mejoresClientes in elemento:
                print("-------------------"+mejoresClientes.tag+"-------------------------")
                for datosMejoresCliente in mejoresClientes:
                    if(datosMejoresCliente.tag=="Nombre"):
                        print(datosMejoresCliente.text)
                        nombreMejorCliente=datosMejoresCliente.text
                    elif(datosMejoresCliente.tag=="CantidadGastada"):
                        print(datosMejoresCliente.text)
                        cantidadGastada=datosMejoresCliente.text
                print("Mejor Cliente Registrado Correctamente")
                listaMejoresClientesRepo.append([nombreMejorCliente,cantidadGastada])
        if(elemento.tag=="ReporteJuegosMasVendidos"):
            for juegoMasVendido in elemento:
                print("-------------------"+juegoMasVendido.tag+"-------------------------")
                for datosJuegoMasVendido in juegoMasVendido:
                    if(datosJuegoMasVendido.tag=="Nombre"):
                        print(datosJuegoMasVendido.text)
                        nombreJuegoMasVendido=datosJuegoMasVendido.text
                    elif(datosJuegoMasVendido.tag=="AñoLanzamiento"):
                        print(datosJuegoMasVendido.text)
                        añoLanzamientoJuegoMasVendido=datosJuegoMasVendido.text
                    elif(datosJuegoMasVendido.tag=="CopiasVendidas"):
                        print(datosJuegoMasVendido.text)
                        copiasVendidasJuegoMasVendido=datosJuegoMasVendido.text
                print("Juego Mas Vendido Registrado Correctamente")
                listaJuegosMasVendidoRepo.append([nombreJuegoMasVendido,añoLanzamientoJuegoMasVendido,copiasVendidasJuegoMasVendido])    
        if(elemento.tag=="ReporteClasificaciónes"):
            for clasificaciones in elemento:
                print("-------------------"+clasificaciones.tag+"-------------------------")
                for datosclasificaciones in clasificaciones:
                    if(datosclasificaciones.tag=="TipoClasificación"):
                        print(datosclasificaciones.text)
                        letraClasificacion=datosclasificaciones.text
                    elif(datosclasificaciones.tag=="Cantidad"):
                        print(datosclasificaciones.text)
                        cantidadClasificacion=datosclasificaciones.text
                print("Clasificacion Juego Registrada Correctamente")
                listaClasificacionRepo.append([letraClasificacion,cantidadClasificacion])
        if(elemento.tag=="ReporteCumpleañeros"):
            for Cumpleañeros in elemento:
                print("-------------------"+Cumpleañeros.tag+"-------------------------")
                for datoCumpleañero in Cumpleañeros:
                    if(datoCumpleañero.tag=="Nombre"):
                        print(datoCumpleañero.text)
                        nombreCumpleañero=datoCumpleañero.text
                    elif(datoCumpleañero.tag=="FechaNacimiento"):
                        print(datoCumpleañero.text)
                        fechaCumpleañero=datoCumpleañero.text
                print("Clasificacion Juego Registrada Correctamente")
                listaCumpleañerosRepo.append([nombreCumpleañero,fechaCumpleañero])
        if(elemento.tag=="ReporteJuegos"):
            for Juego in elemento:
                print("-------------------"+Juego.tag+"-------------------------")
                for datoJuego in Juego:
                    if(datoJuego.tag=="Nombre"):
                        print(datoJuego.text)
                        nombreJuego=datoJuego.text
                    elif(datoJuego.tag=="Stock"):
                        print(datoJuego.text)
                        stockJuego=datoJuego.text
                print("Clasificacion Juego Registrada Correctamente")
                listaJuegosRepo.append([nombreJuego,stockJuego])
    
    print("\n------------ Listas de Datos ya Procesados -----------------------\n")

    print("\n-------------- MejoresClientes ---------------\n")
    for i in listaMejoresClientesRepo:
        print(i)
    print("\n-------------- JuegosMasVendidos ---------------\n")
    for i in listaJuegosMasVendidoRepo:
        print(i)
    print("\n-------------- Clasificaciónes ---------------\n")
    for i in listaClasificacionRepo:
        print(i)
    print("\n-------------- Cumpleañeros ---------------\n")
    for i in listaCumpleañerosRepo:
        print(i)
    print("\n-------------- listaJugos ---------------\n")
    for i in listaJuegosRepo:
        print(i)
    


        

                
    context={'ReporteData':strxml_ReportesFrontend}
    return render(request,'Reportes.html',context)

def verXmlReporte(request):
    global xml_ReportesFrontend
    print(xml_ReportesFrontend)
    return redirect('Reportes')
    