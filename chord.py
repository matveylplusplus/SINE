# TODO: make Chord a vDict, but how to bundle animations with said vDict?
# should the chordcircle be asking for the scene, or should the scene be asking
# for the chordcircle?

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
        # redraw functions, called every frame
        def get_trav_dot():
            wiggle = 0
            circ_prop = (self.theta / 360) % 1
            if circ_prop == 1 or circ_prop == 0:
                """
                tiny initial position offset, for same reason as explained in
                go_around_circle(). Otherwise, the first frame can't render
                """
                wiggle = self.center_offset
            return Dot(
                point=self.circle.point_from_proportion(circ_prop) + wiggle,
                radius=dot_radius,
                color=dot_color,
                fill_opacity=dot_opacity,
            )

        def get_mov_line():
            return Line(center, self.trav_dot.get_center(), color=mov_color)

        def get_chord_line():
            return Line(self.trav_dot.get_center(), ORIGIN, color=chord_color)

        def get_angle():
            return Angle(
                self.stat_line, self.mov_line, angle_radius, color=angle_color
            )

        # static mobjects (no move)
        self.theta = ValueTracker(init_prop * 360)
        self.center_dot = Dot(
            point=center, radius=dot_radius, color=center_color
        )
        self.circle = Circle(
            radius=circle_radius, color=circle_color, arc_center=center
        )
        self.stat_line = Line(center, ORIGIN, color=stat_color)
        self.center_offset = UP * 0.001

        # dynamic mobjects (do move)
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
            self.theta = (self.theta + (dt * speed)) % 1

            """
            There has to be a tiny offset to trav_dot's position whenever it
            gets to the start of the circle to prevent mov_line and stat_line
            from ever being parallel so that the construction of the Angle
            object in get_angle() doesn't crap itself
            """
            wiggle = 0
            if self.theta == 1 or self.theta == 0:
                wiggle = self.center_offset

            mob.move_to(self.circle.point_from_proportion(self.theta) + wiggle)

        # attach updater and wait
        self.trav_dot.add_updater(go_around_circle)
        self.wait(rotations / speed)

        # can updater after sum secs and slow to full stop
        self.trav_dot.remove_updater(go_around_circle)
        # self.play(quarter_slo_down(self, speed, runtime=1))


# TODO: run!! if works, delete all bloat
class DemonstrateChord(Scene):
    def construct(self):
        cc = ChordCircle()
        self.add(cc)

        theta = cc.theta
        self.play(theta.animate.set_value(1080), run_time=12)
