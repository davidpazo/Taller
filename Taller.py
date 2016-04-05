# -*- coding: utf-8 -*-
import sqlite3 as dbapi
from gi.repository import Gtk, Gdk
import Generarpdf as pdf

class Taller:

    """  
    La clase Taller, contiene todos los metodos de consultas a la base de datos, 
    el treeview, y todos los metodos necesarios para el funcionamiento del programa
    
    Este cursor, genera la tabla en la base de datos sqlite, 
    al estar creada la dejo comentada como muestra
    """
   # cursor.execute("CREATE TABLE taller (matricula VARCHAR(7) PRIMARY KEY NOT NULL,"
    #                        "vehiculo VARCHAR(20),"
     #                       "kilometros INT,"
      #                      "fecha VARCHAR(50) ,"
       #                     "cliente VARCHAR(10),"
        #                    "cif VARCHAR(10),"
         #                   "telefono INT,"
          #                  "direccion VARCHAR(10))")

    def __init__(self):
        """
        Declaramos atributo condicion para realizar las excepciones

        Conexion con la base de datos.
        Siempre se debe hacer un commit al terminar una consulta

        Declaramos los nombres de las señales,
        que reciben los botones de glade,
        para llamar al metodo correspondiente.


        Abrimos y conectamos a la interfaz de taller.glade

        """
        self.condicion= bool
        self.bd = dbapi.connect("basedatos.dat")
        self.cursor = self.bd.cursor()

        self.builder = Gtk.Builder()
        self.builder.add_from_file("Taller.glade")
        self.inicializar()
        self.ventana = self.builder.get_object("Taller")

        sinais = {"on_insertar_clicked": self.insertar,
                  "on_borrar_clicked": self.borrar,
                  "on_modificar_clicked": self.modificar,
                  "on_ayuda_clicked": self.informacion,
                  "on_imprimir_clicked": self.imprimir,
                  "delete-event": Gtk.main_quit}
        self.builder.connect_signals(sinais)
        self.ventana.set_title("Taller.")
        self.ventana.show_all()


    def inicializar(self):
        """
        treeview o tabla, en el que se
        muestran los datos de la base de datos
        """
        self.box = self.builder.get_object("box2")
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.vista = Gtk.TreeView()
        self.box.add(self.scroll)
        self.scroll.add(self.vista)
        self.scroll.set_size_request(500, 500)
        self.scroll.show()

        self.lista = Gtk.ListStore(str, str, str, str, str, str, str, str)

        self.lista.clear()
        self.cursor.execute("select * from taller")
       
        for clientes in self.cursor:
            self.lista.append(clientes)

        self.vista.set_model(self.lista)

        for i, title in enumerate(["MATRICULA","VEHICULO","KILOMETROS","FECHA ENTREGA","CLIENTE","CIF/NIF", "TELEFONO", "DIRECCION"]):
            render = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(title, render, text=i)
            self.vista.append_column(columna)

    
    def informacion(self, widget):
        """
        Metodo Informacion:
        Da una pequeña orientacion al usuario explicando
        como usar los botones y el programa en si
        """
        self.popup("-->Boton +:\nAñade un nuevo cliente a la base de datos\n-->Boton -:\nQuita un cliente de la base de datos\n(solo clica en el treeview la fila seleccionada)\n-->Boton Lapiz:\nEste boton permite modificar un cliente de la base, solo escribe la matricula y los campos que quieras cambiar\n-->Boton ?:\nSi no lo necesitaras no estarias aqui :D\n-->Boton Imprimir:\nGenera un pdf con la lista de clientes.")

    def borrar(self, widget):
        """
        Metodo borrar:
        Que borra seleccionando la fila en en el treeview
        """
        selection = self.vista.get_selection()
        model, selec = selection.get_selected()
        if selec != None:
            self.matricula = model[selec][0]
            self.cursor.execute("delete from taller where matricula ='" + self.matricula + "'")
            self.actualizar()
            self.bd.commit()
            self.popup("Borrado")


    def modificar(self, modificar):
        """
        Metodo Modificar: Modifica a traves de la primary Key
        """
        matricula = self.builder.get_object("matricula").get_text()
        vehiculo = self.builder.get_object("vehiculo").get_text()
        kilometros = self.builder.get_object("kilometros").get_text()
        fecha = self.builder.get_object("fecha").get_text()
        cliente = self.builder.get_object("cliente").get_text()
        cifnif = self.builder.get_object("cifnif").get_text()
        telefono = self.builder.get_object("telefono").get_text()
        direccion = self.builder.get_object("direccion").get_text()

        if kilometros.isdigit and len(cifnif)==9 and telefono.isdigit and len(telefono)==9:
            self.condicion = True
        else:
            self.popup("Datos invalidos.")
            self.condicion = False

        if(self.condicion):

            try:
                self.cursor.execute("update taller set vehiculo ='" + vehiculo + "'"
                                                     ",kilometros='" + kilometros + "'"
                                                     ",fecha='" + fecha + "'"
                                                     ",cliente='" + cliente + "'"
                                                     ",cif='" + cifnif +"'"
                                                     ",telefono='" + telefono +"'"
                                                     ",direccion='" + direccion +"' where matricula='" + matricula + "'")
                self.popup("Modificado")
                self.bd.commit()
                self.actualizar()
            except dbapi.IntegrityError:
                self.popup("La matricula ya existe")


    def insertar(self, control):
        """
        Metodo insertar: 
        Inserta a la base de datos 
        todos los campos recogiendo 
        el texto de los Gtxentrys del glade.
        
        """
        matricula = self.builder.get_object("matricula").get_text()
        vehiculo = self.builder.get_object("vehiculo").get_text()
        kilometros = self.builder.get_object("kilometros").get_text()
        fecha = self.builder.get_object("fecha").get_text()
        cliente = self.builder.get_object("cliente").get_text()
        cifnif = self.builder.get_object("cifnif").get_text()
        telefono = self.builder.get_object("telefono").get_text()
        direccion = self.builder.get_object("direccion").get_text()

        if kilometros.isdigit and len(cifnif)==9 and telefono.isdigit and len(telefono)==9:
            self.condicion = True
        else:
            self.popup("Datos invalidos. ")
            self.condicion = False

        if(self.condicion):

            try:
                self.cursor.execute(
                    "insert into taller values('" + matricula + "'"
                                             ",'" + vehiculo + "'"
                                             ",'" + kilometros + "'"
                                             ",'" + fecha+"'"
                                             ",'" + cliente + "'"
                                             ",'" + cifnif +"'"
                                             ",'" + telefono +"'"
                                             ",'" + direccion +"')")
                self.popup("Insertado")
                self.actualizar()
                
                self.bd.commit()
            except dbapi.IntegrityError:
                self.popup("La matricula ya existe")



    def actualizar(self):
        """
        Metodo actualizar:
        Este metodo simplemente actualiza
        la tabla de la base de datos,
        haciendo un select y
        refrescando el treeview
        """
        self.lista.clear()
        self.cursor.execute("select * from taller")
        #print(self.cursor.fetchall())
        for merla in self.cursor:
            self.lista.append(merla)

        self.vista.set_model(self.lista)

    def cerrar(self, widget):
        """"
        Metodo cerrar:
        Destruye la ventana emergente que nos 
        muestra el mensaje de informacion
        """
        self.ventana.destroy()

    def imprimir(self,widget):
        """
        Metodo Imprimir:
        Este metodo simplemente llama a la clase Generarpdf.py 
        para generar el pdf, con el contenido de la base de datos
        """
        obj = pdf.PDF()
        obj.pdf()

    def popup(self, texto):
        """
        Este metodo abre
        una ventana emergente
        que muestra el texto
        correspondiente que
        le pasa cada metodo
        """
        window = Gtk.Window(title="Aviso")
        label = Gtk.Label(texto)
        label.set_padding(30, 30)
        window.add(label)
        window.connect("delete-event", self.cerrar)
        window.set_position(Gtk.BaselinePosition.CENTER)
        #window.set_position(Gtk.PositionType.TOP)
        window.show_all()
