# -*- coding: iso-8859-15 -*-

# ------------------------------------------------ #
# Hontza - Vigilancia tecnológica                  #
# Versión: 0.5                                     #
# ------------------------------------------------ #
# Módulo: lst_busquedas.py                         #
# Contiene: Clase Lst_busquedas                    #
#                                                  #
# Autores:                                         #
#          Karlos G. Liberal (karlos@investic.net) #
#          Unai Garcés (ugarces@gmail.com)         #
# ------------------------------------------------ #
# La licencia de este programa es GPL.             #
# ------------------------------------------------ #

import gtk
import gobject
import webbrowser
import os
import sys
from iconos import Iconos

iconos = Iconos()

class Lst_busquedas:
	
	def __init__(self, mainGlade, db):
		self.lista = mainGlade.get_widget("lst_busquedas")
		self.guardar_pagina = mainGlade.get_widget("busqueda_guardar")
		self.ventana_buscar = mainGlade.get_widget("nuevas_busquedas")
		#glade menu busqueda
		self.menu = mainGlade.get_widget("mnu_busqueda")
		self.nueva = mainGlade.get_widget("mnu_busqueda_nueva")
		self.navegar = mainGlade.get_widget("mnu_busqueda_navegar")
		self.menu_guardar_pagina = mainGlade.get_widget("mnu_busqueda_guardar_pagina")
		self.duplicar = mainGlade.get_widget("mnu_busqueda_duplicar")
		self.actualizar = mainGlade.get_widget("mnu_busqueda_actualizar")
		self.analizar = mainGlade.get_widget("mnu_busqueda_analizar_vinculos")
		self.borrar = mainGlade.get_widget("mnu_busqueda_borrar")
		self.ayuda = mainGlade.get_widget("mnu_busqueda_ayuda")

		self.lista.connect("event", self.menu_mostrar)
		self.navegar.connect("activate", self.on_navegar, "tmp.html")
		self.menu_guardar_pagina.connect("activate", self.abrir_guardar_pagina)

		self.db = db
		
		self.modelo = gtk.ListStore(gobject.TYPE_INT, gtk.gdk.Pixbuf, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)
		self.lista.set_model(self.modelo)
		self.lista.set_headers_visible(False)
		self.renderer = gtk.CellRendererPixbuf()
		self.columna = gtk.TreeViewColumn("", self.renderer, pixbuf = 1)
		self.lista.append_column(self.columna)
		self.renderer = gtk.CellRendererText()
		for i in range(2,5):
			self.columna = gtk.TreeViewColumn("", self.renderer, markup = i)
			self.lista.append_column(self.columna)
		return
		
	def mostrar(self, id_carpeta = 0):
		self.modelo.clear()
		if id_carpeta != 0:
			resultado = self.db.sql("SELECT id, texto, op_fe, op_and, op_or, num_resultados, fecha, id_categoria FROM busquedas WHERE id_carpeta = %d" % id_carpeta)
			for elemento in resultado:
				if elemento[2] == 1:
					tipo_busqueda = u"Búsqueda exacta"
				elif elemento[3] == 1:
					tipo_busqueda = "Todas las palabras"
				else:
					tipo_busqueda = "Cualquier palabra"
				categoria = self.db.sql_una("SELECT nombre FROM categorias WHERE id = %d" % elemento[7])[0]
				if len(categoria) > 40:
					categoria = categoria[:40] + "..."
				self.modelo.append([elemento[0], iconos.busqueda, u"<b>%s</b>\n<span foreground='blue'>%s</span>" % (elemento[1], categoria), "%s\n<span foreground='grey'>%s resultados</span>" % (tipo_busqueda, elemento[5]), "%s\n%s" % (elemento[6][:10], elemento[6][11:])])
			self.lista.show()
		while gtk.events_pending():
			gtk.main_iteration()
		self.lista.emit("cursor-changed")
		return
		
	def get_seleccion(self):
		seleccion, iterador = self.lista.get_selection().get_selected()
		if iterador == None:
			return 0
		retorno = seleccion.get_value(iterador, 0)
		return retorno
		
	def set_seleccion(self, id_busqueda):
		iterador = 0
		while 1:
			if self.modelo.get_value(self.modelo.get_iter((iterador,)), 0) == id_busqueda:
				break
			iterador += 1
		self.lista.get_selection().select_iter(self.modelo.get_iter((iterador,)))
		return
		
	def add_elemento(self, texto):
		if texto == "":
			return
		resultados = conexion.lanzarBusqueda(texto)
		op_fe = buscar.tipo_busqueda == "fe"
		op_and = buscar.tipo_busqueda == "and"
		op_or = buscar.tipo_busqueda == "or"
		self.db.sql("INSERT INTO busquedas (texto, op_fe, op_and, op_or, id_categoria, num_resultados, fecha, id_carpeta) VALUES ('%s', %d, %d, %d, %d, %d, '%s', %d)" % (texto, op_fe, op_and, op_or, lst_categorias.get_seleccion(), len(resultados), time.strftime("%d/%m/%Y %H:%M:%S"), tre_busquedas.get_seleccion()))
		id_busqueda = self.db.sql_una("SELECT id FROM busquedas ORDER BY id DESC")[0]
		self.mostrar(tre_busquedas.get_seleccion())
		self.set_seleccion(id_busqueda)
		self.lista.scroll_to_cell((len(self.modelo) - 1,))
		lst_resultados.add_elemento(id_busqueda, resultados)
		self.mostrar(tre_busquedas.get_seleccion())
		return
		
	def del_elemento(self, id_busqueda):
		sel = self.get_seleccion()
		carpeta = self.db.sql_una("SELECT id_carpeta FROM busquedas WHERE id = %d" % sel)[0]
		self.db.sql("DELETE FROM resultados WHERE id_busqueda = %d" % sel)
		self.db.sql("DELETE FROM busquedas WHERE id = %d" % sel)
		self.mostrar(carpeta)
		return

	def menu_mostrar(self, widget, event):
		if event.type == gtk.gdk.KEY_PRESS and event.keyval == 65535 and self.get_seleccion() != 0:
			self.del_elemento(self.get_seleccion())
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
	
	def on_navegar(self, widget, nombre):
		id_busqueda = self.get_seleccion()
		resultado = self.db.sql_una("SELECT texto, fecha, id_categoria, op_fe, op_and, op_or, num_resultados FROM busquedas WHERE id = %d" % id_busqueda)
		categoria = self.html(self.db.sql_una("SELECT nombre FROM categorias WHERE id = %d" % resultado[2])[0])
		if resultado[3]:
			tipo_busqueda = "B&uacute;squeda exacta"
		elif resultado[4]:
			tipo_busqueda = "Todas las palabras"
		else:
			tipo_busqueda = "Cualquier palabra"
		fichero = open(nombre, "w")
		fichero.write("<html>\n \
					   <head>\n \
					   <title>Resultados de la b&uacute;squeda</title>\n \
					   	   <style type='text/css'>\n \
 						    body {\n \
							 padding:0em 1em 0em 1em;\n \
							font-family: monospace;\n \
							background-color: #fff }\n \
 						   A:Link {\n \
								line-height: 23px;\n \
								 font-size:14px;\n \
								color:#516884;\n \
								 text-decoration: none; \n \
								font-weight: bold}\n \
 						   A:Visited {\n \
								 font-size:12px;\n \
								color:#516884; \n \
								text-decoration: none; \n \
								font-weight: bold;}\n \
 						   A:Hover {\n \
								text-decoration:underline;\n \
								 color:#203241}\n \
 						   h2 { \n \
								color:#005C76}\n \
						  tr { \n \
								color:#005C76}\n \
						table{ \n \
							border-spacing: 2px;\n \
							padding:1em 1em 1em 1em;\n \
							background-color:#ADD8E6;\n \
							}\n \
 						    </style>\n \
					   </head>\n \
					   <body>\n \
					   <table bgcolor='#76BF5F' align='center' width='100%%'>\n \
					   <tr><td colspan='2'><h2>Resultados de la b&uacute;squeda</h2></td></tr>\n \
					   <tr><td colspan='2'><hr /></td></tr>\n \
					   <tr><td><b>B&uacute;squeda:</b> %s</td><td><b>Fecha:</b> %s</td></tr>\n \
					   <tr><td><b>Categor&iacute;a:</b> %s</td><td><b>Tipo de b&uacute;squeda:</b> %s</td></tr>\n \
					   <tr><td><b>Resultados:</b> %d</td><td></td></tr>\n \
					   </table>\n" % (resultado[0], resultado[1], categoria, tipo_busqueda, resultado[6]))
		resultado = self.db.sql("SELECT titulo, texto, enlace, id_fuente FROM resultados WHERE id_busqueda = %d" % id_busqueda)
		for elemento in resultado:
			fichero.write("<a href='%s'><b>%s</b></a><br>\n \
						   %s<br>\n \
						   <a href='%s'>%s</a><br>\n \
						   Fuente: %s\n \
						   <hr />\n" % (elemento[2], self.html(elemento[0]), self.html(elemento[1]), elemento[2], elemento[2], self.html(elemento[3])))
		fichero.write("</body>\n \
					   </html>\n")
		fichero.close()
		#webbrowser.open("file:tmp.html") ruta completa para gnu/linux y mirar solución
		if nombre == "tmp.html":
			webbrowser.open("tmp.html")
		return
	
	def html(self, texto):
		texto = texto.replace(u"á", "&aacute;")
		texto = texto.replace(u"é", "&eacute;")
		texto = texto.replace(u"í", "&iacute;")
		texto = texto.replace(u"ó", "&oacute;")
		texto = texto.replace(u"ú", "&uacute;")
		texto = texto.replace(u"Á", "&Aacute;")
		texto = texto.replace(u"É", "&Eacute;")
		texto = texto.replace(u"Í", "&Iacute;")
		texto = texto.replace(u"Ó", "&Oacute;")
		texto = texto.replace(u"Ú", "&Uacute;")
		texto = texto.replace(u"ñ", "&ntilde;")
		texto = texto.replace(u"Ñ", "&Ntilde;")
		return texto
	
	def abrir_guardar_pagina(self, widget):
		self.guardar_pagina.set_default_response(gtk.RESPONSE_OK)
		response = self.guardar_pagina.run()
		if response == gtk.RESPONSE_OK:
			if self.guardar_pagina.get_filename() != "":
				if self.guardar_pagina.get_filename()[-5:] != ".html":
					nombre = self.guardar_pagina.get_filename()+".html"
				else:
					nombre = self.guardar_pagina.get_filename()
			
				self.on_navegar(self, nombre)
		self.guardar_pagina.hide()
		
