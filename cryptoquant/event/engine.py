"""
Event-driven framework of vn.py framework.
"""

from collections import defaultdict
from queue import Empty, Queue
from threading import Thread
from time import sleep
from typing import Any, Callable

EVENT_TIMER = "eTimer"
EVENT_CTA_STRATEGY = "eCtaStrategy"


class Event:
    """
    Event object consists of a type string which is used
    by event engine for distributing event, and a data
    object which contains the real data.
    """

    def __init__(self, type: str, data: Any = None):
        """"""
        self.type = type
        self.data = data


# Defines handler function to be used in event engine.
HandlerType = Callable[[Event], None]


class EventEngine:
    """
    Event engine distributes event object based on its type
    to those handlers registered.

    It also generates timer event by every interval seconds,
    which can be used for timing purpose.
    """

    def __init__(self, interval: int = 1):
        """
        Timer event is generated every 1 second by default, if
        interval not specified.
        """
        self._interval = interval
        self._queue = Queue()
        self._active = False
        self._thread = Thread(target=self._run)  # 线程
        self._timer = Thread(target=self._run_timer)
        self._handlers = defaultdict(list)
        self._general_handlers = []
        print("eventengine inited")

    def _run(self):
        """
        Get event from queue and then process it.
        """
        while self._active:
            try:
                # print('run event _run')
                event = self._queue.get(block=True, timeout=1)
                # print(f"queue size:{len(self._queue.queue) } {self._queue.qsize()}" )
                self._process(event)
            except Empty:
                # print('empty')
                pass

    def _process(self, event: Event):
        """
        First ditribute event to those handlers registered listening
        to this type.

        Then distrubute event to those general handlers which listens
        to all types.
        """
        # print(self._handlers)
        if event.type in self._handlers:
            # print(self._handlers)
            # print(event.__dict__)
            for handler in self._handlers[event.type]:
                # or "eTick." + "XBTUSD.BITMEX"
                # print('hander', handler)
                # print(event.type, event.__dict__)
                if event.type == EVENT_CTA_STRATEGY:
                    print("hander", handler)
                    print(event.type, event.__dict__)
                # if event.type == "eLog":
                #     print('hander',handler)
                #     print(event.type, event.__dict__)
                #
                # if event.type == "eTick." or event.type == "eTick." + "BTCUSD.BYBIT":
                #     print('hander',handler)
                #     print(event.type, event.__dict__)

                handler(event)
        # if event.type in self._handlers:
        #     [handler(event) for handler in self._handlers[event.type]]

        if self._general_handlers:
            [handler(event) for handler in self._general_handlers]

    def _run_timer(self):
        """
        Sleep by interval second(s) and then generate a timer event.
        """
        while self._active:
            sleep(self._interval)
            # print('1')
            event = Event(EVENT_TIMER)
            self.put(event)

    def start(self):
        """
        Start event engine to process events and generate timer events.
        """
        self._active = True
        self._thread.start()
        self._timer.start()

    def stop(self):
        """
        Stop event engine.
        """
        self._active = False
        self._timer.join()
        self._thread.join()

    def put(self, event: Event):
        """
        Put an event object into event queue.
        """
        # print(event.__dict__)
        self._queue.put(event)

    def register(self, type: str, handler: HandlerType):
        """
        Register a new handler function for a specific event type. Every
        function can only be registered once for each event type.
        """
        handler_list = self._handlers[type]
        if handler not in handler_list:
            handler_list.append(handler)

    def unregister(self, type: str, handler: HandlerType):
        """
        Unregister an existing handler function from event engine.
        """
        handler_list = self._handlers[type]

        if handler in handler_list:
            handler_list.remove(handler)

        if not handler_list:
            self._handlers.pop(type)

    def register_general(self, handler: HandlerType):
        """
        Register a new handler function for all event types. Every
        function can only be registered once for each event type.
        """
        if handler not in self._general_handlers:
            self._general_handlers.append(handler)

    def unregister_general(self, handler: HandlerType):
        """
        Unregister an existing general handler function.
        """
        if handler in self._general_handlers:
            self._general_handlers.remove(handler)


if __name__ == "__main__":
    pass

    # 第一步 实例化类
    import random
    import time

    def get_price(data):
        if event.type == "tick":
            print("tick price",event.data)

    engine = EventEngine(5)
    # 2. 启动EventEngine.
    engine.start()
    # 3. 注册要监听处理的事件。
    engine.register("tick", get_price)

    while True:
        # 循环生产事件.
        price = random.randrange(0, 800, 1)
        event = Event(type="tick", data=price)
        engine.put(event)
        time.sleep(3)
