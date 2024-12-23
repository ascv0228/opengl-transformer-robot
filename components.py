from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

class Node:
    wireframe_color = (0, 0, 0)
    """基礎節點類，提供基本的變換和渲染功能"""
    def __init__(self, name):
        self.name = name
        self.children = []
        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0, 0]  # (angle, x, y, z)
        self.visible = True
        self.parent = None
        self.color = (1.0, 1.0, 1.0)  # 預設白色
        self.fill = True
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        return child
        
    def set_translation(self, x, y, z):
        self.translation = [x, y, z]
        
    def set_rotation(self, angle, x, y, z):
        self.rotation = [angle, x, y, z]
        
    def set_color(self, r, g, b):
        self.color = (r, g, b)
    
    def set_fill(self, fill):
        self.fill = fill

    def render(self):
        """基礎渲染方法"""
        glPushMatrix()
        
        # 先進行平移和旋轉
        glTranslatef(*self.translation)
        if self.rotation[0] != 0:
            glRotatef(*self.rotation)
        
        # 如果可見就繪製
        if self.visible:
            self.draw()

        # 繪製所有子節點
        for child in self.children:
            child.render()
            
        glPopMatrix()
    
    def draw(self):
        """由子類實現具體的繪製方法"""
        pass

class Cube(Node):
    """立方體節點"""
    initial_vertices = [
            (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
            (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5)
        ]
    
    def __init__(self, name, scale=(1,1,1)):
        super().__init__(name)
        self.scale = scale
        self.fill = True
        self.visible = True
        self.vertices = self.set_vertices_by_scale()

    def set_vertices_by_scale(self):
        # 將 vertices, scale, offset 轉換為 NumPy 陣列
        vertices_array = np.array(self.initial_vertices)
        scale_array = np.array(self.scale)
        # 放大
        transformed_vertices = vertices_array * scale_array
        
        return transformed_vertices.tolist()
    
    def move(self, x, y, z):
        vertices_array = np.array(self.vertices)
        offset_array = np.array([x, y, z])
        # move
        transformed_vertices = vertices_array + offset_array
        
        self.vertices = transformed_vertices.tolist()

    def draw(self):
        faces = [
            (0,1,2,3), (4,5,6,7), (0,4,7,3),
            (1,5,6,2), (0,1,5,4), (3,2,6,7)
        ]
        
        if self.fill:
            glColor3f(*self.color)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            for face in faces:
                glBegin(GL_QUADS)
                for vertex in face:
                    glVertex3fv(self.vertices[vertex])
                glEnd()
        
        # 繪製黑色邊框
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glColor3f(*self.wireframe_color)
        for face in faces:
            glBegin(GL_LINE_LOOP)
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
            glEnd()

class Sphere(Node):
    """球體節點"""
    def __init__(self, name, radius=0.5, slices=16, stacks=16):
        super().__init__(name)
        self.radius = radius
        self.slices = slices
        self.stacks = stacks
        self.fill = True
        self.visible = True
    
    def draw(self):
        quadric = gluNewQuadric()
        if self.fill:
            glColor3f(*self.color)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            gluQuadricDrawStyle(quadric, GLU_FILL)
            gluSphere(quadric, self.radius, self.slices, self.stacks)
        else:
            glColor3f(*self.wireframe_color)
            gluQuadricDrawStyle(quadric, GLU_LINE)
            gluSphere(quadric, self.radius, self.slices, self.stacks)
        gluDeleteQuadric(quadric)

class Joint(Sphere):
    """關節節點，繼承自球體"""
    def __init__(self, name, angle_limit=(-360, 360), axis=(0, 0, 1), radius=0.5):
        super().__init__(name, radius=radius)
        self.min_angle, self.max_angle = angle_limit
        self.axis = axis
        self.set_angle(self.min_angle)
        self.visible = False
        self.fill = False
        self.state = "dinosaur"
        self.step = 0 # max step = 19
    
    def set_angle(self, angle):
        # 限制角度在範圍內
        self.angle = max(self.min_angle, min(self.max_angle, angle))
        # 設置自身的旋轉
        self.set_rotation(self.angle, *self.axis)
        
        # 將相同的旋轉應用到所有直接子節點
        for child in self.children:
            child.set_rotation(self.angle, *self.axis)
        
    def rotate(self):
        self.add_step()
    def set_axis(self, x, y, z):
        self.axis = [x, y, z]
    def set_angle_limit(self, angle_limit=(0, 360)):
        self.min_angle, self.max_angle = angle_limit

    def add_step(self):
        if self.state == "dinosaur":
            if self.step > 20:
                return
            self.set_angle(self.min_angle + (self.max_angle - self.min_angle) * self.step / 20)
            self.step += 1
        
        if self.state == "car":
            if self.step < 0:
                return
            self.set_angle(self.min_angle + (self.max_angle - self.min_angle) * self.step / 20)
            self.step -= 1

    def set_state(self, state):
        self.state = state


class Wheel(Node):
    """中空圓柱體輪子節點"""
    def __init__(self, name, inner_radius=0.3, outer_radius=0.5, height=0.2, segments=32):
        super().__init__(name)
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.height = height
        self.segments = segments
    
    def draw(self):
        h = self.height / 2
        
        if self.fill:
            glColor3f(*self.color)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            # 繪製頂面和底面
            for y in [h, -h]:
                glBegin(GL_QUAD_STRIP)
                for i in range(self.segments + 1):
                    angle = 2 * math.pi * i / self.segments
                    x_outer = self.outer_radius * math.cos(angle)
                    z_outer = self.outer_radius * math.sin(angle)
                    x_inner = self.inner_radius * math.cos(angle)
                    z_inner = self.inner_radius * math.sin(angle)
                    glVertex3f(x_outer, y, z_outer)
                    glVertex3f(x_inner, y, z_inner)
                glEnd()
            
            # 繪製外側面和內側面
            for radius in [self.outer_radius, self.inner_radius]:
                glBegin(GL_QUAD_STRIP)
                for i in range(self.segments + 1):
                    angle = 2 * math.pi * i / self.segments
                    x = radius * math.cos(angle)
                    z = radius * math.sin(angle)
                    glVertex3f(x, h, z)
                    glVertex3f(x, -h, z)
                glEnd()
        
        # 繪製黑色線框
        glColor3f(*self.wireframe_color)
        self._draw_wireframe(h)
    
    def _draw_wireframe(self, h):
        """繪製線框"""
        # 繪製頂部和底部的圓
        for y in [h, -h]:
            for radius in [self.outer_radius, self.inner_radius]:
                glBegin(GL_LINE_LOOP)
                for i in range(self.segments):
                    angle = 2 * math.pi * i / self.segments
                    x = radius * math.cos(angle)
                    z = radius * math.sin(angle)
                    glVertex3f(x, y, z)
                glEnd()
        
        # 繪製連接線
        for radius in [self.outer_radius, self.inner_radius]:
            glBegin(GL_LINES)
            for i in range(self.segments):
                angle = 2 * math.pi * i / self.segments
                x = radius * math.cos(angle)
                z = radius * math.sin(angle)
                glVertex3f(x, h, z)
                glVertex3f(x, -h, z)
            glEnd()

class Cylinder(Node):
    """實心圓柱體節點"""
    def __init__(self, name, radius=0.5, height=1.0, segments=32):
        super().__init__(name)
        self.radius = radius
        self.height = height
        self.segments = segments
        self.fill = True
        self.visible = True
    
    def draw(self):
        h = self.height / 2
        
        if self.fill:
            glColor3f(*self.color)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            # 繪製頂面和底面
            for y in [h, -h]:
                glBegin(GL_TRIANGLE_FAN)
                glVertex3f(0, y, 0)  # 圓心
                for i in range(self.segments + 1):
                    angle = 2 * math.pi * i / self.segments
                    x = self.radius * math.cos(angle)
                    z = self.radius * math.sin(angle)
                    glVertex3f(x, y, z)
                glEnd()
            
            # 繪製側面
            glBegin(GL_QUAD_STRIP)
            for i in range(self.segments + 1):
                angle = 2 * math.pi * i / self.segments
                x = self.radius * math.cos(angle)
                z = self.radius * math.sin(angle)
                glVertex3f(x, h, z)
                glVertex3f(x, -h, z)
            glEnd()
        
        # 繪製黑色線框
        glColor3f(*self.wireframe_color)
        self._draw_wireframe(h)
    
    def _draw_wireframe(self, h):
        """繪製線框"""
        # 繪製頂部和底部的圓
        for y in [h, -h]:
            glBegin(GL_LINE_LOOP)
            for i in range(self.segments):
                angle = 2 * math.pi * i / self.segments
                x = self.radius * math.cos(angle)
                z = self.radius * math.sin(angle)
                glVertex3f(x, y, z)
            glEnd()
        
        # 繪製連接線
        glBegin(GL_LINES)
        for i in range(self.segments):
            angle = 2 * math.pi * i / self.segments
            x = self.radius * math.cos(angle)
            z = self.radius * math.sin(angle)
            glVertex3f(x, h, z)
            glVertex3f(x, -h, z)
        glEnd()

