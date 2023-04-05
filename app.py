from PyQt5.QtWidgets import QApplication, QMainWindow
from mainUI import MainWindow
import sys, os
import ReporteRapido as rr
import subprocess



class app(QMainWindow): #Creamos la clase que contendra la interfaz prinicpal
    def __init__(self) -> None: #Creamos el constructor de la clase
        super().__init__() #Inicializamos e contructor del padre
        self.ui = MainWindow() #heredamos todo los objetos de la interfaz a la variable self.ui
        self.ui.setupUi(self) 
        self.show() #Mostramos la interfaz
        self.comboBoxRR() #Añadimos los elementos al comboBox
        
        # FUNCIONALIDAD BOTONES
        self.ui.btn_ReporteSV.clicked.connect(self.reporteSV)
        self.ui.btn_AplicativoWeb.clicked.connect(self.reporteWeb)
        self.ui.btn_Comparar.clicked.connect(self.reporteCom)


    def comboBoxRR(self):
        '''Añadimos los elementos al  comboBox de Reporte Rapido'''
        self.ui.cmbB_Opcion1.addItems(['PFIZER','SINOVAC','ASTRAZENECA','MODERNA','JANSSEN'])
        self.ui.cmbB_Opcion2.addItems(['PFIZER','SINOVAC','ASTRAZENECA','MODERNA','JANSSEN'])
        archivos = os.listdir('Data/')
        archivos_combo = [i[:-4] for i in archivos]
        self.ui.cmbB_ReporteSV.addItems(archivos_combo)

    def reporteSV(self):
        '''Se genera un reporte Rapido'''
        
        path = 'Data/'+self.ui.cmbB_ReporteSV.currentText()+'.csv'
        nombre = self.ui.cmbB_ReporteSV.currentText()
        sep = os.path.sep
        generador = rr.reporte(path)
        if 'AsignacionDosisCovid19' in path:
            generador.reporte_simple(nombre,delimitador=',',sep=sep)
        else:
            generador.reporte_simple(nombre,sep=sep)
        
    def reporteWeb(self):
        subprocess.run(['streamlit','run','ReporteST.py'])
        
    
    def reporteCom(self):
        opc1 = self.ui.cmbB_Opcion1.currentText()
        opc2 = self.ui.cmbB_Opcion2.currentText()
        rr.reporte().asignacionDosisCovid19(opc1,opc2)


if __name__ == "__main__": #Creamos la clase principal
    aplicacion = QApplication([])   
    #aplicacion.setStyle('windowsvista')
    dialog = app()
    dialog.show()
    sys.exit(aplicacion.exec_())    #Cierra el bucle que muestra la interfaz