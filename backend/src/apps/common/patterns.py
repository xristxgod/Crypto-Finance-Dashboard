from .meta import SingletonMeta

__all__ = (
    'Singleton',
)


class Singleton(metaclass=SingletonMeta):
    """ Singleton pattern """
    pass
