"""
TODO: 1) Graph chord length with respect to theta 2) Consolidate redraw
functions into one big one that returns a tuple/list? This would be much more
efficient
"""

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
                arc_center=get_center_dot().get_center(),
            )

        def get_stat_line():
            start = get_center_dot().get_center()
            return Line(
                start=start,
                end=start + array([circle_radius, 0, 0]),
                color=stat_color,
            )

        def get_trav_dot():
            """
            This code could easily be put into get_mov_line() if we decide we
            don't really need a dot to travel around the circle n shit
            """
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
                point=get_circle().point_from_proportion(circ_prop) + wiggle,
                radius=dot_radii,
                color=trav_dot_color,
                fill_opacity=trav_dot_opacity,
            )

        def get_mov_line():
            return Line(
                start=get_center_dot().get_center(),
                end=get_trav_dot().get_center(),
            ).set_color(
                ("#0A68EF", "#4AF1F2", "#0A68EF")  # gradient!!
            )

        def get_chord_line():
            return Line(
                start=get_trav_dot().get_center(),
                end=get_center_dot().get_center()
                + array([circle_radius, 0, 0]),
                color=chord_color,
            )

        def get_angle():
            return Angle(
                line1=get_stat_line(),
                line2=get_mov_line(),
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

    # Animation Functions!
    def set_theta(self, theta):
        return self.theta.animate.set_value(theta)

    def set_center_x(self, center_x):
        return self.center_x.animate.set_value(center_x)

    def set_center_y(self, center_y):
        return self.center_y.animate.set_value(center_y)
