from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Image
from reportlab.pdfgen import canvas
import sqlite3 as dbapi
from gi.repository import Gtk


class PDF():
    """
    Esta clase PDF contiene todo lo relacion con la generacion del pdf,
    con el contenido de la base de datos,
    podriamos cambiarlo facilmente
    para utilizarlo como generador de facturas
    """

    def __init__(self):
        """
        Conexion con la base de datos
        """
        self.bd = dbapi.connect("basedatos.dat")
        self.cursor = self.bd.cursor()
        self.historialpdf = "Clientes.pdf"
        self.canvas = None

        # foto = Image("./talleres-rodal.jpg")

    def pdf(self):
        """
        Metodo pdf:
        Este metodo genera el pdf, y en el nombre
        le pone la fecha en la que es generado
        utilizamos canvas, y llamamos al metodo tabla
        para agregar la tabla al pdf
        """
        self.canvas = canvas.Canvas(self.historialpdf, pagesize=letter)
        titulos = [
            ["MATRICULA", "VEHICULO", "KILOMETROS", "FECHA ENTRADA", "CLIENTE", "CIF/NIF", "TELEFONO", "DIRECCION"]]
        clientes = titulos + list(self.cursor.execute("select * from taller"))
        tabla = Table(clientes)

        estilo = TableStyle([('GRID', (0, 0), (-1, -1), 2, colors.white),
                             ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                             ('BACKGROUND', (0, 0), (-1, 0), colors.lightcoral)])
        tabla.setStyle(estilo)


        self.canvas.drawString(20, 800, "Impresion lista clientes")

        tabla.wrapOn(self.canvas, 20, 30)
        tabla.drawOn(self.canvas, 20, 600)
        self.canvas.save()

        self.popup("PDF Generado")

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
        window = Gtk.Window(title="Oye!")
        label = Gtk.Label(texto)
        label.set_padding(15, 15)
        window.add(label)
        window.connect("delete-event", self.cerrar)
        window.set_position(Gtk.PositionType.RIGHT)
        window.show_all()
        # PDF().pdf()

PDF().pdf()