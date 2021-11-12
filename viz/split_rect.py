from typing import List, Union, BinaryIO
from PIL import Image

from viz.gif_drawer import SequentialDrawer
from viz.draw_primitives import CrossObject, EmptyObject, RoundedRectObject, RingObject
from viz.animation_primitives import ZoomToCamera


class SplitRect(SequentialDrawer):
    def __init__(self, choices: List[int], corrects: List[bool], colors: List[str],
        side: int = 800, initial_side: int = 700, line_width: int = 2,
        bg_color = "#ffffff", line_color = "#000000",
        fps: int = 30):

        super().__init__(Image.new("RGB", (side, side), bg_color), fps=fps)

        assert min(choices) >= 0, "min_choice index is >= 0"
        assert max(choices) <= 3, "max_choice index is <= 3"
        assert len(colors) >= 4

        self.side = side
        self.initial_side = initial_side
        self.line_width = line_width

        self.bg_color = bg_color
        self.line_color = line_color

        self.choices = choices
        self.corrects = corrects
        self.colors = colors
    
    def init_steps(self):
        delta = (self.side - self.initial_side) / 2
        x1, y1 = delta, delta
        x2, y2 = self.side - delta, self.side - delta
        prev_box = (0, 0, self.side, self.side)

        self.add_object(
            RoundedRectObject(
                x1, y1, x2, y2, radius=0,
                outline=self.line_color,
                border_width=self.line_width
            ),
            duration=0.1
        )
        for choice, is_correct in zip(self.choices, self.corrects):
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2

            if choice == 0:
                x1, y1, x2, y2 = x1, y1, mx, my
            elif choice == 1:
                x1, y1, x2, y2 = mx, y1, x2, my
            elif choice == 2:
                x1, y1, x2, y2 = x1, my, mx, y2
            elif choice == 3:
                x1, y1, x2, y2 = mx, my, x2, y2
            
            cur_color = self.colors[choice]
            self.add_object(
                RoundedRectObject(x1, y1, x2, y2, radius=0, fill=cur_color),
                duration=0.2
            )

            corr_width = (y2 - y1) / 10
            if is_correct:
                self.add_object(
                    RingObject(
                        x1, y1, x2, y2,
                        line_color=self.line_color, line_width=corr_width 
                    ),
                    duration=0.3
                )
            else:
                self.add_object(
                    CrossObject(
                        x1, y1, x2, y2,
                        line_color=self.line_color, line_width=corr_width 
                    ),
                    duration=0.3
                )
            
            self.add_object(EmptyObject(), duration=0.3)

            cam_dx, cam_dy = (x2 - x1) * 0.05, (y2 - y1) * 0.05
            self.add_camera_transform(ZoomToCamera(prev_box, (x1 - cam_dx, y1 - cam_dy, x2 + cam_dx, y2 + cam_dy), self.side, self.side), 0.5)
            prev_box = (x1, y1, x2, y2)

        self.add_object(EmptyObject(), duration=0.3)
        self.add_camera_transform(ZoomToCamera(prev_box, (0, 0, self.side-1, self.side-1), self.side, self.side), 0.2 * len(self.choices))
        self.add_object(EmptyObject(), duration=5)
    
    def save_gif(self, fp: Union[str, BinaryIO]):
        self.init_steps()
        return super().save_gif(fp)
