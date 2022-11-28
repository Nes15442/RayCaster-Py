import pygame
import numpy
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
from shaders import shaders
from src.Obj import *

if __name__ == '__main__':
  # ----------- Pygame Init -----------
  pygame.init()

  screen = pygame.display.set_mode(
    (800, 800),
    pygame.OPENGL | pygame.DOUBLEBUF
  )

  glViewport(0, 0, 800, 800)
  glClearColor(0.1, 0.1, 0.3, 1)

  # ----------- Compilacion de shaders -----------
  compiled_vertex_shader = compileShader(shaders['normal_color'][0], GL_VERTEX_SHADER)
  compiled_fragment_shader = compileShader(shaders['normal_color'][1], GL_FRAGMENT_SHADER)
  compiled_vertex_shader = compileShader(shaders['text_color'][0], GL_VERTEX_SHADER)
  compiled_fragment_shader = compileShader(shaders['text_color'][1], GL_FRAGMENT_SHADER)
  shader = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader
  )
  glUseProgram(shader)

  # ----------- Carga de modelos -----------
  Cube = Obj('./models/NoText/Sphere.obj')
  Cube = Obj('./models/SpaceX/f.obj')
  Cube = Obj('./models/NoText/Rims&Tires.obj')
  Cube = Obj('./models/Guitar/GUITAR.obj')
  Cube = Obj('./models/NoText/cube.obj')
  Cube = Obj('./models/plant/plant.obj')
  Cube = Obj('./models/Astronaut/astronaut.obj')
  Cube = Obj('./models/Mario/Mario.obj')
  Cube = Obj('./models/Moon/Moon.obj')
  Cube = Obj('./models/E/Globe.obj')
  Cube = Obj('./models/Face/face.obj')

  # ----------- Carga Texturas -----------
  texture_path = './models/plant/text.jpeg'
  texture_path = './models/Astronaut/texture.bmp'
  texture_path = './models/Mario/Mario.bmp'
  texture_path = './models/Moon/moon2.bmp'
  texture_path = './models/E/Albedo-diffuse_Low-end.bmp'
  texture_path = './models/Face/model.bmp'
  texture = glGenTextures(1)
  glBindTexture(GL_TEXTURE_2D, texture)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

  image = pygame.image.load(texture_path).convert()
  image_width, image_height = image.get_rect().size
  image_data = pygame.image.tostring(image, 'RGB')
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image_width, image_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
  glGenerateMipmap(GL_TEXTURE_2D)
  # glActiveTexture(GL_TEXTURE0)

  # ----------- Carga vertex_data -----------
  face_count, vertex_data = Cube.get_vertex_data(True)

  # apartir de esas lineas, las instrucciones se aplican
  # al vertex_buffer_object especificamente
  vertex_buffer_object = glGenBuffers(1)
  glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)

  # Mandar vertex_data a memoria de video
  glBufferData(
    GL_ARRAY_BUFFER, # tipo de datos
    vertex_data.nbytes, # tamano de la data en bytes
    vertex_data, # puntero a la data en la memoria
    GL_STATIC_DRAW # opcional, para optimizacion
  )

  # Crear estructura de organizacion de datos en memoria
  vertex_array_object = glGenVertexArrays(1)
  glBindVertexArray(vertex_array_object)

  # ----------- Carga de datos para shaders -----------
  
  # Cargar Vertices
  glVertexAttribPointer(
    0, # ubicacion para shader
    3,
    GL_FLOAT,
    GL_FALSE,
    8 * 4, # Offset de 9 floats de 4 bytes cada uno
    ctypes.c_void_p(0) # void pointer
  )
  glEnableVertexAttribArray(0)

  # Cargar Normales
  glVertexAttribPointer(
    1, # ubicacion para shader
    3,
    GL_FLOAT,
    GL_FALSE,
    8 * 4, # Offset de 9 floats de 4 bytes cada uno
    ctypes.c_void_p(3 * 4) # Offset del inicio, void pointer
  )
  glEnableVertexAttribArray(1)

  # Cargar coordenadas de texturas
  glVertexAttribPointer(
    2, # ubicacion para shader
    2,
    GL_FLOAT,
    GL_FALSE,
    8 * 4, # Offset de 9 floats de 4 bytes cada uno
    ctypes.c_void_p(6 * 4) # Offset del inicio, void pointer
  )
  glEnableVertexAttribArray(2)

  # ----------- Transformaciones -----------
  def calculateMatrix(angle):
    i = glm.mat4(1)
    translate = glm.translate(i, glm.vec3(0, -1.5, 0))
    translate = glm.translate(i, glm.vec3(0, 0, 0))
    rotate = glm.rotate(glm.radians(angle), glm.vec3(0,1,0))
    scale = glm.scale(i, glm.vec3(0.1, 0.1, 0.1))
    scale = glm.scale(i, glm.vec3(1, 1, 1))
    view = glm.lookAt(
      glm.vec3(0, 0, 5),
      glm.vec3(0, 0, 0),
      glm.vec3(0, 1, 0)
    )
    projection = glm.perspective(
      glm.radians(45),
      1,
      0.1,
      1000.0
    )
    amatrix = projection * view * translate * rotate * scale

    glUniformMatrix4fv(
      glGetUniformLocation(shader, 'amatrix'),
      1,
      GL_FALSE,
      glm.value_ptr(amatrix)
    )

  r = 0
  running = True
  clicking = False
  while running:
    # Clear
    glClear(GL_COLOR_BUFFER_BIT)

    # Calculate
    calculateMatrix(r)  # Transormaciones
    glDrawArrays(GL_TRIANGLES, 0, face_count) # Pintar triangulos
    r += 0.2 # Aumento de angulo

    # Flip
    pygame.display.flip()

    # Event Stack
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
