from manim import *
from numpy import exp, copy

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
    def __init__(self, mobject, path, start_prop, origin_offset, start_speed):
        self.path = path
        self.start_prop = start_prop
        self.origin_offset = origin_offset
        self.start_speed = start_speed

        """
        run_time is a property not open to the user
        """
        super().__init__(mobject, run_time=6)

    @cache
    def interpolate_mobject(self, alpha):
        def exp_decay(x):
            return (
                (-self.start_speed * exp(-1.1 * x))
                + self.start_speed
                + self.start_prop
            )

        pfp = self.path.point_from_proportion(exp_decay(self.run_time * alpha))
        if (pfp == ORIGIN).all():
            pfp += self.origin_offset
        self.mobject.move_to(pfp)
