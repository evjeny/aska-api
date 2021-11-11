from typing import Tuple
from viz.gif_drawer import AnimatedCamera


bbox = Tuple[float, float, float, float]


class ZoomToCamera(AnimatedCamera):
    def __init__(self, box1: bbox, box2: bbox, width: float, height: float):
        super().__init__()

        x11, y11, x12, y12 = box1
        x21, y21, x22, y22 = box2

        self.dx1 = x11
        self.dy1 = y11
        self.dx2 = x21
        self.dy2 = y21

        self.sx1 = width / (x12 - x11 + 1)
        self.sy1 = height / (y12 - y11 + 1)
        self.sx2 = width / (x22 - x21 + 1)
        self.sy2 = height / (y22 - y21 + 1)
    
    def _in_alpha(self, a: float, b: float, alpha: float) -> float:
        return a + (b - a) * alpha

    def set_alpha(self, alpha: float):
        super().set_alpha(alpha)

        self.dx = self._in_alpha(self.dx1, self.dx2, alpha)
        self.dy = self._in_alpha(self.dy1, self.dy2, alpha)
        self.sx = self._in_alpha(self.sx1, self.sx2, alpha)
        self.sy = self._in_alpha(self.sy1, self.sy2, alpha)
        self.sw = (self.sx + self.sy) / 2
