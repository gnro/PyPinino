from qgis.core import QgsVectorLayer, QgsDataSourceUri, QgsProject
from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MyMSSQL:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction(QIcon("ruta_al_icono.png"), "Agregar Capa SQL Server", self.iface.mainWindow())
        self.action.triggered.connect(self.agregar_capa_sql_server)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)

    def agregar_capa_sql_server(self):
        uri = QgsDataSourceUri()
        uri.setConnection("192.168.3.16", "1433", "Cartografia", "ulectura", "ulectura123")
        uri.setDataSource("sde", "PREDIO_CONDOMINIO", "polygon", "")

        capa = QgsVectorLayer(uri.uri(), "PREDIO_CONDOMINIO", "mssql")

        if not capa.isValid():
            QMessageBox.critical(self.iface.mainWindow(), "Error", "No se pudo cargar la capa desde SQL Server.")
            return

        QMessageBox.information(self.iface.mainWindow(), "ok", "Si se pudo cargar la capa desde SQL Server.")
        QgsProject.instance().addMapLayer(capa)
        self.iface.mapCanvas().refresh()