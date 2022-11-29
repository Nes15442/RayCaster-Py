''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  shaders.py
  - Shaders escritos para openGL

  Last modified (yy-mm-dd): 2022-11-28
--------------------------------------
'''

# Texturas
texture_vertex_shader = '''
#version 450 core
layout (location = 0) in vec3 position;
layout (location = 2) in vec2 aTexCoord;
uniform mat4 amatrix;

out vec2 TexCoord;

void main()
{
  gl_Position = amatrix * vec4(position, 1.0f);
  TexCoord = aTexCoord;
}
'''

texture_fragment_shader = '''
#version 450 core
out vec4 FragColor;
in vec2 TexCoord;

uniform sampler2D ourTexture;

void main()
{
  FragColor = texture(ourTexture, TexCoord);
}
'''

# Transpolacion de texturas con vertices de normal
texture_normal_vertex = '''
#version 450 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;
uniform mat4 amatrix;

out vec3 ourColor;
out vec2 TexCoord;

void main()
{
  gl_Position = amatrix * vec4(position, 1.0f);
  ourColor = aColor;
  TexCoord = aTexCoord;
}
'''

texture_normal_fragment = '''
#version 450 core
out vec4 FragColor;
in vec3 ourColor;
in vec2 TexCoord;

uniform sampler2D ourTexture;

void main()
{
  FragColor = texture(ourTexture, TexCoord) * vec4(ourColor, 1.0f);
}
'''


# Golden Stripes
stripes_vertex = """
#version 450 core
layout (location = 0) in vec3 position;
layout (location = 2) in vec2 texturecords;
layout (location = 1) in vec2 normals;
uniform mat4 amatrix;
out vec2 text_cord;
out vec2 normal_cords;

void main()
{
  text_cord = texturecords;
  normal_cords = normals;
  gl_Position = amatrix * vec4(position, 1.0);
}
"""

stripes_fragment = '''
#version 450 core
out vec4 FragColor;
in vec2 text_cord;
in vec2 normal_cords;

uniform sampler2D ourTexture;

void main()
{
  if ((int(text_cord.y * 100) % 2 == 0)){
    FragColor = texture(ourTexture, normal_cords) * vec4(0.0, 0.2, 0.5, 1.0);
  } else {
    FragColor = texture(ourTexture, text_cord);
  }
}
'''

shaders = [
  [texture_vertex_shader, texture_fragment_shader],
  [texture_normal_vertex, texture_normal_fragment],
  [stripes_vertex, stripes_fragment],
]