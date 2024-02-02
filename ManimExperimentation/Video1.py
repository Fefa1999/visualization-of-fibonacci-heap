from manim import *
#From the Benjamin Hackl youtube chanel on his series on manim
#https://www.youtube.com/watch?v=rUsUrbWb2D4&list=PLsMrDyoG1sZm6-jIUQCgN3BVyEVOZz3LQ&index=1&ab_channel=BenjaminHackl

#We learn to create mobjects, set relations and add to scene.
class firstExample(Scene): #We inherit from Scene in the manim libary
    def construct(self):
        #mobject = manim objects
        #You create/instanciate them, this does not mean it added to the scene.
        blue_circle = Circle(color=BLUE, fill_opacity=0.5)
        green_square = Square(color=GREEN, fill_opacity=0.8)

        #Still not added to scene, but we set the relation between them
        #When addion mobjects to scene the center of the object will be the center of the scene.
        #If nothing else is declared.
        green_square.next_to(blue_circle,RIGHT)

        #Here we add them to the scene. 
        #Here the blue circle will have its center in the center of the scene and the green will be to its right.
        self.add(blue_circle, green_square)

        #Running manim is done by the follow:
        #manim -qm -p filename.py classnameInFile
        #This will render an output file..
        # -qm is quality medium
        # -p is a preview

#We learn about the Axes mobject and its methods plot and get_area.
#We learn about animation and how to edit the play.
class secondExample(Scene):
    def construct(self):
        ax = Axes(x_range=(-3,3), y_range=(-3,3))
        #When plotting a function we could write a function and instantiate it outside.
        #Or write an inline function with lamba
        curve = ax.plot(lambda x: (x+2)*x*(x-2)/2, color=RED)

        #The axes also have an area method, lets instantiate it and add it.
        area = ax.get_area(curve, x_range=(-2,0))

        #self.add(ax, curve, area)

        #We can edit the scene in multiple ways. 
        #self.add adds the mobject from the beginning in a still frame
        #self.wait add a pause. This will make the render into a video of a still frame
        #self.play this plays and animation on the scene 
        ##Animation can, 
            #add mobjects with (Create, FadeIn,..)
            #change mobjects with (Transform,.. )
            #emphasize mobjects with (Indicate Circumscribe,..)
            #remove mobjects with (Uncreate, Fadeout,..)
        """self.play(Create(ax))
        self.play(Create(curve))
        self.wait(1)
        self.play(Uncreate(ax), Uncreate(curve))"""
        

        #We can also make it create 2 things at the same time by passing multiple arguemtns to play
        #We can also change the change animation to make is slower or faster.
        self.play(Create(ax),Create(curve), run_time=3)
        #you could also give them different runtimes self.play(Create(ax) run_time=3,Create(curve), run_time=5)
        self.play(FadeIn(area))
        self.wait(2)


class thirdExample(Scene): 
    def construct(self):
        green_square = Square(color=GREEN, fill_opacity=0.7)
        self.play(DrawBorderThenFill(green_square))

        blue_cirlce = Circle(color=BLUE, fill_opacity= 0.7)
        self.play(Transform(green_square, blue_cirlce))
        self.play(Wait(2))

        self.play(Indicate(green_square))

        #This will not work. Since transform makes the first argument the secound arguement
        #So green_square now contains the blue circle.
        #self.play(FadeOut(blue_cirlce))
        #To make this work you could use a ReplacementTransform(green_square, blue_cirlce)
        #Therfor to remove it we need to remove the gree_square.
        self.play(FadeOut(green_square))