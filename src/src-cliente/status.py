# -*- coding: iso-8859-15 -*-

import gtk

class Status:

	def __init__(self, mainGlade):
		self.statusbar = mainGlade.get_widget("statusbar")
		return
		
	def mostrar(self, texto):
		self.statusbar.push(0, " %s" % texto)
		while gtk.events_pending():
			gtk.main_iteration()
		return
