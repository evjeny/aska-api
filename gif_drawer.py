from typing import List, Union, BinaryIO
from PIL import Image


class DrawnObject:
    def draw(self, canvas: Image.Image, alpha: float = 1) -> Image.Image:
        return canvas


class DrawStep:
    def __init__(self, drawn_object: DrawnObject, alphas: List[float]):
        self.drawn_object = drawn_object
        self.alphas = alphas
    
    def draw(self, base_image: Image.Image) -> List[Image.Image]:
        return [self.drawn_object.draw(base_image, alpha) for alpha in self.alphas]


class SequentialDrawer:
    def __init__(self, base_image: Image.Image, fps: int = 30):
        self.base = base_image
        self.fps = fps

        self.steps: List[DrawStep] = []

    def add_step(self, drawn_object: DrawnObject, duration: float = 0):
        if duration < 0:
            raise Exception("Duration should be > 0")
        elif duration == 0:
            alphas = [1]
        else:
            alphas = [frame / self.fps for frame in range(int(duration * self.fps))]
            if len(alphas) == 0 or alphas[-1] != 1:
                alphas.append(1)
        
        self.steps.append(DrawStep(drawn_object, alphas))
    
    def export_frames(self) -> List[Image.Image]:
        frames: List[Image.Image] = [self.base.copy()]

        for step in self.steps:
            for frame in step.draw(frames[-1]):
                frames.append(frame)
        
        return frames
    
    def save_gif(self, fp: Union[str, BinaryIO]):
        frames = self.export_frames()
        first_frame = frames.pop(0)
        duration = int(1000 / self.fps)
        
        first_frame.save(fp, format="gif", save_all=True, append_images=frames, optimize=False, duration=duration, loop=0)
