from threading import Thread
from queue import Queue
import cv2
import time
import numpy as np


class VideoFileReader:
    def __init__(self, video_path: str) -> None:
        self.video_path = video_path
        self.stream = cv2.VideoCapture(self.video_path)
        self.total_frames = int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.stream.get(cv2.CAP_PROP_FPS))
        self.stopped = False

        # thread init
        self.Q = Queue(maxsize=500)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.pfps = 0
        self.fps_data = []
        self.frame_number = 0

    def start(self) -> None:
        self.thread.start()

    def update(self) -> None:
        while True:
            if self.stopped:
                break

            if not self.Q.full():
                start_time = time.perf_counter()
                (grabbed, frame) = self.stream.read()

                if not grabbed:
                    self.stopped = True
                    data = None
                else:
                    data = {
                        "start": time.time(),
                        "frame_num": self.frame_number,
                        "total_frames": self.total_frames,
                        "image": frame,
                        "runtime_fps": self.pfps,
                        "num_stages": 1,
                    }
                self.Q.put(data)
                self.frame_number += 1
                self.pfps = 1 / (time.perf_counter() - start_time)
                self.fps_data.append(self.pfps)
            else:
                time.sleep(0.1)

        self.stream.release()

    def read(self) -> np.ndarray:
        return self.Q.get()

    def running(self):
        return self.more() or not self.stopped

    def more(self):
        tries = 0
        while self.Q.qsize() == 0 and not self.stopped and tries < 5:
            time.sleep(0.1)
            tries += 1
        return self.Q.qsize() > 0

    def stop(self):
        self.stopped = True
        self.thread.join()
