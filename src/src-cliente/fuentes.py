# -*- coding: iso-8859-15 -*-

# ------------------------------------------------ #
# Hontza - Vigilancia tecnológica                  #
# Versión: 0.5                                     #
# ------------------------------------------------ #
# Módulo: fuentes.py                               #
# Contiene: Clase Fuentes                          #
#                                                  #
# Autores:                                         #
#          Karlos G. Liberal (karlos@investic.net) #
#          Unai Garcés (ugarces@gmail.com)         #
# ------------------------------------------------ #
# La licencia de este programa es GPL.             #
# ------------------------------------------------ #

import gtk
import gobject

class Fuentes:
	
	def __init__(self, mainGlade, db):
		self.fuentes = mainGlade.get_widget("fuentes")
		self.lst_categoria = mainGlade.get_widget("lst_categorias2")
		self.lst_fuente = mainGlade.get_widget("lst_fuentes")
		self.aceptar = mainGlade.get_widget("btn_fuentes_aceptar")
		self.db = db
		self.abierta = False
		
		self.lst_categoria.connect("cursor-changed", self.on_categoria_cambio)
		self.aceptar.connect("clicked", self.ocultar)
		
		self.mdl_categoria = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
		self.lst_categoria.set_model(self.mdl_categoria)
		self.lst_categoria.set_headers_visible(False)
		self.renderer = gtk.CellRendererText()
		self.columna = gtk.TreeViewColumn("", self.renderer, text = 1)
		self.lst_categoria.append_column(self.columna)
		
		self.mdl_fuente = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
		self.lst_fuente.set_model(self.mdl_fuente)
		self.lst_fuente.set_headers_visible(False)
		self.renderer = gtk.CellRendererToggle()
		self.renderer.set_property("activatable", True)
		self.renderer.connect("toggled", self.on_fuente_seleccion)
		self.columna = gtk.TreeViewColumn("", self.renderer, active = 1)
		self.lst_fuente.append_column(self.columna)
		self.renderer = gtk.CellRendererText()
		self.columna = gtk.TreeViewColumn("", self.renderer, text = 2)
		self.lst_fuente.append_column(self.columna)
		return
		
	def mostrar(self):
		self.mdl_categoria.clear()
		resultado = self.db.sql("SELECT id, nombre FROM categorias WHERE activa = 1")
		if resultado == []:
			return False
		for elemento in resultado:
			self.mdl_categoria.append([elemento[0], elemento[1]])
		self.pinta()
		resultado = self.db.sql("SELECT id FROM categorias WHERE seleccion = 1")
		if resultado == []:
			self.db.sql("UPDATE categorias SET seleccion = 1 WHERE id = 1")
			self.set_seleccion(1)
		else:
			self.set_seleccion(resultado[0][0])
		self.lst_categoria.emit("cursor-changed")
		self.fuentes.show()
		self.abierta = True
		return True
		
	def get_seleccion(self):
		seleccion, iterador = self.lst_categoria.get_selection().get_selected()
		if iterador == None:
			return False
		retorno = seleccion.get_value(iterador, 0)
		return retorno
	
	def set_seleccion(self, id_categoria):
		iterador = 0
		while 1:
			if self.mdl_categoria.get_value(self.mdl_categoria.get_iter((iterador,)), 0) == id_categoria:
				break
			iterador += 1
		self.lst_categoria.get_selection().select_iter(self.mdl_categoria.get_iter((iterador,)))
		return

	def on_categoria_cambio(self, widget):
		self.mdl_fuente.clear()
		self.pinta()
		return
		
	def pinta(self):
		resultado = self.db.sql("SELECT id, seleccion, nombre FROM fuentes WHERE activa = 1 and id_categoria = %d" % self.get_seleccion())
		if resultado == []:
			return False
		for elemento in resultado:
			self.mdl_fuente.append([elemento[0], elemento[1], elemento[2]])
		return True
		
	def on_fuente_seleccion(self, celda, ruta):
		self.mdl_fuente[ruta][1] = not self.mdl_fuente[ruta][1]
		self.db.sql("UPDATE fuentes SET seleccion = %d WHERE id = %d" % (self.mdl_fuente[ruta][1], self.mdl_fuente[ruta][0]))
		return

	def ocultar(self, widget):
		self.fuentes.hide()
		self.abierta = False
		return
		