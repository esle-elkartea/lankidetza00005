# -*- coding: iso-8859-15 -*-

# ------------------------------------------------ #
# Hontza - Vigilancia tecnológica                  #
# Versión: 0.5                                     #
# ------------------------------------------------ #
# Módulo: conexion.py                              #
# Contiene: Clase Conexion                         #
#                                                  #
# Autores:                                         #
#          Karlos G. Liberal (karlos@investic.net) #
#          Unai Garcés (ugarces@gmail.com)         #
# ------------------------------------------------ #
# La licencia de este programa es GPL.             #
# ------------------------------------------------ #

from SOAPpy import WSDL

class Conexion:
	
	def __init__(self, db):
		self.db = db
		return
	
	def inicializa(self):
		url_servidor = self.db.sql_una("SELECT servidor FROM configuracion")[0]
		try:
			self.servidor = WSDL.Proxy(url_servidor)
		except:
			return False
		return True
	
	def getFuentes(self):
		id_cliente = self.db.sql_una("SELECT id_cliente FROM configuracion")[0]
		try:
			self.fuentes = self.servidor.getFuentes(id_cliente)
		except:
			return False
		if self.fuentes == [] or self.fuentes == None:
			return False
		self.db.sql("UPDATE fuentes SET activa=0")
		self.db.sql("UPDATE categorias SET activa=0")
		for elemento in self.fuentes:
			op_fe = 0
			op_and = 0
			op_or = 0
			if elemento[4].count("fe"):
				op_fe = 1
			if elemento[4].count("and"):
				op_and = 1
			if elemento[4].count("or"):
				op_or = 1
			if self.db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id=%s" % elemento[0])[0] == 0:
				self.db.sql("INSERT INTO fuentes (id, nombre, op_fe, op_and, op_or, id_categoria) VALUES (%s, '%s', %d, %d, %d, %s)" % (elemento[0], elemento[1], op_fe, op_and, op_or, elemento[2]))
			else:
				self.db.sql("UPDATE fuentes SET op_fe = %d, op_and = %d, op_or = %d WHERE id = %s" % (op_fe, op_and, op_or, elemento[0]))
			
			if self.db.sql_una("SELECT COUNT(*) FROM categorias WHERE id=%s" % elemento[2])[0] == 0:
				self.db.sql("INSERT INTO categorias (id, nombre) VALUES (%s, '%s')" % (elemento[2], elemento[3]))
			self.db.sql("UPDATE fuentes SET activa=1 WHERE id=%s" % elemento[0])
			self.db.sql("UPDATE categorias SET activa=1 WHERE id=%s" % elemento[2])
		return True
		
	def lanzarBusqueda(self, texto, tipo_busqueda, fuentes):
		id_cliente = self.db.sql_una("SELECT id_cliente FROM configuracion")[0]
		resultados = self.servidor.lanzarBusqueda(id_cliente, texto, tipo_busqueda, fuentes)
		return resultados
		