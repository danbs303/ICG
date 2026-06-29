import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from PIL import Image
import os

# classe do shader
class Shader:
    def __init__(self, vertex_path, fragment_path):
        with open(vertex_path, 'r') as f:
            vertex_code = f.read()
        with open(fragment_path, 'r') as f:
            fragment_code = f.read()
        
        vertex = compileShader(vertex_code, GL_VERTEX_SHADER)
        fragment = compileShader(fragment_code, GL_FRAGMENT_SHADER)
        self.ID = compileProgram(vertex, fragment)
        
        glDeleteShader(vertex)
        glDeleteShader(fragment)
    
    def use(self):
        glUseProgram(self.ID)
    
    def set_int(self, name, value):
        location = glGetUniformLocation(self.ID, name)
        glUniform1i(location, value)


# função para carregar textura
def load_texture(image_path):
    """Carrega uma imagem e cria uma textura OpenGL"""
    
    # Abre a imagem com PIL
    image = Image.open(image_path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL usa origem no canto inferior
    img_data = np.array(image, dtype=np.uint8)
    
    # Obtém dimensões e formato
    width, height = image.size
    
    # Converte para RGB ou RGBA
    if image.mode == 'RGB':
        format = GL_RGB
    elif image.mode == 'RGBA':
        format = GL_RGBA
    else:
        image = image.convert('RGB')
        img_data = np.array(image, dtype=np.uint8)
        format = GL_RGB
    
    # Gera a textura
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    # exercício 1: configuração com gl_repeat
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)  # Eixo S (horizontal)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  # Eixo T (vertical)
    
    # Configura os filtros 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # Envia os dados da imagem para a GPU
    glTexImage2D(GL_TEXTURE_2D, 0, format, width, height, 0, format, GL_UNSIGNED_BYTE, img_data)
    
    # Desvincula a textura
    glBindTexture(GL_TEXTURE_2D, 0)
    
    return texture


# callback do teclado
def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


# função principal
def main():
    # --- INICIALIZAÇÃO ---
    if not glfw.init():
        print("Falha ao inicializar GLFW")
        return -1
    
    window = glfw.create_window(800, 600, "Exercício 1 - Textura com GL_REPEAT 3x3", None, None)
    if not window:
        print("Falha ao criar janela")
        glfw.terminate()
        return -1
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    
    # --- carrega shaders ---
    try:
        shader = Shader("vertex_shader.glsl", "fragment_shader.glsl")
        print("Shaders carregados com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar shaders: {e}")
        glfw.terminate()
        return -1
    
    # --- CARREGA TEXTURA ---
    try:
        # Certifique-se de ter uma imagem chamada "textura.jpg" na mesma pasta
        texture = load_texture("textura.jpg")
        print("Textura carregada com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar textura: {e}")
        print("Certifique-se de ter uma imagem 'textura.jpg' na pasta do projeto")
        glfw.terminate()
        return -1
    
    # Vértices: posição (x,y) | coordenadas UV (s,t)
    # UV variam de 0 a 3 para repetir a textura 3x3
    vertices = np.array([
        # Posições (x,y)    # UV (s,t)
        -0.5, -0.5,         0.0, 0.0,   # Vértice 0: inferior esquerdo
         0.5, -0.5,         3.0, 0.0,   # Vértice 1: inferior direito
         0.5,  0.5,         3.0, 3.0,   # Vértice 2: superior direito
        -0.5,  0.5,         0.0, 3.0,   # Vértice 3: superior esquerdo
    ], dtype=np.float32)
    
    indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
    
    # --- buffers ---
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    
    # Posição 
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # uv 
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(GLfloat), ctypes.c_void_p(2 * sizeof(GLfloat)))
    glEnableVertexAttribArray(1)
    
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    
    # --- configurações ---
    glClearColor(0.2, 0.2, 0.2, 1.0)

    
    # --- loop principal ---
    while not glfw.window_should_close(window):
        # Limpa a tela
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Usa o shader
        shader.use()
        
        # Ativa e vincula a textura
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        shader.set_int("uTexture", 0)
        
        # Desenha o quadrado
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        
        # Troca buffers
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    # --- LIMPEZA ---
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteBuffers(1, [EBO])
    glDeleteTextures(1, [texture])
    glDeleteProgram(shader.ID)
    glfw.terminate()
    return 0


if __name__ == "__main__":
    main()