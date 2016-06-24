# -*- coding: iso-8859-15 -*-

# ------------------------------------------------ #
# Hontza - Vigilancia tecnológica                  #
# Versión: 0.5                                     #
# ------------------------------------------------ #
# Módulo: error.py                                 #
# Contiene: Clase Error                            #
#                                                  #
# Autores:                                         #
#          Karlos G. Liberal (karlos@investic.net) #
#          Unai Garcés (ugarces@gmail.com)         #
# ------------------------------------------------ #
# La licencia de este programa es GPL.             #
# ------------------------------------------------ #

import gtk

class Error:

	def __init__(self, mainGlade):
		self.error = mainGlade.get_widget("error")
		self.lbl_error = mainGlade.get_widget("lbl_error")
		self.btn_cerrar_error = mainGlade.get_widget("btn_cerrar_error")
		self.btn_configuracion = mainGlade.get_widget("btn_configuracion")
		
		self.error.connect("delete_event", self.on_cerrar)
		self.btn_cerrar_error.connect("clicked", self.on_btn_cerrar_error)
		self.btn_configuracion.connect("clicked", self.on_btn_configuracion)
		self.abierta = False
		self.configuracion = False
		self.cerrar = False
		return
		
	def mostrar(self, texto, config = 0, salir = 0):
		self.salir = salir
		self.lbl_error.set_text(texto)
		if config == 1:
			self.btn_configuracion.show()
			self.configuracion = True
		else:
			self.btn_configuracion.hide()
			self.configuracion = False
		self.error.show()
		self.abierta = True
		return
		
	def on_btn_cerrar_error(self, widget):
		if self.salir == 1:
			self.cerrar = True
		else:
			self.cerrar = False
		self.error.hide()
		self.abierta = False
		return

	def on_btn_configuracion(self, widget):
		self.error.hide()
		self.abierta = False
		self.configuracion = True
		return

	def on_cerrar(self, widget, data):
		return True
		