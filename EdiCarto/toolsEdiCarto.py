import os
from datetime import datetime
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface

class MyBtn:
    def __init__(self):
        self.initUI()
    def __init__(self,ifacc):
        self.iface=ifacc
        self.initUI()
        
    def initUI(self):
        try:
            #return
            self.init_Gui()
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "p.png")
            icon = QIcon(icon_path)
            action = QAction(icon,'Show', iface.mainWindow())
            action.setEnabled(True)
            action.triggered.connect(self.show_time)
            iface.addToolBarIcon(action)
        except Exception as e:
            print(f'Error al crear el botón: {str(e)}')
            
    def show_time(self):
        print("Cuack")
        #self.show_custom_dialog()
        
    def show_custom_dialog(self):
        dialog = MyDialog()
        dialog.exec_()
        pass

    def init_Gui(self):
        from qgis.PyQt.QtCore import QUrl
        from qgis.PyQt.QtGui import QIcon
        from qgis.PyQt.QtWidgets import QAction
        from qgis.core import QgsApplication
        """Create the menu & tool bar items within QGIS"""
        icon = QIcon(     os.path.join(os.path.dirname(os.path.abspath(__file__)), "e.png"))
        #icon = QIcon(os.path.dirname(__file__) + "/icon.png")
        self.kmlAction = QAction(icon, "Import KML/KMZ", self.iface.mainWindow())
        self.kmlAction.triggered.connect(self.show_custom_dialog)
        self.kmlAction.setCheckable(False)
        self.iface.addToolBarIcon(self.kmlAction)
        self.iface.addPluginToVectorMenu("KML Tools", self.kmlAction)
        # Expansion of HTML description field
        icon = QIcon(     os.path.join(os.path.dirname(os.path.abspath(__file__)), "e2.png"))
        self.htmlDescAction = QAction(icon, "Expand HTML description field", self.iface.mainWindow())
        self.htmlDescAction.triggered.connect(self.show_custom_dialog)
        self.htmlDescAction.setCheckable(False)
        self.iface.addToolBarIcon(self.htmlDescAction)
        self.iface.addPluginToVectorMenu("KML Tools", self.htmlDescAction)
        # Help
        icon = QIcon(     os.path.join(os.path.dirname(os.path.abspath(__file__)), "e.png"))
        self.helpAction = QAction(icon, "Help", self.iface.mainWindow())
        self.htmlDescAction.setCheckable(False)
        self.helpAction.triggered.connect(self.show_custom_dialog)
        self.iface.addPluginToVectorMenu('KML Tools', self.helpAction)

        # Add the processing provider
    
    

from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from qgis.utils import iface  
class MyDialog(QDialog):
    def __init__(self):
        super().__init__(iface.mainWindow())
        self.setWindowTitle("Mi Ventana de Diálogo")
        
        layout = QVBoxLayout()
        label = QLabel("Esta es una ventana de diálogo personalizada en QGIS.")
        layout.addWidget(label)
        
        button = QPushButton("Cerrar")
        button.clicked.connect(self.close)
        layout.addWidget(button)
        
        self.setLayout(layout)
'''
'''