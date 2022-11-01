
import pygame
from OpenGL.GL import *

def pixel(x, y, color):
  glEnable(GL_SCISSOR_TEST)
  glScissor(x, y, blocksize-1, blocksize-1)
  glClearColor(*color, 1)
  glClear(GL_COLOR_BUFFER_BIT)
  glDisable(GL_SCISSOR_TEST)

def draw_rect(x, y, color):
  pygame.draw.rect(
    screen,
    color,
    (x*blocksize, H - y*blocksize, blocksize-1, blocksize-1)
  )

def paint_grid():
  while len(changes) > 0:
    x, y = changes.pop()
    color = (255, 255, 215) if GRID[y][x][actualgrid] else (10, 10, 40)
    draw_rect(x, y, color)
    
def init_grid(pattern = []):
  for y in range(len(pattern)):
    for x in range(len(pattern[0])):
      if pattern[y][x] == 1:
        set_grid(x, y)

  for y in range(H):
    for x in range(W):
      color = (255, 255, 215) if GRID[y][x][0] else (10, 10, 40)
      draw_rect(x, y, color)
      
def __getVecinos(x, y, GRID, actualgrid):
  xi = x+1 if x+1 < len(GRID[0]) else 0
  yi = y+1 if y+1 < len(GRID) else 0
  
  vecinos_count = 0
  vecinos_count += 1 if GRID[y][xi][actualgrid] else 0
  vecinos_count += 1 if GRID[yi][x][actualgrid] else 0
  vecinos_count += 1 if GRID[yi][xi][actualgrid] else 0
  vecinos_count += 1 if GRID[yi][x-1][actualgrid] else 0
  vecinos_count += 1 if GRID[y-1][x-1][actualgrid] else 0
  vecinos_count += 1 if GRID[y-1][xi][actualgrid] else 0
  vecinos_count += 1 if GRID[y-1][x][actualgrid] else 0
  vecinos_count += 1 if GRID[y][x-1][actualgrid] else 0

  return vecinos_count

def compute_game(actualgrid, nextgrid):
  for y in range(H):
    for x in range(W):
      GRID[y][x][nextgrid] = GRID[y][x][actualgrid]
      alive = __getVecinos(x, y, GRID, actualgrid)
      cell = GRID[y][x][actualgrid]

      if cell and alive not in [2, 3]:
        GRID[y][x][nextgrid] = False
        changes.append((x, y))
      
      if not cell and alive == 3:
        GRID[y][x][nextgrid] = True
        changes.append((x, y))

  return nextgrid, actualgrid

def set_grid(x, y, value=True):
  GRID[y][x][0] = value

if __name__ == '__main__':
  blocksize = 15
  W, H = (800, 600)

  GRID = [
    [[False, False] for x in range(W)]
      for y in range(H)
  ]

  pattern = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],
    [0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  ]
  
  pygame.display.set_caption("John Conway's Game of Life")
  screen = pygame.display.set_mode((W, H))
  init_grid(pattern)
  pygame.init()

  actualgrid, nextgrid = 0, 1
  running = True
  changes = []

  while running:
    # Paint_grid
    paint_grid()

    # Operate iteration
    actualgrid, nextgrid = compute_game(actualgrid, nextgrid)

    # Flip
    pygame.display.update()

    for event in pygame.event.get():
      match event.type:
        case pygame.QUIT:
          running = False
  