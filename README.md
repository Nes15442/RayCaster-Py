# 🤖 Lab 4: model Viewer

## 📡 Tecnologias Utilizadas
- Python 🐍: Modern syntax, Interpreted Languaje
  > Python 10.0 or higher needed

# ✅Rubrica

  - [x] (0 a 30 puntos) [Criterio subjetivo] Según la estética de su nivel
  - [x] (0 a 30 puntos) Según cuantos fps pueda renderizar su software (5 fps en promedio)
    - [x] 10 puntos mas por colocar un contador de fps
  - [x] (20 puntos) Por implementar una cámara con movimiento hacia delante y hacia atrás y rotación (como la que hicimos en clase)
    - [x] No debe poder atravesar a las paredes 
    - [x] 10 puntos más por implementar rotación con el mouse (solo horizontal)
  - [ ] (10 puntos) Por implementar un minimapa que muestre la posición de jugador en el mundo. No puede estar lado a lado del mapa principal, debe estar en una esquina. 
  - [x] (5 puntos) Por agregar música de fondo.
  - [ ] (10 puntos) Por agregar efectos de sonido
  - [ ] (20 puntos) Por agregar al menos 1 animación a alguna sprite en la pantalla
  - [x] (5 puntos) Por agregar una pantalla de bienvenida 
    - [x] (10 puntos mas) si la pantalla permite seleccionar entre multiples niveles 
  - [x] (10 puntos) Por agregar una pantalla de exito cuando se cumpla una condicion en el nivel


## 🗃️ Estructura de Archivos

- **`backgrounds`**: Imagenes de fondo (para menus y titulos)
- **`maps`**: mapas de niveles del juego.
  - `map1.txt`: Nivel 1
  - `map2.txt`: Nivel 2
  - `map3.txt`: Nivel 3
- **`sounds`**: Musica del juego.
- **`sprites`**: sprites para enemigos.
- **`Textures`**: Texturas para paredes.

- `cast.py`: Implementacion de rayCaster.
- `main.py`: Programa principal.

## ⚒️ Getting Started

1. Ejecute el archivo `main.py`.
2. Si no existen errores en ejecución, se abrira una ventana con el juego.

## 🕹️ Instrucciones

Cuando se abra la ventana de pygame se pueden usar los siguientes controles:

- `W`, `A`, `S`, `D` para moverse.
- Flechas `<-` y `->` para rotar.
- `click` para usar el mouse para rotar.
- `click` otra vez para dejar de usar el mouse para rotar.

## 🤓 Autor

Diego Cordova - 20212
