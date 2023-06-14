""" Implements Stage Class """


class Stage(object):
    """The Stage is an assembly of workers of identical functionality"""

    def __init__(
        self,
        worker_class,
        size=1,
        disable_result=False,
        do_stop_task=False,
        input_tube=None,
        **worker_args
    ) -> None:
        self._worker_class = worker_class
        self._worker_args = worker_args
        self._size = size
        self._disable_result = disable_result
        self._do_stop_task = do_stop_task
        self._input_tube = (
            self._worker_class.get_tube_class()() if not input_tube else input_tube
        )
        self._output_tubes = list()
        self._next_stages = list()

    def put(self, task):
        """Put task on the stage's input tube"""
        self._input_tube.put((task, 0))

    def get(self, timeout=None):
        """retrieve results from all the outputs tubes"""
        valid = False
        result = None

        for tube in self._output_tubes:
            if timeout:
                valid, result = tube.get(timeout)
                if valid:
                    result = result[0]
            else:
                result = tube.get()[0]

        if timeout:
            return valid, result
        return result

    def results(self):
        while True:
            result = self.get()
            if result is None:
                break
            yield result

    def link(self, next_stage):
        if next_stage is self:
            raise ValueError("cannot link stage to itself")

        self._output_tubes.append(next_stage._input_tube)
        self._next_stages.append(next_stage)

    def get_leaves(self):
        result = list()
        if not self._next_stages:
            result.append(self)
        else:
            for stage in self._next_stages:
                leaves = stage.get_leaves()
                result += leaves
        return result

    def build(self):
        if not self._output_tubes:
            self._output_tubes.append(self._worker_class.get_tube_class()())

        self._worker_class.assemble(
            self._worker_args,
            self._input_tube,
            self._output_tubes,
            self._disable_result,
            self._do_stop_task,
        )
        for stage in self._next_stages:
            stage.build()
