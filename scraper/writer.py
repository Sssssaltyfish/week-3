from logging import Logger
from typing import (
    Callable,
    Generic,
    TypeVar,
    List,
    IO,
    Any,
    Optional,
)
from queue import Empty, Queue
from threading import Thread

_FeedT = TypeVar('_FeedT')

class Writer(Thread, Generic[_FeedT]):
    def __init__(
            self,
            iofunc: Callable[[_FeedT, IO], None],
            timeout: int = 0,
            file_name: str = '',
            file_mode: str = 'w',
            data: Any = None,
            logger: Optional[Logger] = None,
            **file_args) -> None:
        self.logger = logger
        self.__iofunc = iofunc
        self.__queue: Queue[_FeedT] = Queue()
        self.__is_active = False
        self.__timeout = timeout
        self.file_name = file_name
        self.file_mode = file_mode
        self.file_args = file_args
        self.data = data
        super().__init__(target=self.run, daemon=True)

    def write(self):
        with open(self.file_name, self.file_mode, **self.file_args) as file:
            try:
                pass
            except:
                pass
            finally:
                self.__iofunc(self.data, file)


    def run(self):
        self.__is_active = True
        while self.__is_active:
            try:
                while value := self.__queue.get(True, self.__timeout):
                    self.data.update(value)
            except Empty:
                pass
            finally:
                self.write()

    def add(self, *feeds: List[_FeedT]) -> None:
        for feed in feeds:
            self.__queue.put(feed)

    @ property
    def timeout(self):
        return self.__timeout

    @ timeout.setter
    def _(self, new_timeout: int):
        self.__timeout = new_timeout

    @ property
    def get_queue(self):
        return self.__queue

    def stop(self):
        self.__is_active = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.write()
        self.stop()
        if self.logger and exc_value is not None:
            self.logger.error("An exception occured", exc_info=(exc_type, exc_value, traceback))
            return False
        return True