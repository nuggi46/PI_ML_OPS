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
min_reviews2= pd.read_parquet("data/funcion_4.parquet")
sentimiento_analysis= pd.read_parquet("data/funcion_5.parquet")
modelo_item_3= pd.read_parquet("data/funcion_6.parquet")

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

@app.get("/UsersRecommend/{anio}", name = "USERSRECOMMEND")
async def UsersRecommend(anio:int):
    tabla1=max_reviews3[max_reviews3["year"] == anio]
    tabla1.reset_index()
    
    dato = tabla1[tabla1["year"]== anio]["app_name"].iloc[0]
    dato1 = tabla1[tabla1["year"]== anio]["app_name"].iloc[1]
    dato2 = tabla1[tabla1["year"]== anio]["app_name"].iloc[2]
    
    return {"Los juegos más recomendados para el año": anio, "Puesto 1": dato,"Puesto 2": dato1,"Puesto 3": dato2}

@app.get("/UsersNotRecommend/{anio}", name = "USERSNOTRECOMMEND")
async def UsersNotRecommend(anio:int):
    tabla11=min_reviews2[min_reviews2['year']== anio]
    tabla11.reset_index()
    
    dato0 = tabla11[tabla11["year"]== anio]["app_name"].iloc[0]
    dato11 = tabla11[tabla11["year"]== anio]["app_name"].iloc[1]
    dato22 = tabla11[tabla11["year"]== anio]["app_name"].iloc[2]
    
    return {"Los juegos menos recomendados para el año": anio, "Puesto 1": dato0,"Puesto 2": dato11,"Puesto 3": dato22}



@app.get("/sentiment_analysis/{anio}", name = "SENTIMENTANALYSIS")
async def sentiment_analysis(anio:int):
    
    reviews_por_anio=sentimiento_analysis[sentimiento_analysis["Año de lanzamiento"]== anio]
    
 
    Negativos = 0
    Neutral = 0
    Positivos = 0
    

    for i in reviews_por_anio["sentiment_analisis"]:
        if i == 0:
            Negativos += 1
        elif i == 1:
            Neutral += 1 
        elif i == 2:
            Positivos += 1

    count_sentiment ={"Negative": Negativos , "Neutral" : Neutral, "Positive": Positivos}
    
    return count_sentiment


@app.get("/recomendacion_juego/{item_id}", name = "RECOMENDACIONJUEGO")
async def recomendacion_juego(item_id):
    

    # Filtrar el juego e igualarlo a  su ID
    juego_seleccionado = modelo_item_3[modelo_item_3['item_id'] == item_id]
    # devolver error en caso de vacio
    if juego_seleccionado.empty:
        return "El juego con el ID especificado no existe en la base de datos."
    
    # Calcular la matriz de similitud coseno
    similitudes = cosine_similarity(modelo_item_3.iloc[:,3:])
    
    # Calcula la similitud del juego que se ingresa con otros juegos del dataframe
    similarity_scores = similitudes[modelo_item_3[modelo_item_3['item_id'] == item_id].index[0]]
    
    # Calcula los índices de los juegos más similares (excluyendo el juego de entrada)
    indices_juegos_similares = similarity_scores.argsort()[::-1][1:6]
    
    # Obtener los nombres de los juegos 5 recomendados
    juegos_recomendados = modelo_item_3.iloc[indices_juegos_similares]['app_name']
    
    return juegos_recomendados