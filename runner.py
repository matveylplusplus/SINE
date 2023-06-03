from manim import *
from chord import ChordCircle


class DemonstrateChord(Scene):
    def construct(self):
        cc = ChordCircle(center_x=-3, angle_color=("#c32222", "#fdbb2d"))
        self.add(cc)

        self.play(cc.set_theta(270))
        self.wait(frozen_frame=False)
        self.play(cc.set_center_x(0))
        self.wait(frozen_frame=False)
        self.play(cc.set_center_y(1))
        self.wait(frozen_frame=False)
        self.play(cc.set_theta(90))
        self.wait(frozen_frame=False)

        """
        frozen_frame=False prevents the scene from freezing on a near-full angle
        circle and makes sure it's adequately reset to 0 at the end of the
        360-degree turn
        """
