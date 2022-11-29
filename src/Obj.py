''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  Obj.py (Object)
  - Object used to read .obj models

  Last modified (yy-mm-dd): 2022-11-28
--------------------------------------
'''

import numpy as np

class Obj:
  '''
  .obj file reader

  Atributes
  ---------
  - lines: lines written in the .obj file
  - vertices: Vertices of the model
  - faces: faces of the model
  - n_vertices: normal vertices
  - object_data: vertex data for openGl
  - count_faces: polygon count for openGL
  '''
  def __init__(self, filename):
    self.object_data = []
    self.count_faces = 0

    with open(filename) as f:
      self.lines = f.read().splitlines()
    
    self.vertices = []
    self.faces = []
    self.tverctices = []
    self.n_vertices = []

    for line in self.lines:
      try:
        prefix, value = line.split(' ', 1)
      except:
        continue

      match prefix:
        case 'v':
          self.vertices.append([
            float(n) for n in list(filter(
              lambda v: v != '', value.split(' ')
            ))
          ])
        
        case 'vn':
          self.n_vertices.append([
            float(n) for n in list(filter(
              lambda v: v != '', value.split(' ')
            ))
          ])
        
        case 'f':
          self.faces.append([
            [int(n) for n in face.split('/')]
              for face in list(filter(
              lambda v: v != '', value.split(' ')
            ))
          ])

        case 'vt':
          self.tverctices.append([
            float(n) for n in list(filter(
              lambda v: v != '', value.split(' ')
            ))
          ])

  def load_model(self, texture_path):
    for face in self.faces:
      face_vertex = []
      text_vertex = []
      normal_vertex = []

      for actual_v in face:
        face_vertex.append(self.vertices[actual_v[0] - 1])

        temp_texture = self.tverctices[actual_v[1] - 1] if texture_path else (0, 0)
        text_vertex.append(temp_texture)

        temp_normals = self.n_vertices[actual_v[2] - 1] \
          if len(self.n_vertices) - 1 >= actual_v[2] - 1 \
          else (0, 0, 0)
        normal_vertex.append(temp_normals)

      self.poly_triangle(face_vertex, text_vertex, normal_vertex)

  def poly_triangle(self, face:list, text:list, normals:list):
    if len(face) < 3: raise Exception('Invalid Polygon:', face)

    for index in range(len(face) - 2):
      self.count_faces += 3
      vertex = (face[0], face[index+1], face[index+2])
      t_normals = (normals[0], normals[index+1], normals[index+2])
      textures = (text[0], text[index+1], text[index+2])

      for i in range(3):
        # Vertex
        self.object_data.append(vertex[i][0])
        self.object_data.append(vertex[i][1])
        self.object_data.append(vertex[i][2])

        # Normals        
        self.object_data.append(t_normals[i][0])
        self.object_data.append(t_normals[i][1])
        self.object_data.append(t_normals[i][2])
        
        # Textures        
        self.object_data.append(textures[i][0])
        self.object_data.append(1 - textures[i][1])
    
  def get_vertex_data(self, texture_path=False):
    self.load_model(texture_path)
    vertex_data = np.array(self.object_data, dtype=np.float32)
    return self.count_faces, vertex_data
