import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Inicialização GLFW
if not glfw.init():
    raise Exception("Falha ao iniciar GLFW")

window = glfw.create_window(800, 600, "AABB - Identificação da Direção do Impacto", None, None)
if not window:
    glfw.terminate()
    raise Exception("Falha ao criar janela")

glfw.make_context_current(window)
gluOrtho2D(-5, 5, -5, 5)

# --- OBJETO 1 (Jogador) ---
pos_jogador = [0.0, 0.0]
vel_jogador = 2.0
tamanho_jogador = 0.8

# --- OBJETO 2 (Obstáculo) ---
pos_obstaculo = [2.0, 1.5]
tamanho_obstaculo = 0.8

# --- VARIÁVEIS DE ESTADO ---
em_colisao = False
direcao_impacto = "NENHUMA"  # Pode ser: DIREITA, ESQUERDA, CIMA, BAIXO, NENHUMA
cor_colisao = (0.0, 0.0, 1.0)  # Azul normalmente

# Função para obter os limites AABB de um objeto
def obter_limites_aabb(pos_x, pos_y, tamanho):
    return {
        'min_x': pos_x - tamanho,
        'max_x': pos_x + tamanho,
        'min_y': pos_y - tamanho,
        'max_y': pos_y + tamanho
    }

# Função para verificar colisão AABB e identificar direção do impacto
def verificar_colisao_aabb_com_direcao(pos1, tam1, pos2, tam2):
    # Obtém limites
    obj1 = obter_limites_aabb(pos1[0], pos1[1], tam1)
    obj2 = obter_limites_aabb(pos2[0], pos2[1], tam2)

    # Verifica se há colisão
    colidiu = (obj1['max_x'] >= obj2['min_x'] and obj1['min_x'] <= obj2['max_x'] and
               obj1['max_y'] >= obj2['min_y'] and obj1['min_y'] <= obj2['max_y'])

    if not colidiu:
        return False, "NENHUMA"

    # CALCULA A SOBREPOSIÇÃO EM CADA EIXO
    sobreposicao_x = min(obj1['max_x'] - obj2['min_x'], obj2['max_x'] - obj1['min_x'])
    sobreposicao_y = min(obj1['max_y'] - obj2['min_y'], obj2['max_y'] - obj1['min_y'])

    # DETERMINA A DIREÇÃO DO IMPACTO (a menor sobreposição define o eixo de contato)
    if sobreposicao_x < sobreposicao_y:
        # Impacto no eixo X
        if pos1[0] < pos2[0]:
            direcao = "DIREITA"  # Objeto 1 está à esquerda, colidiu pela direita
        else:
            direcao = "ESQUERDA"  # Objeto 1 está à direita, colidiu pela esquerda
    else:
        # Impacto no eixo Y
        if pos1[1] < pos2[1]:
            direcao = "CIMA"  # Objeto 1 está abaixo, colidiu por cima
        else:
            direcao = "BAIXO"  # Objeto 1 está acima, colidiu por baixo

    return True, direcao

# Função para desenhar um quadrado
def desenhar_quadrado(x, y, tamanho, cor):
    glColor3f(cor[0], cor[1], cor[2])
    glBegin(GL_QUADS)
    glVertex2f(x - tamanho, y - tamanho)
    glVertex2f(x + tamanho, y - tamanho)
    glVertex2f(x + tamanho, y + tamanho)
    glVertex2f(x - tamanho, y + tamanho)
    glEnd()

# Função para desenhar o contorno AABB (modo debug)
def desenhar_contorno_aabb(x, y, tamanho, cor):
    glColor3f(cor[0], cor[1], cor[2])
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x - tamanho, y - tamanho)
    glVertex2f(x + tamanho, y - tamanho)
    glVertex2f(x + tamanho, y + tamanho)
    glVertex2f(x - tamanho, y + tamanho)
    glEnd()

