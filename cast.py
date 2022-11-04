import pygame
import random
from OpenGL.GL import *
from cmath import pi
from math import cos, sin

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class RayCaster:
  def __init__(self, screen) -> None:
    self.screen:pygame.display = screen
    _, _, self.width, self.height = screen.get_rect()
    self.map = []
    self.blocksize = 50
    self.player = {
      "x": int(self.blocksize + self.blocksize / 2), 
      "y": int(self.blocksize + self.blocksize / 2),
      'fov': int(pi/3),
      'a': int(pi/3)
    }


  def point(self, x, y, c = WHITE):
    glEnable(GL_SCISSOR_TEST)
    glScissor(x, y, self.blocksize, self.blocksize)
    glClearColor(*c, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)

  def point(self, x, y, c = WHITE):
    self.screen.set_at((x, y), c)
    self.screen.set_at((x, y), c)

  def block(self, x, y, c = WHITE):
    for i in range(x, x + self.blocksize + 1):
      for j in range(y, y + self.blocksize + 1):
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
        return d, self.map[j][i]

      self.point(x, y)
      d += 5

  def draw_map(self):
    for x in range(0, 500, self.blocksize):
      for y in range(0, 500, self.blocksize):
        j = int(x/self.blocksize)
        i = int(y/self.blocksize)
        if self.map[i][j] != ' ':
          self.block(x, y, colors[int(self.map[i][j])])

  def draw_player(self):
    self.point(self.player['x'], self.player['y'])

  def render(self):
    self.draw_map()
    self.draw_player()

    density = 100
    fov = self.player['fov']

    for i in range(0, density):
      a = self.player['a'] - fov/2 + fov * i/10
      d, c = self.cast_ray(a)

    for i in range(0, 500):
      self.point(499, i)
      self.point(500, i)
      self.point(501, i)
    
    for i in range(0, density):
      a = self.player['a'] - fov/2 + fov * i/10
      d, c = self.cast_ray(a)

      x = int(self.width/2) + i
      h = self.width/(d * cos(a - self.player['a'])) * 100
      self.draw_strake(x, h, colors[int(c)])

  def draw_strake(self, x, h, c):
    start_y = int(self.height/2 - h/2)
    end_y = int(self.height + h/2)

    for y in range(start_y, end_y):
      self.point(x, y, c)

pygame.init()
screen = pygame.display.set_mode((1000, 500))
r = RayCaster(screen)
r.load_map('./map.txt')

colors = [
  (),
  (255/4, 255/40, 255/63),
  (0, 255/91, 255/82),
  (255/219, 255/242, 255/38),
]

colors = [
  (),
  (4, 40, 63),
  (0, 91, 82),
  (219, 242, 38),
]

running = True
while running:
  screen.fill(BLACK)

  r.render()

  pygame.display.flip()

  for event in pygame.event.get():
    match event.type:
      case pygame.QUIT:
        running = False

      case pygame.K_RIGHT:
        r.player['x'] += 10
      
      case pygame.K_LEFT:
        r.player['x'] -= 10
      
      case pygame.K_UP:
        r.player['y'] -= 10
      
      case pygame.K_DOWN:
        r.player['y'] += 10
      
      case pygame.K_a:
        r.player['a'] -= pi/10
      
      case pygame.K_d:
        r.player['a'] += pi/10