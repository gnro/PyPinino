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
        from qgis.core import Qgis
        from qgis.core import QgsProject
        ban=1
        capas = ['PREDIO', 'CONSTRUCCION', 'MANZANA','CASCADA', 'MUNICIPIO']
        n=len(capas)
        i=0
        while (ban==1) and (n>i):
            #self.iface.messageBar().pushMessage("Error", capas[i], level=Qgis.Critical)
            capa=capas[i]
            #self.iface.messageBar().pushMessage("capa: "+str(i),capa, level=Qgis.Info)
            layer = QgsProject.instance().mapLayersByName(capa)[0]
            
            i=1+i
            #self.iface.messageBar().pushMessage("Error", layer.name() , level=Qgis.Critical)
            if (layer.name() ==''):
                self.iface.messageBar().pushMessage("ERROr: ","Falta la capa:"+capa, level=Qgis.Critical)
                return
                ban=0
            