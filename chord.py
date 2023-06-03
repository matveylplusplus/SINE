"""
TODO: 1) Graph chord length with respect to theta on some lil axes 3) Add theta
symbol that follows angle around 4) Add a valuetracker for the circle radius to
enable re-scaling 5) Let users set a gradient for components and background
"""

from manim import *
from numpy import array


class ChordCircle(VMobject):
    def __init__(
        self,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_dot_color: tuple = (WHITE),
        dot_radii: float = 0.1,
        trav_dot_opacity: float = 0.0,
        trav_dot_color: tuple = None,
        circle_radius: float = 3.0,
        circle_color: tuple = (RED),
        mov_color: tuple = (BLUE),  # mov_line color
        stat_color: tuple = (PURPLE),  # stat_line color
        chord_color: tuple = (ORANGE),  # chord_line color
        angle_radius: float = 0.5,
        angle_color: tuple = (YELLOW),
        init_degrees: float = 0.0,
    ):
        # redraw functions, called every frame
        def get_components():
            # define constants
            circle_center_point = array(
                [self.center_x.get_value(), self.center_y.get_value(), 0.0]
            )
            wiggle = 0
            circ_prop = (self.theta.get_value() / 360) % 1
            stat_end_point = circle_center_point + array([circle_radius, 0, 0])

            # build components
            center_dot = Dot(
                point=circle_center_point,
                radius=dot_radii,
            ).set_color(center_dot_color)

            circle = Circle(
                radius=circle_radius,
                arc_center=circle_center_point,
            ).set_color(circle_color)

            """
            This code could easily be put into get_mov_line() if we decide we
            don't really need a dot to travel around the circle n shit
            """
            if circ_prop == 1 or circ_prop == 0:
                """
                There has to be a tiny wiggle/offset to trav_dot's position
                whenever it gets to the start of the circle to prevent mov_line
                and stat_line from ever being parallel so that the construction
                of the Angle object in get_angle() doesn't crap itself.
                """
                wiggle = UP * 0.001  # lil wiggle
            trav_center_point = circle.point_from_proportion(circ_prop) + wiggle
            trav_dot = Dot(
                point=trav_center_point,
                radius=dot_radii,
                fill_opacity=trav_dot_opacity,
            ).set_color(trav_dot_color)

            stat_line = Line(
                start=circle_center_point,
                end=stat_end_point,
            ).set_color(stat_color)

            mov_line = Line(
                start=circle_center_point,
                end=trav_center_point,
            ).set_color(mov_color)

            chord_line = Line(
                start=trav_center_point, end=stat_end_point
            ).set_color(chord_color)

            angol = Angle(
                line1=stat_line,
                line2=mov_line,
                radius=angle_radius,
            ).set_color(angle_color)

            return VGroup(
                stat_line,
                circle,
                trav_dot,
                angol,
                mov_line,
                chord_line,
                center_dot,
            )

        # call upper-level constructors before adding shit
        super().__init__()

        # ValueTrackerz for shit
        self.center_x = ValueTracker(center_x)
        self.center_y = ValueTracker(center_y)
        self.theta = ValueTracker(init_degrees)

        # always redraw and add
        component_VGroup = always_redraw(get_components)
        self.add(component_VGroup)

    # Animation Functions!
    def set_theta(self, theta):
        return self.theta.animate.set_value(theta)

    def set_center_x(self, center_x):
        return self.center_x.animate.set_value(center_x)

    def set_center_y(self, center_y):
        return self.center_y.animate.set_value(center_y)
