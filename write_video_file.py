import os
from vidgear.gears import WriteGear
from unordered_worker import UnorderedWorker


class WriteVideoFile(UnorderedWorker):
    def __init__(self) -> None:
        super().__init__()
        output_params = {
            "-input_framerate": 30,
            "-vcodec": "libx264",
            "-crf": 18,
            "-preset": "veryfast",
        }

        self.video_file_writer = WriteGear(output="output.mp4", **output_params)

    def do_task(self, task):
        if task["frame"]:
            self.video_file_writer.write(task["frame"])
