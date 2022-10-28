
import pygame
from OpenGL.GL import *

def paint_grid(screen):
  for y in range(H):
    for x in range(W):
      last = GRID[y][x][actualgrid]
      actual = GRID[y][x][nextgrid]

      if last != actual:
        color = (255, 255, 215) if last else (10, 10, 40)
        pygame.draw.rect(screen, color, pygame.Rect(x*blocksize, y*blocksize, blocksize-1, blocksize-1))

def init_grid(screen):
  for y in range(H):
    for x in range(W):
      color = (255, 255, 215) if GRID[y][x][0] else (10, 10, 40)
      pygame.draw.rect(screen, color, pygame.Rect(x*blocksize, y*blocksize, blocksize-1, blocksize-1))

def __getVecinos(x, y, GRID, actualgrid):
  xi, yi = x+1, y+1

  try:
    u1 = GRID[y][x+1][actualgrid]
  except:
    xi = 0
  
  try:
    u2 = GRID[y+1][x][actualgrid]
  except:
    yi = 0
  
  vecinos:list = [
    GRID[y][xi][actualgrid],
    GRID[yi][x][actualgrid],
    GRID[yi][xi][actualgrid],
    GRID[yi][x-1][actualgrid],
    GRID[y-1][x-1][actualgrid],
    GRID[y-1][xi][actualgrid],
    GRID[y-1][x][actualgrid],
    GRID[y][x-1][actualgrid]
  ]

  return vecinos.count(True)

def compute_game(actualgrid, nextgrid):
  for y in range(H):
    for x in range(W):
      GRID[y][x][nextgrid] = GRID[y][x][actualgrid]
      alive = __getVecinos(x, y, GRID, actualgrid)
      cell = GRID[y][x][actualgrid]

      if cell and alive not in [2, 3]:
        GRID[y][x][nextgrid] = False
      
      if not cell and alive == 3:
        GRID[y][x][nextgrid] = True

  return nextgrid, actualgrid

def set_grid(x, y, value=True):
  GRID[y][x][0] = value

if __name__ == '__main__':
  blocksize = 20
  windowsize = (800, 600)
  W, H = windowsize

  GRID = [
    [[False, False] for x in range(W)]
      for y in range(H)
  ]

  pattern = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  ]
  for y in range(len(pattern)):
    for x in range(len(pattern[0])):
      if pattern[y][x] == 1:
        set_grid(x, y)

  pygame.display.set_caption("John Conway's Game of Life")
  screen = pygame.display.set_mode(windowsize, pygame.DOUBLEBUF)
  init_grid(screen)
  pygame.init()

  actualgrid = 0
  nextgrid = 1
  running = True

  while running:
    # Paint_grid
    paint_grid(screen)

    # Operate iteration
    actualgrid, nextgrid = compute_game(actualgrid, nextgrid)

    # Flip
    pygame.display.update()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
