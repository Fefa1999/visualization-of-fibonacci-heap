from manim import *

#Running manim is done by the follow:
    #manim -qm -p filename.py classnameInFile
    #This will render an output file..
    # -qm is quality medium
    # -p is a preview

class zNone(MovingCameraScene):
    def construct(self):
        dotRadius = 300
        wasBlue = False
        dots = VGroup()
        for _ in range(300):
            dotColor = BLUE
            if wasBlue:
                dotColor = RED
                wasBlue = False
            else: 
                wasBlue = True

            dot = Dot([300.0, 0.0, 0.0], radius=dotRadius, color=dotColor)
            dotRadius -= 1
            dot.generate_target()
            dot.target.set_x(-300)
            self.add(dot)
            dots.add(dot)
        self.camera.frame.set(width=300*4+5)
        self.play(AnimationGroup(*[MoveToTarget(d) for d in dots], lag_ratio=0))
        
class zAxes(MovingCameraScene):
    def construct(self):
        dotRadius = 300
        wasBlue = False
        dots = VGroup()
        for _ in range(300):
            dotColor = BLUE
            if wasBlue:
                dotColor = RED
                wasBlue = False
            else: 
                wasBlue = True

            dot = Dot([300.0, 0.0, 300-dotRadius], radius=dotRadius, color=dotColor)
            dotRadius -= 1
            dot.generate_target()
            dot.target.set_x(-300)
            self.add(dot)
            dots.add(dot)
        self.camera.frame.set(width=300*4+5)
        self.play(AnimationGroup(*[MoveToTarget(d) for d in dots], lag_ratio=0))

class zIndex(MovingCameraScene):
    def construct(self):
        dotRadius = 300
        wasBlue = False
        dots = VGroup()
        for _ in range(300):
            dotColor = BLUE
            if wasBlue:
                dotColor = RED
                wasBlue = False
            else: 
                wasBlue = True

            dot = Dot([300.0, 0.0, 0.0], radius=dotRadius, color=dotColor).set_z_index(300-dotRadius)
            dotRadius -= 1
            dot.generate_target()
            dot.target.set_x(-300)
            self.add(dot)
            dots.add(dot)
        self.camera.frame.set(width=300*4+5)
        self.play(AnimationGroup(*[MoveToTarget(d) for d in dots], lag_ratio=0))




