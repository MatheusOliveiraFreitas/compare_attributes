# -*- coding: utf-8 -*-
"""
/***************************************************************************
 attributes
                                 A QGIS plugin
 Compare Attributes
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-02-19
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Matheus Oliveira de Freitas
        email                : matheus18.1@yahoo.com
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
from ast import Expression, While
from asyncio.windows_events import NULL
from dataclasses import fields
from math import fabs
from tarfile import NUL
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from PyQt5.QtCore import QVariant
from qgis.core import *

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .Compare_attributes_dialog import attributesDialog
import os.path
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from osgeo import ogr
import processing
from qgis.core import QgsVectorLayer,QgsProject,QgsVectorDataProvider,QgsField,QgsFields,QgsFeature,QgsVectorFileWriter
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsWkbTypes


class attributes:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'attributes_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Compare Attributes')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('attributes', message)


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
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

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
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Compare_attributes/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Compare Attributes'),
                action)
            self.iface.removeToolBarIcon(action)


    def carregaVetor(self):
        """CArregar VETOR"""
        #UPLOAD VECTOR
        self.dlg.comboBox.clear()
        lista_layers =[layer for layer in QgsProject.instance().mapLayers().values()]
        lista_layers_vetor = []
        for layer in lista_layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                lista_layers_vetor.append(layer.name())
        self.dlg.comboBox.addItems(lista_layers_vetor)
        
    def carregaVetor_2(self):
        """CArregar VETOR"""
        #UPLOAD VECTOR
        self.dlg.comboBox_3.clear()
        lista_layers_2 =[layer for layer in QgsProject.instance().mapLayers().values()]
        lista_layers_vetor_2 = []
        for layer in lista_layers_2:
            if layer.type() == QgsMapLayer.VectorLayer:
                lista_layers_vetor_2.append(layer.name())
        self.dlg.comboBox_3.addItems(lista_layers_vetor_2)


    def abrirVetor(self):
        #It will open the folders to add to the project        #traduzir
        camada_abrir=str(QFileDialog.getOpenFileName(caption="Input layer,......", 
                                                        filter="Shapefiles(*.shp)")[0])
        #Nao pode ser vazio
        if (camada_abrir != ""):
            self.iface.addVectorLayer(camada_abrir, str.split(os.path.basename(camada_abrir),".")[0], "ogr")
            self.carregaVetor()

    def camadaEnt(self):
        #Layer 1
        layer=None
        self.nomecamada=self.dlg.comboBox.currentText()
        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.name()==self.nomecamada:
                layer=lyr
                break
        return layer
    
    def camadaEnt_2(self):
        #Layer 2
        layer=None
        self.nomecamada_2=self.dlg.comboBox_3.currentText()
        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.name()==self.nomecamada_2:
                layer=lyr
                break
        return layer 
       
    def definirSaida(self):
        """SALVAR A SAIDA"""
        #Traduzir/// Select Output Folder
        camada_salvar=str(QFileDialog.getSaveFileName(caption="Select Output Folder, ......", 
                                                            filter="Shapefiles(*.shp)")[0])
        self.dlg.lineEdit.setText(camada_salvar)

    def definirSaida_2(self):
        """SALVAR A SAIDA"""
        #Traduzir///Select Output Folder
        camada_salvar=str(QFileDialog.getSaveFileName(caption="Select Output Folder, ......", 
                                                            filter="Shapefiles(*.shp)")[0])
        self.dlg.lineEdit_2.setText(camada_salvar)

    def coluna1(self):
        self.dlg.comboBox_2.clear()
        #self.dlg.comboBox_2.addItem("Selecione a coluna:")
        #Layer Column
        camada=None
        nome_camada01=self.dlg.comboBox.currentText()
        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.name()==nome_camada01:
                camada=lyr
                break
        if camada:
            campos=camada.fields()
            for campos in campos:
                self.dlg.comboBox_2.addItem(campos.name())
        self.dlg.comboBox.currentIndexChanged.connect(self.coluna1)
        

    def coluna2(self):
        self.dlg.comboBox_4.clear()
        #self.dlg.comboBox_4.addItem("Selecione a coluna:")
        #Layer Column
        camada=None
        nome_camada01=self.dlg.comboBox_3.currentText()
        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.name()==nome_camada01:
                camada=lyr
                break
        if camada:
            campos=camada.fields()
            for campos in campos:
                self.dlg.comboBox_4.addItem(campos.name())
        self.dlg.comboBox_3.currentIndexChanged.connect(self.coluna2)

    def variais(self):
        #Entrada
        #Input layer
        self.camada=self.camadaEnt()
        self.camada_2=self.camadaEnt_2()

        #Saida///Select Output Folder
        self.saida=self.dlg.lineEdit.text()
        self.saida_2=self.dlg.lineEdit_2.text()

        self.tres_primeiras_letras = self.nomecamada_2[:3]
        #Tabela Selecionada////Selected Table
        self.tabela_1=self.dlg.comboBox_2.currentText()
        self.tabela_2=self.dlg.comboBox_4.currentText()
        self.tabela_2_pr=self.tabela_2 + '_' + self.tres_primeiras_letras
        
        

        # Identificar o tipo da geometria da camada 1///Identify the type of layer 1 geometry
        tipo=self.camada.geometryType()

        if tipo==QgsWkbTypes.PointGeometry:
            self.rep=QgsWkbTypes.Point

        elif tipo==QgsWkbTypes.LineGeometry:
            self.rep=QgsWkbTypes.LineString

        elif tipo==QgsWkbTypes.PolygonGeometry:
            self.rep=QgsWkbTypes.Polygon

        elif tipo==QgsWkbTypes.MultiPoint:
            self.rep=QgsWkbTypes.MultiPoint

        elif tipo==QgsWkbTypes.MultiLineString:
            self.rep=QgsWkbTypes.MultiLineString

        elif tipo==QgsWkbTypes.MultiPolygon:
            self.rep=QgsWkbTypes.MultiPolygon
        


            

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = attributesDialog()

        # show the dialog
        self.dlg.show()
        
        #Load vector    
        self.carregaVetor()
        self.carregaVetor_2()

        #Abrir Vetor///Open Vector
        self.dlg.toolButton.clicked.connect(self.abrirVetor)
        self.dlg.toolButton_3.clicked.connect(self.abrirVetor)

        #Definir saida///Set output
        self.dlg.toolButton_2.clicked.connect(self.definirSaida)
        self.dlg.toolButton_4.clicked.connect(self.definirSaida_2)
        
        #select the column
        self.coluna1()
        self.coluna2()



        # Run the dialog event loop
        result = self.dlg.exec_()
        #Desconectar os botoes de abrir///Disconnect the open buttons
        self.dlg.toolButton.clicked.disconnect(self.abrirVetor)
        self.dlg.toolButton_3.clicked.disconnect(self.abrirVetor)

        #Desconectar os botoes de saida///Disconnect the exit  buttons
        self.dlg.toolButton_2.clicked.disconnect(self.definirSaida)
        self.dlg.toolButton_4.clicked.disconnect(self.definirSaida_2)


        # See if OK was pressed
        if result:
            self.variais()

            
            #Retirar os valores nao nulos da coluna da camada 1///Remove non-null values ​​from the layer 1 column
            limpo1=processing.run("native:extractbyexpression",
                                 {'INPUT':self.camada,
                                  'EXPRESSION':f'"{self.tabela_1}" is not NUL',
                                  'OUTPUT':'memory:'})
            
            #Retirar os valores nao nulos da coluna da camada 2///Remove non-null values ​​from the layer 2 column
            limpo2=processing.run("native:extractbyexpression",
                                 {'INPUT':self.camada_2,
                                  'EXPRESSION':f'"{self.tabela_2}" is not NULL',
                                  'OUTPUT':'memory:'})

            
            #QgsProject.instance().addMapLayer(limpo1['OUTPUT'])
             
            # Saber o tipo da coluna ///Know the column type
            oi = limpo2['OUTPUT']
            col = oi.fields()                        
            coli1 = limpo1['OUTPUT']            
            Col1= coli1.fields()
            for ti in col:
                if ti.name()==self.tabela_2:
                    tipo_da_2=ti.typeName()
            for ti in Col1:
                if ti.name()==self.tabela_1:
                    tipo_da_1=ti.typeName()
                    
            if  tipo_da_1 ==tipo_da_2:
                #Traduzir
                atr=f"Compatible Column Type{tipo_da_1}={tipo_da_2} "
                
                
                
            # Caso os tipos da coluna for diferente vira tudo str e foda-se///If the column types are different, everything changes
            else:
                #Traduzir
                atr=f"Incompatible Column Type {tipo_da_1} != {tipo_da_2}, the columns were converted to text type "
                #atr1='d'
                
                #Troca o tipo para String da camada 1///Change the type to String from layer 1
                
                if tipo_da_1 != 'string':
                
                    idx = limpo1['OUTPUT'].fields().indexFromName(self.tabela_1)
 
                    # Iniciar edição da camada1//Start layer editing1
                    limpo1['OUTPUT'].startEditing()
                     
                    # Convertendo o tipo da coluna para string//Converting column type to string
                    limpo1['OUTPUT'].dataProvider().changeAttributeValues({f.id(): {idx: str(f[self.tabela_1])} for f in limpo1['OUTPUT'].getFeatures()})
                     
                    # Terminar a edição da camada1///Finish editing the layer 1
                    limpo1['OUTPUT'].commitChanges()
                    
                                 
                #Troca o tipo para String da camada 2 ///Change the type to String from layer2
                elif tipo_da_2 !='string':
                    idx_2 = limpo2['OUTPUT'].fields().indexFromName(self.tabela_2_pr)
 
                    # Iniciar edição da camada2//Start layer editing2
                    limpo2['OUTPUT'].startEditing()
                     
                    # Convertendo o tipo da coluna para string//Converting column type to string
                    limpo2['OUTPUT'].dataProvider().changeAttributeValues({f.id(): {idx_2: str(f[self.tabela_2_pr])} for f in limpo2['OUTPUT'].getFeatures()})
                     
                    # Terminar a edição da camada2///Finish editing the layer 2
                    limpo2['OUTPUT'].commitChanges()


                    
            #QgsProject.instance().addMapLayer(limpo2['OUTPUT']) 
            #QgsProject.instance().addMapLayer(limpo1['OUTPUT'])      
            provider = limpo2['OUTPUT'].dataProvider()

            fields = provider.fields()                     

            for i in range(fields.count()):
                field = fields[i]
                new_name = field.name() +'_' + self.tres_primeiras_letras
                limpo2['OUTPUT'].startEditing()
                limpo2['OUTPUT'].renameAttribute(i, new_name)
                limpo2['OUTPUT'].commitChanges()

            # Obtenha os campos atualizados de limpo2['OUTPUT']///Get the updated fields from limpo2['OUTPUT']
            fields2 = limpo2['OUTPUT'].dataProvider().fields()

            # Adicione os campos de limpo2['OUTPUT'] a limpo1['OUTPUT']///Add the fields from limpo2['OUTPUT'] a limpo1['OUTPUT']
            limpo1['OUTPUT'].dataProvider().addAttributes(fields2)
            limpo1['OUTPUT'].updateFields()

            # Obtenha os campos atualizados de limpo1['OUTPUT']///Get the updated fields from limpo1['OUTPUT']
            fields = limpo1['OUTPUT'].dataProvider().fields()
            
            #QgsProject.instance().addMapLayer(limpo1['OUTPUT'])

            
                    

            # Camada a ser gerada///Layer to be generated
            camada_gerada = QgsVectorFileWriter(self.saida, "UTF-8", fields, self.rep , self.camada.crs(),'ESRI Shapefile')

            for C1 in limpo1['OUTPUT'].getFeatures():
                for C2 in limpo2['OUTPUT'].getFeatures():
                    # Verificar se as feições têm atributos comuns///Check if features have common attributes
                    if C1[self.tabela_1] == C2[self.tabela_2_pr]:
                        # Criar uma nova feição
                        feature = QgsFeature(fields)
                        feature.setAttribute(f"{self.tabela_1}", C1[f"{self.tabela_1}"])
                        feature.setAttribute(f"{self.tabela_2_pr}", C2[f"{self.tabela_2_pr}"])

                        for atributo in C1.fields():
                            feature.setAttribute(atributo.name(), C1[atributo.name()])
                        for atributo in C2.fields():
                            feature.setAttribute(atributo.name(), C2[atributo.name()])
                        geometry = C1.geometry() 
                        feature.setGeometry(geometry)
                        camada_gerada.addFeature(feature)

            #Deletar                    
            del camada_gerada
                                            

                           
            
            caminho=self.saida                   
            self.iface.addVectorLayer(caminho, str.split(os.path.basename(caminho),".")[0], "ogr")

            while True:
                contar2=len(self.saida_2)
                if contar2>=2:
                    local_1=processing.run("native:extractbylocation", 
                                {'INPUT':self.camada,
                                'INTERSECT':self.saida,
                                'PREDICATE': [2],
                                'OUTPUT': 'memory:'})
                    limpo_01=processing.run("native:extractbyexpression",
                                 {'INPUT':local_1['OUTPUT'],
                                  'EXPRESSION':f'"{self.tabela_1}" is not NUL',
                                  'OUTPUT':'memory:'})
                    caminho2=self.saida_2
                    nome1=limpo_01['OUTPUT']            
                    res=QgsVectorFileWriter.writeAsVectorFormat(nome1,caminho2,"utf-8",nome1.crs(),"ESRI Shapefile")                   
                    self.iface.addVectorLayer(caminho2, str.split(os.path.basename(caminho2),".")[0], "ogr")
                    #Mensagem no finalizador/// Traduzir
                    opi=str(f"A Shape was generated with the unique attributes of Shapes {self.nomecamada}")
                    break
                else:
                #Traduzir
                    opi=str(f"A Shape with the unique attributes of Shapes was not generated {self.nomecamada}")
                    break
                    pass
                    
            #Limpar a saida  ///Clean the exit                                           
            self.dlg.lineEdit.clear()
            self.dlg.lineEdit_2.clear()
            
            #Abrir uma janela com resultado//traduzir
            mensagem = QMessageBox()
            mensagem.setWindowTitle("Finishing")
            mensagem.setText(f"\n Shapefile 1: {self.nomecamada}; Selected Column= {self.tabela_1}.\n Shapefile 2: {self.nomecamada_2}; Selected Column= {self.tabela_2}.\n Optional File: {opi}. {atr}\n")
            mensagem.exec_()
        
            pass