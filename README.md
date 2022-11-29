# 🤖 Lab 4: model Viewer

## 📡 Tecnologias Utilizadas
- Python 🐍: Modern syntax, Interpreted Languaje
  > Python 10.0 or higher needed

# ✅Rubrica

  - [x] 20 puntos por cada shader distinto que se implemente. Máximo de 3 shaders (pueden poner los shaders que quieran, pero solo los primeros 3 valen puntos, si el shader no hace nada más que pasar las variables al pipeline no cuenta).
  - [x] 10 puntos por utilizar texturas
  - [ ] 10 puntos por utilizar normales.
    > Utilizo las normales en los shaders solo por motivos esteticos
  - [x] 20 puntos por implementar una cámara (para que valga puntos, la cámara debe poder moverse o rotar)
  - [x] 20 puntos gratis!

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

