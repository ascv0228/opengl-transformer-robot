from components import Joint, Cube, Sphere, Cylinder, Wheel, Node
from RobotView import RobotView

class Robot:
    def __init__(self):
        # 初始化視圖
        self.view = RobotView()

        self.state = 0
        self.robot_states = ["dinosaur", "car"]
        self.robot_state = self.robot_states[self.state]
        self.step = 0

        self.fill = True
        
        # 創建機器人結構
        self.create_robot_structure()
        
    def create_robot_structure(self):
        # 創建機器人節點樹
        self.root_joint = Joint("root_joint", angle_limit=(0, 45))
        self.root_joint.set_axis(-1, 0, 0)

        self.body = Cube("body", scale=(2.5, 1.5, 5))
        self.neck_joint_0 = Joint("neck_joint_0", angle_limit=(0, 15))
        self.neck_joint_1 = Joint("neck_joint_1", angle_limit=(0, 15))
        self.head = Cube("head", scale=(3, 1.5, 2))
        self.mouth = Cube("mouth", scale=(3, 0.5, 2))

        self.body.set_color(1, 1, 1)
        self.head.set_color(173/255, 216/255, 230/255)
        self.mouth.set_color(173/255, 216/255, 230/255)

        self.root_joint.add_child(self.body)
        self.body.add_child(self.neck_joint_0)
        self.body.add_child(self.neck_joint_1)
        self.neck_joint_0.add_child(self.head)
        self.neck_joint_1.add_child(self.mouth)
        
        self.neck_joint_0.set_translation(0, 0+0.4, (self.body.scale[2]/2))
        self.neck_joint_1.set_translation(0, 0-0.6, (self.body.scale[2]/2))
        self.neck_joint_0.set_axis(1, 0, 0)
        self.neck_joint_1.set_axis(1, 0, 0)
        self.head.move(0, 0, (self.head.scale[2]/2))
        self.mouth.move(0, 0, (self.mouth.scale[2]/2))

        self.eye_left = Sphere("eye_left", radius=0.3)
        self.eye_right = Sphere("eye_right", radius=0.3)
        self.eye_left.set_color(1, 0, 0)
        self.eye_right.set_color(1, 0, 0)


        self.head.add_child(self.eye_left)
        self.head.add_child(self.eye_right)

        self.eye_left.set_translation((self.head.scale[0]/2), 0.4, 0.5)
        self.eye_right.set_translation(-(self.head.scale[0]/2), 0.4, 0.5)

        self.left_shoulder_joint = Joint("left_shoulder_joint", angle_limit=(0, 60))
        self.left_shoulder_joint.set_axis(-1, 0, 0)
        self.left_shoulder_joint.set_translation((self.body.scale[0]/2), 0, 2)
        self.body.add_child(self.left_shoulder_joint)

        self.left_hand = Cube("left_hand", scale=(0.3, 0.3, 2))
        self.left_hand.set_color(238/255, 221/255, 102/255)
        self.left_hand.move((self.left_hand.scale[0]/2), 0, -(self.left_hand.scale[2]/2))
        self.left_shoulder_joint.add_child(self.left_hand)

        self.right_shoulder_joint = Joint("right_shoulder_joint", angle_limit=(0, 60))
        self.right_shoulder_joint.set_axis(-1, 0, 0)
        self.right_shoulder_joint.set_translation(-(self.body.scale[0]/2), 0, 2)
        self.body.add_child(self.right_shoulder_joint)

        self.right_hand = Cube("right_hand", scale=(0.3, 0.3, 2))
        self.right_hand.set_color(238/255, 221/255, 102/255)
        self.right_hand.move(-(self.right_hand.scale[0]/2), 0, -(self.right_hand.scale[2]/2))
        self.right_shoulder_joint.add_child(self.right_hand)

        # # 創建一個藍色圓柱體
        self.pelvis_joint = Joint("pelvis_joint", angle_limit=(90, 90), axis=(0, 0, 1))
        self.pelvis_joint.set_translation(0, 0, -1.5)
        self.body.add_child(self.pelvis_joint)

        self.pelvis = Cylinder("pelvis", 
            radius=0.5,      # 半徑
            height=4.0,      # 高度
            segments=32)     # 圓周分段數
        self.pelvis.set_color(0, 0, 1)  # 設置為藍色
        self.pelvis_joint.add_child(self.pelvis)

        self.right_leg_joint = Joint("right_leg_joint", angle_limit=(0, 60), axis=(0, -1, 0))
        self.left_leg_joint = Joint("left_leg_joint", angle_limit=(0, 60), axis=(0, -1, 0))
        self.right_leg_joint.set_translation(0, self.pelvis.height/2, 0)
        self.left_leg_joint.set_translation(0, -self.pelvis.height/2, 0)
        self.pelvis.add_child(self.right_leg_joint)
        self.pelvis.add_child(self.left_leg_joint)


        self.right_leg = Cube("right_leg", scale=(2, 0.3, 4))
        self.right_leg.set_color(1, 0, 0)
        self.right_leg.move(0, 0, self.right_leg.scale[2]/2)
        self.right_leg_joint.add_child(self.right_leg)

        self.left_leg = Cube("left_leg", scale=(2, 0.3, 4))
        self.left_leg.set_color(1, 0, 0)
        self.left_leg.move(0, 0, self.left_leg.scale[2]/2)
        self.left_leg_joint.add_child(self.left_leg)

        self.front_right_wheel = Wheel("front_right_wheel", 
            inner_radius=0.5,  # 內徑
            outer_radius=1,  # 外徑
            height=0.2,        # 高度
            segments=32)       # 圓周分段數（越大越圓滑）
        self.front_right_wheel.set_color(0, 1, 0)
        self.front_right_wheel.set_translation(0, self.right_leg.scale[1]/2, +self.right_leg.scale[2])
        self.right_leg.add_child(self.front_right_wheel)

        self.front_left_wheel = Wheel("front_left_wheel", 
            inner_radius=0.5,  # 內徑
            outer_radius=1,  # 外徑
            height=0.2,        # 高度
            segments=32)       # 圓周分段數（越大越圓滑）
        self.front_left_wheel.set_color(0, 1, 0)
        self.front_left_wheel.set_translation(0, -self.left_leg.scale[1]/2, +self.left_leg.scale[2])
        self.left_leg.add_child(self.front_left_wheel)

        
        self.back_right_wheel = Wheel("back_right_wheel", 
            inner_radius=0.5,  # 內徑
            outer_radius=1,  # 外徑
            height=0.2,        # 高度
            segments=32)       # 圓周分段數（越大越圓滑）
        self.back_right_wheel.set_color(0, 1, 0)
        self.back_right_wheel.set_translation(0, self.right_leg.scale[1]/2, 0)
        self.right_leg.add_child(self.back_right_wheel)

        self.back_left_wheel = Wheel("back_left_wheel", 
            inner_radius=0.5,  # 內徑
            outer_radius=1,  # 外徑
            height=0.2,        # 高度
            segments=32)       # 圓周分段數（越大越圓滑）
        self.back_left_wheel.set_color(0, 1, 0)
        self.back_left_wheel.set_translation(0, -self.left_leg.scale[1]/2, 0)
        self.left_leg.add_child(self.back_left_wheel)

        self.tail_joint = Joint("tail_joint", angle_limit=(0, 100), axis=(-1, 0, 0))
        self.tail_joint.set_translation(0, self.body.scale[1]/2, -self.body.scale[2]/2)
        self.body.add_child(self.tail_joint)

        self.tail = Cube("tail", scale=(2.5, 0.3, 5))
        self.tail.set_color(173/255, 216/255, 230/255)
        self.tail.move(0, (self.tail.scale[1]/2), +(self.tail.scale[2]/2))
        self.tail_joint.add_child(self.tail)

        self.test_angle()


    def test_angle(self):
        pass
        # 測試 root_joint 的旋轉
        # self.root_joint.set_angle(45)
        # self.left_shoulder_joint.set_angle(60)
        # self.right_shoulder_joint.set_angle(60)


    def change_state(self):
        self.state = (self.state + 1) % len(self.robot_states)
        self.robot_state = self.robot_states[self.state]
        joints = [self.root_joint, self.left_shoulder_joint, self.right_shoulder_joint, self.left_leg_joint, self.right_leg_joint, self.tail_joint]
        for joint in joints:
            joint.set_state(self.robot_state)

    def change_fill(self):
        objects = [self.body, self.head, self.mouth, self.eye_left, self.eye_right, self.left_hand, self.right_hand, 
                   self.pelvis, self.left_leg, self.right_leg, self.front_left_wheel, self.front_right_wheel, self.back_left_wheel, self.back_right_wheel,
                   self.tail]
        
        self.fill = not self.fill
        Node.wireframe_color = (0, 0, 0) if self.fill else (173/255, 217/255, 0)

        for object in objects:
            object.set_fill( self.fill)


    def all_add_step(self):
        # print("self.step = ", self.step)
        if self.step > 20:
            self.step -= 1
            if self.robot_state == "dinosaur":
                # print("self.robot_state == dinosaur")
                self.change_state()
        
        elif self.step < 0:
            self.step += 1
            if self.robot_state == "car":
                # print("self.robot_state == car")
                self.change_state()

        if self.robot_state == "dinosaur":
            self.step += 1
        elif self.robot_state == "car":
            self.step -= 1
        
        joints = [self.root_joint, self.left_shoulder_joint, self.right_shoulder_joint, self.left_leg_joint, self.right_leg_joint, self.tail_joint]
        for joint in joints:
            joint.add_step()