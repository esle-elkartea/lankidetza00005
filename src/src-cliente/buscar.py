# -*- coding: iso-8859-15 -*-

# ------------------------------------------------ #
# Hontza - Vigilancia tecnológica                  #
# Versión: 0.5                                     #
# ------------------------------------------------ #
# Módulo: buscar.py                                #
# Contiene: Clase Buscar                           #
#                                                  #
# Autores:                                         #
#          Karlos G. Liberal (karlos@investic.net) #
#          Unai Garcés (ugarces@gmail.com)         #
# ------------------------------------------------ #
# La licencia de este programa es GPL.             #
# ------------------------------------------------ #

class Buscar:
	
	def __init__(self, mainGlade):
		self.txt_buscar = mainGlade.get_widget("txt_buscar")
		self.btn_buscar = mainGlade.get_widget("btn_buscar")
		self.radio_and = mainGlade.get_widget("radio_and")
		self.radio_or = mainGlade.get_widget("radio_or")
		self.radio_fe = mainGlade.get_widget("radio_fe")
		#ventana de nuevas busquedas
		
		self.ventana_combo = mainGlade.get_widget("combo_nuevas_busquedas")
		self.ventana_txt_buscar = mainGlade.get_widget("txt_nuevas_busquedas")
		self.ventana_btn_buscar = mainGlade.get_widget("btn_nuevas_busquedas_buscar")
		self.ventana_radio_and = mainGlade.get_widget("radio_nuevas_busquedas_and")
		self.ventana_radio_or = mainGlade.get_widget("radio_nuevas_busquedas_or")
		self.ventana_radio_fe = mainGlade.get_widget("radio_nuevas_busquedas_fe")
		
		
		self.radio_and.connect("toggled", self.on_radio_toggled, "and")
		self.radio_or.connect("toggled", self.on_radio_toggled, "or")
		self.radio_fe.connect("toggled", self.on_radio_toggled, "fe")

		self.ventana_radio_and.connect("toggled", self.on_radio_toggled, "and")
		self.ventana_radio_or.connect("toggled", self.on_radio_toggled, "or")
		self.ventana_radio_fe.connect("toggled", self.on_radio_toggled, "fe")
		
		
		self.tipo_busqueda = "and"
		return
		
	def on_radio_toggled(self, widget, datos):
		if widget.get_active():
			self.tipo_busqueda = datos
		return
		
	def mostrar_tipo_busqueda(self, op_fe, op_and, op_or):
		self.radio_fe.set_property("sensitive", op_fe)
		self.radio_or.set_property("sensitive", op_or)
		self.radio_and.set_property("sensitive", op_and)
		self.radio_fe.set_property("active", op_fe)
		self.radio_or.set_property("active", op_or)
		self.radio_and.set_property("active", op_and)
		return
		
	def mostrar_tipo_busqueda_ventana(self, op_fe, op_and, op_or):
		self.ventana_radio_fe.set_property("sensitive", op_fe)
		self.ventana_radio_or.set_property("sensitive", op_or)
		self.ventana_radio_and.set_property("sensitive", op_and)
		self.ventana_radio_fe.set_property("active", op_fe)
		self.ventana_radio_or.set_property("active", op_or)
		self.ventana_radio_and.set_property("active", op_and)
		return
		