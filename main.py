import pygame as pg
from cmath import pi
from math import cos, sin
from cast import RayCaster

colors = [
  (0,20,10),
  (4,40,63),
  (0,91,82),
  (219,248,38),
  (2,248,50),
]

textures = {
  '1': pg.image.load('./Textures/wall1.png'),
  '2': pg.image.load('./Textures/wall2.png'),
  '3': pg.image.load('./Textures/wall3.png'),
  '4': pg.image.load('./Textures/wall4.png'),
  '5': pg.image.load('./Textures/wall5.png'),
}

sprite1 = pg.image.load('./sprites/sprite1.png')
sprite2 = pg.image.load('./sprites/sprite2.png')
sprite3 = pg.image.load('./sprites/sprite3.png')

enemies = [
  {
    'x': 150,
    'y': 150,
    'sprite': sprite1
  },
  {
    'x': 300,
    'y': 300,
    'sprite': sprite2
  },
  {
    'x': 380,
    'y': 380,
    'sprite': sprite3
  }
]

if __name__ == '__main__':
  pg.init()
  screen = pg.display.set_mode((500, 500), pg.DOUBLEBUF | pg.HWACCEL)

  # ------- Title screen ------- 
  running = True
  titleImg = pg.image.load('./backgrounds/1.png').convert()
  screen.blit(titleImg, (0, 0))

  pg.display.flip()

  soundtrack = pg.mixer.music.load('./sounds/Horizon.mp3')
  pg.mixer.music.play(-1)
  while running:
    for event in pg.event.get():
      match event.type:
        case pg.MOUSEBUTTONDOWN:
          running = False

        case pg.KEYDOWN:
          running = False
  
  # ------- Instrucciones ------- 
  titleImg = pg.image.load('./backgrounds/2.png').convert()
  screen.blit(titleImg, (0, 0))
  pg.display.flip()

  running = True
  while running:
    for event in pg.event.get():
      match event.type:
        case pg.MOUSEBUTTONDOWN:
          running = False

        case pg.KEYDOWN:
          running = False

  r = RayCaster(screen, enemies, textures)
  level = 1
  last_level = 1
  r.load_map('./maps/map1.txt')

  clock = pg.time.Clock()
  font = pg.font.SysFont('Arial', 25, bold=True)

  def fps_counter():
    fps = f'FPS {clock.get_fps()}'
    fps = font.render(fps, 1, pg.Color('WHITE'))
    screen.blit(fps, (10, 2))

  running = True
  useMouse = False
  while running:

    print([r.player['x'], r.player['y']])
    if 106 < r.player['x'] < 165 and 311 < r.player['y'] < 332:
      running = False
    # clear
    clock.tick()
    screen.fill((118, 188, 222))
    screen.fill((84, 121, 89), (0, r.height/2, r.width, r.height/2))
    r.clearZ()

    # Render
    r.render()

    # FPS counter
    fps_counter()

    # Flip
    pg.display.flip()

    for event in pg.event.get():
      match event.type:
        case pg.QUIT:
          running = False

        case pg.MOUSEBUTTONDOWN:
          pg.mouse.set_visible(useMouse)
          useMouse = not useMouse

        case pg.KEYDOWN:
          r.player['last_x'] = r.player['x']
          r.player['last_y'] = r.player['y']

          match event.key:
            case pg.K_RIGHT:
              r.player['a'] += pi/10
          
            case pg.K_LEFT:
              r.player['a'] -= pi/10
          
            case pg.K_w:
              r.player['x'] += int(20 * cos(r.player['a']))
              r.player['y'] += int(20 * sin(r.player['a']))
          
            case pg.K_s:
              r.player['x'] -= int(20 * cos(r.player['a']))
              r.player['y'] -= int(20 * sin(r.player['a']))
          
            case pg.K_a:
              r.player['x'] -= int(20 * cos(pi/2 + r.player['a']))
              r.player['y'] -= int(20 * sin(pi/2 + r.player['a']))
          
            case pg.K_d:
              r.player['x'] += int(20 * cos(pi/2 + r.player['a']))
              r.player['y'] += int(20 * sin(pi/2 + r.player['a']))
        
      if r.player['a'] > 2 * pi:
        r.player['a'] = r.player['a'] - 2 * pi
      
      elif r.player['a'] < 0:
        r.player['a'] = 2 * pi + r.player['a'] 

    if useMouse:
      r.player['a'] += pi * (pg.mouse.get_rel()[1] / 30)
      pg.mouse.set_pos((int(r.width/2), int(r.height/2)))

  titleImg = pg.image.load('./backgrounds/win.png').convert()
  screen.blit(titleImg, (0, 0))
  pg.display.flip()

  running = True
  while running:
    for event in pg.event.get():
      match event.type:
        case pg.MOUSEBUTTONDOWN:
          running = False

        case pg.KEYDOWN:
          running = False