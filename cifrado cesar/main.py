# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 02:07:00 2020

@author: sebastian
"""

#!/usr/bin/python 
# -*- coding: utf-8 -*- 
from descifrado_cesar import descifrar
def cifrar(desplazamiento, texto):
    texto_cifrado = ""
    for caracter in texto:
        texto_cifrado = texto_cifrado + chr(ord(caracter) + desplazamiento)
    return texto_cifrado
 
texto_original = input("ingrese el mensaje a encriptar :").upper()
desplazamiento = int(input("ingrese el desplazamiento :"))
print("\n")
texto_cifrado = cifrar(desplazamiento, texto_original)
print ("El Texto Cifrado para su desplazamiento es: " + texto_cifrado)
print("Con el valor encriptado llamaremos la funcion que desencripta el mensaje \n")
print("le daremos como argumento el mensaje cifrado y el desplazamiento con el que fue encriptado\n ")
print("EJECUTANDO FUNCION DE DESCIFRADO....")
print("EL MENSAJE ORIGINAL FUE :")
descifrar(texto_cifrado,desplazamiento)
