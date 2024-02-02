from manim import *


#Every animation i tied to a mobject.
#We have worked with run_time of animation. with fx self.play(Create(ax) run_time=3,Create(curve), run_time=5)

from manim import ManimColor

class firstExample3(Scene):
    def construct(self):
        polys = VGroup(
            *[RegularPolygon(5, radius=1, fill_opacity=0.5,
            color=ManimColor(((j*200+100)%110,(j*200)%70,(j*200)%120))) for j in range(5)]
            ).arrange(RIGHT)
        
        self.play(DrawBorderThenFill(polys), runtime=2)

        self.play(
            Rotate(polys[0], PI, rate_func=lambda t: t), #rate=func=linear would do the same
            Rotate(polys[1], PI, rate_func=smooth),
            Rotate(polys[2], PI, rate_func=lambda t: np.sin(t*PI)),
            Rotate(polys[3], PI, rate_func=there_and_back),
            Rotate(polys[4], PI, rate_func=lambda t: 1 - abs(1-2*t)),
            run_time=2
            )   
        self.wait(2)


#Parsing mulitple animation in one play like self.play(animation1, animation2,..)
#Will mke them play at the same time. 
#Passing a animation keyword like run_time in self.play(animation1, animation2, run_time=3)
#Will be applied to all animations.  (Before it until it encounters another keyword ***I think)

#Manim does not raise an error if you parse conflicting animations like move the same object left and right at the same time.
#But it will very likely only play the last animation parsed.

class secondExample3(Scene):
    def construct(self):
        s = Square()
        self.add(s)
        self.play(Rotate(s, PI), Rotate(s, -PI), run_time=2)
#It only rotates clockwise aka -PI

#You can group our animation as you do with your mobjects in vgroups. 
#You can group animation in AnimationGroup.
#It takes a lag_ratio. On a lag_ratio of 0 they will play at the same time. On a lag_ratio of 1 they will go after each other.
#Between 0 and 1 the animation will overlap.
#Finer control posible by editing list in anims_with_timings attribute.
        
class thirdExample3(Scene):
    def construct(self):
        squares = VGroup(*[Square(fill_opacity=0.5, color=ManimColor(
        ((j*200+100)%110,(j*200)%70,(j*200)%120))) for j in range(20)]).arrange_in_grid(4, 5).scale(0.75)
        self.play(AnimationGroup(*[FadeIn(s) for s in squares], lag_ratio=0.15))
        self.wait(2)




#It is a bit tricky to make the mobject do animation from  functions. 
#Usually a method on called object mobj.method() returns the mobject which cant se passed to play.
#Manim has a workaround with the .animate propperty which can build animatitons. 

class fourthExample3(Scene):
    def construct(self):
        s = Square()
        self.play(s.animate.shift(RIGHT*2)) # The shift animation to the right with .animate
        self.play(s.animate(run_time=2).scale(3)) #Supports animation keywords
        self.play(s.animate.scale(1/3).shift(4*LEFT)) #Supports chaining 

#.animate does not know how your mobjects changes.
#It only knows the start and end and interpolates linearly between them.
class fithedExample3(Scene):
    def construct(self):
        s = Square(color=GREEN, fill_opacity=0.5)
        c = Circle(color=RED, fill_opacity=0.5)
        self.add(s, c)

        self.play(s.animate.shift(UP), c.animate.shift(DOWN))
        self.play(VGroup(s, c).animate.arrange(RIGHT, buff=1))
        self.play(c.animate(rate_func=linear).shift(RIGHT).scale(2))
        #All this will work

class sixedExample3(Scene):
    def construct(self):
        l_square = Square()
        r_square = Square()
        VGroup(l_square, r_square).arrange()
        self.add(l_square, r_square)
        self.play(l_square.animate.rotate(PI), Rotate(r_square, PI), run_time=(2))
        self.wait()
        #This doesn't work as intended for the left one. It looks like the square shrinks and grows. 
        #What happens is that rotate make the top rigth corner move to the down left corners position and like wise for its counter-part.
        #.animate makes it move the shortest path which is straigth across the middle.

#There are animation that does the same .animate. By creating a new mobject at the target and linear animate between them.
#Like MoveToTarget. That mob.generate_target() then modifies mob.target - animate with MoveToTarget(mob)

#Restore: that save the sate of you mobject as a new mobject. Then you can edit transform an so on on the old mobj and later return to the generated one.
#Is done by calling mob.save_state(), and later Restore(mob) to return. (it is the opisite of MoveToTarget())
class seventhExample3(Scene):
    def construct(self):
        c = Circle()

        c.generate_target()
        c.target.set_fill(color=GREEN, opacity=0.4)
        c.target.shift(2*RIGHT+UP).scale(0.5)

        self.add(c)
        self.wait()
        self.play(MoveToTarget(c))
        #We se the cirle move linear to the target mobj/state

        s = Square()

        s.save_state()
        self.play(FadeIn(s))
        self.play(s.animate.set_color(PURPLE).set_opacity(0.5).shift(4*LEFT).scale(3))
        self.play(s.animate.shift(DOWN*2).rotate(PI/4))
        self.wait()
        self.play(Restore(s), run_time=2)
        self.wait()

#You can make your own custom animations
#Image an animation as being a function mapping of a (mobject, completion ratio) to a mobject

def move_somewhere(mobj, alpha):
    mobj.move_to(alpha * RIGHT + alpha**2 * 2*UP)        
#At alpha 0 the animation will not have started and at alpha 1 the animation will have moved 1 unit right and 2 units up.

#With such a function we can give it to UpdateFromAlphaFunc and i constructs the animation
class eigthExample3(Scene):
    def construct(self):
        def spiral_out(mobject, t):
            radius = 4*t
            angle = 2*t * 2*PI
            mobject.move_to(radius*(np.cos(angle)*RIGHT + np.sin(angle)*UP))
            mobject.set_color(color=ManimColor(((255-t*200), 255, 0)))
            mobject.set_opacity(1-t)
        
        d = Dot(color=WHITE)
        self.add(d)
        self.play(UpdateFromAlphaFunc(d, spiral_out, run_time=5))
