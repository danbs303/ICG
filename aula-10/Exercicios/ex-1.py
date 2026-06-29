import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Inicialização GLFW
if not glfw.init():
    raise Exception("Falha ao iniciar GLFW")

window = glfw.create_window(800, 600, "Colisão com Mudança de Cor", None, None)
if not window:
    glfw.terminate()
    raise Exception("Falha ao criar janela")

glfw.make_context_current(window)
gluOrtho2D(-5, 5, -5, 5)

# --- VARIÁVEIS DO JOGADOR ---
pos_jogador = [0.0, 0.0]
vel_jogador = 2.0  # unidades por segundo
tamanho = 0.5

# --- VARIÁVEIS DA BARREIRA (AABB) ---
barreira_min = [1.0, 1.0]
barreira_max = [1.5, 1.5]

# --- VARIÁVEL DE CONTROLE DE COR ---
em_colisao = False

# Função para verificar colisão AABB
def verificar_colisao_aabb(pos_x, pos_y, tamanho, barreira_min, barreira_max):
    # Calcula os limites do jogador
    jogador_min_x = pos_x - tamanho
    jogador_max_x = pos_x + tamanho
    jogador_min_y = pos_y - tamanho
    jogador_max_y = pos_y + tamanho
    
    # Verifica se há interseção (AABB vs AABB)
    if (jogador_max_x >= barreira_min[0] and jogador_min_x <= barreira_max[0] and
        jogador_max_y >= barreira_min[1] and jogador_min_y <= barreira_max[1]):
        return True
    return False

# Função para desenhar o jogador
def desenhar_jogador(x, y, em_colisao):
    glBegin(GL_QUADS)
    if em_colisao:
        glColor3f(1.0, 0.0, 0.0)  # VERMELHO quando em colisão
    else:
        glColor3f(0.0, 0.0, 1.0)  # AZUL normalmente
    glVertex2f(x - tamanho, y - tamanho)
    glVertex2f(x + tamanho, y - tamanho)
    glVertex2f(x + tamanho, y + tamanho)
    glVertex2f(x - tamanho, y + tamanho)
    glEnd()

# Função para desenhar a barreira
def desenhar_barreira():
    glColor3f(0.0, 1.0, 0.0)  # VERDE
    glBegin(GL_QUADS)
    glVertex2f(barreira_min[0], barreira_min[1])
    glVertex2f(barreira_max[0], barreira_min[1])
    glVertex2f(barreira_max[0], barreira_max[1])
    glVertex2f(barreira_min[0], barreira_max[1])
    glEnd()

# --- LOOP PRINCIPAL ---
tempo_anterior = glfw.get_time()

while not glfw.window_should_close(window):
    # CALCULA DELTA TIME
    tempo_atual = glfw.get_time()
    delta_time = tempo_atual - tempo_anterior
    tempo_anterior = tempo_atual
    
    # CONTROLES DO JOGADOR (Movimento contínuo)
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        pos_jogador[0] -= vel_jogador * delta_time
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        pos_jogador[0] += vel_jogador * delta_time
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        pos_jogador[1] += vel_jogador * delta_time
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        pos_jogador[1] -= vel_jogador * delta_time
    
    # VERIFICA COLISÃO AABB
    em_colisao = verificar_colisao_aabb(
        pos_jogador[0], pos_jogador[1], tamanho,
        barreira_min, barreira_max
    )
    
    # RENDERIZAÇÃO
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    desenhar_barreira()
    desenhar_jogador(pos_jogador[0], pos_jogador[1], em_colisao)
    
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()