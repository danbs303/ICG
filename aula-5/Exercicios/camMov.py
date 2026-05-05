import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

eyeX = 8
eyeY = 5
eyeZ = 8
centerX = 0
centerY = 0
centerZ = 0

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)

def resize(window, w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w / h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def load_obj(path):
    vertices = []
    faces = []
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

def draw_ground():
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-50, -0.1, -50)
    glVertex3f(50, -0.1, -50)
    glVertex3f(50, -0.1, 50)
    glVertex3f(-50, -0.1, 50)
    glEnd()

def draw_axes():
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(10, 0, 0)
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 10, 0)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 10)
    glEnd()

def display(carro_v, carro_f, roda_v, roda_f):
    global T, T2, T3
    global eyeX, eyeY, eyeZ, centerX, centerY, centerZ

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, 0, 1, 0)

    glPushMatrix()
    glRotatef(T, 0, 1, 0)
    glTranslatef(0, 0, T3)

    glPushMatrix()
    glTranslatef(0, 1, 0)
    glColor3f(0.1, 0.3, 1.0)
    draw_obj(carro_v, carro_f)
    glPopMatrix()

    posicoes = [(1.2, 1, 3), (-1.2, 1, 3), (1.2, 1, -3), (-1.2, 1, -3)]
    for x, y, z in posicoes:
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(T2, 1, 0, 0)
        glColor3f(1, 0.2, 0.2)
        draw_obj(roda_v, roda_f)
        glPopMatrix()

    glPopMatrix()
    draw_ground()
    draw_axes()

def key_callback(window, key, scancode, action, mods):
    global eyeX, eyeY, eyeZ
    global centerX, centerY, centerZ

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:
            eyeZ -= 1
            centerZ -= 1
        elif key == glfw.KEY_DOWN:
            eyeZ += 1
            centerZ += 1
        elif key == glfw.KEY_LEFT:
            eyeX -= 1
            centerX -= 1
        elif key == glfw.KEY_RIGHT:
            eyeX += 1
            centerX += 1
        elif key == glfw.KEY_PAGE_UP:
            eyeY += 1
            centerY += 1
        elif key == glfw.KEY_PAGE_DOWN:
            eyeY -= 1
            centerY -= 1

def main():
    global T, T2, T3
    T = 0
    T2 = 0
    T3 = -20

    if not glfw.init():
        return

    window = glfw.create_window(1280, 720, "Camera Movivel", None, None)
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, resize)
    glfw.set_key_callback(window, key_callback)

    init()
    carro_v, carro_f = load_obj("carro.obj")
    roda_v, roda_f = load_obj("roda2.obj")

    while not glfw.window_should_close(window):
        display(carro_v, carro_f, roda_v, roda_f)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
