#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# ------------------------------------------------ #
# Hontza - Vigilancia tecnológica                  #
# Versión: 0.5                                     #
# ------------------------------------------------ #
# Módulo: hontza.py                                #
# Contiene: Clase Principal                        #
#           Arranque de la aplicación              #
#                                                  #
# Autores:                                         #
#          Karlos G. Liberal (karlos@investic.net) #
#          Unai Garcés (ugarces@gmail.com)         #
# ------------------------------------------------ #
# La licencia de este programa es GPL.             #
# ------------------------------------------------ #

# Módulos de python
import pygtk
import gtk
import gtk.glade
import gobject
import time
import os.path
import webbrowser
import codecs

# Módulos propios
from lst_categoria import Lst_categoria
from tre_busquedas import Tre_busquedas
from lst_busquedas import Lst_busquedas
from lst_resultados import Lst_resultados
from buscar import Buscar
from conexion import Conexion
from fuentes import Fuentes
from configuracion import Configuracion
from splash import Splash
from error import Error
from db import Db
from status import Status

class Principal:

	def __init__(self):
		# <Elementos de la ventana> ------------------------------------
		self.principal = mainGlade.get_widget("principal")
		self.lst_categorias = Lst_categoria(mainGlade, db)
		self.tre_busquedas = Tre_busquedas(mainGlade, db)
		self.lst_busquedas = Lst_busquedas(mainGlade, db)
		self.lst_resultados = Lst_resultados(mainGlade, db)
		self.buscar = Buscar(mainGlade)
		self.acerca_de = mainGlade.get_widget("acerca_de")
		self.btn_acerca_de = mainGlade.get_widget("boton_cerrar_acerca_de")
		self.animacion = mainGlade.get_widget("animacion")
		self.animacion.set_from_file("hontza_espera.gif")
		self.animacion.show()
		
		self.principal.connect("delete_event", gtk.main_quit)
		self.lst_categorias.lista.connect("cursor-changed", self.lst_categorias_cambio)
		self.tre_busquedas.arbol.connect("cursor-changed", self.tre_busquedas_cambio)
		self.lst_busquedas.lista.connect("cursor-changed", self.lst_busquedas_cambio)
		self.buscar.btn_buscar.connect("clicked", self.on_btn_buscar)
		self.buscar.txt_buscar.connect("activate", self.on_btn_buscar)
		self.buscar.ventana_btn_buscar.connect("clicked", self.on_ventana_btn_buscar)
		self.buscar.ventana_txt_buscar.connect("activate", self.on_ventana_btn_buscar)
		
		self.lst_busquedas.lista.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, [("mover", 0, 0)], gtk.gdk.ACTION_MOVE)
		self.tre_busquedas.arbol.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, [("ordenar", 0, 1)], gtk.gdk.ACTION_MOVE)
		self.tre_busquedas.arbol.enable_model_drag_dest([("mover", 0, 0), ("ordenar", 0, 1)], gtk.gdk.ACTION_MOVE)
		self.tre_busquedas.arbol.connect("drag_data_received", self.on_dragdata_received)
		# </Elementos de la ventana> -----------------------------------
		
		# <Menús> ------------------------------------------------------
		self.mnu_archivo_importar = mainGlade.get_widget("importar")
		self.mnu_archivo_exportar = mainGlade.get_widget("exportar")
		self.mnu_archivo_crear_copia = mainGlade.get_widget("crear_copia")
		self.mnu_archivo_restaurar_copia = mainGlade.get_widget("restaurar_copia")
		self.mnu_archivo_salir = mainGlade.get_widget("mnu_archivo_salir")
		
		self.mnu_categorias_seleccionar_fuentes = mainGlade.get_widget("mnu_categorias_seleccionar_fuentes")
		
		self.mnu_busquedas_nueva_busqueda = mainGlade.get_widget("mnu_busquedas_nueva_busqueda")
		self.mnu_busquedas_navegar = mainGlade.get_widget("mnu_busquedas_navegar")
		self.mnu_busquedas_guardar_pagina = mainGlade.get_widget("guarda_pagina_como")
		self.mnu_busquedas_duplicar = mainGlade.get_widget("mnu_busquedas_duplicar")
		self.mnu_busquedas_actualizar = mainGlade.get_widget("mnu_busquedas_actualizar")
		self.mnu_busquedas_analizar_vinculos = mainGlade.get_widget("mnu_busquedas_analizar_vinculos")
		
		self.mnu_herramientas_configuracion = mainGlade.get_widget("mnu_herramientas_configuracion")
		
		self.mnu_ayuda_acerca_de = mainGlade.get_widget("mnu_ayuda_acerca_de")
		
		self.mnu_archivo_importar.connect("activate", self.abrir_importar)
		self.mnu_archivo_exportar.connect("activate", self.abrir_exportar)
		self.mnu_archivo_crear_copia.connect("activate", self.crear_copia)
		self.mnu_archivo_restaurar_copia.connect("activate", self.restaurar_copia)
		self.mnu_archivo_salir.connect("activate", gtk.main_quit)
		
		self.mnu_categorias_seleccionar_fuentes.connect("activate", self.mnu_herramientas_fuentes_abrir)
		
		self.mnu_busquedas_nueva_busqueda.connect("activate", self.abrir_ventana_buscar)
		self.mnu_busquedas_navegar.connect("activate", self.lst_busquedas.on_navegar, "tmp.html")
		self.mnu_busquedas_guardar_pagina.connect("activate", self.lst_busquedas.abrir_guardar_pagina)
		self.mnu_busquedas_duplicar.connect("activate", self.duplicar)
		self.mnu_busquedas_actualizar.connect("activate", self.actualizar_resultados)
		self.mnu_busquedas_analizar_vinculos.connect("activate", self.analizar)
		
		self.mnu_herramientas_configuracion.connect("activate", self.mnu_herramientas_configuracion_abrir)
		
		self.mnu_ayuda_acerca_de.connect("activate", self.acerca)
		# </Menús> -----------------------------------------------------
		
		# <Barra de herramientas> --------------------------------------
		self.her_importar = mainGlade.get_widget("her_importar")
		self.her_exportar = mainGlade.get_widget("her_exportar")
		self.her_seleccionar_fuentes = mainGlade.get_widget("her_seleccionar_fuentes")
		self.her_nueva_busqueda = mainGlade.get_widget("her_nueva_busqueda")
		self.her_navegar = mainGlade.get_widget("her_navegar")
		self.her_actualizar = mainGlade.get_widget("her_actualizar")
		self.her_analizar = mainGlade.get_widget("her_analizar")
		self.her_acerca_de = mainGlade.get_widget("her_acerca_de")
		
		self.her_importar.connect("clicked", self.abrir_importar)
		self.her_exportar.connect("clicked", self.abrir_exportar)
		self.her_seleccionar_fuentes.connect("clicked", self.mnu_herramientas_fuentes_abrir)
		self.her_nueva_busqueda.connect("clicked", self.abrir_ventana_buscar)
		self.her_navegar.connect("clicked", self.lst_busquedas.on_navegar, "tmp.html")
		self.her_actualizar.connect("clicked", self.actualizar_resultados)
		self.her_analizar.connect("clicked", self.analizar)
		self.her_acerca_de.connect("clicked", self.acerca)
		# </Barra de herramientas> -------------------------------------
		
		# <Elementos externos> -----------------------------------------
		self.guardar = mainGlade.get_widget("busqueda_guardar")
		self.abrir = mainGlade.get_widget("abrir")
		self.lst_categorias.seleccionar_fuentes.connect("activate", self.mnu_herramientas_fuentes_abrir)
		self.lst_busquedas.borrar.connect("activate", self.borrar_busqueda)
		self.lst_resultados.borrar.connect("activate", self.borrar_resultados)
		self.lst_busquedas.actualizar.connect("activate", self.actualizar_resultados)
		self.lst_busquedas.analizar.connect("activate", self.analizar)
		self.lst_busquedas.duplicar.connect("activate", self.duplicar)
		self.lst_busquedas.nueva.connect("activate", self.abrir_ventana_buscar)
		self.btn_acerca_de.connect("clicked", self.acerca_de_cerrar)

		#combo de la ventana nuevas busquedas	
		self.buscar.ventana_combo.set_model(self.lst_categorias.modelo)
		self.buscar.ventana_combo.set_text_column(1)
		self.lst_busquedas.ventana_buscar.connect("delete_event", self.no_cerrar)
		self.buscar.ventana_combo.connect("changed", self.combo_cambio)
		# </Elementos externos> ----------------------------------------
		
		# <Ayudas> -----------------------------------------------------
		self.btn_configuracion_ayuda = mainGlade.get_widget("btn_configuracion_ayuda")
		self.mnu_ayuda_ayuda = mainGlade.get_widget("mnu_ayuda_ayuda")
		self.mnu_carpeta_ayuda = mainGlade.get_widget("mnu_carpeta_ayuda")
		self.mnu_busqueda_ayuda = mainGlade.get_widget("mnu_busqueda_ayuda")
		self.mnu_resultados_ayuda = mainGlade.get_widget("mnu_resultados_ayuda")
		self.mnu_categoria_ayuda = mainGlade.get_widget("mnu_categoria_ayuda")
		
		self.btn_configuracion_ayuda.connect("clicked", self.ayuda, "configuracion.html")
		self.mnu_ayuda_ayuda.connect("activate", self.ayuda)
		self.mnu_carpeta_ayuda.connect("activate", self.ayuda, "carpetas.html")
		self.mnu_busqueda_ayuda.connect("activate", self.ayuda, "busquedas.html")
		self.mnu_resultados_ayuda.connect("activate", self.ayuda, "resultados.html")
		self.mnu_categoria_ayuda.connect("activate", self.ayuda, "categorias.html")
		# </Ayudas> ----------------------------------------------------
		
		return
	
	def mostrar(self):
		self.lst_categorias.mostrar()
		self.tre_busquedas.mostrar()
		self.tre_busquedas.set_seleccion()
		self.lst_busquedas.mostrar(self.tre_busquedas.get_seleccion())
		self.lst_resultados.mostrar(self.lst_busquedas.get_seleccion())
		
		self.principal.show()
		return
		
	def lst_categorias_cambio(self, widget):
		db.sql("UPDATE categorias SET seleccion = 0")
		db.sql("UPDATE categorias SET seleccion = 1 WHERE id = %d" % self.lst_categorias.get_seleccion())
		id_categoria = self.lst_categorias.get_seleccion()
		op_fe = db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id_categoria = %d AND op_fe = 1 AND seleccion = 1" % id_categoria)[0] == db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id_categoria = %d AND seleccion = 1" % id_categoria)[0] and db.sql_una("SELECT count(*) FROM fuentes WHERE id_categoria = %d" % id_categoria)[0] != 0
		op_and = db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id_categoria = %d AND op_and = 1 AND seleccion = 1" % id_categoria)[0] == db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id_categoria = %d AND seleccion = 1" % id_categoria)[0] and db.sql_una("SELECT count(*) FROM fuentes WHERE id_categoria = %d" % id_categoria)[0] != 0
		op_or = db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id_categoria = %d AND op_or = 1 AND seleccion = 1" % id_categoria)[0] == db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id_categoria = %d AND seleccion = 1" % id_categoria)[0] and db.sql_una("SELECT count(*) FROM fuentes WHERE id_categoria = %d" % id_categoria)[0] != 0
		if db.sql_una("SELECT COUNT(*) FROM fuentes WHERE seleccion = 1 AND activa = 1 AND id_categoria = %d" % id_categoria)[0] == 0:
			self.buscar.txt_buscar.set_property("sensitive", False)
			self.buscar.btn_buscar.set_property("sensitive", False)
			self.buscar.mostrar_tipo_busqueda(False, False, False)
		else:
			self.buscar.txt_buscar.set_property("sensitive", True)
			self.buscar.btn_buscar.set_property("sensitive", True)
			self.buscar.mostrar_tipo_busqueda(op_fe, op_and, op_or)
		return

	def tre_busquedas_cambio(self, widget):
		self.lst_busquedas.mostrar(self.tre_busquedas.get_seleccion())
		self.lst_resultados.mostrar(self.lst_busquedas.get_seleccion())
		return
		
	def lst_busquedas_cambio(self, widget):
 		self.lst_resultados.mostrar(self.lst_busquedas.get_seleccion())
		return
	
	def mnu_herramientas_configuracion_abrir(self, widget):
		status.mostrar(u"Configuración de la aplicación.")
		configuracion.mostrar()
		while configuracion.abierta:
			gtk.main_iteration()
		status.mostrar("Listo.")
		return
		
	def mnu_herramientas_fuentes_abrir(self, widget):
		status.mostrar(u"Seleccione las fuentes sobre las que se realizarán las búsquedas.")
		fuentes.mostrar()
		while fuentes.abierta:
			gtk.main_iteration()
		self.lst_categorias.lista.emit("cursor-changed")
		status.mostrar("Listo.")
		return
		
	def on_btn_buscar(self, widget):
		if self.buscar.txt_buscar.get_text() == "" or self.buscar.txt_buscar.get_text().isspace():
			self.buscar.txt_buscar.set_text("")
			return
		self.mostrar_animacion(1)
		status.mostrar("Buscando...")
		f = db.sql("SELECT id FROM fuentes WHERE seleccion = 1 AND id_categoria = %d" % self.lst_categorias.get_seleccion())
		fu = []
		for elemento in f:
			fu.append(str(elemento[0]))
		fuentes = ",".join(fu)
		resultados = conexion.lanzarBusqueda(self.buscar.txt_buscar.get_text(), self.buscar.tipo_busqueda, fuentes)
		op_fe = self.buscar.tipo_busqueda == "fe"
		op_and = self.buscar.tipo_busqueda == "and"
		op_or = self.buscar.tipo_busqueda == "or"
		db.sql("INSERT INTO busquedas (texto, op_fe, op_and, op_or, id_categoria, num_resultados, fecha, id_carpeta, fuentes) VALUES ('%s', %d, %d, %d, %d, %d, '%s', %d, '%s')" % (self.buscar.txt_buscar.get_text(), op_fe, op_and, op_or, self.lst_categorias.get_seleccion(), len(resultados), time.strftime("%d/%m/%Y %H:%M:%S"), self.tre_busquedas.get_seleccion(), fuentes))
		id_busqueda = db.sql_una("SELECT id FROM busquedas ORDER BY id DESC")[0]
		self.lst_busquedas.mostrar(self.tre_busquedas.get_seleccion())
		self.lst_busquedas.set_seleccion(id_busqueda)
		self.lst_busquedas.lista.scroll_to_cell((len(self.lst_busquedas.modelo) - 1,))
		self.lst_resultados.add_elemento(id_busqueda, resultados, self.lst_busquedas.get_seleccion())
		self.buscar.txt_buscar.set_text("")
		self.mostrar_animacion(0)
		status.mostrar("Listo.")
		return
		
	def on_ventana_btn_buscar(self, widget):
		if self.buscar.ventana_txt_buscar.get_text() == "" or self.buscar.ventana_txt_buscar.get_text().isspace():
			self.buscar.ventana_txt_buscar.set_text("")
			return
		self.mostrar_animacion(1)
		status.mostrar("Buscando...")
		activa = self.buscar.ventana_combo.get_active()
		id_categoria = self.lst_categorias.modelo[activa][0]
		f = db.sql("SELECT id FROM fuentes WHERE seleccion = 1 AND id_categoria = %d" % id_categoria)
		fu = []
		for elemento in f:
			fu.append(str(elemento[0]))
		fuentes = ",".join(fu)
		resultados = conexion.lanzarBusqueda(self.buscar.ventana_txt_buscar.get_text(), self.buscar.tipo_busqueda, fuentes)
		op_fe = self.buscar.tipo_busqueda == "fe"
		op_and = self.buscar.tipo_busqueda == "and"
		op_or = self.buscar.tipo_busqueda == "or"
		db.sql("INSERT INTO busquedas (texto, op_fe, op_and, op_or, id_categoria, num_resultados, fecha, id_carpeta, fuentes) VALUES ('%s', %d, %d, %d, %d, %d, '%s', %d, '%s')" % (self.buscar.ventana_txt_buscar.get_text(), op_fe, op_and, op_or, id_categoria, len(resultados), time.strftime("%d/%m/%Y %H:%M:%S"), self.tre_busquedas.get_seleccion(), fuentes))
		id_busqueda = db.sql_una("SELECT id FROM busquedas ORDER BY id DESC")[0]
		self.lst_busquedas.mostrar(self.tre_busquedas.get_seleccion())
		self.lst_busquedas.set_seleccion(id_busqueda)
		self.lst_busquedas.lista.scroll_to_cell((len(self.lst_busquedas.modelo) - 1,))
		self.lst_resultados.add_elemento(id_busqueda, resultados, self.lst_busquedas.get_seleccion())
		self.buscar.ventana_txt_buscar.set_text("")
		self.lst_busquedas.ventana_buscar.hide()
		self.mostrar_animacion(0)
		status.mostrar("Listo.")
		return
	
	def duplicar(self, widget):
		texto_busqueda = db.sql_una("SELECT texto FROM busquedas WHERE id = %d" % self.lst_busquedas.get_seleccion())[0]
		categoria = db.sql_una("SELECT id_categoria FROM busquedas WHERE id = %d" % self.lst_busquedas.get_seleccion())[0]
		indice = 0
		while 1:
			
			self.buscar.ventana_combo.set_active(indice)
			activa = self.buscar.ventana_combo.get_active()
			if self.lst_categorias.modelo[activa][0] == categoria:
				break
			indice += 1
			
		self.lst_busquedas.ventana_buscar.show()
		self.buscar.ventana_combo.emit("changed")
		self.buscar.ventana_txt_buscar.set_text(texto_busqueda)
		return
		
	def abrir_ventana_buscar(self, widget):
		self.buscar.ventana_txt_buscar.set_text("")
		self.buscar.ventana_combo.set_active(0)
		self.lst_busquedas.ventana_buscar.show()
		return

	def no_cerrar(self, widget, data):
		self.lst_busquedas.ventana_buscar.hide()
		return True
		
	def combo_cambio(self, widget):
		id_categoria = self.lst_categorias.modelo[self.buscar.ventana_combo.get_active()][0]
		op_fe = db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id_categoria = %d AND op_fe = 1 AND seleccion = 1" % id_categoria)[0] == db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id_categoria = %d AND seleccion = 1" % id_categoria)[0] and db.sql_una("SELECT count(*) FROM fuentes WHERE id_categoria = %d" % id_categoria)[0] != 0
		op_and = db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id_categoria = %d AND op_and = 1 AND seleccion = 1" % id_categoria)[0] == db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id_categoria = %d AND seleccion = 1" % id_categoria)[0] and db.sql_una("SELECT count(*) FROM fuentes WHERE id_categoria = %d" % id_categoria)[0] != 0
		op_or = db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id_categoria = %d AND op_or = 1 AND seleccion = 1" % id_categoria)[0] == db.sql_una("SELECT COUNT(*) FROM fuentes WHERE id_categoria = %d AND seleccion = 1" % id_categoria)[0] and db.sql_una("SELECT count(*) FROM fuentes WHERE id_categoria = %d" % id_categoria)[0] != 0
		if db.sql_una("SELECT COUNT(*) FROM fuentes WHERE seleccion = 1 AND id_categoria = %d" % id_categoria)[0] == 0:
			self.buscar.ventana_txt_buscar.set_property("sensitive", False)
			self.buscar.ventana_btn_buscar.set_property("sensitive", False)
			self.buscar.mostrar_tipo_busqueda_ventana(False, False, False)
		else:
			self.buscar.ventana_txt_buscar.set_property("sensitive", True)
			self.buscar.ventana_btn_buscar.set_property("sensitive", True)
			self.buscar.mostrar_tipo_busqueda_ventana(op_fe, op_and, op_or)
		return
		
	def on_dragdata_received(self, treeview, drag_context, x, y, selection, info, eventtime):
		if info == 0:
			model, iter_to_move = treeview.get_selection().get_selected()
			temp = treeview.get_dest_row_at_pos(x, y)
			if temp != None:
				sel = self.tre_busquedas.get_seleccion()
				path, pos = temp
				db.sql("UPDATE busquedas SET id_carpeta = %d WHERE id = %d" % (model[path][0], self.lst_busquedas.get_seleccion()))
				self.lst_busquedas.mostrar(sel)
				self.lst_resultados.mostrar()
				drag_context.finish(True, True, eventtime)
				self.tre_busquedas.set_seleccion(sel)
			else:
				drag_context.finish(False, False, eventtime)
			return
		else:
			model, iter_to_move = treeview.get_selection().get_selected()
			temp = treeview.get_dest_row_at_pos(x, y)
			if temp != None:
				sel = self.tre_busquedas.get_seleccion()
				path, pos = temp
				if model[path][0] != self.tre_busquedas.get_seleccion() and self.tre_busquedas.get_seleccion() != 1:
					if self.es_padre(model, path, self.tre_busquedas.get_seleccion()):
						drag_context.finish(False, False, eventtime)
						return
					db.sql("UPDATE carpetas SET pertenece = %d WHERE id = %d" % (model[path][0], self.tre_busquedas.get_seleccion()))
					drag_context.finish(True, True, eventtime)
				self.tre_busquedas.mostrar()
				self.tre_busquedas.set_seleccion(sel)
			else:
				drag_context.finish(False, False, eventtime)
			return
			
	def es_padre(self, model, path, origen):
		if db.sql_una("SELECT pertenece FROM carpetas where id = %d" % model[path][0])[0] == origen:
			return True
		if model[path].parent != None and model[path].parent[0] != origen:
			return self.es_padre(model[path].parent.model, model[path].parent.path, origen)
		return False
			
	def borrar_busqueda(self, widget):
		db.sql("DELETE FROM resultados WHERE id_busqueda = %d" % self.lst_busquedas.get_seleccion())
		db.sql("DELETE FROM busquedas WHERE id = %d" % self.lst_busquedas.get_seleccion())
		self.lst_busquedas.mostrar(self.tre_busquedas.get_seleccion())
		self.lst_resultados.mostrar()
		return
 
	def borrar_resultados(self, widget):
		db.sql("DELETE FROM resultados WHERE id = %d" % self.lst_resultados.get_seleccion())
		self.lst_resultados.mostrar(self.lst_busquedas.get_seleccion())
		return
		
	def actualizar_resultados(self, widget):
		self.mostrar_animacion(1)
		status.mostrar("Actualizando resultados...")
		resultado = db.sql_una("SELECT id, texto, op_and, op_or, op_fe, id_categoria, id_carpeta FROM busquedas WHERE id = %d" % self.lst_busquedas.get_seleccion())
		db.sql("DELETE FROM resultados WHERE id_busqueda = %d" % resultado[0])
		if resultado[2]:
			tipo_busqueda = "and"
		elif resultado[3]:
			tipo_busqueda = "or"
		else:
			tipo_busqueda = "fe"
		f = db.sql("SELECT id FROM fuentes WHERE seleccion = 1 AND id_categoria = %d" % resultado[5])
		fu = []
		for elemento in f:
			fu.append(str(elemento[0]))
		fuentes = ",".join(fu)
		resultados = conexion.lanzarBusqueda(resultado[1], tipo_busqueda, fuentes)
		op_fe = tipo_busqueda == "fe"
		op_and = tipo_busqueda == "and"
		op_or = tipo_busqueda == "or"
		id_busqueda = resultado[0]
		db.sql("DELETE FROM resultados WHERE id_busqueda = %d" % id_busqueda)
		self.lst_busquedas.mostrar(self.tre_busquedas.get_seleccion())
		self.lst_busquedas.set_seleccion(id_busqueda)
		self.lst_busquedas.lista.scroll_to_cell((len(self.lst_busquedas.modelo) - 1,))
		self.lst_resultados.add_elemento(id_busqueda, resultados, id_busqueda)
		self.mostrar_animacion(0)
		status.mostrar("Listo.")
		return
		
	def analizar(self, widget):
		self.mostrar_animacion(2)
		status.mostrar(u"Analizando vínculos...")
		sel = self.lst_busquedas.get_seleccion()
		datos = db.sql_una("SELECT texto, op_fe, op_and, op_or, fuentes FROM busquedas WHERE id = %d" % sel)
		if datos[1]:
			operador = "fe"
		elif datos[2]:
			operador ="and"
		else:
			operador = "or"
		nuevos = conexion.lanzarBusqueda(datos[0], operador, datos[4])
		self.lst_resultados.actualizar(sel, nuevos)
		self.mostrar_animacion(0)
		status.mostrar("Listo.")
		return
	
	def exportar(self, widget, nombre):
		status.mostrar(u"Exportando búsquedas...")
		fichero = codecs.open(nombre, encoding = "iso-8859-15", mode = "w")
		fichero.write("#c#%s\n" % db.sql_una("SELECT nombre FROM carpetas WHERE id = %d" % self.tre_busquedas.get_seleccion())[0])
		busquedas = db.sql("SELECT id, texto, op_and, op_or, op_fe, num_resultados, fecha FROM busquedas WHERE id_carpeta = %d" % self.tre_busquedas.get_seleccion())
		for busqueda in busquedas:
			fichero.write("#b#%s|%d|%d|%d|%d|%s\n" % (busqueda[1], busqueda[2], busqueda[3], busqueda[4], busqueda[5], busqueda[6]))
			resultados = db.sql("SELECT titulo, texto, enlace, id_fuente, idioma, fecha, nota FROM resultados WHERE id_busqueda = %d" % busqueda[0])
			for resultado in resultados:
				fichero.write("#r#%s|%s|%s|%s|%s|%s|%s\n" % (resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5], resultado[6]))
		fichero.close()
		status.mostrar("Listo.")
		return
		
	def importar(self, widget, nombre):
		status.mostrar(u"Importando búsquedas...")
		fichero = codecs.open(nombre, encoding = "iso-8859-15", mode = "r")
		datos = fichero.readlines()
		fichero.close()
		carpeta = 0
		busqueda = 0
		for linea in datos:
			if linea[:3] == "#c#":
				linea = linea.replace("#c#", "")
				linea = linea.replace("\n", "")
				db.sql("INSERT INTO carpetas (nombre, pertenece, abierta) VALUES ('%s', 1, 1)" % linea)
				carpeta = db.sql_una("SELECT id FROM carpetas ORDER BY id DESC")[0]
			if linea[:3] == "#b#":
				linea = linea.replace("#b#", "")
				linea = linea.replace("\n", "")
				dato = linea.split("|")
				db.sql("INSERT INTO busquedas (texto, op_and, op_or, op_fe, num_resultados, fecha, id_carpeta) VALUES ('%s', %s, %s, %s, %s, '%s', %s)" % (dato[0], dato[1], dato[2], dato[3], dato[4], dato[5], carpeta))
				busqueda = db.sql_una("SELECT id FROM busquedas ORDER BY id DESC")[0]
			if linea[:3] == "#r#":
				linea = linea.replace("#r#", "")
				linea = linea.replace("\n", "")
				dato = linea.split("|")
				db.sql("INSERT INTO resultados (titulo, texto, enlace, id_fuente, idioma, fecha, nota, id_busqueda) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s)" % (dato[0], dato[1], dato[2], dato[3], dato[4], dato[5], dato[6], busqueda))
		self.tre_busquedas.mostrar()
		status.mostrar("Listo.")
		return
		
	def abrir_exportar(self, widget):
		self.guardar.set_default_response(gtk.RESPONSE_OK)
		response = self.guardar.run()
		if response == gtk.RESPONSE_OK:
			if self.guardar.get_filename() != "":
				if self.guardar.get_filename()[-4:] != ".hon":
					nombre = self.guardar.get_filename()+".hon"
				else:
					nombre = self.guardar.get_filename()
				self.exportar(self, nombre)
		self.guardar.hide()
		return
		
	def abrir_importar(self, widget):
		self.abrir.set_default_response(gtk.RESPONSE_OK)
		response = self.abrir.run()
		if response == gtk.RESPONSE_OK:
			if self.abrir.get_filename() != "":
				nombre = self.abrir.get_filename()
			self.importar(self, nombre)
		self.abrir.hide()
		return
		
	def crear_copia(self, widget):
		status.mostrar("Creando copia de seguridad...")
		self.guardar.set_default_response(gtk.RESPONSE_OK)
		self.guardar.set_current_name("hontza.db")
		response = self.guardar.run()
		if response == gtk.RESPONSE_OK:
			fe = open("hontza.db", "rb")
			fs = open(self.guardar.get_filename(), "wb")
			fs.write(fe.read())
			fs.close()
			fe.close()
		self.guardar.hide()
		status.mostrar("Listo.")
		return
		
	def restaurar_copia(self, widget):
		status.mostrar("Restaurando copia de seguridad...")
		self.abrir.set_default_response(gtk.RESPONSE_OK)
		response = self.abrir.run()
		if response == gtk.RESPONSE_OK:
			if os.path.isfile("hontza.db"):
				fe = open("hontza.db", "rb")
				fs = open("hontza.db.bak", "wb")
				fs.write(fe.read())
				fs.close()
				fe.close()
			fe = open(self.abrir.get_filename(), "rb")
			fs = open("hontza.db", "wb")
			fs.write(fe.read())
			fs.close()
			fe.close()
		self.abrir.hide()
		self.tre_busquedas.mostrar()
		self.lst_categorias.mostrar()
		status.mostrar("Listo.")
		return
		
	def acerca(self, widget):
		self.acerca_de.show()
		return
		
	def acerca_de_cerrar(self, widget):
		self.acerca_de.hide()
		return
		
	def ayuda(self, widget, pagina = "index.html"):
		webbrowser.open(os.path.abspath("ayuda/%s" % pagina))
		return
		
	def mostrar_animacion(self, tipo = 0):
		if tipo == 0:
			self.animacion.set_from_file("hontza_espera.gif")
		elif tipo == 1:
			self.animacion.set_from_file("hontza_busca.gif")
		elif tipo == 2:
			self.animacion.set_from_file("hontza_analiza.gif")
		self.animacion.show()
		return
		
