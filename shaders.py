from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# Programacion de Shaders
vertex_shader = '''
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;
out vec3 ourColor;
uniform mat4 amatrix;

void main()
{
  gl_Position = amatrix * vec4(position, 1.0f);
  ourColor = vertexColor;
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

shaders = {
  'color': [vertex_shader, fragment_shader]
}