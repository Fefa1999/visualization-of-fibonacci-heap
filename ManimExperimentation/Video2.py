from manim import *

"""Manim operates with a 3D coordinate system. (Internal: points are NumPy arrays)
It dedaults to 2D setting, the scene frame is
    8 munits (manim units) in height.
    14 + 2/9 = 14.22 munits in width.
The origin is in the middle of the screen at 0,0,0
The pixel measurements of ouput depend on quality settings"""

class firstExample2(Scene): #we will learn positioning.
    def construct(self):
        plane = NumberPlane()#so we can easely see how objects move.
        self.add(plane)

        red_dot = Dot(color=RED)
        green_dot = Dot(color=GREEN)
        green_dot.next_to(red_dot, RIGHT + UP) 
        self.add(red_dot, green_dot)

        #shifting
        orange_square = Square(color=ORANGE)
        orange_square.shift(2*UP + 4*RIGHT) #moves it 4 munit to the right and 2 munit above of red_dot (aka the center)
        self.add(orange_square)

        #Moving
        purple_circle = Circle(color=PURPLE)
        purple_circle.move_to([-3, -2, 0])
        self.add(purple_circle)


        #align_to
        red_circle = Circle(radius=0.5, color=RED, fill_opacity=0.5)
        yellow_cirlce = red_circle.copy().set_color(YELLOW)
        orange_circle = red_circle.copy().set_color(ORANGE)
        red_circle.align_to(orange_square, UP) #aligns the upper edge of the cirle with the upper edge of the square
        #not it is not in the x akses only the y. (Up & Down affects y-akses, Left & Right affects x-akses)
        
        yellow_cirlce.align_to(orange_square, RIGHT)
        orange_circle.align_to(orange_square, UP+RIGHT)
        self.add(red_circle, yellow_cirlce, orange_circle)
        



class secondExample2(Scene):
    def construct(self):
        c = Circle(color=GREEN, fill_opacity=0.5)
        self.add(c)

        for d in [(0,0,0), UP, UR, RIGHT, DR, DOWN, DL, LEFT, UL]: #This edge points and center of the objects.
            #These can be used by fx the move to as anker points.
            self.add(Cross(scale_factor=0.2).move_to(c.get_critical_point(d)))
        
        s1 = Square(color=RED, fill_opacity=0.5)
        s2 = s1.copy().set_color(BLUE)
        s1.move_to([1,0,0], aligned_edge=LEFT) #it Aligns s1 left edge to the point 1,0,0
        s2.move_to([0,1,0], aligned_edge=RIGHT) #It aligns s2 right egde to the point 0,1,0
        self.add(s1, s2)

#Manim have 2 usefull units percent and pixels. But you need to import them
from manim.utils.unit import Percent, Pixels
class thirdExample2(Scene):
    def construct(self):
        for perc in range(5, 51, 5):
            self.add(Circle(radius=perc * Percent(X_AXIS)))
            self.add(Square(side_length=2*perc * Percent(Y_AXIS), color=YELLOW))

        d = Dot()
        d.shift(100*Pixels*RIGHT)
        ##The location of this dot depends on the quality rendered. In medium it is in the 2'nd cirle
        #While in high it is on the edge of the inner cirle. 
        #This is because of the pixels in the image
        self.add(d)
    
#Manim have support for bigger group of objects that need to be alliged. 
class fourthExample2(Scene):
    def construct(self):
        red_dot = Dot(color=RED)
        green_dot = Dot(color=GREEN).next_to(red_dot, RIGHT)
        blue_dot = Dot(color=BLUE).next_to(red_dot, UP)

        #vmobject groups are groups of vobjects. There exists 2 types of mobjects in manim
        #almost all commonly used opjects are vmobjects (Vectorized objects)
        #Fx if you import an image into manim, that image is not a vmobject 

        dot_group = VGroup(red_dot,green_dot,blue_dot)
        dot_group.to_edge(RIGHT)
        self.add(dot_group)

        #circles = VGroup([Circle(radius=0.2) for _ in range(10)])
        #This will not work the VGroup cant take a list or iterator as its first argument

        #the * in python unpacks the list
        circles = VGroup(*[Circle(radius=0.2) for _ in range(10)])

        circles.arrange(UP, buff=0.5) #buff is the space between them. Not needed

        self.add(circles)

        stars = VGroup(*[Star(color=YELLOW, fill_opacity=1).scale(0.5) for _ in range(20)])
        stars.arrange_in_grid(4, 5, buff=0.2) #4 rows 5 collums
        self.add(stars)

#Manim configuration system
# The idea behind config is there exists a "Single Source of truth for 'global' settings"
# See docs and tutorial for manim cofig.
# Can be set in the .py file but for clealyness should be added in a manim.cfg file
# Can be generated with: manim cfg write -l cwd
# Manim will check for the config file 3 places. In the directory it is run from (next to the scene file)
# User level config file -set by the operation system.
# Global config file - dont touch this.

#Some of the most used config and how to set them in the py file

"""
config.background_color = WHITE
config.frame_width = 32
config.frame_height = 18

config.pixel_height = 500
config.pixel_width = 890
"""
class fithExample2(Scene):
    def construct(self):
        plane = NumberPlane(x_range=(-8,8),y_range=(-4.5,4.5)) #ranges needed to scale to new frame size
        t = Triangle(color=PURPLE, fill_opacity=0.5)
        self.add(plane,t)

        Text.set_default(color=BLUE, font_size=100)
        t = Text("Hello World!")
        t.shift(UP*3)

        Text.set_default()
        t2 = Text("Good bye")
        t2.next_to(t,DOWN)
        self.add(t,t2)

