from manim import *
from numpy import ndarray, array
from anim import *

"""
cache is purely for optimizing self.[blank] calls in animation/updater functions
that are called basically every frame
"""
from functools import cache


class Chord(Scene):
    @cache
    def form_chord(
        self,
        dot_radius: float = 0.1,
        dot_opacity: float = 0.0,
        dot_color: str = None,
        circle_radius: float = 3.0,
        circle_color: str = RED,
        center: ndarray = array([-3, 0, 0]),
        center_color: str = WHITE,
        mov_color: str = BLUE,  # mov_line color
        stat_color: str = PURPLE,  # stat_line color
        chord_color: str = ORANGE,  # chord_line color
        angle_radius: float = 0.5,
        angle_color: str = YELLOW,
        init_prop: float = 0,  # init point from proportion of circle
    ):
        # all auxiliary functions
        def get_mov_line():
            return Line(center, self.trav_dot.get_center(), color=mov_color)

        def get_chord_line():
            return Line(self.trav_dot.get_center(), ORIGIN, color=chord_color)

        def get_angle():
            return Angle(
                self.stat_line, self.mov_line, angle_radius, color=angle_color
            )

        # "main" code!
        """
        circ_offset has to be a field of Chord to be modified in the
        go_around_circle updater
        """
        self.circ_offset = 0.0
        self.trav_dot = Dot(
            radius=dot_radius, color=dot_color, fill_opacity=dot_opacity
        )
        self.op_dot = Dot(radius=dot_radius, color=center_color)
        self.circle = Circle(radius=circle_radius, color=circle_color)
        self.stat_line = Line(center, ORIGIN, color=stat_color)
        self.origin_offset = UP * 0.001

        wiggle = 0
        if init_prop == 1 or init_prop == 0:
            """
            tiny initial position offset, for same reason as explained in
            go_around_circle(). Otherwise, the first frame can't render
            """
            wiggle = self.origin_offset

        # move into position
        self.op_dot.move_to(center)
        self.circle.move_to(center)
        self.trav_dot.move_to(
            self.circle.point_from_proportion(init_prop) + wiggle
        )

        # set up redraws
        self.mov_line = always_redraw(get_mov_line)
        self.chord_line = always_redraw(get_chord_line)
        self.angol = always_redraw(get_angle)

        # add everything
        self.add(self.stat_line)
        self.add(self.circle)
        self.add(self.trav_dot)
        self.add(self.angol)
        self.add(self.mov_line)
        self.add(self.chord_line)
        self.add(self.op_dot)

    def construct(self):
        self.form_chord(init_prop=0.45)

    @cache
    def spin_chord(self, speed: float, rotations: float):
        def go_around_circle(mob, dt):
            """
            dt = difference (in seconds) since last frame. At 60fps render, this
            is equivalent to 1/60.
            """
            self.circ_offset += dt * speed
            pfp = self.circle.point_from_proportion(self.circ_offset % 1)
            if (pfp == self.circle.point_from_proportion(0)).all():
                """
                There has to be a tiny offset to trav_dot's position whenever it
                gets to the start of the circle to prevent mov_line and
                stat_line from ever being parallel so that the construction of
                the Angle object in get_angle() doesn't crap itself
                """
                pfp += self.origin_offset
            mob.move_to(pfp)

        # attach updater and wait
        self.trav_dot.add_updater(go_around_circle)
        self.wait(rotations / speed)

        # can updater after sum secs and slow to full stop
        self.trav_dot.remove_updater(go_around_circle)
