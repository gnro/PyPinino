import os
from datetime import datetime
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface

class MyBtn:
    def __init__(self):
        self.initUI()

    def initUI(self):
        try:
           
            action = QAction('Show', iface.mainWindow())
            action.triggered.connect(self.show_time)
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "p.png")
            icon = QIcon(icon_path)
            action.setIcon(icon)
            iface.addToolBarIcon(action)
            
        except Exception as e:
            print(f'Error al crear el botón: {str(e)}')
            
    def show_time(self):
        print("Cuack")
        self.show_custom_dialog()
        
    def show_custom_dialog(self):
        dialog = MyDialog()
        dialog.exec_()

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

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction

