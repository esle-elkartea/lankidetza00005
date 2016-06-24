# -*- coding: iso-8859-15 -*-

# ------------------------------------------------ #
# Hontza - Vigilancia tecnológica                  #
# Versión: 0.5                                     #
# ------------------------------------------------ #
# Módulo: configuracion.py                         #
# Contiene: Clase Configuracion                    #
#                                                  #
# Autores:                                         #
#          Karlos G. Liberal (karlos@investic.net) #
#          Unai Garcés (ugarces@gmail.com)         #
# ------------------------------------------------ #
# La licencia de este programa es GPL.             #
# ------------------------------------------------ #

class Configuracion:

	def __init__(self, mainGlade, db):
		self.db = db
		self.configuracion = mainGlade.get_widget("configuracion")
		self.txt_id = mainGlade.get_widget("txt_id")
		self.txt_servidor = mainGlade.get_widget("txt_servidor")
		self.btn_aceptar = mainGlade.get_widget("btn_configuracion_aceptar")
		self.btn_ayuda = mainGlade.get_widget("btn_configuracion_ayuda")
		
		self.configuracion.connect("delete_event", self.on_cerrar)
		self.btn_aceptar.connect("clicked", self.boton_aceptar)
		self.txt_id.connect("activate", self. boton_aceptar)
		self.txt_servidor.connect("activate", self.boton_aceptar)
		
		self.abierta = False
		return
	def on_cerrar(self, widget, data):
		return True
		
	def boton_aceptar(self, widget):
		if self.txt_id.get_text() == "":
			return
		if self.txt_servidor.get_text() == "":
			return
		self.db.sql("UPDATE configuracion SET id_cliente = '%s', servidor = '%s'" % (self.txt_id.get_text(), self.txt_servidor.get_text()))
		self.configuracion.hide()
		self.abierta = False
		return
		
	def mostrar(self):
		resultado = self.db.sql_una("SELECT id_cliente, servidor FROM configuracion")
		self.txt_id.set_text(resultado[0])
		self.txt_servidor.set_text(resultado[1])
		self.configuracion.show()
		self.abierta = True
		return
		