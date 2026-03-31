from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

angle = 0.0

def display():
    global angle
    
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    glRotatef(angle, 0.0, 0.0, 1.0)
    
    glBegin(GL_QUADS)
    
    # Roxo
    glColor3f(0.5, 0.0, 0.5)
    glVertex2f(-0.5, -0.5)
    
    # Vermelho
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0.5, -0.5)
    
    # Azul
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.5, 0.5)
    
    # Roxo novamente (fecha o gradiente bonito)
    glColor3f(0.7, 0.0, 1.0)
    glVertex2f(-0.5, 0.5)
    
    glEnd()
    
    glFlush()

def update(value):
    global angle
    angle += 1.0
    if angle > 360:
        angle = 0
    
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)

glutCreateWindow(b"Quadrado Animado")

glClearColor(0.0, 0.0, 0.0, 1.0)

glutDisplayFunc(display)
glutTimerFunc(0, update, 0)

glutMainLoop()