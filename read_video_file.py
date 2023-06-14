import cv2
import os
from unordered_worker import UnorderedWorker


class VideoFileReader(UnorderedWorker):
    def __init__(self) -> None:
        super().__init__()
        self.video_path = "carrycan_back_1.mp4"
        self.stream_name = os.path.basename(self.video_path)
        self.stream = cv2.VideoCapture(self.video_path)
        self.total_frames = int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))
        self.stream_fps = int(self.stream.get(cv2.CAP_PROP_FPS))

    def do_task(self, task):
        while True:
            grabbed, frame = self.stream.read()
            if not grabbed:
                return None

            data = {
                "stream_name": self.stream_name,
                "frame": frame,
                "total_frames": self.total_frames,
                "stream_fps": self.stream_fps,
            }
            return data
