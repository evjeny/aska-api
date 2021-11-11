from typing import List, Tuple

from PIL import Image, ImageDraw

from viz.gif_drawer import DrawnObject, Camera


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

        nx1, ny1 = self.camera.txy(self.x1, self.y1)
        nx2, ny2 = self.camera.txy(self.x2, self.y2)

        # print("rect", nx1, ny1, nx2, ny2)

        nradius = self.camera.tw(self.radius)
        nborder_width = self.camera.tw(self.border_width)

        dx = (1 - alpha) * (nx2 - nx1) / 2
        dy = (1 - alpha) * (ny2 - ny1) / 2

        draw = ImageDraw.Draw(result)
        draw.rounded_rectangle(
            (nx1+dx, ny1+dy, nx2-dx, ny2-dy), nradius*alpha,
            fill=self.fill, outline=self.outline, width=int(nborder_width*alpha)
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
        seg_alpha = (target_length - self.lenghts[min_index - 1]) / (self.lenghts[min_index] - self.lenghts[min_index - 1])

        nline_width = self.camera.tw(self.line_width)

        draw = ImageDraw.Draw(result)
        draw.line([self.camera.txy(*xy) for xy in self.xy[:min_index]], fill=self.fill, width=nline_width)

        (x1, y1), (x2, y2) = self.xy[min_index-1: min_index+1]
        nx1, ny1 = self.camera.txy(x1, y1)
        nx2, ny2 = self.camera.txy(x2, y2)

        tx, ty = nx1 + (nx2 - nx1) * seg_alpha, ny1 + (ny2 - ny1) * seg_alpha
        draw.line([(nx1, ny1), (tx, ty)], fill=self.fill, width=nline_width)
        
        return result


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

        nx1, ny1 = self.camera.txy(self.x1, self.y1)
        nx2, ny2 = self.camera.txy(self.x2, self.y2)
        nline_width = self.camera.tw(self.line_width)

        draw = ImageDraw.Draw(result)
        draw.arc(
            [nx1, ny1, nx2, ny2],
            0, int(360 * alpha),
            fill=self.line_color, width=nline_width
        )
        
        return result


class CombinedObject(DrawnObject):
    def __init__(self, objects: List[DrawnObject]):
        self.objects = objects
        self.camera = None

        for object in self.objects:
            object.set_camera(self.camera)
    
    def set_camera(self, camera: Camera):
        self.camera = camera
        for object in self.objects:
            object.set_camera(self.camera)

    def draw(self, canvas: Image.Image, alpha: float = 1) -> Image.Image:
        for object in self.objects:
            canvas = object.draw(canvas, alpha=alpha)
        return canvas


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
