import sweetviz as sv
import pandas as pd
import os,sys
class reporte():
    def __init__(self,path:str=None):
        super().__init__()
        self.path = path

    def reporte_simple(self,nombre:str,delimitador:str=';',sep='\\'):
        '''Se genera un reporte simple deacuerdo a los parametros ingresados y el sistema operativo'''
        path = os.path.abspath(os.getcwd())
        if nombre+'.html' in os.listdir('Reportes'+sep):
                os.system('start chrome '+path+'\\Reportes'+sep+nombre+'.html')
                print('start chrome '+path+'\\Reportes'+sep+nombre+'.html')
        else:
            df = pd.read_csv(self.path,delimiter=delimitador)
            reporte = sv.analyze(df) #Generamos un analisis basico
            reporte.show_html(filepath='Reportes'+sep+nombre+'.html') #Mostramos el analisis en formato HTML
        

        
    def asignacionDosisCovid19(self,opc1,opc2):
        df = pd.read_csv('Data\\AsignacionDosisCovid19.csv')
        df = df[df['Laboratorio_Vacuna'].isin([opc1,opc2])]
        reporte = sv.compare_intra(df,df['Laboratorio_Vacuna']==opc1,list(df.Laboratorio_Vacuna.unique()))
        reporte.show_html()