# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 01:18:13 2020

@author: sebastian
"""

import psycopg2
from parametros_conexion import config
parametros = config()

def borrado_producto(id_producto):
    try:
       connection = psycopg2.connect(parametros)
       cursor = connection.cursor()
       
       borrado_querie = 'delete from productos where cod_prod =  {id_producto}'.format(id_producto = id_producto)
       cursor.execute(borrado_querie)
       connection.commit()
       count = cursor.rowcount
       if count >0:
           print("SE ELIMINO CORRECTAMENTE EL PRODUCTO")
           return "SE ELIMINO CORRECTAMENTE EL PRODUCTO"
     
        
    except (Exception, psycopg2.Error) as error :
        if(connection):
            error_mensaje = "Failed to DELETE record into mobile table", error
            print("Failed to insert record into mobile table", error)
            return error_mensaje
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL CONEXION FINALIZADA")

