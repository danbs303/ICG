import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Inicialização GLFW
if not glfw.init():
    raise Exception("Falha ao iniciar GLFW")

window = glfw.create_window(800, 600, "Esferas Concêntricas - Colisão e Aviso", None, None)
if not window:
    glfw.terminate()
    raise Exception("Falha ao criar janela")

glfw.make_context_current(window)
gluOrtho2D(-10, 10, -10, 10)

# --- OBJETO PRINCIPAL (Jogador) ---
pos_jogador = [0.0, 0.0]
vel_jogador = 3.0
raio_colisao = 1.0      # Raio real de colisão (interno)
raio_aviso = 1.5        # Raio de aviso (externo)

# --- OBSTÁCULO ---
pos_obstaculo = [4.0, 3.0]
raio_obstaculo = 1.0

# --- VARIÁVEIS DE ESTADO ---
estado_colisao = "NORMAL"  # Pode ser "NORMAL", "AVISO" ou "COLISAO"

# Função para verificar distância entre dois pontos
def distancia_entre_pontos(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Função para verificar colisão com esferas concêntricas
def verificar_esferas_concêntricas(pos1, raio_interno, raio_externo, pos2, raio2):
    dist = distancia_entre_pontos(pos1, pos2)
    dist_min_colisao = raio_interno + raio2
    dist_min_aviso = raio_externo + raio2

    if dist <= dist_min_colisao:
        return "COLISAO"
    elif dist <= dist_min_aviso:
        return "AVISO"
    else:
        return "NORMAL"

# Função para desenhar um círculo (como esfera 2D)
def desenhar_circulo(x, y, raio, cor, segments=32):
    glColor3f(cor[0], cor[1], cor[2])
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)  # Centro
    for i in range(segments + 1):
        theta = 2.0 * math.pi * i / segments
        dx = raio * math.cos(theta)
        dy = raio * math.sin(theta)
        glVertex2f(x + dx, y + dy)
    glEnd()

# Função para desenhar o contorno do círculo (modo debug visual)
def desenhar_contorno_circulo(x, y, raio, cor, segments=32):
    glColor3f(cor[0], cor[1], cor[2])
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    for i in range(segments + 1):
        theta = 2.0 * math.pi * i / segments
        dx = raio * math.cos(theta)
        dy = raio * math.sin(theta)
        glVertex2f(x + dx, y + dy)
    glEnd()

# Função para desenhar o jogador com esferas concêntricas
def desenhar_jogador(x, y, estado):
    # Desenha a esfera externa (aviso) - sempre visível
    desenhar_contorno_circulo(x, y, raio_aviso, (1.0, 1.0, 0.0))  # Amarelo

    # Desenha a esfera interna (colisão real)
    if estado == "COLISAO":
        cor = (1.0, 0.0, 0.0)  # Vermelho - colidindo
    elif estado == "AVISO":
        cor = (1.0, 0.5, 0.0)  # Laranja - em aviso
    else:
        cor = (0.0, 0.0, 1.0)  # Azul - normal

    desenhar_circulo(x, y, raio_colisao, cor)

# Função para desenhar o obstáculo
def desenhar_obstaculo(x, y):
    desenhar_circulo(x, y, raio_obstaculo, (0.0, 1.0, 0.0))  # Verde

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

    # VERIFICA ESTADO DA COLISÃO
    estado_colisao = verificar_esferas_concêntricas(
        pos_jogador, raio_colisao, raio_aviso,
        pos_obstaculo, raio_obstaculo
    )

    # RENDERIZAÇÃO
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    desenhar_obstaculo(pos_obstaculo[0], pos_obstaculo[1])
    desenhar_jogador(pos_jogador[0], pos_jogador[1], estado_colisao)

    # Exibe informações na janela (usando texto simples via título)
    titulo = f"Estado: {estado_colisao} | Pos: ({pos_jogador[0]:.1f}, {pos_jogador[1]:.1f})"
    glfw.set_window_title(window, titulo)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