# Função para desenhar a seta indicando direção
def desenhar_seta_direcao(x, y, direcao):
    if direcao == "NENHUMA":
        return

    glColor3f(1.0, 1.0, 0.0)  # Amarelo
    glLineWidth(3.0)

    comprimento = 1.0
    if direcao == "DIREITA":
        glBegin(GL_LINES)
        glVertex2f(x + 0.5, y)
        glVertex2f(x + 0.5 + comprimento, y)
        glEnd()
        # Ponta da seta
        glBegin(GL_TRIANGLES)
        glVertex2f(x + 0.5 + comprimento, y)
        glVertex2f(x + 0.5 + comprimento - 0.2, y + 0.1)
        glVertex2f(x + 0.5 + comprimento - 0.2, y - 0.1)
        glEnd()
    elif direcao == "ESQUERDA":
        glBegin(GL_LINES)
        glVertex2f(x - 0.5, y)
        glVertex2f(x - 0.5 - comprimento, y)
        glEnd()
        glBegin(GL_TRIANGLES)
        glVertex2f(x - 0.5 - comprimento, y)
        glVertex2f(x - 0.5 - comprimento + 0.2, y + 0.1)
        glVertex2f(x - 0.5 - comprimento + 0.2, y - 0.1)
        glEnd()
    elif direcao == "CIMA":
        glBegin(GL_LINES)
        glVertex2f(x, y + 0.5)
        glVertex2f(x, y + 0.5 + comprimento)
        glEnd()
        glBegin(GL_TRIANGLES)
        glVertex2f(x, y + 0.5 + comprimento)
        glVertex2f(x + 0.1, y + 0.5 + comprimento - 0.2)
        glVertex2f(x - 0.1, y + 0.5 + comprimento - 0.2)
        glEnd()
    elif direcao == "BAIXO":
        glBegin(GL_LINES)
        glVertex2f(x, y - 0.5)
        glVertex2f(x, y - 0.5 - comprimento)
        glEnd()
        glBegin(GL_TRIANGLES)
        glVertex2f(x, y - 0.5 - comprimento)
        glVertex2f(x + 0.1, y - 0.5 - comprimento + 0.2)
        glVertex2f(x - 0.1, y - 0.5 - comprimento + 0.2)
        glEnd()

# --- LOOP PRINCIPAL ---
tempo_anterior = glfw.get_time()

while not glfw.window_should_close(window):
    # CALCULA DELTA TIME
    tempo_atual = glfw.get_time()
    delta_time = tempo_atual - tempo_anterior
    tempo_anterior = tempo_atual

    # CONTROLES DO JOGADOR
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        pos_jogador[0] -= vel_jogador * delta_time
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        pos_jogador[0] += vel_jogador * delta_time
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        pos_jogador[1] += vel_jogador * delta_time
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        pos_jogador[1] -= vel_jogador * delta_time

    # VERIFICA COLISÃO E DIREÇÃO DO IMPACTO
    em_colisao, direcao_impacto = verificar_colisao_aabb_com_direcao(
        pos_jogador, tamanho_jogador,
        pos_obstaculo, tamanho_obstaculo
    )

    # ATUALIZA A COR BASEADA NO ESTADO DA COLISÃO
    if em_colisao:
        cor_colisao = (1.0, 0.0, 0.0)  # Vermelho quando colide
    else:
        cor_colisao = (0.0, 0.0, 1.0)  # Azul normalmente

    # RENDERIZAÇÃO
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # Desenha obstáculo (verde)
    desenhar_quadrado(pos_obstaculo[0], pos_obstaculo[1], tamanho_obstaculo, (0.0, 1.0, 0.0))
    desenhar_contorno_aabb(pos_obstaculo[0], pos_obstaculo[1], tamanho_obstaculo, (0.5, 1.0, 0.5))

    # Desenha jogador (cor varia com colisão)
    desenhar_quadrado(pos_jogador[0], pos_jogador[1], tamanho_jogador, cor_colisao)
    desenhar_contorno_aabb(pos_jogador[0], pos_jogador[1], tamanho_jogador, (0.5, 0.5, 1.0))

    # Desenha seta indicando a direção do impacto
    if em_colisao:
        desenhar_seta_direcao(pos_jogador[0], pos_jogador[1], direcao_impacto)

    # Atualiza título da janela com informações
    titulo = f"Colisão: {'SIM' if em_colisao else 'NÃO'} | Direção: {direcao_impacto}"
    glfw.set_window_title(window, titulo)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
