import abc
import pyrsistent as _pyr
import typing as ty


class _Common(abc.ABC):
    _pyr_type = ...

    @classmethod
    def _from_pyr(cls, pyr_data):
        return cls(pyr_data)

    @classmethod
    @abc.abstractmethod
    def _pyr_make(cls, *args):
        ...

    def __init__(self, data=None):
        if isinstance(data, self._pyr_type):
            self.pyr_data = data
        elif data is None:
            self.pyr_data = self._pyr_make()
        else:
            self.pyr_data = self._pyr_make(data)

    @classmethod
    def convert(cls, value):
        if isinstance(value, cls):
            return value
        else:
            return cls(value)


class _ForwardToPyr:
    def __set_name__(self, owner, name):
        self.pyr_attribute_name = name

    def __get__(self, obj, objtype=None):
        return getattr(obj.pyr_data, self.pyr_attribute_name)


K = ty.TypeVar("K")
V = ty.TypeVar("V")


class _SimpleIterableMixin:
    __iter__ = _ForwardToPyr()
    __len__ = _ForwardToPyr()
    __bool__ = _ForwardToPyr()
    __contains__ = _ForwardToPyr()


class _EqAndBoolMixin:
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self.pyr_data == other.pyr_data

    def __bool__(self):
        return len(self.pyr_data) > 0


class HashTrieMap(_EqAndBoolMixin, _SimpleIterableMixin, _Common, ty.Generic[K, V]):
    _pyr_type = _pyr.PMap

    @classmethod
    def _pyr_make(cls, *args):
        p = _pyr.m()
        if args:
            p = cls._pyr_update(p, args[0])
        return p

    def insert(self, key, value):
        # TODO: maybe use evolver to delay the operations?
        return self._from_pyr(self.pyr_data.set(key, value))

    def remove(self, key):
        return self._from_pyr(self.pyr_data.remove(key))

    def discard(self, key):
        return self._from_pyr(self.pyr_data.discard(key))

    @staticmethod
    def _pyr_update(pyr_data, values):
        e = pyr_data.evolver()

        if isinstance(values, ty.Mapping):
            values = values.items()

        for k, v in values:
            e[k] = v

        return e.persistent()

    def update(self, values):
        p = self.pyr_data

        if isinstance(values, type(self)):
            p = p.update(values.pyr_data)
        else:
            p = self._pyr_update(p, values)

        return self._from_pyr(p)

    __getitem__ = _ForwardToPyr()
    keys = _ForwardToPyr()
    values = _ForwardToPyr()
    items = _ForwardToPyr()
    get = _ForwardToPyr()


class HashTrieSet(_EqAndBoolMixin, _SimpleIterableMixin, _Common, ty.Generic[K]):
    _pyr_type = _pyr.PSet

    @staticmethod
    def _pyr_make(*args):
        if not args:
            return _pyr.pset(pre_size=128)
        else:
            return _pyr.pset(*args)

    def insert(self, key):
        return self._from_pyr(self.pyr_data.add(key))

    def remove(self, key):
        return self._from_pyr(self.pyr_data.remove(key))

    def discard(self, key):
        return self._from_pyr(self.pyr_data.discard(key))

    def update(self, values):
        return self._from_pyr(self.pyr_data.update(values))


class List(_EqAndBoolMixin, _SimpleIterableMixin, _Common, ty.Generic[V]):
    _pyr_type = _pyr.PList

    @staticmethod
    def _pyr_make(*args):
        return _pyr.plist(*args)

    def push_front(self, value):
        return self._from_pyr(self.pyr_data.cons(value))

    __getitem__ = _ForwardToPyr()
    index = _ForwardToPyr()
