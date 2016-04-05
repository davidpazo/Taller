#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from Taller import Taller


#proyecto entregado
class Login:
    """
    La clase Login, contiene la primera interfaz,
    la cual te pide que te registres para poder acceder a la aplicacion
    """
    def __init__(self):

            builder2 = Gtk.Builder()
            builder2.add_from_file("inicio.glade")

            self.nombre = builder2.get_object("nombre")
            self.contrasena = builder2.get_object("contrasena")
            self.ventana1 = builder2.get_object("inicio")

            sinais = {"on_Entrada_clicked": self.inicio,
                      "delete-event": self.cerrar}

            builder2.connect_signals(sinais)
            self.ventana1.set_title("LOG IN")
            self.ventana1.show_all()

    def inicio(self, widget):
        """
        Metodo inicio:
        Metodo que limita el acceso al programa
        mediante usuario y contraseña,
        la contraseña se ha ocultado
        """
        nombre = self.nombre.get_text();
        contrasena = self.contrasena.get_text();
        if nombre == "taller" and contrasena == "root":
            Taller()
            self.ventana1.destroy()

        else:
            self.popup("Prueba otra vez")

    def cerrar(self, widget):
        """"
        Metodo cerrar:
        Destruye la ventana emergente que nos
        muestra el mensaje de informacion
        """
        widget.destroy()

    def popup(self, texto):
        """
        Este metodo abre
        una ventana emergente
        que muestra el texto
        correspondiente que
        le pasa cada metodo
        """
        window = Gtk.Window(title="Warning")
        label = Gtk.Label(texto)
        label.set_padding(15,15)
        window.add(label)
        window.connect("delete-event", self.cerrar)
        window.set_position(Gtk.PositionType.RIGHT)
        window.show_all()
"""
Desde esta clase iniciamos el programa y llamamos a la siguiente clase.
"""
Login()
Gtk.main()
