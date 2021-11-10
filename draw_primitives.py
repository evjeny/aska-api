from typing import List, Tuple
from PIL import Image, ImageDraw
from gif_drawer import DrawnObject


class EmptyObject(DrawnObject):
    pass


class RoundedRectObject(DrawnObject):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, radius: float,
        fill = None, outline = None, border_width: float = 0):

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.radius = radius

        self.fill = fill
        self.outline = outline
        self.border_width = border_width
    
    def draw(self, canvas: Image.Image, alpha: float = 1) -> Image.Image:
        result = canvas.copy()

        if alpha < 0.5:
            return result

        draw = ImageDraw.Draw(result)
        draw.rounded_rectangle(
            (self.x1, self.y1, self.x2, self.y2), self.radius,
            fill=self.fill, outline=self.outline, width=self.border_width
        )
        
        return result


class LineObject(DrawnObject):
    def __init__(self, xy: List[Tuple[int, int]],
        fill, line_width: int = 1):

        self.xy = xy
        self.fill = fill
        self.line_width = line_width
    
    def draw(self, canvas: Image.Image, alpha: float = 1) -> Image.Image:
        result = canvas.copy()

        if alpha < 0.5:
            return result

        draw = ImageDraw.Draw(result)
        draw.line(self.xy, fill=self.fill, width=self.line_width)
        
        return result
