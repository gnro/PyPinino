# -*- coding: utf-8 -*-
"""
/***************************************************************************
 cats
                                 A QGIS plugin
 Gato guardian
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-08-21
        git sha              : $Format:%H$
        copyright            : (C) 2023 by nemo
        email                : nemo@sea.co
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .CatWatch_dialog import catsDialog 
import os.path

class cats:
    def __init__(self, iface):
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'cats_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GatoVigilante')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('cats', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        self.dlg=catsDialog()
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)
        self.actions.append(action)
        return action

    def initGui(self):
        icon_path = ':/plugins/CatWatch/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        #self.first_start = True
        self.dlg.pushButton.clicked.connect(self.accede)
        self.dlg.pushButtonS.clicked.connect(self.salir)  

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&GatoVigilante'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""
        
        #self.dlg.qTxtPasswd.clear()
        self.dlg.qTxtUser.setText("gjimenez")
        self.dlg.qTxtPasswd.setText("123")
        if self.first_start == True:
            self.first_start = False
            self.dlg = catsDialog()

        # show the dialog
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            pass
    
    def handle_error(error):
        print(f'Error: {error}')
    
    def handle_response(self, response):
        # Manejar la respuesta aquí
        if response.error() == QNetworkReply.NoError:
            # La solicitud se completó correctamente
            data = response.readAll()
            # Procesar la respuesta JSON u otros datos aquí
            print(data)
        else:
            # Hubo un error en la solicitud
            self.handle_error(response.errorString())
    
    def accede(self):
        try:
            from .ApiRequests import carCapas
            rrr=carCapas("")
            passWd = self.dlg.qTxtPasswd.text()
            userS = self.dlg.qTxtUser.text()
            data = {
                "usuario":userS,
                "passwd": passWd,
                "verssion": 1,
                "sistema": "GEO"
            }
            #rrr.consumeGet("Gusanito")
            datos_diccionario = rrr.consumePost("initSesion", data)
            print(datos_diccionario["mensaje"])
            
            if (datos_diccionario["mensaje"]!='Inicio de sesión correcta'):
                QMessageBox.critical(self.iface.mainWindow(), "Error", "Usuario o contraseña incorrecta.")
                self.dlg.qTxtPasswd.clear()
                self.dlg.qTxtUser.clear()
                return
            else:
                self.cargaLayer()
        except Exception as e:
            print(f'Error al realizar la accede: {str(e)}')
        
    def cargaLayer(self):
        from qgis.core import QgsProject
        # Get the project instance
        project = QgsProject.instance()
       # project.read('D:/escritorio/carto_3.qgz')
        ifaceq=self.iface
       
        from qgis.PyQt.QtGui import QIcon
        icon = QIcon(":/plugins/CatWatch/icon.png")
        from .CatCapas import carCapas
        c= carCapas(ifaceq)
        c.limpiaCapas()
        c.cargaCapas()
        print(project.fileName())
        ifaceq.mainWindow().setWindowTitle("My QGIS")
        ifaceq.mainWindow().setWindowIcon(icon)
        self.dlg.hide()
        pass
    
    def salir(self):
        pass
    
