class SingletonMeta(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

class Singleton(SingletonMeta):
    pass

a = Singleton()
b = Singleton()

print('IDS', id(a), id(b))