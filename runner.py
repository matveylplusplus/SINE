from manim import *
from chord import ChordCircle


class DemonstrateChord(Scene):
    def construct(self):
        cc = ChordCircle(center_x=-3)
        self.add(cc)

        self.play(
            cc.set_theta(720),
            cc.set_center_x(3),
            cc.set_center_y(-0.5),
            run_time=3,
        )

        """
        frozen_frame=False prevents the scene from freezing on a near-full angle
        circle and makes sure it's adequately reset to 0 at the end of the
        360-degree turn
        """
        self.wait(frozen_frame=False)
