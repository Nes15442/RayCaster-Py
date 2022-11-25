''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  Render.py (Object)
  - Object used to render a bmp image

  Last modified (yy-mm-dd): 2022-11-25
--------------------------------------
'''

from math import cos, sin
from Texture import Texture
from Obj import Obj
from MStructs.Vector import *
from MStructs.Matrix import *
import glm
from OpenGL.GL import *
from ..shaders import *
import pygame

color = lambda r, g, b: bytes([b, g, r])

class Render(object):

  def __init__(self):
    self.texture = None
    self.current_shader = None

  # ---------- Drawing of models
  def load_model(
    self, model_path, L,
    translate=(0, 0, 0),
    scale    =(1, 1, 1),
    rotate   =(0, 0, 0),
    texture_path = None
  ):
    self.loadModelMatrix(translate, scale, rotate)
    model:Obj = Obj(model_path)

    if texture_path: self.texture = Texture(texture_path)

    for face in model.faces:
      face_vertex = []
      text_vertex = []
      normal_vertex = []

      for actual_v in face:
        temp = model.vertices[actual_v[0] - 1]
        temp = self.__transform_vertex(temp)
        face_vertex.append(temp)
        normal_vertex.append(V3(*model.n_vertices[actual_v[2] - 1]))

        if self.texture:
          temp_texture = V3(*model.tverctices[actual_v[1] - 1])
          text_vertex.append(temp_texture)

      self.poly_triangle(face_vertex, text_vertex, normal_vertex, L)

  def poly_triangle(
    self, face:list[V3],
    text:list[V3],
    normals:list[V3],
    L:tuple
  ):
    if len(face) < 3: raise Exception('Invalid Polygon:', face)

    for v in range(len(face) - 2):
      vertex = (face[0], face[v+1], face[v+2])
      t_normals = (normals[0], normals[v+1], normals[v+2])

      if not self.texture:
        self.triangle(vertex, t_normals, L)
      else:
        textures = (text[0], text[v+1], text[v+2])
        self.triangle(vertex, t_normals, L, textures)

  def calculateMatrix(self, angle, shader):
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
      1,
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

if __name__ == '__main__':
  pygame.init()

  screen = pygame.display.set_mode(
    (800, 800),
    pygame.OPENGL | pygame.DOUBLEBUF
  )

  # Compilacion de shaders
  compiled_vertex_shader = compileShader(shaders['color'][0], GL_VERTEX_SHADER)
  compiled_fragment_shader = compileShader(shaders['color'][1], GL_FRAGMENT_SHADER)
  shader = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader
  )
  glUseProgram(shader)


else:
  SR = Render()
  SR.initWindow(800, 800)

  center = (0, 0, 0)
  eye = (0, 0, 1)
  up = (0, 1, 0)
  coeff = 0.001

  # Ship - model
  model = './models/NoText/cube.obj'
  texture = None

  LIGHT = (1, 1, 1) # y z x
  SIZE = 0.3
  rotate = (
    0,
    0,
    0
  )
  transform = (
    0,
    0,
    0
  )
  scale = (SIZE, SIZE, SIZE)

  SR.lookAt(V3(*eye), V3(*center), V3(*up), coeff)
  SR.load_model(
    model, 
    LIGHT,
    transform,
    scale    ,
    rotate   ,
    texture
  )

  # write_bmp('./Renders/cube.bmp', SR.framebuffer)
