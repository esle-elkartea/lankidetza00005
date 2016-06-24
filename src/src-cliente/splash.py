# -*- coding: iso-8859-15 -*-

import gtk

class Splash:
	
	def __init__(self, mainGlade):
		self.splash = mainGlade.get_widget("splash")
		self.lbl_splash = mainGlade.get_widget("lbl_splash")
		return
		
	def mostrar(self):
		self.splash.show()
		while gtk.events_pending():
			gtk.main_iteration()
		return
		
	def ocultar(self):
		self.splash.hide()
		return
		
	def set_texto(self, texto):
		self.lbl_splash.set_text(texto)
		while gtk.events_pending():
			gtk.main_iteration()
		return

