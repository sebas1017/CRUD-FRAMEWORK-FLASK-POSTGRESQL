from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from conexion_datos import conexion_base_datos
from functions.borrado_producto import borrado_producto
from functions.procedimiento_almacenado import stored_procedured,querie_to_dataframe
import pandas as pd
import json
import json2html
from flask_caching import Cache
from functions.consulta_productos import consulta_productos
from functions.registro_productos import registro_productos
from functions.active_inactive_products import active_product,inactive_product
from functions.registro_productos import registro_detalle_facturas,registro_facturas
from datetime import date
from functions.var_groupby import group_by

app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cars_api"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#aqui renderizamos el template de inicio en la ruta/ actual
#dentro del index.html se hace el llamado a los metodos siguientes los cuales cada uno retornan
#respuestas en distintos html dependiendo del metodo
@app.route('/')

def main():
    return render_template('index.html')
#---------------------------------------------------------------
@app.route('/consultarClientes')
def my_form_update():
    mensaje = "DIGITE S PARA VISUALIZAR LOS CLIENTES REGISTRADOS"
    return render_template("consultar.html",opcion1 = mensaje)

#se hace la carga del querie y se convierte los resultados en un objeto dataframe de pandas
#luego se parsea con json.loads para darle formato en la salida del html response
@app.route('/consultarClientes',methods=['POST'])
def my_form_update_post():
    text = request.form['text']
    querie ="select * from clientes;"
    if text != None:        
        datos_clientes =querie_to_dataframe(querie)
    if datos_clientes == "NO EXISTEN DATOS EN EL SISTEMA PARA ESTE MODULO":
        return render_template("volver.html")+datos_clientes
    
    else:
        df = pd.DataFrame(datos_clientes,columns=['Cedula_cliente', 'nombre_cliente', 'direccion','telefono'])
        result = df.to_json(orient="records")
        infoFromJson = json.loads(result)
        data_design = render_template("design_clientes.html")+"<P>INFORMACION DE CLIENTES</P>"
        data = json2html.json2html.convert(json = infoFromJson) +str(data_design)
        return data              
#-----------------------------------------------------------------------------
@app.route('/showDelete')
def my_form():
    return render_template('borrado.html')
#-----------------------------------------------------------------------------
# se ejecuta procedimiento almacenado para el borrado en cascada de clientes y facturas
#creando temporal de facturas para mayor seguridad
@app.route('/showDelete', methods=['POST'])
def my_form_post():
    text = request.form['text']
    if text !='':
        resultado = stored_procedured(text)
    else:
        resultado="INGRESE DATOS POR FAVOR"
    ruta ='/showDelete'
    template= render_template("volver.html",ruta = ruta)+"<P>{resultado}</P>".format(resultado =resultado)
    return template

#-----------------------------------------------------------------------------

@app.route('/consultClients')
def consultClients():
    mensaje ="DIGITE S PARA REGISTRAR CLIENTE"
    return render_template('registro_clientes.html',opcion1 =mensaje)
#-----------------------------------------------------------------------------
@app.route('/consultClients',methods=['POST','GET'])
def consultClients_post():
           print("AQUI LEO LOS DATOS CON EL METODO REQUEST Y OBTENGO LOS CAMPOS")
           _cedula = request.form['inputCedula']
           _nombrecliente = request.form['inputNombre_cliente']
           _direccion = request.form['inputDireccion']  
           _telefono = request.form['inputTelefono']
           opcion = request.form['text']
       # LLAMO LA FUNCION QUE REALIZA EL INSERT        
           if opcion !='' :
                proceso_final =conexion_base_datos(_cedula, _nombrecliente, _direccion,_telefono)
           if proceso_final !="CLIENTE REGISTRADO CORRECTAMENTE" :
               return proceso_final+render_template("volver.html")
           else:
               ruta = "/consultClients"  
               home = render_template("volver.html",ruta=ruta)
               return  "<p>{RESULTADO}</p>".format(RESULTADO =proceso_final)+home
##----------------------------------------------------------------------------

@app.route('/registerProducts')
def registerProducts():
    return render_template('formulario_productos.html')

