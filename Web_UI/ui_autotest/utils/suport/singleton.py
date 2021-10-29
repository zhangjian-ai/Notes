import threading
from collections import defaultdict


class Singleton(type):
    __instance_lock = threading.Lock()
    __instance_dict = defaultdict()

    def __call__(cls, *args, **kwargs):
        key = str(args) + str(kwargs)

        with Singleton.__instance_lock:
            if key not in cls.__instance_dict:
                cls.__instance_dict[key] = super().__call__(*args, **kwargs)
        return cls.__instance_dict[key]
