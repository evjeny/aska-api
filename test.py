from PIL import Image
from viz.animation_primitives import ZoomToCamera

from viz.split_rect import SplitRect
from viz.gif_drawer import SequentialDrawer, AnimatedCamera
from viz.draw_primitives import EmptyObject, RoundedRectObject


def draw_split_rect():
    r = SplitRect(
        choices=[0, 1, 2, 3, 0, 1, 2, 3], corrects=[0, 1, 0, 1, 1, 0, 1, 0],
        colors=["#ff0000", "#00ff00", "#0000ff", "#ffff00"]
    )
    r.save_gif("rect_example.gif")


def draw_sequential():
    w = 800
    h = 800
    s = SequentialDrawer(Image.new("RGB", (w, h), "#ffffff"))

    for x1, y1 in [[50, 50], [450, 50], [50, 450], [450, 450]]:
        s.add_object(RoundedRectObject(x1, y1, x1+300, y1+300, 30, "#000000"), 0.3)
        s.add_object(EmptyObject(), 0.1)

    s.add_object(EmptyObject(), 0.3)

    for box1, box2 in [
        [(0, 0, w, h), (0, 0, w//2, h//2)],
        [(0, 0, w//2, h//2), (w//2, 0, w, h//2)],
        [(w//2, 0, w, h//2), (w//2, h//2, w, h)],
        [(w//2, h//2, w, h), (0, h//2, w//2, h)],
        [(0, h//2, w//2, h), (w//2, 0, w, h//2)],
        [(w//2, 0, w, h//2), (0, 0, w, h)],
    ]:
        s.add_camera_transform(ZoomToCamera(box1, box2, w, h), 1)
        s.add_object(EmptyObject(), 0.3)

    s.add_object(EmptyObject(), 3)

    s.save_gif("sequential_example.gif")


draw_split_rect()
draw_sequential()
