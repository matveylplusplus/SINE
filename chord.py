# TODO: make Chord a vDict, but how to bundle animations with said vDict?

from manim import *
from numpy import ndarray, array
from anim import *

"""
cache is purely for optimizing self.[blank] calls in animation/updater functions
that are called basically every frame
"""
from functools import cache


class ChordCircle(VMobject):
    def __init__(
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

        """
        circ_offset has to be a field of Chord to be modified in the
        go_around_circle updater
        """
        self.circ_prop = init_prop
        self.trav_dot = Dot(
            radius=dot_radius, color=dot_color, fill_opacity=dot_opacity
        )
        self.op_dot = Dot(radius=dot_radius, color=center_color)
        self.circle = Circle(radius=circle_radius, color=circle_color)
        self.stat_line = Line(center, ORIGIN, color=stat_color)
        self.center_offset = UP * 0.001

        wiggle = 0
        if init_prop == 1 or init_prop == 0:
            """
            tiny initial position offset, for same reason as explained in
            go_around_circle(). Otherwise, the first frame can't render
            """
            wiggle = self.center_offset

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

        # call upper-level constructors before adding shit
        super().__init__()

        # add shit
        self.add(self.stat_line)
        self.add(self.circle)
        self.add(self.trav_dot)
        self.add(self.angol)
        self.add(self.mov_line)
        self.add(self.chord_line)
        self.add(self.op_dot)

    @cache
    def spin_chord(self, speed: float, rotations: float):
        # updater function
        def go_around_circle(mob, dt):
            """
            dt = difference (in seconds) since last frame. At 60fps render, this
            is equivalent to 1/60. Even though this parameter is not at all
            necessary to achieve what we want go_around_circle's to do (you can
            replace it with 1/config.frame_rate, as is done in anim.py), it is
            necessary to pass in because otherwise the3 updater will literally
            not fucking do anything
            """
            self.circ_prop = (self.circ_prop + (dt * speed)) % 1

            """
            There has to be a tiny offset to trav_dot's position whenever it
            gets to the start of the circle to prevent mov_line and stat_line
            from ever being parallel so that the construction of the Angle
            object in get_angle() doesn't crap itself
            """
            wiggle = 0
            if self.circ_prop == 1 or self.circ_prop == 0:
                wiggle = self.center_offset

            mob.move_to(
                self.circle.point_from_proportion(self.circ_prop) + wiggle
            )

        # attach updater and wait
        self.trav_dot.add_updater(go_around_circle)
        self.wait(rotations / speed)

        # can updater after sum secs and slow to full stop
        self.trav_dot.remove_updater(go_around_circle)
        # self.play(quarter_slo_down(self, speed, runtime=1))


class DemonstrateChord(Scene):
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
        self.circ_prop = init_prop
        self.trav_dot = Dot(
            radius=dot_radius, color=dot_color, fill_opacity=dot_opacity
        )
        self.op_dot = Dot(radius=dot_radius, color=center_color)
        self.circle = Circle(radius=circle_radius, color=circle_color)
        self.stat_line = Line(center, ORIGIN, color=stat_color)
        self.center_offset = UP * 0.001

        wiggle = 0
        if init_prop == 1 or init_prop == 0:
            """
            tiny initial position offset, for same reason as explained in
            go_around_circle(). Otherwise, the first frame can't render
            """
            wiggle = self.center_offset

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

    @cache
    def spin_chord(self, speed: float, rotations: float):
        # updater function
        """
        dt = difference (in seconds) since last frame. At 60fps render, this is
        equivalent to 1/60. Even though this parameter is not at all necessary
        to achieve what we want go_around_circle's to do (you can replace it
        with 1/config.frame_rate, as is done in anim.py), it is necessary to
        pass in because otherwise the3 updater will literally not fucking do
        anything
        """

        def go_around_circle(mob, dt):
            self.circ_prop = (self.circ_prop + (dt * speed)) % 1

            """
            There has to be a tiny offset to trav_dot's position whenever it
            gets to the start of the circle to prevent mov_line and stat_line
            from ever being parallel so that the construction of the Angle
            object in get_angle() doesn't crap itself
            """
            wiggle = 0
            if self.circ_prop == 1 or self.circ_prop == 0:
                wiggle = self.center_offset

            mob.move_to(
                self.circle.point_from_proportion(self.circ_prop) + wiggle
            )

        # attach updater and wait
        self.trav_dot.add_updater(go_around_circle)
        self.wait(rotations / speed)

        # can updater after sum secs and slow to full stop
        self.trav_dot.remove_updater(go_around_circle)
        self.play(quarter_slo_down(self, speed, runtime=1))

    def construct(self):
        cc = ChordCircle()
        self.add(cc)
        # self.form_chord(init_prop=0)
        # self.spin_chord(speed=0.25, rotations=3)
