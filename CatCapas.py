'''
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtWidgets import QAction
from .CatWatch_dialog import catsDialog 
import os.path
'''
from qgis.PyQt.QtCore import *

class carCapas:
    def __init__(self, iface):
        self.iface = iface
    
    def cargaCapas(self):
        pass
        '''
        from qgis.core import QgsVectorLayer, QgsProject
        layer1 = QgsVectorLayer("Point?crs=EPSG:4326", "layer name you like 2", "memory")
        QgsProject.instance().addMapLayer(layer1, False)
        node_layer1 = root.addLayer(layer1)
        # Remove it
        QgsProject.instance().removeMapLayer(layer1)
        '''

    def verifiCapas(self):
        capas = ['PREDIO', 'CONSTRUCCION', 'MANZANA','PREDIO_CONDOMINIO', 'MUNICIPIO']
        n=len(capas)
        from .MiConnect import MyMSSQL
        ssql=MyMSSQL(self.iface)
        while (n>0):
            n=n-1
            ssql.agregar_capa_sql_server(capas[n])            
        self.iface.mapCanvas().refresh()