@app.route('/registerProducts',methods=['POST','GET'])
def registerProducts_post():
        codigo_producto = request.form['codigo_producto']
        categoria_producto = request.form['categoria_producto']
        nombre_producto = request.form['nombre_producto']
        precio_producto = request.form['precio_producto']
        stock_producto = request.form['stock_producto']
        estado_producto = request.form['estado_producto']
        estado_producto = estado_producto.upper()
        process =registro_productos(codigo_producto,categoria_producto,nombre_producto,precio_producto,stock_producto,estado_producto)
        back_page = registerProducts()
        return back_page + " <p>{process}</p>".format(process =process)   
##-------------------------------------------------------------------------
@app.route('/showProducts')
def showProducts():
    mensaje = "SI DESEA MOSTRAR INFORMACION DE LOS PRODUCTOS ACTUALES DIGITE S"
    return render_template('consultar.html',opcion1 = mensaje)
#-------------------------------------------------------------------------
@app.route('/showProducts',methods=['POST','GET'])
def showProducts_post():
    datos_producto =consulta_productos()
    df = pd.DataFrame(datos_producto,columns=['CODIGO_PRODUCTO', 'CATEGORIA', 'NOMBRE_PRODUCTO','PRECIO','STOCK_DISPONIBLE','ESTADO'])
    result = df.to_json(orient="records")
    infoFromJson = json.loads(result)
    mensaje = "INFORMACION DE LOS PRODUCTOS ACTUALES"
    data_design = render_template("design_clientes.html",opcion1 = mensaje)
    data = json2html.json2html.convert(json = infoFromJson) +str(data_design)
    return data
#-----------------------------------------------------------------------------
@app.route('/deleteProducts')
def deleteProducts():
    return render_template('borrado_productos.html')
#-----------------------------------------------------------------------------
@app.route('/deleteProducts', methods=['POST'])
def deleteProducts_post():
    text = request.form['text']
    proceso = borrado_producto(text)
    resultado = render_template("delete.html",resultado =proceso)    
    return resultado 

#-----------------------------------------------------------------------------
@app.route('/inactiveProducts')
def inactiveProducts():
    return render_template('inactive_products.html')
#-----------------------------------------------------------------------------
@app.route('/inactiveProducts', methods=['POST'])
def inactiveProducts_post():
   opcion = request.form['opcion']
   opcion = str(opcion)
   codigo_producto = request.form['codigo_producto']
   if opcion == "1":
      resultado =active_product(codigo_producto)
   elif opcion =="2":
      resultado=inactive_product(codigo_producto)
   ruta ="inactiveProducts"   
   home =render_template("volver.html",ruta =ruta)   
   return resultado + home
#----------------------------------------------------------------------------
@app.route('/consultarProductosinactivos')
def consultarProductosinactivos():
    mensaje = "DIGITE S PARA VER LOS PRODUCTOS DESACTIVADOS"
    return render_template("consultar.html",opcion1 = mensaje)

#------------------------------------------------------------------------------
@app.route('/consultarProductosinactivos',methods=['POST'])
def consultarProductosinactivos_post():
    text = request.form['text']
    estado = 'INACTIVO'
    postgreSQL_select_Query = "select * from productos where estado = '{estado}';".format(estado=estado)
    if text != None: 
        productos_inactivos =querie_to_dataframe(postgreSQL_select_Query)
    if productos_inactivos == "NO EXISTEN DATOS EN EL SISTEMA PARA ESTE MODULO":
        return render_template("volver.html")+productos_inactivos
    else:
        df = pd.DataFrame(productos_inactivos,columns=['CODIGO_PRODUCTO', 'CATEGORIA', 'NOMBRE_PRODUCTO','PRECIO','STOCK_DISPONIBLE','ESTADO'])
        result = df.to_json(orient="records")
        infoFromJson = json.loads(result)
        mensaje = "INFORMACION DE LOS PRODUCTOS INACTIVOS"
        data_design = render_template("design_products_inactive.html",opcion1 = mensaje)
        data = json2html.json2html.convert(json = infoFromJson) +str(data_design)
        return data

@app.route('/registerFacture')
def registerFacture():
    return render_template('registro_facturas.html')