if __name__ == "__main__":
	db = Db("hontza.db")
	mainGlade = gtk.glade.XML("hontza.glade")
	fuentes = Fuentes(mainGlade, db)
	conexion = Conexion(db)
	configuracion = Configuracion(mainGlade, db)
	splash = Splash(mainGlade)
	error = Error(mainGlade)
	status = Status(mainGlade)
	principal = Principal()
	if os.path.isfile("hontza.db") == False:
		fichero = open("inicializacion.sql", "r")
		datos = fichero.readlines()
		fichero.close()
		db.inicializa(datos)
		configuracion.mostrar()
		while configuracion.abierta:
			gtk.main_iteration()
	splash.set_texto("Conectando al servidor WSDL...")
	splash.mostrar()
	while conexion.inicializa() == False:
		splash.ocultar()
		error.mostrar(u"Error al conectar al servidor WSDL. Compruebe la configuración.", 1, 1)
		while error.abierta:
			gtk.main_iteration()
		if error.cerrar:
			gtk.main_quit()
		if error.configuracion:
			configuracion.mostrar()
			while configuracion.abierta:
				gtk.main_iteration()
		splash.set_texto("Conectando al servidor WSDL...")
		splash.mostrar()
	splash.set_texto("Cargando fuentes...")
	while conexion.getFuentes() == False:
		splash.ocultar()
		error.mostrar(u"Error al actualizar las fuentes.", 1, 1)
		while error.abierta:
			gtk.main_iteration()
		if error.cerrar:
			break
		if error.configuracion:
			configuracion.mostrar()
			while configuracion.abierta:
				gtk.main_iteration()
		splash.set_texto("Cargando fuentes...")
		splash.mostrar()
	splash.ocultar()
	if db.sql_una("SELECT COUNT(*) FROM fuentes WHERE seleccion = 0")[0] == db.sql_una("SELECT COUNT(*) FROM fuentes")[0]:
		fuentes.mostrar()
		while fuentes.abierta:
			gtk.main_iteration()
	status.mostrar("Listo.")
	principal.mostrar()
	gtk.main()
