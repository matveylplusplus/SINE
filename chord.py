from manim import *
import copy

"""
cache is purely for optimizing self.[blank] calls in animation/updater functions
that are called basically every frame
"""
from functools import cache

"""
config.background_color = "#0c0b29"
config.pixel_height = 1080
config.pixel_width = 1920
config.quality = "example_quality"
"""


class Chord(Scene):
    def form_chord(
        self,
        dr: float,  # dot radius
        dc: str,  # dot color
        ts: float,  # travel speed (of dot)
        cr: float,  # circle radius
        cc: str,  # circle color
        op: np.ndarray,  # origin point
        opc: str,  # origin point color
        mlc: str,  # mov_line color
        slc: str,  # stat_line color
        clc: str,  # chord_line color
        ar: float,  # angle radius
        ac: str,  # angle color
    ):
        # all auxiliary functions
        @cache
        def go_around_circle(mob, dt):
            """
            dt = difference (in seconds) since last frame. At 60fps render, this
            is equivalent to 1/60.
            """
            self.circ_offset += dt * ts
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

        def get_mov_line():
            return Line(op, self.trav_dot.get_center(), color=mlc)

        def get_chord_line():
            return Line(self.trav_dot.get_center(), ORIGIN, color=clc)

        def get_angle():
            return Angle(self.stat_line, mov_line, ar, color=ac)

        # "main" code!
        """
        circ_offset has to be a field of Chord to be modified in the
        go_around_circle updater
        """
        self.circ_offset = 0.0
        self.trav_dot = Dot(radius=dr, color=dc, fill_opacity=0.0)
        self.op_dot = Dot(radius=dr, color=opc)
        self.circle = Circle(radius=cr, color=cc)
        self.stat_line = Line(op, ORIGIN, color=slc)
        self.origin_offset = UP * 0.01

        """
        tiny initial position offset, for same reason as explained in
        go_around_circle(). Otherwise, the first frame can't render
        """
        self.trav_dot.move_to(ORIGIN + self.origin_offset)

        self.op_dot.move_to(op)
        self.circle.move_to(op)

        # init updater and redraw
        mov_line = always_redraw(get_mov_line)
        chord_line = always_redraw(get_chord_line)
        self.trav_dot.add_updater(go_around_circle)
        angol = always_redraw(get_angle)

        # add everything
        self.add(self.stat_line)
        self.add(self.circle)
        self.add(self.trav_dot)
        self.add(angol)
        self.add(mov_line)
        self.add(chord_line)
        self.add(self.op_dot)

        # can updater after sum secs
        self.wait(3)
        self.trav_dot.remove_updater(go_around_circle)
        self.play(
            quarter_slo_down(self.trav_dot, self.circle, 0.75, self.origin_offset, ts)
        )
        self.play(
            trav_logistically(
                self.trav_dot,
                self.circle,
                self.circ_offset,
                3.25,
                self.origin_offset,
                5,
            )
        )  # providing a start_prop might not be necessary...why not use self.circ_offset?

    def construct(self):
        self.form_chord(
            0.1,
            YELLOW,
            0.25,
            3.0,
            RED,
            np.array([-3, 0, 0]),
            WHITE,
            BLUE,
            PURPLE,
            ORANGE,
            0.5,
            YELLOW,
        )


class trav_logistically(Animation):
    def __init__(self, mobject, path, path_offset, rotations, origin_offset, runtime):
        self.path = path
        self.init_path_offset = copy.copy(path_offset)
        self.curr_path_offset = path_offset
        self.rotations = rotations
        self.origin_offset = origin_offset
        super().__init__(mobject, run_time=runtime)

    @cache
    def interpolate_mobject(self, alpha):
        def logistic(x):
            return (
                self.rotations / (1 + np.exp((-20 * x) + 10))
            ) + self.init_path_offset

        pfp = self.path.point_from_proportion(logistic(alpha) % 1)
        if (pfp == ORIGIN).all():
            pfp += self.origin_offset
        self.mobject.move_to(pfp)


class quarter_slo_down(Animation):
    def __init__(self, mobject, path, start_prop, origin_offset, start_speed):
        self.path = path
        self.start_prop = start_prop
        self.origin_offset = origin_offset
        self.start_speed = start_speed

        """
        run_time is a property not open to the user
        """
        super().__init__(mobject, run_time=6)

    def interpolate_mobject(self, alpha):
        def exp_decay(x):
            return (
                (-self.start_speed * np.exp(-1.1 * x))
                + self.start_speed
                + self.start_prop
            )

        pfp = self.path.point_from_proportion(exp_decay(self.run_time * alpha))
        if (pfp == ORIGIN).all():
            pfp += self.origin_offset
        self.mobject.move_to(pfp)
