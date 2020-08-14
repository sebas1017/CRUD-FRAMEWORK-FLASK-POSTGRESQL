# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 01:49:56 2020

@author: sebastian
"""

group_by ="""	
	
	select
	count(*) as cantidad_facturas ,
	id_cliente as cedula,
	d.nombre_cliente as nombre_cliente,
	sum(val_total) as valor_total,
	cod_factura as codigo_factura
from
	facturas a ,
	detalle_factura b ,
	productos c,
	clientes d
where
	a.cod_factura = b.id_factura
	and b.id_producto = c.cod_prod
	and a.id_cliente = d.cedula
group by
	id_cliente ,
	d.nombre_cliente ,
	val_total ,
	cod_factura
order by 1 
	
	"""