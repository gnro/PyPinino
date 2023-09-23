from qgis.core import QgsVectorLayer, QgsDataSourceUri, QgsProject
from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MyMSSQL:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction(QIcon("icon.png"), "Agregar Capa SQL Server", self.iface.mainWindow())
        self.action.triggered.connect(self.agregar_capa_sql_server)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)

    def agregar_capa_sql_server(self,laCapa):
        from qgis.core import QgsDataSourceUri, QgsVectorLayer, QgsWkbTypes
        uri = QgsDataSourceUri()
        uri.setConnection("192.168.3.16", "1433", "Cartografia", "ulectura", "ulectura123")
        uri.setDataSource("sde",laCapa, "Shape", "")
        uri.setSrid('32614')
        uri.setWkbType(QgsWkbTypes.Polygon)
        capa = QgsVectorLayer(uri.uri(), laCapa, "mssql")
        
        if not capa.isValid():
            QMessageBox.critical(self.iface.mainWindow(), "Error", "No se pudo cargar la capa: '"+laCapa+"' desde SQL Server.")
            return
        QgsProject.instance().addMapLayer(capa)