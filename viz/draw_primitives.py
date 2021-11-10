from typing import List, Tuple

from PIL import Image, ImageDraw

from viz.gif_drawer import DrawnObject


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

        dx = (1 - alpha) * (self.x2 - self.x1) / 2
        dy = (1 - alpha) * (self.y2 - self.y1) / 2

        draw = ImageDraw.Draw(result)
        draw.rounded_rectangle(
            (self.x1+dx, self.y1+dy, self.x2-dx, self.y2-dy), self.radius*alpha,
            fill=self.fill, outline=self.outline, width=int(self.border_width*alpha)
        )
        
        return result


class LineObject(DrawnObject):
    def __init__(self, xy: List[Tuple[int, int]],
        fill, line_width: int = 1):

        self.xy = xy
        self.fill = fill
        self.line_width = line_width

        self.lenghts = [0]
        for (x1, y1), (x2, y2) in zip(xy[:-1], xy[1:]):
            segment_length = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
            self.lenghts.append(self.lenghts[-1] + segment_length)
    
    def draw(self, canvas: Image.Image, alpha: float = 1) -> Image.Image:
        result = canvas.copy()

        if alpha == 0:
            return result

        target_length = self.lenghts[-1] * alpha
        min_index = min(i for i in range(len(self.lenghts)) if target_length <= self.lenghts[i])

        draw = ImageDraw.Draw(result)
        draw.line(self.xy[:min_index], fill=self.fill, width=self.line_width)

        (x1, y1), (x2, y2) = self.xy[min_index-1: min_index+1]
        seg_alpha = (target_length - self.lenghts[min_index - 1]) / (self.lenghts[min_index] - self.lenghts[min_index - 1])
        tx, ty = x1 + (x2 - x1) * seg_alpha, y1 + (y2 - y1) * seg_alpha
        draw.line([(x1, y1), (tx, ty)], fill=self.fill, width=self.line_width)
        
        return result


class CombinedObject(DrawnObject):
    def __init__(self, objects: List[DrawnObject]):
        self.objects = objects
    
    def draw(self, canvas: Image.Image, alpha: float = 1) -> Image.Image:
        for object in self.objects:
            canvas = object.draw(canvas, alpha=alpha)
        return canvas


class RingObject(DrawnObject):
    def __init__(self, x1: int, y1: int, x2: int, y2: int, line_color, line_width: float = 1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.line_color = line_color
        self.line_width = line_width
    
    def draw(self, canvas: Image.Image, alpha: float = 1) -> Image.Image:
        result = canvas.copy()

        draw = ImageDraw.Draw(result)
        draw.arc(
            [self.x1, self.y1, self.x2, self.y2],
            0, int(360 * alpha),
            fill=self.line_color, width=self.line_width
        )
        
        return result


class CrossObject(CombinedObject):
    def __init__(self, x1: int, y1: int, x2: int, y2: int, line_color, line_width: int = 1):
        p = line_width / 2**1.5
        super().__init__([
            LineObject(
                [(x1+p, y1+p), (x2-p, y2-p)],
                fill=line_color, line_width=line_width
            ),
            LineObject(
                [(x2-p, y1+p), (x1+p, y2-p)],
                fill=line_color, line_width=line_width
            )
        ])
