# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:54:09 2020

@author: sebastian
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 11:19:41 2020

@author: sebastian
"""

import psycopg2
from parametros_conexion import config
parametros = config()

def querie_to_dataframe(querie):
    try:
       querie = "select * from clientes;"
       connection = psycopg2.connect(parametros)
       cursor = connection.cursor()
       postgreSQL_select_Query =querie  
       cursor.execute(postgreSQL_select_Query)
       print("Selecting rows from mobile table using cursor.fetchall")
       mobile_records = cursor.fetchall() 
       
      
       if len(mobile_records)>0: 
           return mobile_records
       else:
           return "NO EXISTEN DATOS EN EL SISTEMA PARA ESTE MODULO"
    
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        