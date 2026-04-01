import glfw
from OpenGL.GL import *

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Gato", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)


        glBegin(GL_TRIANGLES)

        # orelha direita
        glColor3f(1.0, 0.71, 0.75)
        glVertex2f( 0.10, 0.7)  
        glVertex2f( 0.25, 0.5)  
        glVertex2f( 0.5, 1.0)  
 
        #  orelha esquerda
        glColor3f(1.0, 0.71, 0.75)
        glVertex2f( -0.10, 0.7)  
        glVertex2f( -0.25, 0.5)  
        glVertex2f( -0.5, 1.0)  

        # corpo cima
        glColor3f(0.7, 0.7, 0.7)
        glVertex2f(-0.4, 0.1)  
        glVertex2f( 0.4, 0.1)  
        glVertex2f( 0.0, 0.7)  
        
        # corpo baixo
        glColor3f(0.7, 0.7, 0.7)
        glVertex2f(-0.6, -0.8) 
        glVertex2f( 0.6, -0.8) 
        glVertex2f( 0.0, 0.1) 
        glEnd()

      
        glBegin(GL_QUADS)

        # Olho esquerdo
        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(-0.10, 0.40)
        glVertex2f(-0.17, 0.40)
        glVertex2f(-0.17, 0.45)
        glVertex2f(-0.10, 0.45)

        # Olho direito
        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(0.10, 0.40)
        glVertex2f(0.17, 0.40)
        glVertex2f(0.17, 0.45)
        glVertex2f(0.10, 0.45)

        glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

main()


