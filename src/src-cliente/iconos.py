# -*- coding: iso-8859-15 -*-

import gtk

class Iconos:

	def __init__(self):
		folder_op = [
			    "16 16 5 1",
			    " 	c none",
			    ".	c black",
			    "X	c tan",
			    "o	c wheat",
			    "O	c grey",
			    "                ",
			    "         ...    ",
			    "        .XXX.   ",
			    "  ......XXXXX.. ",
			    "  .XXXXXXXXXXX. ",
			    " ...........XX.O",
			    ".oooooooooo.XX.O",
			    ".oooooooooo.XX.O",
			    " .oooooooooo.X.O",
			    " .oooooooooo.X.O",
			    "  .ooooooooo.X.O",
			    "  .oooooooooo..O",
			    "  .ooooooooooo.O",
			    "  .............O",
			    "   OOOOOOOOOOOO ",
			    "                "
			    ]
		folder_cl = [
			    "16 16 5 1",
			    " 	c none",
			    ".	c black",
			    "X	c tan",
			    "o	c wheat",
			    "O	c grey",
			    "                ",
			    "         ...    ",
			    "        .XXX.   ",
			    "       .XXXXX.  ",
			    " .............  ",
			    " .ooooooooooo.  ",
			    " .ooooooooooo.O ",
			    " .ooooooooooo.O ",
			    " .ooooooooooo.O ",
			    " .ooooooooooo.O ",
			    " .ooooooooooo.O ",
			    " .ooooooooooo.O ",
			    " .ooooooooooo.O ",
			    " .............O ",
			    "  OOOOOOOOOOOOO ",
			    "                "
			    ]
		lupa_busq = [
			    "16 16 5 1",
			    " 	c None",
			    ".	c black",
			    "X	c white",
			    "C	c cyan",
			    "c	c red",
			    " ..........     ",
			    " .XXXXXXXX..    ",
			    " .XX...XXX.X.   ",
			    " .X.CCC.XX.XX.  ",
			    " ..CXXCC.X..... ",
			    " ..CXCCC.XXXXX. ",
			    " ..CCCCC.XXXXX. ",
			    " .X.CCC..XXXXX. ",
			    " .XX....c.XXXX. ",
			    " .XXXXXX.c.XXX. ",
			    " .XXXXXXX.c.XX. ",
			    " .XXXXXXXX.c.X. ",
			    " .XXXXXXXXX..X. ",
			    " .XXXXXXXXXXXX. ",
			    " .XXXXXXXXXXXX. ",
			    " .............. "
			    ]
		actu_no = [
			   "16 16 4 1",
				" 	c none",
				".	c black",
				"X	c white",
				"c	c gray",
				" ..........     ",
				" .XXXXXXXX..    ",
				" .XXXXXXXX.X.   ",
				" .Xccccccc.XX.  ",
				" .XXXXXXXX..... ",
				" .XccccccccccX. ",
				" .XXXXXXXXXXXX. ",
				" .XccccccccccX. ",
				" .XXXXXXXXXXXX. ",
				" .XccccccccccX. ",
				" .XXXXXXXXXXXX. ",
				" .XccccccccccX. ",
				" .XXXXXXXXXXXX. ",
				" .XccccccccccX. ",
				" .XXXXXXXXXXXX. ",
				" .............. "
			    ]
		actu = [
			   "16 16 4 1",
				" 	c none",
				".	c black",
				"X	c red",
				"c	c gray",
				" ..........     ",
				" .XXXXXXXX..    ",
				" .XXXXXXXX.X.   ",
				" .Xccccccc.XX.  ",
				" .XXXXXXXX..... ",
				" .XccccccccccX. ",
				" .XXXXXXXXXXXX. ",
				" .XccccccccccX. ",
				" .XXXXXXXXXXXX. ",
				" .XccccccccccX. ",
				" .XXXXXXXXXXXX. ",
				" .XccccccccccX. ",
				" .XXXXXXXXXXXX. ",
				" .XccccccccccX. ",
				" .XXXXXXXXXXXX. ",
				" .............. "
			    ]
		self.carpeta_abierta = gtk.gdk.pixbuf_new_from_xpm_data(folder_op)
		self.carpeta_cerrada = gtk.gdk.pixbuf_new_from_xpm_data(folder_cl)
		self.busqueda = gtk.gdk.pixbuf_new_from_xpm_data(lupa_busq)
		self.actualizado = gtk.gdk.pixbuf_new_from_xpm_data(actu)
		self.no_actualizado = gtk.gdk.pixbuf_new_from_xpm_data(actu_no)
		
