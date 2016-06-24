# -*- coding: iso-8859-15 -*-

# ------------------------------------------------ #
# Hontza - Vigilancia tecnológica                  #
# Versión: 0.5                                     #
# ------------------------------------------------ #
# Módulo: lst_resultados.py                        #
# Contiene: Clase Lst_resultados                   #
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
import urllib
import re
import md5
import codecs
from iconos import Iconos

iconos = Iconos()

class Lst_resultados:
	
	def __init__(self, mainGlade, db):
		self.lista = mainGlade.get_widget("lst_resultados")
		# glade menu resultados
		self.menu = mainGlade.get_widget("mnu_resultados")
		self.guardar_pagina = mainGlade.get_widget("busqueda_guardar")
		self.ventana_notas = mainGlade.get_widget("notas")
		self.texto_notas = mainGlade.get_widget("txt_notas")
		self.abrir = mainGlade.get_widget("mnu_resultados_abrir")
		self.guardar_pagina_como = mainGlade.get_widget("mnu_resultados_guardar_pagina_como1")
		self.notas = mainGlade.get_widget("mnu_resultados_notas")
		self.borrar = mainGlade.get_widget("mnu_resultados_borrar")
		self.ayuda = mainGlade.get_widget("mnu_resultados_ayuda")

		self.lista.connect("event", self.menu_mostrar)
		self.abrir.connect("activate", self.menu_abrir)
		
		self.notas.connect("activate", self.abrir_notas)
		self.texto_notas.connect("activate", self.texto_guardar_notas)
		
		self.guardar_pagina_como.connect("activate", self.abrir_guardar_pagina)
		self.db = db
		
		#self.lista.connect("event", self.on_event)
		
		self.modelo = gtk.ListStore(gobject.TYPE_INT, gtk.gdk.Pixbuf, gobject.TYPE_STRING)
		self.lista.set_model(self.modelo)
		self.lista.set_headers_visible(False)
		self.renderer = gtk.CellRendererPixbuf()
		self.columna = gtk.TreeViewColumn("", self.renderer, pixbuf = 1)
		self.lista.append_column(self.columna)
		self.renderer = gtk.CellRendererText()
		self.columna = gtk.TreeViewColumn("", self.renderer, markup = 2)
		self.lista.append_column(self.columna)
		return

	def mostrar(self, id_busqueda = 0):
		self.modelo.clear()
		if id_busqueda != 0:
			resultado = self.db.sql("SELECT id, titulo, texto, enlace, id_busqueda, id_fuente, nota, icono FROM resultados WHERE id_busqueda = %d" % id_busqueda)
			for elemento in resultado:
				titulo = self.colorea(self.cambia_caracteres(elemento[1]), elemento[4])
				texto = self.colorea(self.cambia_caracteres(elemento[2]), elemento[4])
				if elemento[7] == 0:
					icono = iconos.no_actualizado
				else:
					icono = iconos.actualizado
				self.modelo.append([elemento[0], icono, "<span weight='bold'>%s</span>\n%s\nNotas: <span foreground='#AAAAAA'>%s</span>\n<span foreground='blue' underline='single'>%s</span> <span foreground='gray'>(%s)</span>" % (self.cambia_caracteres(titulo), self.cambia_caracteres(texto), elemento[6], elemento[3].replace("&","&amp;"), elemento[5])])
		return
	
	def cambia_caracteres(self, texto):
		texto = texto.replace("&amp;", "&")
		texto = texto.replace("&acute;", "\'")
		texto = texto.replace("&aacute;", u"á")
		texto = texto.replace("&eacute;", u"é")
		texto = texto.replace("&iacute;", u"í")
		texto = texto.replace("&oacute;", u"ó")
		texto = texto.replace("&uacute;", u"ú")
		texto = texto.replace("&ntilde;", u"ñ")
		texto = texto.replace("&Ntilde;", u"Ñ")
		texto = texto.replace("&#225;",u"á")
		texto = texto.replace("&#233;",u"é")
		texto = texto.replace("&#237;",u"í")
		texto = texto.replace("&#243;",u"ó")
		texto = texto.replace("&#250;",u"ú")
		texto = texto.replace("&#324;",u"ñ")
		texto = texto.replace("&#209;",u"Ñ")
		texto = texto.replace("&", "&amp;")
		return texto
		
	def get_seleccion(self):
		seleccion, iterador = self.lista.get_selection().get_selected()
		if iterador == None:
			return 0
		retorno = seleccion.get_value(iterador, 0)
		return retorno
		
	def add_elemento(self, id_busqueda, resultados, fuente):
		for elemento in resultados:
			for i in range(6):
				elemento[i] = elemento[i].replace("'", "&acute;")
			self.db.sql("INSERT INTO resultados (titulo, texto, enlace, id_fuente, idioma, id_busqueda, fecha) VALUES ('%s', '%s', '%s', '%s', '%s', %d, '%s')" % (elemento[0], elemento[2], elemento[1], elemento[4], elemento[5], fuente, elemento[3]))
		self.mostrar(id_busqueda)
		return

	def del_elemento(self, id_busqueda):
		sel = self.get_seleccion()
		busqueda = self.db.sql_una("SELECT id_busqueda FROM resultados WHERE id = %d" %sel)[0]
		self.db.sql("DELETE FROM resultados WHERE id = %d" % sel)
		num_res = self.db.sql_una("SELECT COUNT(*) FROM resultados WHERE id_busqueda = %d" % busqueda)[0]
		self.db.sql("UPDATE busquedas SET num_resultados = %d WHERE id = %d" % (num_res, busqueda))
		self.mostrar(busqueda)
		return

	def colorea(self, texto, busqueda):
		resultado = self.db.sql_una("SELECT texto FROM busquedas WHERE id = %d" % busqueda)[0]
		texto = texto.replace("<", "&lt;")
		palabras_clave = resultado.split(" ")
		palabras_texto = texto.split(" ")
		texto_final = []
		for elemento in palabras_texto:
			color = False
			for palabra in palabras_clave:
				pal = palabra
				ele = elemento
				for puntuacion in list(u"¡!/()=?¿<>,.-;:_[]+*\"'"):
					pal = pal.replace(puntuacion, "")
					ele = ele.replace(puntuacion, "")
				if self.quitar_acentos(pal.lower()) == self.quitar_acentos(ele.lower()):
					color = True
			if color:
				texto_final.append(elemento.replace(elemento, "<span foreground='#FF0000'><b>%s</b></span>" % elemento))
			else:
				texto_final.append(elemento)
		return " ".join(texto_final)
		
	def quitar_acentos(self, texto):
		texto = texto.replace(u"á", "a")
		texto = texto.replace(u"é", "e")
		texto = texto.replace(u"í", "i")
		texto = texto.replace(u"ó", "o")
		texto = texto.replace(u"ú", "u")
		return texto
		
	def limpia(self):
		self.modelo.clear()
		return

	def on_event(self, widget, event):
		try:
			posx = event.x
		except:
			return
		if self.lista.get_path_at_pos(int(event.x), int(event.y)) == None:
			return
		if event.type == gtk.gdk.BUTTON_PRESS:
			self.lista.get_selection().select_path(self.lista.get_path_at_pos(int(event.x), int(event.y))[0])
		if event.type == gtk.gdk._2BUTTON_PRESS and event.button == 1:
			webbrowser.open(self.db.sql_una("SELECT enlace FROM resultados WHERE id = %d" % self.get_seleccion())[0])
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
		if event.type == gtk.gdk._2BUTTON_PRESS and event.button == 1:
			webbrowser.open(self.db.sql_una("SELECT enlace FROM resultados WHERE id = %d" % self.get_seleccion())[0])
		return

	def menu_abrir(self, widget):
			webbrowser.open(self.db.sql_una("SELECT enlace FROM resultados WHERE id = %d" % self.get_seleccion())[0])
			return

	def descargar_pagina(self, url_envio, nombre):
		URL = self.db.sql_una("SELECT enlace FROM resultados WHERE id = %d" % self.get_seleccion())[0]
		try:
			url = urllib.FancyURLopener().open(URL)
		except:
			return False
	
		web = url.readlines()
		url.close()
		fichero = codecs.open(nombre, encoding = "iso-8859-15", mode = "w")
		codigo = []
		for linea in web:
			linea = unicode(linea, "iso-8859-15")
			img = re.compile("(<[I i][M m][G g].*?>)", re.DOTALL)
			imagen = img.findall(linea)
			if imagen != []:
				recorte = re.compile("([S s][R r][C c]=\".*?\")", re.DOTALL)
				direccion = recorte.findall(imagen[0])
				if direccion != []:
					if direccion[0][5:9] != "http":
						if direccion[0][5] != "/":
							linea = linea.replace(direccion[0][0:5], direccion[0][0:5] + URL + "/")
						else:
							linea = linea.replace(direccion[0][0:5], direccion[0][0:5] + URL)
			link = re.compile("(<[A a].*?>)", re.DOTALL)
			enlace = link.findall(linea)
			if enlace != []:
				recorte = re.compile("([H h][R r][E e][F f]=\".*?\")", re.DOTALL)
				direccion = recorte.findall(enlace[0])
				if direccion != []:
					if direccion[0][6:10] != "http":
						if direccion[0][6] != "/":
							linea = linea.replace(direccion[0][0:6], direccion[0][0:6] + URL + "/")
						else:
							linea = linea.replace(direccion[0][0:6], direccion[0][0:6] + URL)
			codigo.append(linea)
		fichero.write("".join(codigo))
		fichero.close()
		
	def abrir_guardar_pagina(self, widget):
		self.guardar_pagina.set_default_response(gtk.RESPONSE_OK)
		#self.guardar_pagina.set_current_folder("C:\\")
		response = self.guardar_pagina.run()
		if response == gtk.RESPONSE_OK:
			if self.guardar_pagina.get_filename()[-5:] != ".html":
				nombre = self.guardar_pagina.get_filename()+".html"
			else:
				nombre = self.guardar_pagina.get_filename()
			self.descargar_pagina(self, nombre)
		self.guardar_pagina.hide()

	def abrir_notas(self, widget):
		texto = self.db.sql_una("SELECT nota FROM resultados WHERE id = %d" % self.get_seleccion())[0]
		if texto == None:
			texto = ""
		self.texto_notas.set_text(texto)
		self.texto_notas.select_region(0, len(texto))
		self.ventana_notas.show()
		return
	
	def texto_guardar_notas(self, widget):
		
		self.db.sql("UPDATE resultados SET nota= '%s' WHERE id = %d" % (self.texto_notas.get_text(), self.get_seleccion()))
		self.ventana_notas.hide()
		self.mostrar(self.db.sql("SELECT id_busqueda FROM resultados WHERE id = %d" % self.get_seleccion())[0])
				
		return
		
	def actualizar(self, id_busqueda, nuevos):
		checksum = ""
		resultado = self.db.sql("SELECT id, enlace, checksum FROM resultados WHERE id_busqueda = %d" % id_busqueda)
		for elemento in resultado:
			cambio = True
			for linea in nuevos:
				if elemento[1] == linea[1]:
					checksum = md5.new(linea[0] + linea[2]).hexdigest()
					if elemento[2] == "" or elemento[2] == checksum:
						cambio = False
						break
			if cambio:
				self.db.sql("UPDATE resultados SET icono = 1, checksum = '%s' WHERE id = %d" % (checksum, elemento[0]))
			else:
				self.db.sql("UPDATE resultados SET icono = 0, checksum = '%s' WHERE id = %d" % (checksum, elemento[0]))
		self.mostrar(id_busqueda)
		return
