# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 23:47:38 2020

@author: sebastian
"""


import psycopg2
from parametros_conexion import config
parametros = config()

def registro_productos(codigo_producto,categoria_producto,nombre_producto,precio_producto,stock_producto,estado_producto):
    try:
       connection = psycopg2.connect(parametros)
       cursor = connection.cursor()
       postgres_insert_query = """ insert into productos (cod_prod, categoria,nombre ,precio ,cantidad_bodega ,estado  ) VALUES (%s,%s,%s,%s,%s,%s)"""
       record_to_insert = (codigo_producto,categoria_producto,nombre_producto,precio_producto,stock_producto,estado_producto)
       cursor.execute(postgres_insert_query, record_to_insert)
       connection.commit()
       resultado ="PRODUCTO REGISTRADO CORRECTAMENTE"
       return resultado
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





def registro_facturas(id_cliente ,cantidad_productos ,fecha_compra ,val_total,metodo_pago):
    try:
       connection = psycopg2.connect(parametros)
       cursor = connection.cursor()
       postgres_insert_query = """  
   insert into facturas (id_cliente ,cantidad_productos ,fecha_compra ,val_total,metodo_pago )
   VALUES (%s,%s,%s,%s,%s)RETURNING cast(cod_factura as integer);"""
       record_to_insert = (id_cliente ,cantidad_productos ,fecha_compra ,val_total,metodo_pago)
       cursor.execute(postgres_insert_query ,record_to_insert)
       result=cursor.fetchone()
       result =result[0]
       print(result)
       connection.commit()
       return str(result)
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

def registro_detalle_facturas(id_factura , productos):
    try:
       connection = psycopg2.connect(parametros)
       cursor = connection.cursor()
       values = "values({id_factura},".format(id_factura=int(id_factura))
       querie ="insert into detalle_factura (id_factura , id_producto ) "+values+"unnest(string_to_array('{productos}', ',')::int[]));".format(productos=str(productos))   
       print(querie)
       cursor.execute(querie)
       connection.commit()
       resultado ="PRODUCTOS DEL CLIENTE INSERTADOS EN LA FACTURA"
       return resultado
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