@app.route('/registerFacture',methods=['POST','GET'])
def registerFacture_post():
    today = date.today()
    d1 = today.strftime("%Y/%d/%m")
    inputCedula = request.form["inputCedula"]
    inputCantidad_productos= request.form["inputCantidad_productos"]
    inputFecha_compra = d1
    inputValortotal= request.form["inputValortotal"]
    inputMetodo_pago= request.form["inputMetodo_pago"]
    inputProductos = request.form["inputProductos"]
    id_incrementable=registro_facturas(inputCedula ,inputCantidad_productos ,inputFecha_compra ,inputValortotal,inputMetodo_pago)
    resultado_final =registro_detalle_facturas(id_incrementable , inputProductos)
    return resultado_final + render_template("volver.html")
@app.route('/showFacture')
def showFacture():
    mensaje = "SI DESEA MOSTRAR INFORMACION DE LAS FACTURAS ACTUALES DIGITE S"
    return render_template('consultar.html',opcion1 = mensaje)
#-------------------------------------------------------------------------
@app.route('/showFacture',methods=['POST','GET'])
def showFacture_post():
    text =request.form["text"]
    if text != None:
        records =querie_to_dataframe("SELECT * FROM FACTURAS;")
    if records == "NO EXISTEN DATOS EN EL SISTEMA PARA ESTE MODULO":
        return render_template("volver.html")+records
    else:
        df = pd.DataFrame(records,columns=['CODIGO_FACTURA', 'CEDULA_CLIENTE', 'CANTIDAD_PRODUCTOS','FECHA_COMPRA','VALOR_TOTAL','METODO_PAGO'])        
        result = df.to_json(orient="records",date_format='iso')
        infoFromJson = json.loads(result)
        mensaje = "INFORMACION DE LAS FACTURAS ACTUALES"
        data_design = render_template("design_products_inactive.html",opcion1 = mensaje)
        data = json2html.json2html.convert(json = infoFromJson) +str(data_design)
        return data    
#-----------------------------------------------------------------------------
@app.route('/showFacture_temporary')
def showFacture_temporary():
    mensaje = "SI DESEA MOSTRAR INFORMACION DE LAS FACTURAS ELIMINADAS DIGITE S"
    return render_template('consultar.html',opcion1 = mensaje)
#-------------------------------------------------------------------------
@app.route('/showFacture_temporary',methods=['POST','GET'])
def showFacture_temporary_post():
    text =request.form["text"]
    if text != '':
       data_temporary= querie_to_dataframe("SELECT * FROM temporal.facturas_borradas;")
    if data_temporary == "NO EXISTEN DATOS EN EL SISTEMA PARA ESTE MODULO":
        return render_template("volver.html")+data_temporary
    else:
        df = pd.DataFrame(data_temporary,columns=['CODIGO_FACTURA', 'CEDULA_CLIENTE', 'CANTIDAD_PRODUCTOS','FECHA_COMPRA','VALOR_TOTAL','METODO_PAGO'])
        result = df.to_json(orient="records")
        infoFromJson = json.loads(result)
        mensaje = "INFORMACION DE LAS FACTURAS ELIMINADAS"
        data_design = render_template("design_products_inactive.html",opcion1 = mensaje)
        data = json2html.json2html.convert(json = infoFromJson) +str(data_design)
        return data     
@app.route('/showFacture_client')
def showFacture_client():
    mensaje = "SI DESEA MOSTRAR INFORMACION DE LAS FACTURAS POR CLIENTE DIGITE S"
    return render_template('consultar.html',opcion1 = mensaje)
#-------------------------------------------------------------------------
@app.route('/showFacture_client',methods=['POST','GET'])
def showFacture_client_post():
    text = request.form["text"]
    if text != '':
        resultado =querie_to_dataframe(group_by)
        if resultado == "NO EXISTEN DATOS EN EL SISTEMA PARA ESTE MODULO":
            return render_template("volver.html")+resultado
        else:
             df = pd.DataFrame(resultado,columns=['cantidad_facturas', 'cedula', 'nombre_cliente','valor_total','codigo_factura'])
             result = df.to_json(orient="records")
             infoFromJson = json.loads(result)
             mensaje = "INFORMACION DE LAS FACTURAS POR CLIENTE"
             data_design = render_template("design_products_inactive.html",opcion1 = mensaje)
             data = json2html.json2html.convert(json = infoFromJson) +str(data_design)
             return data        
    else:
        return render_template("volver.html")+"INGRESE DATOS POR FAVOR"
if __name__ == "__main__":
    #app.debug = True
    cache.init_app(app)
    app.run(port=5002)
