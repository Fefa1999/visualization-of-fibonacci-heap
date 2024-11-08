from manim import *
from manim.typing import Point3D
from manim.typing import Vector3
import time

class FiboScene(ThreeDScene):
    def construct(self):
        st = time.time()
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    n = Dot3D(point=[x,y,z],radius=0.15, color=BLUE)
                    self.add(n)
        self.wait(2)
        self.move_camera(frame_center=[1.5,2,1.5],zoom=1)
        self.wait(1)
        self.move_camera(frame_center=[1.5,2,1.5],distance = 1)
        self.wait(1)
        self.move_camera(phi=45*DEGREES,theta=45*DEGREES)
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait(1)
        # self.move_camera(frame_center=[1.5,2,1.5],zoom=10)
        # self.wait(1)
        # self.move_camera(frame_center=[1.5,2,-15],zoom=2)
        # self.wait(1)
        # self.move_camera(frame_center=[1.5,1.5,1.5],zoom=2)
        # self.move_camera(phi=0)
        # self.wait(1)

        print(time.time()-st)
                