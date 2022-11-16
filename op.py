import pygame
import numpy
import random
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm

pygame.init()

screen = pygame.display.set_mode(
  (800, 800),
  pygame.OPENGL | pygame.DOUBLEBUF
)

# Programacion de Shaders
vertex_shader = '''
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;
out vec3 ourColor;
uniform mat4 amatrix;

void main()
{
  gl_Position = amatrix * vec4(position, 1.0f);
  ourColor = vertexColor;
}
'''
fragment_shader = '''
#version 460

layout (location = 0) out vec4 fragColor;
uniform vec3 color;
in vec3 ourColor;

void main()
{
  // fragColor = vec4(ourColor.x, ourColor.y, ourColor.z, 1.0f);
  fragColor = vec4(color, 1.0f);
}
'''

# Compilacion de shaders
compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
shader = compileProgram(
  compiled_vertex_shader,
  compiled_fragment_shader
)
glUseProgram(shader)

vertex_data = numpy.array([
  -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
  0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
  0.0, 0.5, 0.0, 0.0, 0.0, 1.0
], dtype=numpy.float32)


# apartir de esas lineas, las instrucciones se aplican
# al vertex_buffer_object especificamente
vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)

# Mandar vertices a memoria de video
glBufferData(
  GL_ARRAY_BUFFER, # tipo de datos
  vertex_data.nbytes, # tamano de la data en bytes
  vertex_data, # puntero a la data en la memoria
  GL_STATIC_DRAW # opcional, para optimizacion
)

# Crear estructura de organizacion de datos en memoria
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

glVertexAttribPointer(
  0, # ubicacion para shader
  3,
  GL_FLOAT,
  GL_FALSE,
  6 * 4, # Offset de 6 floats de 4 bytes cada uno
  ctypes.c_void_p(0) # void pointer
)

glEnableVertexAttribArray(0)

# Cargar colores
glVertexAttribPointer(
  1, # ubicacion para shader
  3,
  GL_FLOAT,
  GL_FALSE,
  6 * 4, # Offset de 6 floats de 4 bytes cada uno
  ctypes.c_void_p(3 * 4) # Offset del inicio, void pointer
)

glEnableVertexAttribArray(1)

def calculateMatrix(angle):
  i = glm.mat4(1)
  translate = glm.translate(i, glm.vec3(0, 0, 0))
  rotate = glm.rotate(i, glm.radians(angle), glm.vec3(1, 1, 0.5))
  scale = glm.scale(i, glm.vec3(1, 1, 1))

  model = translate * rotate * scale

  view = glm.lookAt(
    glm.vec3(0, 0, 5),
    glm.vec3(0, 0, 0),
    glm.vec3(0, 1, 0)
  )

  projection = glm.perspective(
    glm.radians(45),
    800/800,
    0.1,
    1000.0
  )

  amatrix = projection * view * model

  glUniformMatrix4fv(
    glGetUniformLocation(shader, 'amatrix'),
    1,
    GL_FALSE,
    glm.value_ptr(amatrix)
  )

glViewport(0, 0, 800, 800)

glClearColor(0.1, 0.1, 0.3, 1)
r = 0

running = True
while running:
  # Clear
  glClear(GL_COLOR_BUFFER_BIT)

  # Calculate
  r += 1
  color1 = random.random()
  color2 = random.random()
  color3 = random.random()
  color = glm.vec3(color1, color2, color3)
  color = glm.vec3(1, 1, 1)

  glUniform3fv(
    glGetUniformLocation(shader,'color'),
    1,
    glm.value_ptr(color)
  )

  calculateMatrix(r)
  glDrawArrays(GL_TRIANGLES, 0, 3)
  pygame.time.wait(1)

  # Flip
  pygame.display.flip()

  # Event Stack
  for event in pygame.event.get():
    match event.type:
      case pygame.QUIT:
        running = False
  