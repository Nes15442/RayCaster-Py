''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  Vector.py
  - Implementation of Vector3 object
  
  Last modified (yy-mm-dd): 2022-08-08
--------------------------------------
'''

class V3(object):
  def __init__(self, x, y, z=0):
    self.x = x
    self.y = y
    self.z = z

  # ----------- Overloads

  def __repr__(self) -> str:
    return f'V3({self.x}, {self.y}, {self.z})'

  def __add__(self, other):
    return V3(
      self.x + other.x,
      self.y + other.y,
      self.z + other.z
    )

  def __sub__(self, other):
    return V3(
      self.x - other.x,
      self.y - other.y,
      self.z - other.z
    )

  def __mul__(self, other):
    if type(other) in [int, float]:
      return V3(
        self.x * other,
        self.y * other,
        self.z * other
      )
    elif type(other) == V3:
      return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

  def __matmul__(self, other):
    return self.cross(other)
  
  # --- Methods

  def size(self):
    return (self.x**2 + self.y**2 + self.z**2)**0.5
  
  def cross(self, other):
    return V3(
      self.y * other.z - self.z * other.y,
      self.z * other.x - self.x * other.z,
      self.x * other.y - self.y * other.x
    )

  def round(self):
    self.x = round(self.x)
    self.y = round(self.y)
    self.z = round(self.z)

  def normalize(self):
    return V3(
      self.x / self.size(),
      self.y / self.size(),
      self.z / self.size()

    ) if self.size() > 0 else V3(0, 0, 0)

# ----------- Functions ------------
def cross(v1:V3, v2:V3):
  return (
    v1.y * v2.z - v1.z * v2.y,
    v1.z * v2.x - v1.x * v2.z,
    v1.x * v2.y - v1.y * v2.x
  )
