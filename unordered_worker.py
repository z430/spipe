from tubeq import TubeQ
from threading import Thread


class UnorderedWorker:
    def __init__(self) -> None:
        pass

    def init2(self, input_tube, output_tubes, disable_result, do_stop_task):
        self._tube_task_input = input_tube
        self._tubes_result_output = output_tubes
        self._disable_result = disable_result
        self._do_stop_task = do_stop_task

        self.worker = Thread(target=self.run)
        self.worker.daemon = True

    def start(self):
        self.worker.start()

    @staticmethod
    def get_tube_class():
        return TubeQ

    def put_result(self, result):
        for tube in self._tubes_result_output:
            tube.put((result, 0))

    @classmethod
    def assemble(
        cls, args, input_tube, output_tubes, disable_result, do_stop_task
    ) -> None:
        worker = cls(**args)
        worker.init2(input_tube, output_tubes, disable_result, do_stop_task)
        worker.start()

    def run(self):
        self.do_init()
        while True:
            try:
                (task, count) = self._tube_task_input.get()
            except:
                (task, count) = (None, 0)

            # In case the task is None, it represents the "stop" request
            # the count being the number of workers in this stage had already stopped
            if task is None:
                count += 1
                self._tube_task_input.put((None, count))

                if self._do_stop_task:
                    self.do_task(None)

                break

            # the task is not None meaning that it is an actual task to be processed.
            # therefore let's call do_task()
            result = self.do_task(task)

            if not self._disable_result and result is not None:
                self.put_result(result)

    def do_init(self):
        return None

    def do_task(self, task):
        return True
