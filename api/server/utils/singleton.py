def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls.__new__(cls, *args, **kwargs)

            # Initialize the instance only once
            if hasattr(instances[cls], '__initialized'):
                return instances[cls]

            cls.__init__(instances[cls], *args, **kwargs)
            instances[cls].__initialized = True

        return instances[cls]

    def clear_instance():
        if cls in instances:
            instances.pop(cls)

    cls.clear = staticmethod(clear_instance)
    return get_instance
