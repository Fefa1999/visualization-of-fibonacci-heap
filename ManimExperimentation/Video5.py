from manim import *
from manim.opengl import *

class OpenGLIntro(Scene):
    def construct(self):
        hello_world = Tex("Hello World!").scale(3)
        self.play(Write(hello_world))
        self.play(
            self.camera.animate.set_euler_angles(
                theta=-10*DEGREES,
                phi=50*DEGREES
            )
        )
        self.play(FadeOut(hello_world))
        surface = OpenGLSurface(
            lambda u, v: (u, v, u*np.sin(v) + v*np.cos(u)),
            u_range=(-3, 3),
            v_range=(-3, 3)
        )
        surface_mesh = OpenGLSurfaceMesh(surface)
        self.play(Create(surface_mesh))
        self.play(FadeTransform(surface_mesh, surface))
        self.wait()
        light = self.camera.light_source
        self.play(light.animate.shift([0, 0, -20]))
        self.play(light.animate.shift([0, 0, 10]))
        self.play(self.camera.animate.set_euler_angles(theta=60*DEGREES))
        
        # self.interactive_embed()

        # self.play(self.camera.animate.set_euler_angles(theta=0*DEGREES))
        # self.play(FadeOut(surface, shift=np.array([0, 0, -2])))

        # red_sphere = Sphere(color=RED)
        # self.play(Create(red_sphere))
        # self.play(red_sphere.animate.scale(3))

        # sphere_mesh = OpenGLSurfaceMesh(red_sphere)
        # play(Transform(red_sphere, sphere_mesh))  # graphics glitch :-)

        # self.play(self.camera.animate.set_euler_angles(phi=0, theta=0))

class InteractiveRadius(Scene):
    def construct(self):
        plane = NumberPlane()
        cursor_dot = Dot().move_to(3*RIGHT + 2*UP)
        red_circle = Circle(
            radius=np.linalg.norm(cursor_dot.get_center()),
            color=RED
        )
        red_circle.add_updater(
            lambda mob: mob.become(
                Circle(
                    radius=np.linalg.norm(cursor_dot.get_center()),
                    color=RED
                )
            )
        )
        self.play(Create(plane), Create(red_circle), FadeIn(cursor_dot))
        self.cursor_dot = cursor_dot
        self.interactive_embed()  # not supported in online environment

    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key as pyglet_key
        if symbol == pyglet_key.G:
            self.play(
                self.cursor_dot.animate.move_to(self.mouse_point.get_center())
            )
        super().on_key_press(symbol, modifiers)

class NewtonIteration(Scene):
    def construct(self):
        self.axes = Axes()
        self.f = lambda x: (x+6) * (x+3) * x * (x-3) * (x-6) / 300
        curve = self.axes.plot(self.f, color=RED)
        self.cursor_dot = Dot(color=YELLOW)
        self.play(Create(self.axes), Create(curve), FadeIn(self.cursor_dot))
        self.interactive_embed()  # not supported in online environment

    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key as pyglet_key
        from scipy.misc import derivative
        if symbol == pyglet_key.P:
            x, y = self.axes.point_to_coords(self.mouse_point.get_center())
            self.play(
                self.cursor_dot.animate.move_to(self.axes.c2p(x, self.f(x)))
            )

        if symbol == pyglet_key.I:
            x, y = self.axes.point_to_coords(self.cursor_dot.get_center())
            # Newton iteration: x_new = x - f(x) / f'(x)
            x_new = x - self.f(x) / derivative(self.f, x, dx=0.01)
            curve_point = self.cursor_dot.get_center()
            axes_point = self.axes.c2p(x_new, 0)
            tangent = Line(
                curve_point + (curve_point - axes_point)*0.25,
                axes_point + (axes_point - curve_point)*0.25,
                color=YELLOW,
                stroke_width=2,
            )
            self.play(Create(tangent))
            self.play(self.cursor_dot.animate.move_to(self.axes.c2p(x_new, 0)))
            self.play(
                self.cursor_dot.animate.move_to(self.axes.c2p(x_new, self.f(x_new))),
                FadeOut(tangent)
            )
        
        super().on_key_press(symbol, modifiers)