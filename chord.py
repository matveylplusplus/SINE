# TODO: make Chord a vDict, but how to bundle animations with said vDict?
# should the chordcircle be asking for the scene, or should the scene be asking
# for the chordcircle?

from manim import *
from numpy import array


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
                point=array(
                    [self.center_x.get_value(), self.center_y.get_value(), 0.0]
                ),
                radius=dot_radii,
                color=center_dot_color,
            )

        def get_circle():
            return Circle(
                radius=circle_radius,
                color=circle_color,
                arc_center=array(
                    [self.center_x.get_value(), self.center_y.get_value(), 0.0]
                ),
            )

        def get_stat_line():
            return Line(
                start=array(
                    [self.center_x.get_value(), self.center_y.get_value(), 0.0]
                ),
                end=array(
                    [
                        self.center_x.get_value() + circle_radius,
                        self.center_y.get_value(),
                        0.0,
                    ]
                ),
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
                wiggle = UP * 0.001  # lil wiggle
            return Dot(
                point=self.circle.point_from_proportion(circ_prop) + wiggle,
                radius=dot_radii,
                color=trav_dot_color,
                fill_opacity=trav_dot_opacity,
            )

        def get_mov_line():
            return Line(
                start=array(
                    [
                        self.center_x.get_value(),
                        self.center_y.get_value(),
                        0.0,
                    ]
                ),
                end=self.trav_dot.get_center(),
            ).set_color(
                ("#0A68EF", "#4AF1F2", "#0A68EF")  # gradient!!
            )

        def get_chord_line():
            return Line(
                start=self.mov_line.get_end(),
                end=self.stat_line.get_end(),
                color=chord_color,
            )
            """
                start=self.trav_dot.get_center(),
                end=array(
                    [
                        self.center_x.get_value() + circle_radius,
                        self.center_y.get_value(),
                        0.0,
                    ]
                ),
                color=chord_color,
                """

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

    def set_center_x(self, center_x):
        return self.center_x.animate.set_value(center_x)

    def set_center_y(self, center_y):
        return self.center_y.animate.set_value(center_y)


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
        cc = ChordCircle(
            center_x=-3, trav_dot_opacity=1.0, trav_dot_color=GREEN
        )
        self.add(cc)

        self.play(
            cc.set_theta(360),
            cc.set_center_x(3),
            cc.set_center_y(1),
            run_time=10,
        )

        """
        frozen_frame=False prevents the scene from freezing on a near-full angle
        circle and makes sure it's adequately reset to 0 at the end of the
        360-degree turn
        """
        self.wait(frozen_frame=False)
