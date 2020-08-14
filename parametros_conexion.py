# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 19:40:17 2020

@author: sebastian
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 00:09:46 2020

@author: sebastian
"""
def config():
    # Crear el parser y leer el archivo
   f = open ('config.txt','r')
   mensaje = f.read()
   f.close()
   mensaje = str(mensaje)
   return mensaje





