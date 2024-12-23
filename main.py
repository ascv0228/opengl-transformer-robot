import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from robot import Robot
import sys

class Application:
    def __init__(self, width=1000, height=1000):
        # 初始化Pygame
        pygame.init()
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Robot Arm Simulation")
        
        # 創建機器人實例
        self.robot = Robot()
        
        # 控制器相關屬性
        self.mouse_pressed = False
        self.last_mouse_pos = None
        self.keys_pressed = {
            pygame.K_z: False,
            pygame.K_x: False,
            pygame.K_c: False,
            pygame.K_v: False,
            pygame.K_b: False,
            pygame.K_n: False,
            pygame.K_a: False,
            
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False
        }
        
        # 添加新的控制變數
        self.auto_stepping = False
        self.step_count = 0
    
    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左鍵按下
                self.mouse_pressed = True
                self.last_mouse_pos = pygame.mouse.get_pos()
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 左鍵釋放
                self.mouse_pressed = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_pressed:
                current_pos = pygame.mouse.get_pos()
                if self.last_mouse_pos:
                    # 計算滑鼠移動距離
                    dx = current_pos[0] - self.last_mouse_pos[0]
                    dy = current_pos[1] - self.last_mouse_pos[1]
                    
                    # 更新視角旋轉
                    self.robot.view.view_rot_y += dx * 0.5
                    self.robot.view.view_rot_x += dy * 0.5
                    
                    # 限制x軸旋轉範圍
                    self.robot.view.view_rot_x = max(-90, min(90, self.robot.view.view_rot_x))
                
                self.last_mouse_pos = current_pos
    
    def handle_keyboard_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit()
            # 記錄按鍵按下狀態
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = True

            # 處理 a 鍵的切換
            if event.key == pygame.K_a:
                self.auto_stepping = not self.auto_stepping
                
            if event.key == pygame.K_r:
                self.robot.change_state()

            if event.key == pygame.K_f:
                self.robot.change_fill()    
                
        elif event.type == pygame.KEYUP:
            # 記錄按鍵釋放狀態
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = False
    
    def update_controls(self):
        vec = 0.1
        # 如果自動執行被啟用，調用 all_add_step
        if self.auto_stepping:
            self.step_count += 1
            if self.step_count % 10 == 0:
                self.step_count = 0
                self.robot.all_add_step()
            
        # 檢查並處理所有被按下的按鍵
        if self.keys_pressed[pygame.K_z]:
            self.robot.root_joint.rotate()
            # print("root_joint", self.robot.root_joint.angle)
            pass
        if self.keys_pressed[pygame.K_x]:
            self.robot.right_shoulder_joint.rotate()
            # print("right_shoulder_joint", self.robot.right_shoulder_joint.angle)
            pass
        if self.keys_pressed[pygame.K_c]:
            self.robot.left_shoulder_joint.rotate()
            # print("left_shoulder_joint", self.robot.left_shoulder_joint.angle)

        if self.keys_pressed[pygame.K_v]:
            self.robot.left_leg_joint.rotate()
            # print("left_leg_joint", self.robot.left_leg_joint.angle)
        if self.keys_pressed[pygame.K_b]:
            self.robot.right_leg_joint.rotate()
            # print("right_leg_joint", self.robot.right_leg_joint.angle)

        if self.keys_pressed[pygame.K_n]:
            self.robot.tail_joint.rotate()
            # print("tail_joint", self.robot.tail_joint.angle)

        if self.keys_pressed[pygame.K_LEFT]:
            self.robot.view.view_x += vec
        if self.keys_pressed[pygame.K_RIGHT]:
            self.robot.view.view_x -= vec
        if self.keys_pressed[pygame.K_UP]:
            self.robot.view.view_z += vec
        if self.keys_pressed[pygame.K_DOWN]:
            self.robot.view.view_z -= vec
    
    def run(self):
        """應用程序主循環"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                
                self.handle_mouse_events(event)
                self.handle_keyboard_events(event)
            
            self.update_controls()
            self.robot.view.render(self.robot)
            pygame.time.wait(10)
            
    def quit(self):
        """退出應用程序"""
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    app = Application()
    app.run()
