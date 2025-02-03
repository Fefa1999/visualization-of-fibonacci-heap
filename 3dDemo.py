from manim import *
from manim.typing import Point3D
from manim.typing import Vector3
import time

# Alexander Findings:
# Z needs to be up in the scene.
# So start with a camera oriantation like:
# self.set_camera_orientation(frame_center=[0,0,0],phi=self.camera.get_phi()+70*DEGREES,theta=self.camera.get_theta()+90*DEGREES, zoom=6)
# Camera movements are:
# self.move_camera(phi=self.camera.get_phi()+0*DEGREES, #Rotate up(-) and down(+) (y axes)
#                          theta=self.camera.get_theta()+90*DEGREES, #Rotate right(+) or left(-) (Z axes)
#                          gamma=self.camera.get_gamma()+0*DEGREES, #Rotate around it self
#                          frame_center=[0,0,0], zoom=1,
#                          run_time=2)
# For simple camera movement zoom high zoom = very zoomed in. 
# Do not use the ambient_rotation it is super slow.

class FiboScene(ThreeDScene):
    def construct(self):
        st = time.time()
        axis_config = {
            "x_range": [-5,5,1],
            "y_range": [-5,5,1],
            "z_range": [-5,5,1],
            "x_length": 4.0,
            "y_length": 4.0,
            "z_length": 4.0,
        }
        xes = ThreeDAxes(**axis_config)
        self.add(xes)
        x_text3d = Tex("X").scale(0.5).move_to([2,0.5,0])
        x_text3d.rotate(PI/3, axis= RIGHT)
        Y_text3d = Tex("Y").scale(0.5).move_to([0.5,2,0])
        Z_text3d = Tex("Z").scale(0.5).move_to([0,0.5,2])
        self.add(x_text3d,Y_text3d,Z_text3d)

        for y in range(3):
            for x in range(y+1):
                for z in range(int((y+1)//2)+1):
                    n = Dot3D(point=[-x,y,z],radius=0.15, color=BLUE)
                    m = Dot3D(point=[x,y,z],radius=0.15, color=BLUE)
                    self.add(n,m)
                    n1 = Dot3D(point=[-x,y,-z],radius=0.15, color=BLUE)
                    m1 = Dot3D(point=[x,y,-z],radius=0.15, color=BLUE)
                    self.add(n1,m1)
                    

        self.set_camera_orientation(frame_center=[0,0,0],phi=self.camera.get_phi()+70*DEGREES,theta=self.camera.get_theta()+90*DEGREES, zoom=6)
        self.wait(2)
        self.move_camera(phi=self.camera.get_phi()+0*DEGREES, #Rotate up(-) and down(+) (y axes)
                         theta=self.camera.get_theta()+0*DEGREES, #Rotate right(+) or left(-) (Z axes)
                         gamma=self.camera.get_gamma()+0*DEGREES, #Rotate around it self
                         frame_center=[0,0,0], zoom=1,
                         run_time=2)
        self.move_camera(phi=self.camera.get_phi()+0*DEGREES, #Rotate up(-) and down(+) (y axes)
                         theta=self.camera.get_theta()+90*DEGREES, #Rotate right(+) or left(-) (Z axes)
                         gamma=self.camera.get_gamma()+0*DEGREES, #Rotate around it self
                         frame_center=[0,0,0], zoom=1,
                         run_time=2)
        self.wait(1)
        
        # test = Tex("test").scale(1).move_to([0.1,0.1,-5])
        # #self.add(test)
        print(time.time()-st)

    # Not done:
    # def buildFullFibTrees2d(self, degree: int):
    #     def aux(degree_: int, itteration: int, refY: int):
    #         if (degree_==1):
    #             cir = Dot3D(point=[0,refY,degree],radius=0.15,color=BLUE)
    #         else:
    #             mod = 0
    #             for x in range(degree_):
    #                 aux(degree_, itteration+1, refY)
    #     aux(degree_=degree, itteration=1, refY=0)