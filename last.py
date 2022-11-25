
class xd:
  def __transform_vertex(self, vertex):
    '''Returns the coordinates of a vertex centered to the screen'''
    augmented_vertex = V4([*vertex, 1])
  
    transformed_vertex = (
      # self.viewport
      # @ self.projection
      # @ self.Model
      # @ augmented_vertex
      # @ self.viewMatrix
    ) # .matrix[0]
    
    return V3(
      transformed_vertex[0] / transformed_vertex[3],
      transformed_vertex[1] / transformed_vertex[3],
      transformed_vertex[2] / transformed_vertex[3]
    )
  
  
  def triangle(
    self, vertices:list[V3], normals:list[V3],
    L:tuple, t_vertices:list[V3] = ()
  ):
    A, B, C = vertices
    Min, Max = self.bounding_box(A, B, C)
  
    for x in range(Min.x, Max.x + 1):
      for y in range(Min.y, Max.y + 1):
        if x > len(self.zBuffer[0]) - 1 or y > len(self.zBuffer) - 1: continue
        if x < 0 or y < 0: continue
  
        w, u, v = self.barycentric(A, B, C, V3(x, y))
        if w < 0 or v < 0 or u < 0: continue
  
        z = A.z * w + B.z * u + C.z * v
        if self.zBuffer[y][x] > z: continue
        self.zBuffer[y][x] = z
  
        if self.current_shader:
          self.current_color = self.current_shader(
            self,
            normals=normals,
            texture_coords = t_vertices,
            vertices= vertices,
            bari = (w, u, v),
            light = V3(*L),
            coords = (x, y),
            size = (self.window_w, self.window_h)
          )
            
        self.point(x, y)
  
  