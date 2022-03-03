#%%
"""
inicio de programa 
"""
#librerias 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
#variabes fijas 
#hago el dataframe donde estara anidado los datos del Synergy
tabla_date = pd.read_csv('synergy_logistics_database.csv', index_col=0,parse_dates=['date'])
#hago un dataframe para amacenar los paises y su total_vallue por pais
países=tabla_date.groupby(['origin']).agg({"total_value":'sum'})
#ordenar los paises por el total_value
países_orden=países.sort_values('total_value',ascending=0)
UsuarioMenu=False
MenuPrincipal="""
1.-Rutas de importación y exportación.
2.-Medio de transporte utilizado
3.-Valor total de importaciones y exportaciones
4.-exit
"""
#funcion para calcular el flujo de trasporte 
def flujo(fila):
    """
    multiplico la Valor total de importaciones y exportaciones
    por la frecuencia de flujo para obtener el flujo de trasporte 
    que pasa por la ruta para mejorar la tabla se divide entre 10 mil el flujo 
    """  
    resultado=(fila['Valor total de importaciones y exportaciones']*fila['frecuencia de uso'])/10000
    return resultado
#funcion para calcular el porcentaje que aporta cada pais
def porcentaje(fila,total=países['total_value'].sum()):
    """
    para lograrlo se divide 
    Valor total de importaciones y exportaciones / el total de Valor total de importaciones y exportaciones
    hasta el momento por 100
    """
    resultado=(fila['total_value']/total)*100
    return resultado
#Menu rutas de importación y exportación 
def menu1():
    #  Rutas mas importantes de importación y exportación 
    """
    creo el dataframe que contendra las rutas donde contenga cada fila 
    la Valor total de importaciones y exportaciones de cada ruta se obtiene al usar la funcion sum()
    la frecuencia de uso que tiene cada ruta se obtiene al usar la funcion count() 
    también  renombro las columnas para mejorar el entendimiento de estas
    """
    rutas=tabla_date.groupby(["origin","destination",'transport_mode']).agg({
        "total_value":'sum','company_name':'count'})
    rutas=rutas.rename(columns={'total_value':'Valor total de importaciones y exportaciones',
        'company_name':'frecuencia de uso'})
    #introduzco la columna flujo por 10 mil, mediante la función  flujo
    rutas['flujo por 10 mil']=rutas.apply(flujo,axis=1)
    #creo el dataframe que tendrá  las 10 primeras rutas 
    top_rutas=rutas.sort_values('flujo por 10 mil',ascending=0)
    #imprimo el dataframe de manera ordenada para mejorar la presentacion 
    with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
        print(top_rutas.head(10))
#Valor total de importaciones y exportaciones
def menu2():
    #Medio de transporte utilizado
    """
    Creo el dataframe que contendra los medios de trasporte por año donde contenga cada fila
    la Valor total de importaciones y exportaciones que pasa por ese medio 
    para poder graficar se sube year y transport_mode para conformar una columna 
    """
    medio=tabla_date.groupby(['year','transport_mode']).agg({"total_value":'sum'}).rename(
        columns={'total_value':'Valor total de importaciones y exportaciones'}).reset_index(
        level=['year','transport_mode'])
    """
    creo un datafreme que estara ordenado por la Valor total de importaciones y exportaciones
    del mayor al menor y renombro year y transport_mode
    """
    medio_grafica=medio.sort_values('Valor total de importaciones y exportaciones',ascending=0).rename(
        columns={'transport_mode':'Modo de trasporte','year':'Año'})
    #a continuacion imprimo una grafica de tiempo de los modos de trasportes 
    sns.set_theme(style='darkgrid')
    sns.relplot(x="Año", y="Valor total de importaciones y exportaciones", hue="Modo de trasporte", 
        kind="line",data=medio_grafica)

def menu3():
    #Valor total de importaciones y exportaciones
    """
    haciendo uso de las variables fijas se crea un dataframe países por la Valor total de importaciones y 
    exportaciones con una columna donde se generara el porcentaje acumulado usando la funcion porcentaje y cumsum() 
    """
    países_orden['porcentaje_acumulado']=países_orden.apply(porcentaje,axis=1).cumsum()
    """
    ordeno el dataframe de mayor a menor segun su porcentaje acomulado 
    y renombro total_value por Valor total de importaciones y exportaciones
    """
    acumulado=países_orden.sort_values('porcentaje_acumulado').rename(columns={
        'total_value':'Valor total de importaciones y exportaciones'})
    #me quedo solo con los datos que generan el 80% acomulado 
    paises_grafica=acumulado[acumulado.porcentaje_acumulado<80]
    #mediante una grafica de pastel imprimo los datos resultantes 
    paises_grafica.plot(kind='pie',y='Valor total de importaciones y exportaciones', subplots=True, 
        shadow = True,startangle=30,
    figsize=(15,12), autopct='%1.1f%%')
#menu principal creado mediante while 
while not UsuarioMenu:
    print(MenuPrincipal) 
    opcion=input("introduzca un digito entre 1 y 4 \n") 
    if opcion== '1': 
        menu1()
    elif opcion == '2':
        menu2()
    elif opcion == '3':
        menu3() 
    elif opcion == '4': 
        exit() 
    else: 
        print("opcion no valida")
