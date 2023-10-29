"""
AQUI SE ENCUENTRAN LAS FUNCIONES CREADAS PARA EL PROYECTO INTEGRADOR 1 
MLOPS - STEAM GAMES - 

FUNCIONES PARA ALIMENTAR LA API
"""

#librerías
from fastapi import FastAPI
import pandas as pd


#instanciar la aplicación

app = FastAPI()


#dataframes que se utilizan en las funciones de la API
tabla_final = pd.read_parquet("data/funcion_1.parquet")
tabla_user2 = pd.read_parquet("data/funcion_2.parquet")
max_reviews3= pd.read_parquet("data/funcion_3.parquet")


#Primera función
@app.get("/PlayTimeGenre/{genero}", name = "PLAYTIMEFORGENRE")
async def PlayTimeGenre(genero):
    anio= tabla_final[tabla_final["genres"]==  genero ]["Año de lanzamiento"].iloc[0]
    horas_jugadas= tabla_final[tabla_final["genres"]== genero]["Horas"].iloc[0]
    return {"El género": genero, "en el año de lanzamiento": int(anio),"tiene más horas jugadas": int(horas_jugadas)}


@app.get("/UserForGenre/{genero}", name = "USERFORGENRE")
async def UserForGenre(genero):
    usuario= tabla_user2[tabla_user2["genres"]== genero]["user_id"].iloc[0] #obtengo usuario
    historial=tabla_user2[(tabla_user2['user_id'] == usuario) & (tabla_user2['genres']==genero)] #filtro por el genero y usuario
    historial2 = historial[['Año', 'Horas jugadas']].copy() #me quedo con las columnas necesarias
    historial3=historial2.to_dict(orient="records")
    return {"Usuario":usuario ,"con más horas jugadas para": genero, "Historial acumulado": historial3 }

@app.get("/UsersRecommend/{año}", name = "USERSRECOMMEND")
async def UsersRecommend(año:int):
    tabla1=max_reviews3[max_reviews3['year'] == año]
    tabla2=tabla1[['Acumulado', 'app_name','year']].copy() #me quedo con las columnas necesarias
    tabla2.reset_index()
    
    dato = tabla2[tabla2["year"]== año]["app_name"].iloc[0]
    dato1 = tabla2[tabla2["year"]== año]["app_name"].iloc[1]
    dato2 = tabla2[tabla2["year"]== año]["app_name"].iloc[2]
    
    return {"Los juegos más recomendados para el año": año, "Puesto 1": dato,"Puesto 2": dato1,"Puesto 3": dato2}