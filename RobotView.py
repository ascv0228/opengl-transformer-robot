from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

class RobotView:
    def __init__(self):
        # 初始化視角參數
        self.view_x = 0.0
        self.view_y = 0.0
        self.view_z = -15.0
        self.view_rot_x = 0.0
        self.view_rot_y = 0.0

        # OpenGL視角設置
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, 1, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -5)
        glEnable(GL_DEPTH_TEST)

    def render(self, robot):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # 應用視角變換
        glTranslatef(self.view_x, self.view_y, self.view_z)
        glRotatef(self.view_rot_x, 1, 0, 0)
        glRotatef(self.view_rot_y, 0, 1, 0)
        
        # 渲染機器人
        robot.body.render()
        
        pygame.display.flip() 