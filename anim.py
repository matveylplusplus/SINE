from manim import *
from numpy import exp, copy
from chord import Chord

"""
cache is purely for optimizing self.[blank] calls in animation/updater functions
that are called basically every frame
"""
from functools import cache


class trav_logistically(Animation):
    def __init__(
        self, mobject, path, path_offset, rotations, origin_offset, runtime
    ):
        self.path = path
        self.init_path_offset = copy(path_offset)
        self.curr_path_offset = path_offset
        self.rotations = rotations
        self.origin_offset = origin_offset
        super().__init__(mobject, run_time=runtime)

    @cache
    def interpolate_mobject(self, alpha):
        def logistic(x):
            return (
                self.rotations / (1 + exp((-20 * x) + 10))
            ) + self.init_path_offset

        pfp = self.path.point_from_proportion(logistic(alpha) % 1)
        if (pfp == ORIGIN).all():
            pfp += self.origin_offset
        self.mobject.move_to(pfp)


class quarter_slo_down(Animation):
    def __init__(self, chord: Chord, speed: float, runtime: float):
        self.trav_dot = chord.trav_dot
        self.circle = chord.circle
        self.circ_prop = chord.circ_prop
        self.center_offset = chord.center_offset
        self.start_speed = speed
        super().__init__(chord, run_time=runtime)

    @cache
    def interpolate_mobject(self, alpha):
        self.circ_prop = (
            self.circ_prop
            + ((1 / config.frame_rate) * self.start_speed) * (1 - alpha)
        ) % 1

        wiggle = 0
        if self.circ_prop == 1 or self.circ_prop == 0:
            wiggle = self.center_offset

        self.trav_dot.move_to(
            self.circle.point_from_proportion(self.circ_prop) + wiggle
        )
