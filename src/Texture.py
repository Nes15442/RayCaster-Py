''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  Texture.py (Object)
  - Object used to load textures to
    a model

  Last modified (yy-mm-dd): 2022-08-17
--------------------------------------
'''

from .util import color
import struct

class Texture:
  def __init__(self, path):
    self.path = path
    self.read()

  def read(self):
    img = open(self.path, 'rb')
    img.seek(2 + 4 + 4)
    header_size = struct.unpack('=l', img.read(4))[0]
    
    img.seek(2 + 4 + 4 + 4 + 4)
    self.width = struct.unpack('=l', img.read(4))[0]
    self.height = struct.unpack('=l', img.read(4))[0]

    img.seek(header_size)

    self.pixels = []

    for y in range(self.height):
      self.pixels.append([])
      for x in range(self.width):
        b = ord(img.read(1))
        g = ord(img.read(1))
        r = ord(img.read(1))
        
        actual_color = color(r, g, b, normalized=False)
        self.pixels[y].append(actual_color)

    img.close()
      
  def get_color(self, tx, ty, intensity=1):
    x = round(tx * self.width) - 1
    y = round(ty * self.height) - 1
    p = self.pixels[y][x]

    return color(
      r = max(min(round(p[2] * intensity), 255), 0),
      g = max(min(round(p[1] * intensity), 255), 0),
      b = max(min(round(p[0] * intensity), 255), 0),
      normalized=False
    )

  def get_color_astronaut(self, tx, ty, intensity=1):
    x = round(tx * self.width) - 1
    y = round(ty * self.height) - 1
    p = self.pixels[y][x]

    r = max(min(round(p[2] * intensity), 255), 0)
    g = max(min(round(p[1] * intensity), 255), 0)
    b = max(min(round(p[0] * intensity), 255), 0)

    return (r, g, b)
