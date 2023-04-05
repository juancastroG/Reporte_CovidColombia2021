import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

     

def convertidor(row:str):
  if row.startswith('Segunda'):
    return 'Segunda Dosis'
  else: 
    return row

def etapas(row,clas):
  if row in clas[0] or row in clas[9] or row in clas[2]:
    return '1ra Fase'
  elif row in clas[5:8] or row in clas[10:14]:
    return '2da Fase'
  elif row in clas[-5] or row in clas[14:19] or row in clas[-6]:
    return '3ra Fase'
  elif row in clas[1]:
    return '4ta Fase'
  else:
    return '5ta Fase/Vacunacion abierta'
  
def categoriaXFase(opcion):
  df = data()
  dfCategorias = pd.DataFrame(df[df['Etapa']==opcion])
  figura = barrasEtapasPl(dfCategorias)
  return list(dfCategorias.Uso_vacuna.unique()), figura


def agrupar(df,opcion):
  return pd.DataFrame(df.groupby(opcion)['Cantidad'].sum())
    
def data():
        '''Se hace el filtro de datos y correcciones'''

        df_asigancion = pd.read_csv('C:\Juank\FreeLancer\CasosCovid\Data\Data\AsignacionDosisCovid19 (1).csv')
        #df_asigancion = pd.DataFrame(df_asigancion[df_asigancion['Fecha_Resolucion']<'2021/07/31'])
        df_asigancion.Fecha_Resolucion = pd.to_datetime(df_asigancion.Fecha_Resolucion)
        df_asigancion['mes'] = df_asigancion.Fecha_Resolucion.dt.month
        df_asigancion.mes.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'),inplace=True)
        df_asigancion['semana'] = df_asigancion.Fecha_Resolucion.dt.week
        df_asigancion['dias'] = df_asigancion.Fecha_Resolucion.dt.day
        df_asigancion.dropna(inplace=True)
        df_asigancion['Acum_Asig']=df_asigancion.Cantidad.cumsum(axis=0)
        df_asigancion.Uso_vacuna = df_asigancion['Uso_vacuna'].apply(convertidor)
        df_asigancion.Uso_vacuna.replace({'PILOTOS FFMM':'FFMM',
                                  'PILOTOS POLICIA':'POLICÍA',
                                  'PILOTOS FISCALÍA':'FISCALÍA',
                                  'PILOTOS MEN':'MEN Básica',
                                  'Unificaciòn San Andrès':'Territorio Unificado',
                                  '55 a 59 años':'50 A 59 años',
                                  'Municipios - Etapas abiertas - Mayores de 18':'Etapas Abiertas',
                                  'Ciudades - Etapas abiertas':'Etapas Abiertas'},inplace=True)
        clasificacion = list(df_asigancion.Uso_vacuna.unique())
        df_asigancion['Etapa'] = df_asigancion.Uso_vacuna.apply(etapas,args=([clasificacion]))
        
        
        return df_asigancion

def barrasEtapasPl(df):
  
  dfCategorias = agrupar(df,'Uso_vacuna')
  dfCategorias.reset_index(inplace=True)
  grafica = px.bar(dfCategorias,x='Uso_vacuna',y='Cantidad',color='Uso_vacuna')
  return grafica
  

