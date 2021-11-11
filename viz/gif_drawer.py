from typing import List, Union, Tuple, BinaryIO
from PIL import Image


class Camera:
    def __init__(self):
        self.sx = 1
        self.sy = 1
        self.dx = 0
        self.dy = 0
        self.sw = 1
    
    def txy(self, x: float, y: float) -> Tuple[float, float]:
        return self.sx * (x - self.dx), self.sy * (y - self.dy)
    
    def tw(self, w: float) -> float:
        return self.sw * w


class AnimatedCamera(Camera):
    def set_alpha(self, alpha: float):
        pass


class DrawnObject:
    def __init__(self):
        self.camera: Camera = None
    
    def set_camera(self, camera: Camera):
        self.camera = camera
    
    def draw(self, canvas: Image.Image, alpha: float = 1) -> Image.Image:
        return canvas


class SequentialDrawer:
    def __init__(self, base_image: Image.Image, fps: int = 30):
        self.base = base_image
        self.fps = fps
        self.camera = Camera()

        self.objects: List[DrawnObject] = []
        self.frames: List[Image.Image] = [self.base]

    def duration_to_alphas(self, duration: float) -> List[float]:
        if duration < 0:
            raise Exception("Duration should be > 0")
        elif duration == 0:
            alphas = [1]
        else:
            total_frames = int(duration * self.fps)
            alphas = [frame / total_frames for frame in range(total_frames)]
            if len(alphas) == 0 or alphas[-1] != 1:
                alphas.append(1)
        return alphas

    def add_object(self, drawn_object: DrawnObject, duration: float = 0):
        drawn_object.set_camera(self.camera)
        self.objects.append(drawn_object)
        
        prev_frame = self.frames[-1]
        for alpha in self.duration_to_alphas(duration):
            self.frames.append(drawn_object.draw(prev_frame, alpha))
    
    def add_camera_transform(self, animated_camera: AnimatedCamera, duration: float = 0):
        for alpha in self.duration_to_alphas(duration):
            animated_camera.set_alpha(alpha)
            
            cur_frame = self.base
            for object in self.objects:
                object.set_camera(animated_camera)
                cur_frame = object.draw(cur_frame)
            
            self.frames.append(cur_frame)

    def save_gif(self, fp: Union[str, BinaryIO]):
        first_frame = self.frames.pop(0)
        duration = int(1000 / self.fps)
        
        first_frame.save(fp, format="gif", save_all=True, append_images=self.frames, optimize=False, duration=duration, loop=0)
