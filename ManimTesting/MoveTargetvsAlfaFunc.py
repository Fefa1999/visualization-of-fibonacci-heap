from manim import *

#Running manim is done by the follow:
    #manim -qm -p filename.py classnameInFile
    #This will render an output file..
    # -qm is quality medium
    # -p is a preview

class MoveToTargetExample(MovingCameraScene):
    def construct(self):
        dotRadius = 0.2
        startPoint = [dotRadius*2*150*2, 0.0, 0.0]
        dots = VGroup()
        for _ in range(300):
            dot = Dot(startPoint, radius=dotRadius, color=BLUE)
            startPoint[0] -= dotRadius*4
            dot.generate_target()
            dot.target.set_y(100)
            self.add(dot)
            dots.add(dot)
        self.camera.frame.set(width=dotRadius*2*300*2+5).move_to([0.0, 50.0, 0.0])
        self.play(AnimationGroup(*[MoveToTarget(d) for d in dots], lag_ratio=0))

class AlfaFuncExample(MovingCameraScene):
    def construct(self):
        dotRadius = 0.2
        startPoint = [dotRadius*2*150*2, 0.0, 0.0]
        dots = VGroup()
        for _ in range(300):
            dot = Dot(startPoint, radius=dotRadius, color=BLUE)
            startPoint[0] -= dotRadius*4
            dot.targetP = dot.get_center()
            dot.targetP[1] = 100.0
            self.add(dot)
            dots.add(dot)
        self.camera.frame.set(width=dotRadius*2*300*2+5).move_to([0.0, 50.0, 0.0])

        def amoveto(mobj, alpha):
            mobj.shift((mobj.targetP-mobj.get_center())*alpha)

        self.play(AnimationGroup(*[UpdateFromAlphaFunc(d, amoveto) for d in dots], lag_ratio=0))

          
        