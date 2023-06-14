from queue import Queue
import queue


class TubeQ:
    def __init__(self, maxsize=0) -> None:
        self._queue = Queue(maxsize=maxsize)

    def put(self, data) -> None:
        self._queue.put(data)

    def get(self, timeout=None):
        """Return the next available item from the tube
        Blocks if tube is empty , until a producer for the rube puts an item on it

        Args:
            timeout (_type_, optional): timout status. Defaults to None.
        """
        if timeout:
            try:
                result = self._queue.get(True, timeout)
            except queue.Empty:
                return False, None

            return True, result

        return self._queue.get()
