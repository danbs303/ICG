# Trbalho 1 Introdução a Computação Gráfica
# Aluno: Danilo Barbosa da Silva
# Professora: Taina Isabela Monteiro Da Silva  

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# estado global da câmera
eyeX, eyeY, eyeZ       = 0.0, 15.0, 25.0
centerX, centerY, centerZ = 0.0,  0.0,  0.0

# ângulos de órbita 
angle_terra = 0.0   # terra ao redor do sol
angle_lua   = 0.0   # lua   ao redor da terra
angle_sol   = 0.0   # rotação própria do sol

# controle de pausa e velocidade
pausado    = False
vel_terra  = 1.0    # graus por frame
vel_lua    = 3.0

# escala do sol 
escala_sol = 1.0

# carrega objeto
def load_obj(path):
    vertices = []
    faces    = []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                face = []
                for p in parts:
                    idx = p.split('/')[0]
                    face.append(int(idx) - 1)
                faces.append(face)
    return vertices, faces

def draw_obj(vertices, faces):
    glBegin(GL_TRIANGLES)
    for face in faces:
        for idx in face:
            glVertex3f(*vertices[idx])
    glEnd()

# inicialização opengl
def init():
    glClearColor(0.0, 0.0, 0.05, 1.0)   # fundo quase preto (espaço)
    glEnable(GL_DEPTH_TEST)

# callback de redimensionamento
def resize(window, w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w / h, 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW)


# Equivalente :
# sphere = gluNewQuadric()
# gluSphere(sphere, 1.0, 32, 16)
# função da esfera
# ----------------------------------------------------------------------------------------------# 
# objeto manual
def draw_sphere_manual(radius, stacks, slices, cor_topo, cor_base):
    
    def vertex_color(lat_norm):
        # lat_norm: 0.0 = base, 1.0 = topo
        r = cor_base[0] + (cor_topo[0] - cor_base[0]) * lat_norm
        g = cor_base[1] + (cor_topo[1] - cor_base[1]) * lat_norm
        b = cor_base[2] + (cor_topo[2] - cor_base[2]) * lat_norm
        glColor3f(r, g, b)

    glBegin(GL_TRIANGLES)
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + i       / stacks)
        lat1 = math.pi * (-0.5 + (i + 1) / stacks)
        z0, zr0 = math.sin(lat0), math.cos(lat0)
        z1, zr1 = math.sin(lat1), math.cos(lat1)
        t0 = (i)       / stacks   # 0→1 de baixo para cima
        t1 = (i + 1)   / stacks

        for j in range(slices):
            lng0 = 2 * math.pi * j       / slices
            lng1 = 2 * math.pi * (j + 1) / slices
            x00, y00 = math.cos(lng0) * zr0, math.sin(lng0) * zr0
            x10, y10 = math.cos(lng0) * zr1, math.sin(lng0) * zr1
            x01, y01 = math.cos(lng1) * zr0, math.sin(lng1) * zr0
            x11, y11 = math.cos(lng1) * zr1, math.sin(lng1) * zr1

            # triângulo 1
            vertex_color(t0); glVertex3f(x00 * radius, y00 * radius, z0 * radius)
            vertex_color(t1); glVertex3f(x10 * radius, y10 * radius, z1 * radius)
            vertex_color(t1); glVertex3f(x11 * radius, y11 * radius, z1 * radius)
            # triângulo 2
            vertex_color(t0); glVertex3f(x00 * radius, y00 * radius, z0 * radius)
            vertex_color(t1); glVertex3f(x11 * radius, y11 * radius, z1 * radius)
            vertex_color(t0); glVertex3f(x01 * radius, y01 * radius, z0 * radius)
    glEnd()
# ----------------------------------------------------------------------------------------------# 

# eixos de coordenadas 
def draw_axes(size=5.0):
    glBegin(GL_LINES)
    glColor3f(1, 0, 0); glVertex3f(0,0,0); glVertex3f(size,0,0)
    glColor3f(0, 1, 0); glVertex3f(0,0,0); glVertex3f(0,size,0)
    glColor3f(0, 0, 1); glVertex3f(0,0,0); glVertex3f(0,0,size)
    glEnd()


# círculos pontilhados para referência
def draw_orbit(radius, segments=64):
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        a = 2 * math.pi * i / segments
        glVertex3f(math.cos(a) * radius, 0, math.sin(a) * radius)
    glEnd()


