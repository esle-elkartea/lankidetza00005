# -*- coding: iso-8859-15 -*-

# ------------------------------------------------ #
# Hontza - Vigilancia tecnológica                  #
# Versión: 0.5                                     #
# ------------------------------------------------ #
# Módulo: tre_busquedas.py                         #
# Contiene: Clase Tre_busquedas                    #
#                                                  #
# Autores:                                         #
#          Karlos G. Liberal (karlos@investic.net) #
#          Unai Garcés (ugarces@gmail.com)         #
# ------------------------------------------------ #
# La licencia de este programa es GPL.             #
# ------------------------------------------------ #

import gtk
import gobject
from iconos import Iconos

iconos = Iconos()

class Tre_busquedas:
	
	def __init__(self, mainGlade, db):
		self.db = db
		self.arbol = mainGlade.get_widget("tre_busquedas")
		self.menu = mainGlade.get_widget("mnu_carpetas")
		self.nueva = mainGlade.get_widget("mnu_carpetas_nueva")
		self.renombrar = mainGlade.get_widget("mnu_carpetas_renombrar")
		self.borrar = mainGlade.get_widget("mnu_carpetas_borrar")
		self.ventana_renombrar = mainGlade.get_widget("renombrar")
		self.txt_renombrar = mainGlade.get_widget("txt_renombrar")
		
		self.arbol.connect("row-expanded", self.on_row_expanded)
		self.arbol.connect("row-collapsed", self.on_row_collapsed)
		self.arbol.connect("event", self.menu_mostrar)
		
		self.nueva.connect("activate", self.carpeta_nueva)
		self.renombrar.connect("activate", self.mostrar_renombrar)
		self.borrar.connect("activate", self.carpeta_borrar)
		self.txt_renombrar.connect("activate", self.renombra)
		
		self.modelo = gtk.TreeStore(gobject.TYPE_INT, gtk.gdk.Pixbuf, gtk.gdk.Pixbuf, gobject.TYPE_STRING)
		self.arbol.set_model(self.modelo)
		self.arbol.set_headers_visible(False)
		self.arbol.set_reorderable(False)
		
		self.columna = gtk.TreeViewColumn()
		self.arbol.append_column(self.columna)
		
		self.renderer = gtk.CellRendererPixbuf()
		self.columna.pack_start(self.renderer, expand = False)
		self.columna.add_attribute(self.renderer, "pixbuf", 1)
		self.columna.add_attribute(self.renderer, "pixbuf-expander-open", 2)
		
		self.renderer = gtk.CellRendererText()
		self.columna.pack_start(self.renderer, expand = True)
		self.columna.add_attribute(self.renderer, "text", 3)
		
		self.renderer.set_property("editable", False)
		return
		
	def mostrar(self):
		self.modelo.clear()
		self.bucle_arbol(None, 0)
		self.arbol.show()
		
		self.recorre_arbol(self.modelo)
		
		return
		
	def bucle_arbol(self, padre, depende):
		resultado = self.db.sql("SELECT id, nombre, abierta FROM carpetas WHERE pertenece = %d" % depende)
		if resultado == []:
			return
		for elemento in resultado:
			hijo = self.modelo.append(padre, [elemento[0], iconos.carpeta_cerrada, iconos.carpeta_abierta, elemento[1]])
			self.bucle_arbol(hijo, elemento[0])
		return
		
	def recorre_arbol(self, linea):
		for elemento in linea:
			if self.db.sql_una("SELECT abierta FROM carpetas WHERE id = %d" % elemento[0])[0] == True:
				self.arbol.expand_row(elemento.path, False)
			if elemento.iterchildren() != None:
				self.recorre_arbol(elemento.iterchildren())
			else:
				return
		return
		
	def on_row_expanded(self, treeview, treeiter, path):
		self.db.sql("UPDATE carpetas SET abierta = 1 WHERE id = %d" % self.get_seleccion())
		self.recorre_arbol(self.modelo)
		return
		
	def on_row_collapsed(self, treeview, treeiter, path):
		self.db.sql("UPDATE carpetas SET abierta = 0 WHERE id = %d" % self.get_seleccion())
		return
	
	def get_seleccion(self):
		seleccion, iterador = self.arbol.get_selection().get_selected()
		if iterador == None:
			return 0
		retorno = seleccion.get_value(iterador, 0)
		return retorno
		
	def set_seleccion(self, seleccion = 0):
		if seleccion == 0:
			self.arbol.get_selection().select_iter(self.modelo.get_iter((0,)))
		else:
			self.recorre_arbol_seleccion(self.modelo, seleccion)
		self.arbol.emit("cursor-changed")
		return
		
	def recorre_arbol_seleccion(self, linea, seleccion):
		for elemento in linea:
			if elemento[0] == seleccion:
				self.arbol.get_selection().select_iter(elemento.iter)
			if elemento.iterchildren() != None:
				self.recorre_arbol_seleccion(elemento.iterchildren(), seleccion)
			else:
				return
		return
	
	def menu_mostrar(self, widget, event):
		try:
			posx = event.x
		except:
			return
		if self.arbol.get_path_at_pos(int(event.x), int(event.y)) == None:
			return
		if event.type == gtk.gdk.BUTTON_PRESS:
			self.arbol.get_selection().select_path(self.arbol.get_path_at_pos(int(event.x), int(event.y))[0])
		if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
			if self.get_seleccion() == 1:
				self.borrar.set_property("sensitive", False)
				self.renombrar.set_property("sensitive", False)
			else:
				self.borrar.set_property("sensitive", True)
				self.renombrar.set_property("sensitive", True)
			self.menu.popup(None, None, None, event.button, event.time)
		return
		
	def carpeta_nueva(self, widget):
		sel = self.get_seleccion()
		self.db.sql("INSERT INTO carpetas (nombre, abierta, pertenece) VALUES ('Nueva carpeta', 1, %d)" % sel)
		self.mostrar()
		self.set_seleccion(sel)
		return
		
	def carpeta_borrar(self, widget):
		id_carpeta = self.get_seleccion()
		self.bucle_borrar(id_carpeta)
		self.mostrar()
		self.set_seleccion()
		return
		
	def bucle_borrar(self, id_carpeta):
		carpetas = self.db.sql("SELECT id FROM carpetas WHERE pertenece = %d" % id_carpeta)
		if carpetas != []:
			for carpeta in carpetas:
				self.bucle_borrar(carpeta[0])
		busquedas = self.db.sql("SELECT id FROM busquedas WHERE id_carpeta = %d" % id_carpeta)
		for busqueda in busquedas:
			self.db.sql("DELETE FROM resultados WHERE id_busqueda = %d" % busqueda[0])
			self.db.sql("DELETE FROM busquedas WHERE id = %d" % busqueda[0])
		self.db.sql("DELETE FROM carpetas WHERE id = %d" % id_carpeta)
		return

	def mostrar_renombrar(self, widget):
		texto = self.db.sql_una("SELECT nombre FROM carpetas WHERE id = %d" % self.get_seleccion())[0]
		self.txt_renombrar.set_text(texto)
		self.txt_renombrar.select_region(0, len(texto))
		self.ventana_renombrar.show()
		return
		
	def renombra(self, widget):
		seleccion = self.get_seleccion()
		self.db.sql("UPDATE carpetas SET nombre = '%s' WHERE id = %d" % (self.txt_renombrar.get_text(), self.get_seleccion()))
		self.ventana_renombrar.hide()
		self.mostrar()
		self.set_seleccion(seleccion)
		return
		