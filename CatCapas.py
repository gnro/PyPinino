from qgis.core import  QgsFillSymbol, QgsSingleSymbolRenderer, QgsProject
from qgis.PyQt.QtCore import *

class carCapas:
    def __init__(self, iface):
        self.iface = iface
        self.project = QgsProject.instance()

    def limpiaCapas(self):
        self.project.removeAllMapLayers()

    def cargaCapas(self):
        capas = ['CONSTRUCCION', 'PREDIO', 'MANZANA','PREDIO_CONDOMINIO', 'REGION', 'SUBREGION', 'MUNICIPIO']
        n=len(capas)
        from .MiConnect import MyMSSQL
        ssql=MyMSSQL(self.iface)
        while (n>0):
            n=n-1
            ssql.agregar_capa_sql_server(capas[n])
        #self.agrupaCapas(['PREDIO', 'CONSTRUCCION', 'MANZANA','PREDIO_CONDOMINIO'])
        self.stilaPredio()
        self.stilaConst()
        layerMzn = self.project.mapLayersByName("MANZANA")[0]
        
        self.stilaMzn(layerMzn,{'color': '#fffffee1', 'outline_color': '#ff104c91', 'outline_style': 'solid', 'outline_width': '1.7'})
        self.labelingLayer(layerMzn, "concat('Mzn: ', MANZANA)", '#ff0a315d')
        
        layer = QgsProject.instance().mapLayersByName("SUBREGION")[0]
        self.stilaMzn(layer,{'color': '#094700e0', 'outline_color': '#af4700e0', 'outline_style': 'dash', 'outline_width': '0.9'})
        self.labelingLayer(layer, "concat('subregion: ', SUBREGION)", '#ff190050')
        
        layer = QgsProject.instance().mapLayersByName("REGION")[0]
        self.stilaMzn(layer,{'color': '#06364f00', 'outline_color': '#af364f00', 'outline_style': 'line', 'outline_width': '1.1'})
        self.labelingLayer(layer, "concat('region: ', REGION)", '#ff2b3d00')
        
        layer = QgsProject.instance().mapLayersByName("MUNICIPIO")[0]
        self.stilaMzn(layer,{'color': '#0338acc3', 'outline_color': '#c938acc3', 'outline_style': 'dott', 'outline_width': '2.7'})
        self.labelingLayer(layer, "concat(municipio, ': ', NOMBRE_MUNICIPIO)", '#ff216773')
        
    def agrupaCapas(self,capas):
        from qgis.core import QgsLayerTreeGroup
        group_name = "Group_2"  # Cambia esto al nombre del grupo al que deseas mover la capa
        group = None
        
        root = self.project.layerTreeRoot()
        for child in root.children():
            if isinstance(child, QgsLayerTreeGroup) and child.name() == group_name:
                group = child
                break
        
        if group is None:
            group = QgsLayerTreeGroup(group_name)
            root.addChildNode(group)
            
        for capa in capas:
            layer = project.mapLayersByName(capa)[0]
            group.addLayer(layer)
            self.removeCapa(layer)
    
    def stilaMzn(self, layer, simbolo):
        fill_symbol = QgsFillSymbol.createSimple(simbolo)
        renderer = QgsSingleSymbolRenderer(fill_symbol)
        layer.setRenderer(renderer)
        layer.triggerRepaint()
        QgsProject.instance().addMapLayer(layer)
    
    def stilaPredio(self):
        layer = self.project.mapLayersByName("PREDIO")[0]
        from qgis.core import  QgsFillSymbolLayer, QgsStyle
        from qgis.core import QgsCategorizedSymbolRenderer, QgsRendererCategory
        sym1 = QgsFillSymbol.createSimple({'color': '#3902c8ff', 'outline_color': '#ff0698ed', 'outline_style': 'solid', 'outline_width': '0.4'})
        sym2 = QgsFillSymbol.createSimple({'color': '#ff395700', 'outline_color': '#f54e5b4e', 'outline_style': 'solid', 'outline_width': '1.0'})
        sym3 = QgsFillSymbol.createSimple({'color': '#ff068f91', 'outline_color': '#fff7f7f7', 'outline_style': 'solid', 'outline_width': '0.7'})
        sym4 = QgsStyle.defaultStyle().symbol("hashed black X")#QgsFillSymbol.createSimple({'color': '#ff7e6363', 'outline_color': '#fff7f7f7'})
        
        # Categorized styles: declared order will be the same in the tree view
        categories = [
            QgsRendererCategory('1', sym1, 'Urbano'),
            QgsRendererCategory('2', sym2, 'Rustico'),
            QgsRendererCategory('3', sym3, 'SubUrbano'),
            QgsRendererCategory('', sym4, '')
        ]
        
        renderer = QgsCategorizedSymbolRenderer('TIPO_PREDIO', categories)
        layer.setRenderer(renderer)
        layer.triggerRepaint()
        QgsProject.instance().addMapLayer(layer)
       
    def stilaConst(self):
        
        from qgis.core import QgsSingleSymbolRenderer, QgsFillSymbolLayer, QgsStyle
        layer = self.project.mapLayersByName("CONSTRUCCION")[0]
        self.categoryzeGreys_layer(layer,'NIVEL')
        
    def categoryzeGreys_layer(self, layer, cat_field):
        from PyQt5.QtGui import QPainter, QColor, QPen
        from qgis.core import QgsSymbol, QgsLineSymbol, QgsFillSymbol, QgsCategorizedSymbolRenderer, QgsRendererCategory
        from random import randrange  # Importa randrange desde random
    
        fields = layer.fields()
        fni = fields.indexOf(cat_field)
        
        unique_values = layer.dataProvider().uniqueValues(fni)
        categories = []
        color_values = {'NEW': QColor(0, 255, 0), 'DUPLICATED': QColor(255, 0, 0), 'EXISTS': QColor(240, 150, 0)}
    
        for unique_value in unique_values:
            # Initialize the default symbol for this geometry type
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            try:
                color = color_values.get(unique_value)
                symbol.setColor(color)
            except:
                c=randrange(20, 230)
                color = QColor(c, c, c)
                symbol.setColor(color)
    
            category = QgsRendererCategory(unique_value, symbol, str(unique_value))
            # Entry for the list of category items
            categories.append(category)
    
        # Create a renderer object
        renderer = QgsCategorizedSymbolRenderer(cat_field, categories)
    
        # Assign the created renderer to the layer
        if renderer is not None:
            layer.setRenderer(renderer)
    
        layer.triggerRepaint()
        self.iface.layerTreeView().refreshLayerSymbology(layer.id())
        
    def labelingLayer(self,layer, cadena, _color):
        from qgis.core import QgsPalLayerSettings, QgsTextFormat, QgsVectorLayerSimpleLabeling
        from PyQt5.QtGui import QFont, QColor
        from qgis.core import QgsTextFormat
        #layer = self.project.mapLayersByName(capa)[0]
        
        settings = QgsPalLayerSettings()
        txt_format = QgsTextFormat()
        txt_format.setFont(QFont('PT SANS'))
        txt_format.setSize(19)  # Tamaño de fuente predeterminado
        color = QColor(_color)
        txt_format.setColor(color)
        txt_format.mask().setEnabled(True)
        settings.setFormat(txt_format)
        settings.fieldName = cadena
        settings.placement = QgsPalLayerSettings.OverPoint
        settings.drawLabels = True
        settings.enabled = True  # Habilita el etiquetado
        labels = QgsVectorLayerSimpleLabeling(settings)
        layer.setLabeling(labels)
        layer.setLabelsEnabled(True)
        layer.triggerRepaint()
        