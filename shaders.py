
# Colres de coordenadas de normal
vertex_shader = '''
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normals;
layout (location = 2) in vec3 textur_coords;
out vec3 ourColor;
uniform mat4 amatrix;

void main()
{
  gl_Position = amatrix * vec4(position, 1.0f);
  ourColor = normals;
}
'''
fragment_shader = '''
#version 460

layout (location = 0) out vec4 fragColor;
uniform vec3 color;
in vec3 ourColor;

void main()
{
  fragColor = vec4(ourColor.x, ourColor.y, ourColor.z, 1.0f);
  // fragColor = vec4(color, 1.0f);
}
'''

# Texturas
texture_vertex_shader = '''
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

texture_fragment_shader = '''
#version 450 core
out vec4 FragColor;
in vec3 ourColor;
in vec2 TexCoord;

uniform sampler2D ourTexture;

void main()
{
  FragColor = texture(ourTexture, TexCoord);
}
'''

shaders = {
  'normal_color': [vertex_shader, fragment_shader],
  'text_color': [texture_vertex_shader, texture_fragment_shader],
}