def pastel(opcion:str):
        df_pastel=data() #Obtener los datos
        df_pastel = agrupar(df_pastel,opcion)
        
        # Crear y devolver objetos de figura y objetos de subgrafo de ejes
        fig, ax = plt.subplots(figsize=(12, 6))
        recipe_data = df_pastel.Cantidad
        recipe_labels = df_pastel.index


        # Función utilizada para especificar el formato de salida
        def func(pct, allvals):
            absolute = int(pct/100.*np.sum(allvals))
            return "{:.1f}%\n({:d})".format(pct, absolute)


        wedges, texts, autotexts = ax.pie(x=recipe_data,shadow=True, startangle=90,
                                  labels=recipe_labels,
                                   autopct = '% 1.1f %%',# dos formas seguidas de autopct Este formato es como un decimal con un porcentaje de 12.3%
                                  #autopct=lambda pct: func(pct ,recipe_data),
                                  
                                  #colors=colors,
                                  pctdistance=0.7,
                                  textprops=dict(color="w"),  # Establecer blanco no verá el texto fuera del círculo (el fondo es blanco)
                                  # Establecer la proporción del anillo a la mitad
                                  wedgeprops = {'width': 0.5, 'linewidth': 1, 'edgecolor':'w'}
                                  )

        # Establecer algunas propiedades en la leyenda
        ax.legend(wedges, recipe_labels,
          title="leyenda",
          title_fontsize=15,
          fontsize=17,
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
        plt.axis('equal')
        plt.setp(autotexts, size=12, weight="bold")    # Tamaño del texto y similares
        ax.set_title("Grafico de vacunas Asignadas por Mes y/o laboratorio", fontdict={'fontsize':15, 'fontweight':15})

        return plt.gcf()

def boxplot(df,dpto1,dpto2,dpto3,dpto4,agrup=None):
  df = df[df.Nom_Territorio.isin([dpto1,dpto2,dpto3,dpto4])]
  #TODO agrupar por semana y mostrar el grafico por semanas mediante un boton o checkbox mes/entrega/semana
  #df = agrupar(df,['Laboratorio_Vacuna','Nom_Territorio'])
  if agrup != 'Fecha de asignación':
    df = df.groupby(['Laboratorio_Vacuna','Nom_Territorio',agrup])['Cantidad'].sum()
  df = df.reset_index()
  figura = px.box(df,x='Laboratorio_Vacuna',y='Cantidad',color='Nom_Territorio')
  
  return figura

def violin(df,dpto1,dpto2,dpto3,dpto4,agrup=None):
  df = df[df.Nom_Territorio.isin([dpto1,dpto2])]
  if agrup != 'Fecha de asignación':
    df = df.groupby(['Laboratorio_Vacuna','Nom_Territorio',agrup])['Cantidad'].sum()
  df = df.reset_index()
  #TODO violin/strip
  figura = px.strip(df,x='Laboratorio_Vacuna',y='Cantidad',color='Nom_Territorio')

  return figura

def regresionAsignacion(df,tipoR,vacuna,dpto:str='Opcional'):
  
  df =  df[df.Laboratorio_Vacuna == vacuna]

  if 'Opcional' not in dpto:
    df =  df[df.Nom_Territorio.isin(dpto)]

  if tipoR:
    tipo = 'ols'
  else:
    tipo = 'lowess'
  figura = px.scatter(df,x='Fecha_Resolucion',y='Cantidad',trendline=tipo)
  
  model = px.get_trendline_results(figura)
  if tipoR:
   figura.data[1].line.color = 'red'
   alpha = model.iloc[0]["px_fit_results"].params[0]
   beta = model.iloc[0]["px_fit_results"].params[1]
  else:
   beta=0
   alpha=0
  return figura, beta, alpha

  
def scatter_asiganciones(df,dpto:str = None):
  if dpto != None:
    df =  df[df.Nom_Territorio==dpto]
  #figura = px.scatter(df,x='Fecha_Resolucion',y='Cantidad',color='Laboratorio_Vacuna')
  figura = px.scatter(df,x='Fecha_Resolucion',y='Acum_Asig',color='Laboratorio_Vacuna')
  
  return figura

def line_asignaciones  (df,dpto:str=None):
  if dpto != None:
    df =  df[df.Nom_Territorio==dpto]
  figura = px.line(df,x='Fecha_Resolucion',y='Acum_Asig',color='Laboratorio_Vacuna',)
  return figura

def barrasCom(dpto1):
  df = pd.read_csv('Data\\PlanVacunacion.csv',delimiter=';')
  df1 = df[df['Entidad Territorial']==dpto1]
  
  #TODO Convertir header a una columna para el grafico de barras
  df1 = df1.T
  df1 = df1.reset_index()
  df1.columns=['Distribucion','Cantidad']
  df1 = df1.drop([0,6,7,8,9])
  
  
  grafica = px.bar(df1,x=df1.columns[0],y=df1.columns[1],color=df1.columns[0])
  return grafica

def webApp():
        st.set_page_config(page_title='Visualizacion Casos Covid',page_icon='🦠')
        st.title('Analisis de vacunas del Covid-19')
        st.sidebar.header('Menu de Opciones')
        st.sidebar.write('---')
        st.sidebar.subheader('Grafica de pastel')
        opcion = st.sidebar.multiselect('Escoge al menos una opcion',['mes','Laboratorio_Vacuna','Nom_Territorio','Uso_vacuna','Etapa'],default='mes')
        if  not opcion:
            st.error('Por favor seleccione al menos una opcion')
        else:
            st.pyplot(pastel(opcion=opcion))
        df = data()
        st.write('---')
        st.title('Analisis por Etapa de vacunación')
        st.sidebar.write('---')
        st.sidebar.subheader('Grafica de barras')
        opcion = st.sidebar.selectbox('Seleccione una fase para graficar: ',('1ra Fase','2da Fase','3ra Fase',
        '4ta Fase',  '5ta Fase/Vacunacion abierta'))
        categorias, figura = categoriaXFase(opcion)
        st.write('La opcion: ', opcion,' Incluye: ',categorias)
        st.plotly_chart(figura)
        st.sidebar.write('---')
        st.sidebar.subheader('Grafica de Caja y violin')
        index_Bogota = list(df.Nom_Territorio.unique()).index('BOGOTA D.C.')
        agruparPor = st.sidebar.selectbox('Por favor seleccione por que desea agrupar los datos',['semana','mes','Fecha de asignación'])
        dpto1 = st.sidebar.selectbox('Por favor seleccione un Territorio',df.Nom_Territorio.unique(),index=index_Bogota)
        dpto2 = st.sidebar.selectbox('Por favor seleccione el segundo Territorio para comparar',df.Nom_Territorio.unique(),index=index_Bogota)
        dpto3 = st.sidebar.selectbox('Por favor seleccione el Tercer Territorio para comparar',df.Nom_Territorio.unique(),index=index_Bogota)
        dpto4 = st.sidebar.selectbox('Por favor seleccione el Cuarto Territorio para comparar',df.Nom_Territorio.unique(),index=index_Bogota)
        grafica = boxplot(df,dpto1,dpto2,dpto3,dpto4,agruparPor)
        st.write('---')
        st.title('Analisis por departamentos')
        st.plotly_chart(grafica)
        grafica = violin(df,dpto1,dpto2,dpto3,dpto4,agruparPor)
        st.plotly_chart(grafica)

        st.sidebar.write('---')
        st.sidebar.subheader('Grafica de puntos y lineas')
        index_Bogota = list(df.Nom_Territorio.unique()).index('BOGOTA D.C.')
        #agruparPor = st.sidebar.selectbox('Por favor seleccione por que desea agrupar los datos',['semana','mes','Fecha de asignación'])
        dpto_scatter = st.sidebar.selectbox('Por favor seleccione un Territorio para la grafica de puntos y lineas',df.Nom_Territorio.unique(),index=index_Bogota)
        

        st.write('---')
        st.title('Analisis de asignacion de dosis')
        st.plotly_chart(scatter_asiganciones(df,dpto_scatter))
        st.plotly_chart(line_asignaciones(df,dpto_scatter))

        #Regresion linear
        st.sidebar.write('---')
        st.sidebar.subheader('Grafica de puntos y lineas')
        opciones = list(df.Nom_Territorio.unique())
        
        opciones.append('Opcional')
        dptoMulti = st.sidebar.multiselect('Escoge al menos una opcion',opciones, default='Opcional')
        tipoR = st.sidebar.checkbox('Regresion Lineal')
        vacuna = st.sidebar.selectbox('Seleccione un tipo de vacuna',df.Laboratorio_Vacuna.unique())
        figura, alpha, beta = regresionAsignacion(df,tipoR,vacuna,dptoMulti)       
        st.write('---')
        st.title('Prediccion de vacunas')
        st.write('Alpha = {}\n Beta = {}'.format(alpha,beta))
        st.plotly_chart(figura)

        #Comparar reparticion de vacunas por dpto
        df = pd.read_csv('Data\\PlanVacunacion.csv',delimiter=';',encoding='latin1')
        st.sidebar.write('---')
        st.sidebar.subheader('Grafica de barras distribucion vacunas')
        dptoB1 = st.sidebar.selectbox('Por favor seleccione un Territorio para la grafica de barras',df['Entidad Territorial'].unique(),index=index_Bogota)
        dptoB2 = st.sidebar.selectbox('Por favor seleccione otro Territorio para la grafica de barras',df['Entidad Territorial'].unique(),index=index_Bogota)
        st.write('---')
        st.title('Grafico de barras distribucion de vacunas')
        st.header(dptoB1)
        st.plotly_chart(barrasCom(dptoB1))
        st.header(dptoB2)
        st.plotly_chart(barrasCom(dptoB2))
        



if __name__ == '__main__':
    webApp()
