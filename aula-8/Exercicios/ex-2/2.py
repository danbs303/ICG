import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

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
    
    def set_float(self, name, value):
        location = glGetUniformLocation(self.ID, name)
        glUniform1f(location, value)
    
    def set_vec3(self, name, x, y, z):
        location = glGetUniformLocation(self.ID, name)
        glUniform3f(location, x, y, z)


# callback do teclado 
shininess_value = 32.0  # Valor inicial (material padrão)

def key_callback(window, key, scancode, action, mods):
    global shininess_value
    
    if action == glfw.PRESS:
        if key == glfw.KEY_F:
            shininess_value = 2.0
            print(f"Material FOSCO (shininess = {shininess_value:.1f})")
        
        elif key == glfw.KEY_P:
            shininess_value = 128.0
            print(f"Material POLIDO (shininess = {shininess_value:.1f})")
        
        elif key == glfw.KEY_R:
            shininess_value = 32.0
            print(f"Material PADRÃO (shininess = {shininess_value:.1f})")
        
        # Ajuste fino com + e -
        elif key == glfw.KEY_KP_ADD or key == glfw.KEY_EQUAL:
            shininess_value = min(shininess_value + 5.0, 256.0)
            print(f"Shininess = {shininess_value:.1f}")
        
        elif key == glfw.KEY_KP_SUBTRACT or key == glfw.KEY_MINUS:
            shininess_value = max(shininess_value - 5.0, 1.0)
            print(f"Shininess = {shininess_value:.1f}")
        
        # Sair
        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)


# função principal
def main():
    global shininess_value
    
    # --- inicialização ---
    if not glfw.init():
        print("Falha ao inicializar GLFW")
        return -1
    
    window = glfw.create_window(800, 600, "Exercício 2 - Controle de Shininess", None, None)
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
    
    # --- dados do quadrado ---
    vertices = np.array([
        # Posições (x,y)  # Normais (nx,ny,nz)
        -0.5, -0.5,       0.0, 0.0, 1.0,
         0.5, -0.5,       0.0, 0.0, 1.0,
         0.5,  0.5,       0.0, 0.0, 1.0,
        -0.5,  0.5,       0.0, 0.0, 1.0,
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
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # Normal
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), ctypes.c_void_p(2 * sizeof(GLfloat)))
    glEnableVertexAttribArray(1)
    
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    
    # --- configurações ---
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)
    
    # Posições
    light_pos = np.array([2.0, 2.0, 2.0], dtype=np.float32)
    camera_pos = np.array([0.0, 0.0, 2.0], dtype=np.float32)
    
    # --- menu de controles ---
    print("\n" + "="*60)
    print("EXERCÍCIO 2 - CONTROLE DE SHININESS")
    print("="*60)
    print("\nTeclas de Controle:")
    print("  F - Material FOSCO (shininess = 2.0)")
    print("  P - Material POLIDO (shininess = 128.0)")
    print("  R - Material PADRÃO (shininess = 32.0)")
    print("  + - Aumentar shininess")
    print("  - - Diminuir shininess")
    print("  ESC - Sair")
    print("\nValor atual: shininess = 32.0")
    print("="*60 + "\n")
    
    # --- loop principal ---
    while not glfw.window_should_close(window):
        # Limpa a tela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Usa o shader
        shader.use()
        
        # Envia os uniforms
        shader.set_vec3("uLightPos", light_pos[0], light_pos[1], light_pos[2])
        shader.set_vec3("uViewPos", camera_pos[0], camera_pos[1], camera_pos[2])
        
        # ENVIA O SHININESS PARA O SHADER (parte principal do exercício)
        shader.set_float("uShininess", shininess_value)
        
        # Desenha o quadrado
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        
        # Troca buffers
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