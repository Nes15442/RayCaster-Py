
import pygame
from OpenGL.GL import *
from copy import deepcopy as copy

def paint_grid(screen):
  for y in range(H):
    for x in range(W):
      color = (255, 255, 215) if GRID[y][x] else (10, 10, 40)
      pygame.draw.rect(
        screen,
        color,
        pygame.Rect(x*blocksize, y*blocksize, blocksize-1, blocksize-1)
      )

def set_grid(x, y, value=True):
  GRID[y][x] = value

def getVecinos(x, y, GRID):
  xi, yi = x+1, y+1

  try:
    u1 = GRID[y][x+1]
  except:
    xi = 0
  
  try:
    u2 = GRID[y+1][x]
  except:
    yi = 0
  
  vecinos:list = [
    GRID[y][xi],
    GRID[yi][x],
    GRID[yi][xi],
    GRID[yi][x-1],
    GRID[y-1][x-1],
    GRID[y-1][xi],
    GRID[y-1][x],
    GRID[y][x-1]
  ]

  return vecinos.count(True)

def compute_game(grid):
  newgrid = copy(grid)

  for y in range(H):
    for x in range(W):
      alive = getVecinos(x, y, grid)
      cell = grid[y][x]

      if cell and alive not in [2, 3]:
        newgrid[y][x] = False
      
      if not cell and alive == 3:
        newgrid[y][x] = True

  return newgrid

if __name__ == '__main__':
  blocksize = 5
  windowsize = (1000, 800)
  W, H = windowsize

  GRID = [
    [False for x in range(W)]
      for y in range(H)
  ]
  #set_grid(50, 50)
  #set_grid(50, 51)
  #set_grid(50, 49)
  set_grid(20, 20)
  set_grid(20, 21)
  set_grid(20, 19)

  pygame.display.set_caption("John Conway's Game of Life")
  screen = pygame.display.set_mode(windowsize)
  pygame.init()

  running = True
  while running:
    # Paint_grid
    paint_grid(screen)

    # Operate iteration
    GRID = compute_game(GRID)

    # Flip
    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
