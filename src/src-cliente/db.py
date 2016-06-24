# -*- coding: iso-8859-15 -*-

# ------------------------------------------------ #
# Hontza - Vigilancia tecnológica                  #
# Versión: 0.5                                     #
# ------------------------------------------------ #
# Módulo: db.py                                    #
# Contiene: Clase Db                               #
#                                                  #
# Autores:                                         #
#          Karlos G. Liberal (karlos@investic.net) #
#          Unai Garcés (ugarces@gmail.com)         #
# ------------------------------------------------ #
# La licencia de este programa es GPL.             #
# ------------------------------------------------ #

from pysqlite2 import dbapi2 as sqlite

class Db:
	
	def __init__(self, nombre):
		self.nombre_db = nombre
		return
	
	def sql(self, datos):
		conexion = sqlite.connect(self.nombre_db)
		cursor = conexion.cursor()
		cursor.execute(datos)
		conexion.commit()
		retorno = cursor.fetchall()
		conexion.close()
		return retorno
		
	def sql_una(self, datos):
		retorno = self.sql(datos)
		return retorno[0]

	def inicializa(self, datos):
		conexion = sqlite.connect(self.nombre_db)
		cursor = conexion.cursor()
		for elemento in datos:
			cursor.execute(elemento)
			conexion.commit()
			cursor.fetchall()
		conexion.close()
		return