# funcão display chamado a cada frame
def display(ufo_v,ufo_f):
    global angle_terra, angle_lua, angle_sol
    global eyeX, eyeY, eyeZ, centerX, centerY, centerZ
    global escala_sol, pausado, vel_terra, vel_lua

    # atualiza ângulos (animação) 
    if not pausado:
        angle_terra = (angle_terra + vel_terra) % 360
        angle_lua   = (angle_lua   + vel_lua)   % 360
        angle_sol   = (angle_sol   + 0.3)       % 360

    #  limpa buffers 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # câmera 
    # posição do observador, ponto alvo, vetor "up"
    gluLookAt(eyeX, eyeY, eyeZ,
              centerX, centerY, centerZ,
              0, 1, 0)

    # eixos e órbitas (referência) 
    draw_axes(8.0)
    draw_orbit(8.0)    # órbita da terra
    draw_orbit(3.0)    # órbita da lua (desenhada na origem — relativa)

    # SOL — centro da cena
    glPushMatrix()
    glRotatef(angle_sol, 0, 1, 0)          
    glScalef(escala_sol, escala_sol, escala_sol)  
    draw_sphere_manual(2.0, 20, 20,
                       cor_topo=(1.0, 1.0, 0.3),
                       cor_base=(1.0, 0.4, 0.0))
    glPopMatrix()

    # TERRA — orbita o Sol
    glPushMatrix()
    glRotatef(angle_terra, 0, 1, 0) 
    glTranslatef(8.0, 0.0, 0.0) 
    draw_sphere_manual(0.8, 16, 16,
                       cor_topo=(0.2, 0.5, 1.0),
                       cor_base=(0.1, 0.6, 0.2)) 

    # LUA — orbita a Terra 
    glPushMatrix() 
    glRotatef(angle_lua, 0, 1, 0) 
    glTranslatef(3.0, 0.0, 0.0) 
    draw_sphere_manual(0.3, 12, 12,
                       cor_topo=(0.85, 0.85, 0.85),
                       cor_base=(0.4,  0.4,  0.4))

    # OVNI
    glPushMatrix()
    glRotatef(angle_lua*2, 0, 1, 0)  # orbita a lua 
    glTranslatef(1.0, 0.2, 0.0)    # posição ao redor da lua
    glScalef(0.01, 0.01, 0.01)        # ajusta tamanho
    glColor3f(0.6, 0.0, 5.0)       # cor verde 
    glRotatef(angle_sol*3, 0,1,0)
    draw_obj(ufo_v, ufo_f)

    glPopMatrix()  # fim contexto ovni
    glPopMatrix()  # fim contexto Lua
    glPopMatrix()  # fim contexto Terra


# callbacks de teclado
def key_callback(window, key, scancode, action, mods):
    global eyeX, eyeY, eyeZ, centerX, centerY, centerZ
    global vel_terra, vel_lua, escala_sol, pausado

    if action not in (glfw.PRESS, glfw.REPEAT):
        return

    # câmera 
    if key == glfw.KEY_UP:
        eyeZ -= 1; centerZ -= 1
    elif key == glfw.KEY_DOWN:
        eyeZ += 1; centerZ += 1
    elif key == glfw.KEY_LEFT:
        eyeX -= 1; centerX -= 1
    elif key == glfw.KEY_RIGHT:
        eyeX += 1; centerX += 1
    elif key == glfw.KEY_PAGE_UP:
        eyeY += 1; centerY += 1
    elif key == glfw.KEY_PAGE_DOWN:
        eyeY -= 1; centerY -= 1

    # velocidade das órbitas
    elif key == glfw.KEY_W:
        vel_terra = min(vel_terra + 0.5, 10.0)   # acelera Terra
    elif key == glfw.KEY_S:
        vel_terra = max(vel_terra - 0.5, 0.0)    # freia Terra
    elif key == glfw.KEY_E:
        vel_lua = min(vel_lua + 0.5, 15.0)       # acelera Lua
    elif key == glfw.KEY_D:
        vel_lua = max(vel_lua - 0.5, 0.0)        # freia Lua

    # escala do sol 
    elif key == glfw.KEY_KP_ADD or key == glfw.KEY_EQUAL:
        escala_sol = min(escala_sol + 0.1, 3.0)
    elif key == glfw.KEY_KP_SUBTRACT or key == glfw.KEY_MINUS:
        escala_sol = max(escala_sol - 0.1, 0.2)

    # pausa 
    elif key == glfw.KEY_SPACE:
        pausado = not pausado

    #  sair 
    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)


# loop principal
def main():
    if not glfw.init():
        return

    window = glfw.create_window(1280, 720, "trabalho", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, resize)
    glfw.set_key_callback(window, key_callback)

    init()

    # dispara resize inicial para configurar projeção
    resize(window, 1280, 720)

    # carrega objeto
    ufo_v, ufo_f = load_obj("UFO.obj")
    
    # loop principal
    while not glfw.window_should_close(window):
        display(ufo_v,ufo_f)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()