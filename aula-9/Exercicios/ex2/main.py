import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from PIL import Image
import os
import sys


# CLASSE DO SHADER

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
    
    def set_float(self, name, value):
        location = glGetUniformLocation(self.ID, name)
        glUniform1f(location, value)



# FUNÇÃO PARA CARREGAR TEXTURA COM MIPMAP

def load_texture_with_mipmap(image_path):
    """Carrega uma imagem e cria uma textura com mipmap"""
    
    # Abre a imagem com PIL
    image = Image.open(image_path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(image, dtype=np.uint8)
    
    width, height = image.size
    
    # Converte para RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')
        img_data = np.array(image, dtype=np.uint8)
    
    # Gera a textura
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    # Configura os parâmetros
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    

    # CONFIGURAÇÃO COM MIPMAP

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # Envia os dados da imagem
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    

    # GERA OS MIPMAPS

    glGenerateMipmap(GL_TEXTURE_2D)
    
    glBindTexture(GL_TEXTURE_2D, 0)
    
    print(f"Textura carregada: {width}x{height} com mipmap")
    return texture


# VARIÁVEL GLOBAL
camera_z = -3.0

# CALLBACK DO TECLADO
def key_callback(window, key, scancode, action, mods):
    global camera_z
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_W:
            camera_z += 0.1
            print(f"Distância: {abs(camera_z):.2f}")
        
        elif key == glfw.KEY_S:
            camera_z -= 0.1
            print(f"Distância: {abs(camera_z):.2f}")
        
        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)



# FUNÇÃO PRINCIPAL

def main():
    global camera_z
    
    # --- INICIALIZAÇÃO GLFW ---
    if not glfw.init():
        print("Falha ao inicializar GLFW")
        return -1
    
    # Configuração para compatibilidade
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    
    window = glfw.create_window(800, 600, "Exercício 2 - Mipmap", None, None)
    if not window:
        print("Falha ao criar janela")
        glfw.terminate()
        return -1
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    
    # Mostra versão do OpenGL
    print(f"OpenGL: {glGetString(GL_VERSION)}")
    
    # --- CARREGA SHADERS ---
    try:
        shader = Shader("vertex_shader.glsl", "fragment_shader.glsl")
        print("Shaders carregados com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar shaders: {e}")
        glfw.terminate()
        return -1
    
    # --- CARREGA TEXTURA ---
    # Procura por uma imagem
    image_files = ["textura.jpg", "gato.jpg", "imagem.jpg", "foto.jpg"]
    texture = None
    
    for img_file in image_files:
        if os.path.exists(img_file):
            print(f"Carregando: {img_file}")
            try:
                texture = load_texture_with_mipmap(img_file)
                break
            except Exception as e:
                print(f"Erro ao carregar {img_file}: {e}")
    
    if texture is None:
        print("Nenhuma imagem encontrada!")
        print("Coloque uma imagem (textura.jpg) na pasta do programa")
        glfw.terminate()
        return -1
    

    # DADOS DO CUBO 

    vertices = np.array([
        # Frente (Z = 0.5)
        -0.5, -0.5,  0.5,  0.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 1.0,
        -0.5,  0.5,  0.5,  0.0, 1.0,
        # Trás (Z = -0.5)
        -0.5, -0.5, -0.5,  0.0, 0.0,
         0.5, -0.5, -0.5,  1.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
        -0.5,  0.5, -0.5,  0.0, 1.0,
        # Direita (X = 0.5)
         0.5, -0.5, -0.5,  0.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 1.0,
         0.5,  0.5, -0.5,  0.0, 1.0,
        # Esquerda (X = -0.5)
        -0.5, -0.5, -0.5,  0.0, 0.0,
        -0.5, -0.5,  0.5,  1.0, 0.0,
        -0.5,  0.5,  0.5,  1.0, 1.0,
        -0.5,  0.5, -0.5,  0.0, 1.0,
        # Cima (Y = 0.5)
        -0.5,  0.5, -0.5,  0.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 1.0,
        -0.5,  0.5,  0.5,  0.0, 1.0,
        # Baixo (Y = -0.5)
        -0.5, -0.5, -0.5,  0.0, 0.0,
         0.5, -0.5, -0.5,  1.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 1.0,
        -0.5, -0.5,  0.5,  0.0, 1.0,
    ], dtype=np.float32)
    
    indices = np.array([
        0, 1, 2,  0, 2, 3,       # Frente
        4, 6, 5,  4, 7, 6,       # Trás
        8, 9, 10, 8, 10, 11,     # Direita
        12, 14, 13, 12, 15, 14,  # Esquerda
        16, 17, 18, 16, 18, 19,  # Cima
        20, 22, 21, 20, 23, 22,  # Baixo
    ], dtype=np.uint32)
    
    # --- BUFFERS ---
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    
    # Posição (3 floats)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # UV (2 floats)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
    glEnableVertexAttribArray(1)
    
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    
    # --- CONFIGURAÇÕES ---
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    
    print("\n" + "="*60)
    print("EXERCÍCIO 2 - MIPMAP E CONTROLE DE DISTÂNCIA")
    print("="*60)
    print("\nControles:")
    print("  W - Aproximar")
    print("  S - Afastar")
    print("  ESC - Sair")
    print("="*60 + "\n")
    
    angle = 0.0
    
    # --- LOOP PRINCIPAL ---
    while not glfw.window_should_close(window):
        # Limpa a tela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Usa o shader
        shader.use()
        
        # Ativa e vincula a textura
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        shader.set_int("uTexture", 0)
        
    
        # MATRIZES MANUAIS (SIMPLES)
    
        # Matriz de projeção (perspectiva)
        aspect = 800 / 600
        fov = 1.0 / np.tan(np.radians(45) / 2.0)
        projection = np.array([
            [fov / aspect, 0, 0, 0],
            [0, fov, 0, 0],
            [0, 0, -1.0, -0.1],
            [0, 0, -1.0, 0]
        ], dtype=np.float32)
        
        # Matriz de visualização (câmera em Z)
        view = np.eye(4, dtype=np.float32)
        view[3, 2] = -camera_z
        
        # Matriz de modelo (rotação)
        angle += 0.5
        cos_a = np.cos(np.radians(angle))
        sin_a = np.sin(np.radians(angle))
        model = np.eye(4, dtype=np.float32)
        model[0, 0] = cos_a
        model[0, 2] = sin_a
        model[2, 0] = -sin_a
        model[2, 2] = cos_a
        
        # Envia as matrizes para o shader
        glUniformMatrix4fv(glGetUniformLocation(shader.ID, "uProjection"), 1, GL_FALSE, projection)
        glUniformMatrix4fv(glGetUniformLocation(shader.ID, "uView"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(shader.ID, "uModel"), 1, GL_FALSE, model)
        
        # Desenha o cubo
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
        
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