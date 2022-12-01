import pygame as pg
from cmath import pi
from math import cos, sin
from cast import RayCaster

# ------- Levels Data ------- 

SKY = (
  (118, 188, 222),
  (143, 116, 104),
  (86, 45, 104)
)

GROUND = (
  (84, 121, 89),
  (136, 124, 38),
  (102, 119, 211)
)

MAPS = (
  './maps/map1.txt',
  './maps/map2.txt',
  './maps/map3.txt',
)

GOALS = (
  ((106, 311), (165, 332)),
  ((355, 430), (396, 500)),
  ((355, 430), (396, 500)),
)

textures = {
  '1': pg.image.load('./Textures/wall1.png'),
  '2': pg.image.load('./Textures/wall2.png'),
  '3': pg.image.load('./Textures/wall3.png'),
  '4': pg.image.load('./Textures/wall4.png'),
  '5': pg.image.load('./Textures/wall5.png'),
}

sprite1 = pg.image.load('./sprites/sprite2.png')
sprite2 = pg.image.load('./sprites/sprite3.png')
sprite3 = pg.image.load('./sprites/sprite1.png')

enemies = [
  (
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
  ),
  (
    {
      'x': 300,
      'y': 300,
      'sprite': sprite2
    },
  ),
  (
    {
      'x': 150,
      'y': 150,
      'sprite': sprite1
    },
  )
]

# ------- Funciones Utiles ------- 

def showImg(imagePath):
  img = pg.image.load(imagePath).convert()
  screen.blit(img, (0, 0))
  pg.display.flip()

def fps_counter():
  fps = f'FPS {round(clock.get_fps(), 4)}'
  fps = FONT.render(fps, 1, pg.Color('WHITE'))
  screen.blit(fps, (10, 2))

def checkGoal(r: RayCaster):
  return (
    GOALS[level][0][0] < r.player['x'] < GOALS[level][1][0] \
    and GOALS[level][0][1] < r.player['y'] < GOALS[level][1][1]
  )

if __name__ == '__main__':
  pg.init()
  FONT = pg.font.SysFont('Arial', 22, bold=True)
  screen = pg.display.set_mode((500, 500), pg.DOUBLEBUF | pg.HWACCEL)
  soundtrack = pg.mixer.music.load('./sounds/Horizon.mp3')
  pg.mixer.music.set_volume(.8)
  pg.mixer.music.play(-1)

  # ------- Title screen ------- 
  showImg('./backgrounds/1.png')
  running = True
  while running:
    for event in pg.event.get():
      match event.type:
        case pg.MOUSEBUTTONDOWN:
          running = False

        case pg.KEYDOWN:
          running = False
  
  # ------- Instrucciones ------- 
  showImg('./backgrounds/2.png')
  running = True
  while running:
    for event in pg.event.get():
      match event.type:
        case pg.MOUSEBUTTONDOWN:
          running = False

        case pg.KEYDOWN:
          running = False

  # ------- Levels ------- 
  showImg('./backgrounds/levels.png')
  running = True
  level = 1
  while running:
    for event in pg.event.get():
      if event.type == pg.KEYDOWN:
        match event.key:
          case pg.K_1:
            level = 0
            running = False
          
          case pg.K_2:
            level = 1
            running = False
          
          case pg.K_3:
            level = 2
            running = False

  # ------- Main Game ------- 
  r = RayCaster(screen, enemies[level], textures)
  r.load_map(MAPS[level])

  clock = pg.time.Clock()
  running = True
  useMouse = False
  while running:

    # Check if player pass the level
    if checkGoal(r):
      level += 1
      if level < 3:
        r.reset_level(MAPS[level], enemies[level])
        
      else:
        running = False
        continue
    
    # Clock Tick
    clock.tick()

    # clear
    screen.fill(SKY[level])
    screen.fill(GROUND[level], (0, r.height/2, r.width, r.height/2))
    r.clearZ()

    # Render
    r.render()

    # FPS counter
    fps_counter()

    # Flip
    pg.display.flip()

    # Event Stack
    for event in pg.event.get():
      match event.type:
        case pg.QUIT:
          running = False

        case pg.MOUSEBUTTONDOWN:
          pg.mouse.set_visible(useMouse)
          useMouse = not useMouse

        case pg.KEYDOWN:
          if event.key in [pg.K_w, pg.K_a, pg.K_s, pg.K_d]:
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
        
    # Dejar angulo entre 0 y 2*pi
    if r.player['a'] > 2 * pi:
      r.player['a'] = r.player['a'] - 2 * pi
    
    elif r.player['a'] < 0:
      r.player['a'] = 2 * pi + r.player['a'] 

    # Uso de mouse para rotar
    if useMouse:
      r.player['a'] += pi * (pg.mouse.get_rel()[1] / 30)
      pg.mouse.set_pos((int(r.width/2), int(r.height/2)))

  # ------- Pantalla Final ------- 
  showImg('./backgrounds/win.png')
  while not running:
    for event in pg.event.get():
      match event.type:
        case pg.MOUSEBUTTONDOWN:
          running = not running

        case pg.KEYDOWN:
          running = not running

        case pg.QUIT:
          running = not running
