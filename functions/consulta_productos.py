# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 00:52:44 2020

@author: sebastian
"""


import psycopg2
from parametros_conexion import config
parametros = config()

def consulta_productos():

    try:
       connection = psycopg2.connect(parametros)
       cursor = connection.cursor()
       estado = 'ACTIVO'
       postgreSQL_select_Query = "select * from productos where estado = '{estado}';".format(estado=estado)
       cursor.execute(postgreSQL_select_Query)
       print("Selecting rows from mobile table using cursor.fetchall")
       mobile_records = cursor.fetchall() 
       if len(mobile_records)>0:
           
           return mobile_records
       else:
           return "NO EXISTEN CLIENTES EN EL SISTEMA"
    
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            