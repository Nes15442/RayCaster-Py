from cmath import pi
from math import cos, sin, atan2

class RayCaster:
  def __init__(self, screen, enemies, walls) -> None:
    self.screen = screen
    _, _, self.width, self.height = screen.get_rect()
    self.map = []
    self.blocksize = 50
    self.player = {
      "x": int(self.blocksize + self.blocksize / 2),
      "y": int(self.blocksize + self.blocksize / 2),
      "last_x": int(self.blocksize + self.blocksize / 2),
      "last_y": int(self.blocksize + self.blocksize / 2),
      'fov': int(pi/3),
      'a': int(pi/3)
    }
    self.clearZ()
    self.enemies = enemies
    self.walls = walls
  
  def clearZ(self):
    self.zbuffer = [-99 for z in range(self.width)]

  def point(self, x, y, c = (255, 255, 255)):
    self.screen.set_at((x, y), c)
  
  def point(self, x, y, c = (255, 255, 255)):
    self.screen.fill(
      c,
      (x, y, 1, 1)
    )

  def block(self, x, y, wall):
    for i in range(x, x + self.blocksize):
      for j in range(y, y + self.blocksize):
        tx = int((i - x) * 128 / self.blocksize)
        ty = int((j - y) * 128 / self.blocksize)
        c = wall.get_at((tx, ty))
        self.point(i, j, c)

  def load_map(self, filename):
    with open(filename) as f:
      for line in f.readlines():
        self.map.append(list(line))

  def cast_ray(self, a):
    d = 0
    ox = self.player['x']
    oy = self.player['y']

    while True:
      x = int(ox + d*cos(a))
      y = int(oy + d*sin(a))

      i = int(x/self.blocksize)
      j = int(y/self.blocksize)

      if self.map[j][i] != ' ':
        hitx = x - i * self.blocksize
        hity = y - j * self.blocksize

        if 1 < hitx < self.blocksize - 1:
          maxhit = hitx
        else:
          maxhit = hity

        tx = int(maxhit * 128 / self.blocksize)
        return d, self.map[j][i], tx

      #self.point(x, y)
      d += 0.5

  def draw_map(self):
    for x in range(0, 50, self.blocksize):
      for y in range(0, 50, self.blocksize):
        j = int(y/self.blocksize)
        i = int(x/self.blocksize)
        if self.map[j][i] != ' ':
          self.block(x, y, self.walls[self.map[j][i]])

  def draw_player(self):
    self.point(self.player['x'], self.player['y'])

  def render(self):
    self.draw_map()
    fov = self.player['fov']
    
    # 3D world
    fov = self.player['fov']
    for i in range(0, int(self.width)):
      a = self.player['a'] - (fov/2) + (fov * i/(self.width))
      cos_a = cos(a - self.player['a'])
      d, c, tx = self.cast_ray(a)

      # Colisiones con paredes
      if d == 0:
        self.player['x'] = self.player['last_x']
        self.player['y'] = self.player['last_y']
        a = self.player['a'] - (fov/2) + (fov * i/(self.width))
        d, c, tx = self.cast_ray(a)
      
      h_den = d * cos_a

      if self.zbuffer[i] < d:
        h = (self.width/h_den) * 20
        x = i

        self.draw_strake(x, h, c, tx)
        self.zbuffer[i] = d
    
    for enemy in self.enemies:
      self.draw_sprite(enemy)

  def draw_strake(self, x, h, c, tx):
    start_y = int(self.height/2 - h/2)
    end_y = int(self.height/2 + h/2)
    height = end_y - start_y

    for y in range(start_y, end_y):
      ty = int((y - start_y) * 128/height)
      color = self.walls[c].get_at((tx, ty))
      self.point(x, y, color)

  def draw_sprite(self, sprite):
    d = (
      (self.player['x'] - sprite['x'])**2 +
      (self.player['y'] - sprite['y'])**2
    )**0.5
    sprite_size = int(500/d * (500/10))

    sprite_a = atan2(
      sprite['y'] - self.player['y'],
      sprite['x'] - self.player['x']
    )    
    sprite_x = int(
      0 + # Offset del mapa
      (sprite_a - self.player['a']) * 500/self.player['fov']
      + sprite_size/2
    )
    sprite_y = int(self.height/2 - sprite_size/2)

    for x in range(sprite_x, sprite_x + sprite_size):
      for y in range(sprite_y, sprite_y + sprite_size):
        tx = int((x - sprite_x) * 128/sprite_size)
        ty = int((y - sprite_y) * 128/sprite_size)
        c = sprite['sprite'].get_at((tx, ty))
        
        if c != (0, 0, 0, 0):
          if 0 < x < self.width:
            if self.zbuffer[x - 0] >= d:
              self.point(x, y, c)
              self.zbuffer[x - 0] = d
