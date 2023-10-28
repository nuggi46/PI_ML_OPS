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


#Primera función
@app.get("/PlayTimeGenre/{genero}", name = "PLAYTIMEFORGENRE")
async def PlayTimeGenre(genero):
    anio= tabla_final[tabla_final["genres"]==  genero ]["Año de lanzamiento"].iloc[0]
    horas_jugadas= tabla_final[tabla_final["genres"]== genero]["Horas"].iloc[0]
    return {"El género": genero, "en el año de lanzamiento": int(anio),"tiene más horas jugadas": int(horas_jugadas)}



