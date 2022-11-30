# 🤖 Lab 4: model Viewer

## 📡 Tecnologias Utilizadas
- Python 🐍: Modern syntax, Interpreted Languaje
  > Python 10.0 or higher needed

# ✅Rubrica

  - [x] (0 a 30 puntos) [Criterio subjetivo] Según la estética de su nivel
  - [x] (0 a 30 puntos) Según cuantos fps pueda renderizar su software
    - [x] 10 puntos mas por colocar un contador de fps
  - [x] (20 puntos) Por implementar una cámara con movimiento hacia delante y hacia atrás y rotación (como la que hicimos en clase)
    - [x] No debe poder atravesar a las paredes 
    - [x] 10 puntos más por implementar rotación con el mouse (solo horizontal)
  - [ ] (10 puntos) Por implementar un minimapa que muestre la posición de jugador en el mundo. No puede estar lado a lado del mapa principal, debe estar en una esquina. 
  - [x] (5 puntos) Por agregar música de fondo.
  - [ ] (10 puntos) Por agregar efectos de sonido
  - [ ] (20 puntos) Por agregar al menos 1 animación a alguna sprite en la pantalla
  - [x] (5 puntos) Por agregar una pantalla de bienvenida 
    - [ ] (10 puntos mas) si la pantalla permite seleccionar entre multiples niveles 
  - [x] (10 puntos) Por agregar una pantalla de exito cuando se cumpla una condicion en el nivel


## 🗃️ Estructura de Archivos

- **`models`**: Dentro de esta carpeta se encuentran los modelos a utilizar.
  - `PaperPunch.obj`: Objeto a renderizar.
  - `paperPunch_texture.tga`: Textura del objeto.

- **`src`**: Implementacion de lector de archivos .obj y shaders para OpenGL
  - `shaders.py`: Contiene los shaders a utilizar en openGL.
  - `Obj.py`: Lector de archivos .obj. (tambien carga el vertex_data)

- `main.py`: Programa principal.

## ⚒️ Getting Started

1. Ejecute el archivo `main.py`.
2. Si no existen errores en ejecución, se abrira una ventana con la enderizacion del modelo.

## 🕹️ Instrucciones

Cuando se abra la ventana de pygame se pueden usar los siguientes controles:
- `click` y `arrastrar`: para mover la camara (rotar el modelo)
- `1`, `2` y `3`: para cambiar de shader.
- `SpaceBar`: para cambiar de modo de renderizado.

## 🤓 Autor

Diego Cordova - 20212
