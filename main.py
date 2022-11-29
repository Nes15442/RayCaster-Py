''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  main.py
  - visualizador de modelos
    utilizando openGL

  Last modified (yy-mm-dd): 2022-11-28
--------------------------------------
'''

from src import *

if __name__ == '__main__':
  # ----------- pg Init -----------
  pg.init()

  screen = pg.display.set_mode(
    (800, 800),
    pg.OPENGL | pg.DOUBLEBUF
  )

  glViewport(0, 0, 800, 800)
  glClearColor(0.1, 0.2, 0.25, 1)

  # ----------- Compilacion de shaders -----------
  shader1 = compileProgram(
    compileShader(shaders[0][0], GL_VERTEX_SHADER),
    compileShader(shaders[0][1], GL_FRAGMENT_SHADER)
  )
  shader2 = compileProgram(
    compileShader(shaders[1][0], GL_VERTEX_SHADER),
    compileShader(shaders[1][1], GL_FRAGMENT_SHADER)
  )
  shader3 = compileProgram(
    compileShader(shaders[2][0], GL_VERTEX_SHADER),
    compileShader(shaders[2][1], GL_FRAGMENT_SHADER)
  )

  # ----------- Carga de modelos y texturas -----------
  Cube = Obj('./models/PaperPunch.obj')
  texture_path = './models/paperPunch_texture.tga'

  texture = glGenTextures(1)
  glBindTexture(GL_TEXTURE_2D, texture)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

  image = pg.image.load(texture_path).convert()
  image_width, image_height = image.get_rect().size
  image_data = pg.image.tostring(image, 'RGB')
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image_width, image_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
  glGenerateMipmap(GL_TEXTURE_2D)

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
    8 * 4, # Offset de 8 floats de 4 bytes cada uno
    ctypes.c_void_p(0) # void pointer
  )
  glEnableVertexAttribArray(0)

  # Cargar Normales
  glVertexAttribPointer(
    1, # ubicacion para shader
    3,
    GL_FLOAT,
    GL_FALSE,
    8 * 4, # Offset de 8 floats de 4 bytes cada uno
    ctypes.c_void_p(3 * 4) # Offset del inicio, void pointer
  )
  glEnableVertexAttribArray(1)

  # Cargar coordenadas de texturas
  glVertexAttribPointer(
    2, # ubicacion para shader
    2,
    GL_FLOAT,
    GL_FALSE,
    8 * 4, # Offset de 8 floats de 4 bytes cada uno
    ctypes.c_void_p(6 * 4) # Offset del inicio, void pointer
  )
  glEnableVertexAttribArray(2)

  # ----------- Transformaciones -----------
  def calculateMatrix(angle_x, angle_y, shader):
    i = glm.mat4(1)
    translate = glm.translate(i, glm.vec3(0, 0, 0))
    translate = glm.translate(i, glm.vec3(0, -2.5, -10))
    rotate_x = glm.rotate(glm.radians(angle_x), glm.vec3(1,0,0))
    rotate_y = glm.rotate(glm.radians(angle_y), glm.vec3(0,1,0))
    scale = glm.scale(i, glm.vec3(2, 2, 2))
    scale = glm.scale(i, glm.vec3(1, 1, 1))
    scale = glm.scale(i, glm.vec3(0.5, 0.5, 0.5))
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
    amatrix = projection * view * translate * rotate_x * rotate_y * scale

    glUniformMatrix4fv(
      glGetUniformLocation(shader, 'amatrix'),
      1,
      GL_FALSE,
      glm.value_ptr(amatrix)
    )

  polygonModes = (
    (GL_FRONT_AND_BACK, GL_FILL),
    (GL_FRONT_AND_BACK, GL_LINE),
    (GL_FRONT_AND_BACK, GL_POINT)
  )
  x, y = 0, 0
  running = True
  clicking = False
  mode = 0
  current_shader = shader1

  while running:
    # Clear
    glClear(GL_COLOR_BUFFER_BIT)

    # Polygon Mode y shader
    glPolygonMode(*polygonModes[mode])
    glUseProgram(current_shader)

    # Calculate
    calculateMatrix(x, y, current_shader)  # Transormaciones
    glDrawArrays(GL_TRIANGLES, 0, face_count) # Pintar triangulos

    # Flip
    pg.display.flip()

    # Event Stack
    for event in pg.event.get():
      match event.type:
        case pg.QUIT:
          running = False

        case pg.MOUSEBUTTONDOWN:
          clicking = True
      
        case pg.MOUSEBUTTONUP:
          clicking = False

        case pg.KEYDOWN:
          match event.key:
            case pg.K_SPACE:
              mode = mode + 1 if mode < 2 else 0
            
            case pg.K_1:
              current_shader = shader1
            
            case pg.K_2:
              current_shader = shader2
            
            case pg.K_3:
              current_shader = shader3

    if clicking:
      mouse = pg.mouse.get_rel()
      x += mouse[1] / 2
      y += mouse[0] / 2
