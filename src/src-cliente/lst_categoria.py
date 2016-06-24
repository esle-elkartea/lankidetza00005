# -*- coding: iso-8859-15 -*-

# ------------------------------------------------ #
# Hontza - Vigilancia tecnológica                  #
# Versión: 0.5                                     #
# ------------------------------------------------ #
# Módulo: lst_categorias.py                        #
# Contiene: Clase Lst_categorias                   #
#                                                  #
# Autores:                                         #
#          Karlos G. Liberal (karlos@investic.net) #
#          Unai Garcés (ugarces@gmail.com)         #
# ------------------------------------------------ #
# La licencia de este programa es GPL.             #
# ------------------------------------------------ #

import gtk
import gobject

class Lst_categoria:
	
	def __init__(self, mainGlade, db):
		self.lista = mainGlade.get_widget("lst_categoria")

		self.menu = mainGlade.get_widget("mnu_categoria")
		self.seleccionar_fuentes = mainGlade.get_widget("mnu_categoria_seleccionar_fuentes")
		self.ayuda = mainGlade.get_widget("mnu_categoria_ayuda")
		
		self.lista.connect("event", self.menu_mostrar)
		self.db = db
		
		self.modelo = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
		self.lista.set_model(self.modelo)
		self.lista.set_headers_visible(False)
		self.renderer = gtk.CellRendererText()
		self.columna = gtk.TreeViewColumn("", self.renderer, text = 1)
		self.lista.append_column(self.columna)
		return
		
	def mostrar(self):
		self.modelo.clear()
		resultado = self.db.sql("SELECT id, nombre FROM categorias WHERE activa = 1")
		if resultado == []:
			return False
		for elemento in resultado:
			self.modelo.append([elemento[0], elemento[1]])
		resultado = self.db.sql("SELECT id FROM categorias WHERE seleccion = 1")
		if resultado == []:
			self.db.sql("UPDATE categorias SET seleccion = 1 WHERE id = 1")
			self.set_seleccion(1)
		else:
			self.set_seleccion(resultado[0][0])
		return True
		
	def get_seleccion(self):
		seleccion, iterador = self.lista.get_selection().get_selected()
		if iterador == None:
			return False
		retorno = seleccion.get_value(iterador, 0)
		return retorno
		
	def set_seleccion(self, id_categoria):
		iterador = 0
		while 1:
			if self.modelo.get_value(self.modelo.get_iter((iterador,)), 0) == id_categoria:
				break
			iterador += 1
		self.lista.get_selection().select_iter(self.modelo.get_iter((iterador,)))
		self.lista.emit("cursor-changed")
		return

	def menu_mostrar(self, widget, event):
		try:
			posx = event.x
		except:
			return
		if self.lista.get_path_at_pos(int(event.x), int(event.y)) == None:
			return
		if event.type == gtk.gdk.BUTTON_PRESS:
			self.lista.get_selection().select_path(self.lista.get_path_at_pos(int(event.x), int(event.y))[0])
		if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
			self.menu.popup(None, None, None, event.button, event.time)
		return
		

