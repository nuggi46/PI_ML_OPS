<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>
# <h1 align=center> ![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas) ![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy) ![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib) ![Seaborn](https://img.shields.io/badge/-Seaborn-333333?style=flat&logo=seaborn) ![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-333333?style=flat&logo=scikitlearn) ![FastAPI](https://img.shields.io/badge/-FastAPI-333333?style=flat&logo=fastapi) ![TextBlob](https://img.shields.io/badge/-TextBlob-333333?style=flat&logo=textblob) ![Render](https://img.shields.io/badge/-Render-333333?style=flat&logo=render)
## PI_1-MLOps Juegos Steam - Modelo de recomendación

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300>
</p>

¡Bienvenidos a mi primer proyecto individual de la etapa de labs! En esta ocasión, realizaré un trabajo desde el rol de un ***MLOps Engineer***.  

<hr>  

## **Descripción del problema (Contexto y rol a desarrollar)**

## Contexto

Se debe desarrollar un modelo de sistema de recomendación basados en la plataforma de juegos Steam. Además se considera crear un `Producto Minimo Viable (MVP)`, que contenga una `API`deployada,el modelo de `Machine Learning` y distintas funcionas extras relacionadas a Steam.

El ciclo de vida de un proyecto de Machine Learning debe contemplar desde el tratamiento y recolección de los datos hasta el entrenamiento y mantenimiento del modelo de ML según llegan nuevos datos.


## Descripción del proyecto

Teniendo en cuenta que para este MVP no se necesita perfección, pero si rapidez. Las transformaciones a los datos, tratamiento de variables y creación de tablas serán basados bajo la premisa de velocidad, por lo tanto, para cada función creada, tendrá su propia tabla reducida y las funciones en la API serán exclusivamente para dicha tabla.

El proceso seria: ETL de datos -> EDA -> funciones para la API -> desarrollo de modelo de recomendación -> FastApi -> Deploy 

Habiendo hecho la introducción, los siguientes pasos en caso de replicación son los siguientes:

<br/>

**`Datos`**: Se procede a realizar la extracción, transformación y carga (ETL)

+ **output_steam_games.json** es un dataframe que contiene información sobre los juegos; como nombre del juego, editor, dessarrollador, precios, tags.

+ **australian_users_items.json** es un dataframe que contiene información sobre cada juego que utilizan los usuarios, y el tiempo que cada usuario jugo.

+ **autralian_users_reviews.json** es un dataframe que contiene los comentarios que los usuarios realizaron sobre los juegos que utilizan , recomendaciones o no de ese juego; además de datos como url y user_id.

El diccionaro de los [Dataset](/images/diccionario_games.JPG) 

Los archivos originales [Archivos de inicio](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj)

Los ETL se generaron los siguientes Notebooks [ETL_steam](/01.ETL_steam_games.ipynb), [ETL_reviews](/02.ETL_users_reviews.ipynb) y [ETL_items](/03.ETL_users_items.ipynb). 
En esta misma etapa se construyo el analisis de sentimientos para la tabla user_reviews, ya que formaria parte de las funciones y el EDA más adelante.

Terminada la limpieza se generan los dataset para la siguiente fase en formato CSV

<br/>

**`Análisis exploratorio de los datos`**: _(Exploratory Data Analysis-EDA)_

Ya los datos están limpios, ahora es tiempo de investigar las relaciones que hay entre las variables de los datasets, ver si hay outliers o anomalías (que no tienen que ser errores necesariamente :eyes: ), y ver si hay algún patrón interesante que valga la pena explorar en un análisis posterior.

En el siguiente notebook se puede ver las distintas conclusiones [Analisis exploratorio](/04.EDA.ipynb)

<br/>

**`Desarrollo de API`**: 

Para el desarrolo de la API se utiliza el framework FastAPI, creando las siguientes funciones solicitadas:

+ def **PlayTimeGenre( *`genero` : str* )**:
    Debe devolver `año` con mas horas jugadas para dicho género.
  
    Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

+ def **UserForGenre( *`genero` : str* )**:
    Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

    Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf,
			     "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

+ def **UsersRecommend( *`año` : int* )**:
   Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
  
    Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

+ def **UsersNotRecommend( *`año` : int* )**:
   Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
  
    Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

+ def **sentiment_analysis( *`año` : int* )**:
    Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento. 

    Ejemplo de retorno: {Negative = 182, Neutral = 120, Positive = 278}

Para acceder la construcción de funciones luego del ETL, se puede acceder al siguiente notebook [Construcción Funciones](/05.funciones.ipynb)

Cada función tiene su propia tabla tanto en csv y parquet. La api se alimentará directamente desde parquet, si se quiere acceder a estas tablas, se puede acceder [Dataset API](https://github.com/nuggi46/PI_ML_OPS/tree/main/data)

<br/>

**`Sistema de recomendación`**: 

Una vez que toda la data es consumible por la API, está lista para consumir por los departamentos de Analytics y Machine Learning, y nuestro EDA nos permite entender bien los datos a los que tenemos acceso, es hora de entrenar nuestro modelo de machine learning para armar un sistema de recomendación. 

A partir de la data `steam_games`, con los item_id, generos y nombres de videojuegos se creo el modelo de recomendación.
El mismo se puede acceder al notebook [Modelado](/06.sistema_recomendacion.ipynb). 

+ def **recomendacion_juego( *`item_id` : int* )**: 
 Esta función recibe como parametro el "id" de un titulo de juego y devuelve una lista con 5 juegos recomendacos similares al ingresado tomando como base de similitus el genero. Realizando una comparación  `item_item`

<br/>

**`FastAPI`**:

El código para generar la API se encuentra en el archivo [Main](/main.py).
  
<br/>

**`Deploy`**:

Para el deploy de la API se seleccionó la plataforma Render que es una nube unificada para crear y ejecutar aplicaciones y sitios web, permitiendo el desplegue automnático desde GitHub. 

* Se generó un nuevo servicio en `render.com`, conectando a este repositorio

* Se genera el link donde queda corriendo https://steam-zc5j.onrender.com/docs

<br/>

**`Video`**:

Demostración y funcionamiento de la API se encuentra en ele siguiente [Video]

<br/>

**`Conclusiones`**:

Se logra obtener un modelo automatizado con los criterios MPV. En caso de disponer mayor memoria en el render y tiempo, las funciones y todo el desarrollo del modelo se podrían optimizar aún más, ya basados en la eficencia y no solamente en la rapidez de obtener el modelo.
