# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 09:56:25 2020

@author: sebastian
"""
import psycopg2
from parametros_conexion import config
parametros = config()
estado = "ACTIVO"
estado2 ="INACTIVO"
def active_product(codigo_producto):
    
    try:
       connection = psycopg2.connect(parametros)
       cursor = connection.cursor()
       cadena = "and cod_prod = {codigo_producto}".format(codigo_producto = codigo_producto)
       
       print("ENTRE EN ACTIVAR")
       postgreSQL_select_Query ="update productos   set estado = '{estado}' where estado = 'INACTIVO'".format(estado=estado)+" "+cadena
       
       cursor.execute(postgreSQL_select_Query)
       connection.commit()
       return "SE ACTIVO EL PRODUCTO"      
    
    except (Exception, psycopg2.Error) as error :
        return error
        print ("Error while fetching data from PostgreSQL", error)
    
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            
            
            

def inactive_product(codigo_product1):       
    try:
       connection = psycopg2.connect(parametros)
       cursor = connection.cursor()
       cadena = "and cod_prod = {codigo_producto}".format(codigo_producto = codigo_product1)
       query ="update productos   set estado = '{estado2}' where estado = 'ACTIVO'".format(estado2=estado2)+" "+cadena    
       print("ENTRE EN DESACTIVAR")    
       print(query)
       cursor.execute(query)
       connection.commit()
       return("SE DESACTIVO EL PRODUCTO")       
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
        return error
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")   

         