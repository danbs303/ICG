import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def desenha():
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1.0, 0.0, 0.0)

    glBegin(GL_QUADS)
    glVertex2i(100, 150)
    glVertex2i(100, 100)

    glColor3f(0.0, 0.0, 1.0)
    glVertex2i(150, 100)
    glVertex2i(150, 150)
    glEnd()

def main():
    if not glfw.init():
        print("Erro ao iniciar GLFW")
        return

    window = glfw.create_window(400, 350, "Mistério", None, None)

    if not window:
        glfw.terminate()
        print("Erro ao criar janela")
        return

    glfw.make_context_current(window)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 250, 0, 250)

    while not glfw.window_should_close(window):
        desenha()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

main()
