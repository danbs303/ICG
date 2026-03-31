import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
                # função para desenhar elipse e onda (roubadas da net)
###########################################################################

def draw_ellipse(cx, cy, rx, ry, r, g, b, segments=100):
    glColor3f(r, g, b)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        glVertex2f(cx + rx * math.cos(angle), cy + ry * math.sin(angle))
    glEnd()

def draw_wave(y_center, color, amplitude=0.04, freq=3.5, offset=0.0):
    glColor3f(*color)
    glLineWidth(3.0)
    glBegin(GL_LINE_STRIP)
    steps = 200
    for i in range(steps + 1):
        x = -0.55 + 1.1 * i / steps
        y = y_center + amplitude * math.sin(freq * math.pi * x + offset)
        glVertex2f(x, y)
    glEnd()

###########################################################################

def main():
    if not glfw.init():
        return
    window = glfw.create_window(600, 600, "Ovo", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glClearColor(1.0, 1.00, 1.00, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # sombra
        draw_ellipse(0.03, -0.03, 0.52, 0.63, 0.75, 0.75, 0.76)

        # corpo do ovo 
        draw_ellipse(0.0, 0.0, 0.50, 0.62, 1.0, 0.37, 0.62)

        # reflexo 
        draw_ellipse(-0.15, 0.35, 0.10, 0.08, 1.0, 0.52, 0.75)

        # linha ondulada amarela
        draw_wave(0.08, (0.96, 0.78, 0.26))

        # linha ondulada azul
        draw_wave(-0.08, (0.36, 0.78, 0.96))

        # bolinhas brancas
        draw_ellipse(-0.18, -0.32, 0.07, 0.04, 1.0, 1.0, 1.0)
        draw_ellipse( 0.00, -0.38, 0.07, 0.04, 1.0, 1.0, 1.0)
        draw_ellipse( 0.18, -0.32, 0.07, 0.04, 1.0, 1.0, 1.0)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

main()

