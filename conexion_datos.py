# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 22:04:12 2020

@author: sebastian
"""
import psycopg2
from parametros_conexion import config
parametros = config()

def conexion_base_datos(_cedula, _nombrecliente, _direccion,_telefono):
    try:
       connection = psycopg2.connect(parametros)
       cursor = connection.cursor()
       postgres_insert_query = """ insert into clientes (cedula ,nombre_cliente ,direccion ,telefono ) VALUES (%s,%s,%s,%s)"""
       record_to_insert = (_cedula, _nombrecliente, _direccion,_telefono)
       cursor.execute(postgres_insert_query, record_to_insert)
       connection.commit()
       return "CLIENTE REGISTRADO CORRECTAMENTE"
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error) 
            return error
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL CONEXION FINALIZADA")
