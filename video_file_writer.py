from threading import Thread
from queue import Queue
import time
from vidgear.gears import WriteGear
from loguru import logger


class VideoFileWriter:
    def __init__(self, queue_in: Queue, filename: str, fps: int) -> None:
        output_params = {
            "-input_framerate": fps,
            "-vcodec": "libx264",
            # "-crf": 18,
            # "-preset": "veryfast",
        }

        self.video_file_writer = WriteGear(output=filename, **output_params)

        self.stopped = False
        self.queue_in = queue_in
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.pfps = 0
        self.fps_data = []
        self.frame_number = 0

    def start(self):
        self.thread.start()

    def update(self):
        while True:
            if self.stopped:
                break

            if not self.queue_in.empty():
                start_time = time.perf_counter()
                data = self.queue_in.get()
                if data is None:
                    self.stopped = True
                else:
                    image = data["image"]
                    self.video_file_writer.write(image)
                self.frame_number += 1
                self.pfps = 1 / (time.perf_counter() - start_time)
                self.fps_data.append(self.pfps)
            else:
                time.sleep(0.01)

    def read(self):
        return self.stopped

    def stop(self):
        while not self.queue_in.empty():
            logger.info(f"Writing frame to file -> {self.queue_in.qsize()}")

        self.stopped = True
        self.thread.join()

        if self.video_file_writer:
            self.video_file_writer.close()
