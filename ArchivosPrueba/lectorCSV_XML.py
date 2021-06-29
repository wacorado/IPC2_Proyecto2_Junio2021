from tkinter.constants import TRUE
from tkinter.filedialog import askopenfilename
import csv
import re
from xml.dom import minidom

lista1Clientes=[]
listaPosErrores=[]
listaElimErroresClientes=[]

def cargarArchivo():
    global lista1Client 
    archivo = askopenfilename()#Abre la interfaz para escoger el archivo a cargar
    print(archivo)#se obtiene el URL
    file = open ("ReporteErores.txt","w")


    #Se abre el archivo
    with open(archivo) as csvfile:
        reader = csv.reader(csvfile, delimiter=";",)
        for row in reader:
            lista1Clientes.append(row)
            print(row)
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
                        listaPosErrores.append(x)
                    else:
                        print("Nombre de Cliente Valido")
                if(y==1):
                    apellido=str(lista1Clientes[x][y])
                    apellidoValid=re.search(r'[^a-zA-Z\s\á\é\í\ó\ú]+?',apellido)
                    if(apellidoValid):
                        print("Error en apellido del Cliente")
                        file.write("Error en Apellido: "+apellido+ " Registro #: "+str(x+1)+"\n")
                        listaPosErrores.append(x)
                    else:
                        print("Apellido de Cliente Valido")
                if(y==2):
                    edad=str(lista1Clientes[x][y])
                    edadValid=re.search(r'[^0-9\s]+?',edad)
                    if(edadValid):
                        print("Error en edad del Cliente")
                        file.write("Error en edad: "+edad+ " Registro #: "+str(x+1)+"\n")
                        listaPosErrores.append(x)
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
                        listaPosErrores.append(x)
                if(y==4):
                    fechaUltCompra=str(lista1Clientes[x][y])
                    fechaUltCompraValid=re.search(r'^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$',fechaUltCompra)
                    if(fechaUltCompraValid):
                        print("Fecha de Ultima Compra Valida")
                    else:
                        print("Error en Formato Fecha de Ultima Compra")
                        file.write("Error en formato Fecha: "+fechaNac+" Registro #: "+str(x+1)+"\n")
                        listaPosErrores.append(x)
        listTemp=set(listaPosErrores)
        for i in listTemp:
            print(i)
            lista1Clientes.pop(int(i))             
        print("\n --------------- DepuraCion de Archivo Clientes -------------------------\n")

        for i in lista1Clientes:
            print(i)

    #Escribo el XML los Clientes
    document=minidom.Document()
    root=document.createElement('Chet')
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
    xml_file = root.toprettyxml(indent='\t', encoding='utf-8')
    xmlFinal=open("XmlFinal.xml","w")
    xmlFinal.write(str(xmlFinal))
    xmlFinal.close()

    #print (xml_file)
    return xml_file


cargarArchivo()