import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import sys


# classe do shader 
class Shader:
    def __init__(self, vertex_path, fragment_path):
        # Lê os arquivos
        with open(vertex_path, 'r') as f:
            vertex_code = f.read()
        with open(fragment_path, 'r') as f:
            fragment_code = f.read()
        
        # compila e linka
        vertex = compileShader(vertex_code, GL_VERTEX_SHADER)
        fragment = compileShader(fragment_code, GL_FRAGMENT_SHADER)
        self.ID = compileProgram(vertex, fragment)
        
        # limpeza
        glDeleteShader(vertex)
        glDeleteShader(fragment)
    
    def use(self):
        glUseProgram(self.ID)
    
    def set_float(self, name, value):
        location = glGetUniformLocation(self.ID, name)
        glUniform1f(location, value)
    
    def set_vec3(self, name, x, y, z):
        location = glGetUniformLocation(self.ID, name)
        glUniform3f(location, x, y, z)

#

# callback do teclado
def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)



# função principal

def main():
    # --- inicialização ---
    if not glfw.init():
        return -1
    
    # cria janela
    window = glfw.create_window(800, 600, "Efeito de Alerta - Quadrado Pulsante", None, None)
    if not window:
        glfw.terminate()
        return -1
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    
    # --- carrega shaders ---
    try:
        shader = Shader("vertex_shader.glsl", "fragment_shader.glsl")
    except Exception as e:
        glfw.terminate()
        return -1
    
    # --- dados do quadrado ---
    vertices = np.array([
        # posições     # normais (para iluminação)
        -0.5, -0.5,    0.0,  0.0,  1.0,  # Vértice 0: inferior esquerdo
         0.5, -0.5,    0.0,  0.0,  1.0,  # Vértice 1: inferior direito
         0.5,  0.5,    0.0,  0.0,  1.0,  # Vértice 2: superior direito
        -0.5,  0.5,    0.0,  0.0,  1.0,  # Vértice 3: superior esquerdo
    ], dtype=np.float32)
    
    # Índices para formar dois triângulos
    indices = np.array([
        0, 1, 2,  # Primeiro triângulo
        0, 2, 3   # Segundo triângulo
    ], dtype=np.uint32)
    
    # --- buffers ---
    # vao
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    
    # vbo
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    # ebo
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    
    # configura atributos
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # importante para iluminação
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), ctypes.c_void_p(2 * sizeof(GLfloat)))
    glEnableVertexAttribArray(1)
    
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    
    # --- configurações ---
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)
    
    # posição da luz e da câmera
    light_pos = np.array([2.0, 2.0, 2.0], dtype=np.float32)
    camera_pos = np.array([0.0, 0.0, 2.0], dtype=np.float32)
    
    
    # --- loop principal ---
    while not glfw.window_should_close(window):
        # limpa a tela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # usa o shader
        shader.use()
        
        # envia os uniforms
        shader.set_float("uTime", glfw.get_time())
        shader.set_vec3("uLightPos", light_pos[0], light_pos[1], light_pos[2])
        shader.set_vec3("uViewPos", camera_pos[0], camera_pos[1], camera_pos[2])
        
        # desenha o quadrado
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        
        # troca buffers
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    # --- limpeza ---
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteBuffers(1, [EBO])
    glDeleteProgram(shader.ID)
    glfw.terminate()
    return 0


if __name__ == "__main__":
    main()