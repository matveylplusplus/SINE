# TODO: make Chord a vDict, but how to bundle animations with said vDict?
# should the chordcircle be asking for the scene, or should the scene be asking
# for the chordcircle?

from manim import *
from numpy import ndarray, array


class ChordCircle(VMobject):
    def __init__(
        self,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_dot_color: str = WHITE,
        dot_radii: float = 0.1,
        trav_dot_opacity: float = 0.0,
        trav_dot_color: str = None,
        circle_radius: float = 3.0,
        circle_color: str = RED,
        mov_color: str = BLUE,  # mov_line color
        stat_color: str = PURPLE,  # stat_line color
        chord_color: str = ORANGE,  # chord_line color
        angle_radius: float = 0.5,
        angle_color: str = YELLOW,
        init_degrees: float = 0.0,
    ):
        # redraw functions, called every frame

        def get_center_dot():
            return Dot(
                point=np.array(
                    [self.center_x.get_value(), self.center_y.get_value(), 0.0]
                ),
                radius=dot_radii,
                color=center_dot_color,
            )

        def get_circle():
            return Circle(
                radius=circle_radius,
                color=circle_color,
                arc_center=self.center_dot.get_center(),
            )

        def get_stat_line():
            return Line(
                start=self.center_dot.get_center(),
                end=self.circle.point_from_proportion(0),
                color=stat_color,
            )

        def get_trav_dot():
            wiggle = 0
            circ_prop = (self.theta.get_value() / 360) % 1
            if circ_prop == 1 or circ_prop == 0:
                """
                There has to be a tiny wiggle/offset to trav_dot's position
                whenever it gets to the start of the circle to prevent mov_line
                and stat_line from ever being parallel so that the construction
                of the Angle object in get_angle() doesn't crap itself.
                """
                wiggle = UP * 1  # lil wiggle
            return Dot(
                point=self.circle.point_from_proportion(circ_prop) + wiggle,
                radius=dot_radii,
                color=trav_dot_color,
                fill_opacity=trav_dot_opacity,
            )

        def get_mov_line():
            return Line(
                start=self.center_dot.get_center(),
                end=self.trav_dot.get_center(),
                color=mov_color,
            )

        def get_chord_line():
            return Line(
                start=self.trav_dot.get_center(),
                end=self.stat_line.get_end(),
                color=chord_color,
            )

        def get_angle():
            return Angle(
                line1=self.stat_line,
                line2=self.mov_line,
                radius=angle_radius,
                color=angle_color,
            )

        # ValueTrackerz
        self.center_x = ValueTracker(center_x)
        self.center_y = ValueTracker(center_y)
        self.theta = ValueTracker(init_degrees)

        # dynamic mobjects (do move)
        self.center_dot = always_redraw(get_center_dot)
        self.circle = always_redraw(get_circle)
        self.stat_line = always_redraw(get_stat_line)
        self.trav_dot = always_redraw(get_trav_dot)
        self.mov_line = always_redraw(get_mov_line)
        self.chord_line = always_redraw(get_chord_line)
        self.angol = always_redraw(get_angle)

        # call upper-level constructors before adding shit
        super().__init__()

        # add shit as submobjects
        self.add(self.stat_line)
        self.add(self.circle)
        self.add(self.trav_dot)
        self.add(self.angol)
        self.add(self.mov_line)
        self.add(self.chord_line)
        self.add(self.center_dot)

    def set_theta(self, theta):
        return self.theta.animate.set_value(theta)


"""
1) make cc.theta.animate.set_value(720) be a return value of a ChordCircle
   function, ensuring proper OOP
2) make the center of the ChordCircle be a ValueTracker that all submobjects
   orient themelves around; when you want to move the ChordCircle, you just put
   in self.play a call to a ChordCircle function that returns something like
   self.center_point.animate.set_value(point_to_move_to)
"""


class DemonstrateChord(Scene):
    def construct(self):
        cc = ChordCircle(center_x=0, trav_dot_opacity=1.0, trav_dot_color=GREEN)
        self.add(cc)

        self.play(cc.set_theta(720), run_time=6)
        self.wait()
        self.play(cc.center_y.animate.set_value(1), run_time=1)
        # self.play(FadeOut(cc.chord_line))
        self.play(cc.set_theta(810), run_time=1)
