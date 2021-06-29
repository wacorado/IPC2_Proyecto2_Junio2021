from flask import *
import xml.etree.ElementTree as ET
from flask.wrappers import Request
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
    # clientes=[]
    # mejoresClientes=[]
    # juegos=[]
    # juegosVendidos=[]
    # cantidadGastada=0
    str_Archivo= request.data.decode('UTF-8')
    strBkpReturn=request.data.decode('UTF-8')
    #print(str(str_Archivo))
    raiz = ET.fromstring(str_Archivo)


    for hijo in raiz:
        print("------------hijo.tag ------------------")
    #     if(hijo.tag()=="cliente")
    #     #print("---------------------"+hijo.tag+"--------------------------")
    #     if(hijo.tag == "cliente"):
    #         for subhijo in hijo:
    #             if(subhijo.tag=="nombre"):
    #                 nombre=subhijo.text
    #             elif(subhijo.tag=="apellido"):
    #                 apellido=subhijo.text
    #             elif(subhijo.tag=="edad"):
    #                 edad=subhijo.text
    #             elif(subhijo.tag=="fechaCumpleaños"):
    #                 cumpleFecha=subhijo.text
    #             elif(subhijo.tag=="cantidadGastada"):
    #                 cantidadGastada=subhijo.text
    #         clientes.append([nombre,apellido,edad,cumpleFecha,cantidadGastada])
    #         print("Cliente Guardado Correctamente")
        
    #     elif(hijo.tag=="mejoresClientes"):
    #         for subhijo in hijo:
    #             if(subhijo.tag=="nombre"):
    #                 nombre=subhijo.text
    #             elif(subhijo.tag=="fechaUltimaCompra"):
    #                 fechaUltimaC=subhijo.text
    #             elif (subhijo.tag=="cantidadComprada"):
    #                 cantComprada=subhijo.text
    #             elif(subhijo.tag=="cantidadGastada"):
    #                 cantidadGastada=subhijo.text
    #         mejoresClientes.append([nombre, fechaUltimaC, cantComprada, cantidadGastada])
    #         print("Mejor Cliente Guardado Correctamente")
        
    #     elif(hijo.tag=="juegos"):
    #         for subhijo in hijo:
    #             if(subhijo.tag=="nombre"):
    #                 nombre=subhijo.text
    #             elif(subhijo.tag=="plataforma"):
    #                 plataforma=subhijo.text
    #             elif(subhijo.tag=="añoLanzamiento"):
    #                 yearLanzamiento=subhijo.text
    #             elif(subhijo.tag=="clasificacion"):
    #                 clasificacion=subhijo.text
    #             elif (subhijo.tag=="stock"):
    #                 stock=subhijo.text
    #         juegos.append([nombre,plataforma,yearLanzamiento,clasificacion,stock])
    #         print("Juego Guardado Exitosamente")
        
    #     elif(hijo.tag=="juegosMasVendidos"):
    #         for subhijo in hijo:
    #             if(subhijo.tag=="nombre"):
    #                 nombre=subhijo.text
    #             elif(subhijo.tag=="fechaUltimaCompra"):
    #                 fechUltimaC=subhijo.text
    #             elif(subhijo.tag=="copiasVendidas"):
    #                 copiVendid=subhijo.text
    #             elif(subhijo.tag=="stock"):
    #                 stock=subhijo.text
    #         juegosVendidos.append([nombre,fechUltimaC,copiVendid,stock])
    #         print("Juego Mas Vendido Guardado Exitosamente")

    # print("------------------------ Registro Completo Exito ----------------------------------------------")

    # for i in clientes:
    #     print(i)
    # print("###################### CLIENTES #######################")


    # for i in mejoresClientes:
    #     print(i)
    # print("###################### MEJORES CLIENTES #######################")

    # for i in juegos:
    #     print(i)
    # print("###################### JUEGOS #######################")

    # for i in juegosVendidos:
    #     print(i)
    # print("###################### MEJORES JUEGOS #######################")

    return Response(status=200)

@app.route('/returnXMLCompleto', methods = ['GET'])
def return_XML():
    global strBkpReturn
    #print(str(strBkpReturn))    
    return strBkpReturn

if __name__ == '__main__':
    app.run(debug=True)
