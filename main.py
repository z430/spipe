from unordered_worker import UnorderedWorker
from stage import Stage
from pipeline import Pipeline
from read_video_file import VideoFileReader
from write_video_file import WriteVideoFile


class Incrementor(UnorderedWorker):
    def do_task(self, value):
        return value + 1


class Doubler(UnorderedWorker):
    def do_task(self, value):
        return value * 2


class Printer(UnorderedWorker):
    def do_task(self, value):
        print(value)


stage1 = Stage(VideoFileReader)
stage2 = Stage(WriteVideoFile)

# stage1 = Stage(Incrementor)
# stage2 = Stage(Doubler)
# stage3 = Stage(Printer)
# stage4 = Stage(Printer)

stage1.link(stage2)
# stage1.link(stage3)
# stage2.link(stage4)

pipe = Pipeline(stage1)
pipe.put(1)

# for number in range(2):
#     pipe.put(number)

pipe.put(None)
