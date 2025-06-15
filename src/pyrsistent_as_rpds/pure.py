import abc
import typing as ty
from collections import abc as cabc

try:
    import pyrsistent
except ImportError:
    raise AssertionError(
        "You must install this package as either `pyrsistent-as-rpds-py[pyrsistent]` or "
        "`pyrsistent-as-rpds-py[rpds-py]`.\n\nThis is necessary because pip does not support "
        "alternative dependencies (e.g., require either X or Y to be installed)."
    )


__all__ = ["HashTrieMap", "HashTrieSet", "Queue", "List", "is_pure_pyrsistent_as_rpds"]

is_pure_pyrsistent_as_rpds = True


class _ReprMixin(abc.ABC):
    @abc.abstractmethod
    def _repr_iter(self):
        ...

    def __repr__(self):
        return "".join(self._repr_iter())


class _Common(_ReprMixin, abc.ABC):
    _abstract_type = ...
    _pyr_type = ...

    @classmethod
    def _from_pyr(cls, pyr_data):
        return cls(pyr_data)

    @classmethod
    @abc.abstractmethod
    def _pyr_make(cls, *args):
        ...

    def __init__(self, *args, **kwargs):
        # fast path
        if len(args) == 1 and not kwargs and isinstance((a := args[0]), self._pyr_type):
            self.pyr_data = a
        else:
            if args and kwargs:
                raise AssertionError

            if args:
                _types_map = cabc.Mapping
                _types_iter = (cabc.Iterable, cabc.Iterator)
                a = []
                for x in args:
                    if isinstance(x, _types_map):
                        a += x.items()
                    elif isinstance(x, _types_iter):
                        a += x
                    else:
                        a.append(x)
            else:
                a = kwargs

            if isinstance(a, self._pyr_type):
                self.pyr_data = a
            elif a is None:
                self.pyr_data = self._pyr_make()
            else:
                self.pyr_data = self._pyr_make(a)

        self.is_empty = not len(self.pyr_data)

    @classmethod
    def convert(cls, value):
        if isinstance(value, cls):
            return value
        else:
            return cls(value)


class _FwAttr:
    def __set_name__(self, owner, name):
        self.pyr_attribute_name = name

    def __get__(self, obj, objtype=None):
        return getattr(obj.pyr_data, self.pyr_attribute_name)


class _ForwardMethodHandler:
    def __init__(self, name, obj, objtype):
        self.name = name
        self.obj = obj
        self.objtype = objtype

    def outer(self, result):
        return result

    def run(self, *args, **kwargs):
        return self.outer(getattr(self.obj.pyr_data, self.name)(*args, **kwargs))


class _ForwardMethodHandlerSetLikeBinOp(_ForwardMethodHandler):
    def run(self, x):
        ot = self.objtype
        if not isinstance(x, ot):
            x = ot(x)
        return super().run(x)


class _ForwardMethodHandlerSetLikeBinOpWithPyrResult(_ForwardMethodHandlerSetLikeBinOp):
    def outer(self, result):
        return self.objtype(result)


class _FwMeth:
    def __init__(self, handler: type[_ForwardMethodHandler]):
        self.handler = handler

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        return self.handler(self.name, obj, objtype).run


K = ty.TypeVar("K")
V = ty.TypeVar("V")


class _PyrCollection:
    __iter__ = _FwAttr()
    __len__ = _FwAttr()
    __contains__ = _FwAttr()


class _PyrEqBoolHash:
    __hash__ = _FwAttr()

    def __ne__(self, other):
        return not (self == other)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.pyr_data == other.pyr_data

        if isinstance(other, self._abstract_type):
            return self.pyr_data == other

        return False

    def __bool__(self):
        return not self.is_empty


class _ReprMixinSetLike(_ReprMixin):
    _repr_start = "({"
    _repr_end = "})"

    def _repr_iter(self):
        yield type(self).__name__
        yield self._repr_start
        comma = ""
        for v in self:
            yield comma
            yield repr(v)
            comma = ", "
        yield self._repr_end


class _ReprMixinListLike(_ReprMixinSetLike):
    _repr_start = "(["
    _repr_end = "])"


class HashTrieMap(_PyrEqBoolHash, _PyrCollection, _Common, ty.Generic[K, V], cabc.Mapping, ty.Hashable):
    _abstract_type = cabc.Mapping
    _pyr_type = pyrsistent.PMap

    @classmethod
    def _pyr_make(cls, *args):
        p = pyrsistent.m()
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

    @classmethod
    def fromkeys(cls, iterable, value=None):
        return cls((k, value) for k in iterable)

    def update(self, *mappings):
        p = self.pyr_data

        for m in mappings:
            if isinstance(m, type(self)):
                p = p.update(m.pyr_data)
            else:
                p = self._pyr_update(p, m)

        return self._from_pyr(p)

    __getitem__ = _FwAttr()
    values = _FwAttr()
    items = _FwAttr()
    get = _FwAttr()

    def keys(self):
        return keys_view(hash_trie_map=self)

    def values(self):
        return values_view(hash_trie_map=self)

    def items(self):
        return items_view(hash_trie_map=self)

    def _repr_iter(self):
        yield type(self).__name__
        yield "({"
        comma = ""
        for k, v in self.items():
            yield comma
            yield repr(k)
            yield ": "
            yield repr(v)
            comma = ", "
        yield "})"


class _keys_and_items_common:
    def __init__(self, *, hash_trie_map=None):
        self.original_map = hash_trie_map

    def __eq__(self, other):
        if self is other:
            return True

        if isinstance(other, cabc.Collection):
            if len(self) != len(other):
                return False
            for x in other:
                if x not in self:
                    return False
            return True
        else:
            return False

    @staticmethod
    def _setify(x):
        return set(x)

    def __or__(self, other):
        result = self._setify(other)
        result.update(iter(self))
        return result

    def __sub__(self, other):
        result = self._setify(self)
        result -= other
        return result

    def __xor__(self, other):
        return self._setify(other) ^ set(self)

    def __len__(self):
        return len(self.original_map)

    def union(self, other):
        return self | other

    def intersection(self, other):
        return self & other

    def difference(self, other):
        return self - other

    def symmetric_difference(self, other):
        return self ^ other

    def __bool__(self):
        return bool(len(self))


class keys_view(_keys_and_items_common, _ReprMixinSetLike, cabc.KeysView, ty.Hashable):
    def __and__(self, other):
        f = self.original_map.pyr_data.__contains__
        return {x for x in other if f(x)}

    def __iter__(self):
        return iter(self.original_map.pyr_data.keys())

    def __hash__(self):
        return hash(self.original_map.pyr_data.keys())

    def __contains__(self, x):
        return x in self.original_map


class items_view(_keys_and_items_common, _ReprMixinListLike, cabc.ItemsView, ty.Hashable):
    def __and__(self, other):
        return set(self) & {x for x in other if isinstance(x, tuple)}

    def __iter__(self):
        return iter(self.original_map.pyr_data.items())

    def __hash__(self):
        return hash(self.original_map.pyr_data.items())

    def __contains__(self, x):
        try:
            k, v = x
        except (TypeError, IndexError, ValueError):
            return False
        return k in self.original_map and self.original_map[k] == v


class values_view(_ReprMixinListLike, cabc.ValuesView, ty.Hashable):
    def __init__(self, *, hash_trie_map=None):
        self.original_map = hash_trie_map

    def __len__(self):
        return len(self.original_map)

    def __iter__(self):
        return iter(self.original_map.pyr_data.values())

    def __contains__(self, x):
        return x in self.original_map.pyr_data.values()

    def __hash__(self):
        return hash(self.original_map.pyr_data.values())


class HashTrieSet(_PyrEqBoolHash, _PyrCollection, _ReprMixinSetLike, _Common, ty.Generic[K], cabc.Set, ty.Hashable):
    _abstract_type = cabc.Set
    _pyr_type = pyrsistent.PSet

    @staticmethod
    def _pyr_make(*args):
        if not args:
            return pyrsistent.pset(pre_size=128)
        else:
            return pyrsistent.pset(*args)

    def insert(self, key):
        return self._from_pyr(self.pyr_data.add(key))

    def remove(self, key):
        return self._from_pyr(self.pyr_data.remove(key))

    def discard(self, key):
        return self._from_pyr(self.pyr_data.discard(key))

    def update(self, values):
        return self._from_pyr(self.pyr_data.update(values))

    __lt__ = _FwMeth(_ForwardMethodHandlerSetLikeBinOp)
    __gt__ = _FwMeth(_ForwardMethodHandlerSetLikeBinOp)
    __le__ = _FwMeth(_ForwardMethodHandlerSetLikeBinOp)
    __ge__ = _FwMeth(_ForwardMethodHandlerSetLikeBinOp)
    __or__ = _FwMeth(_ForwardMethodHandlerSetLikeBinOpWithPyrResult)
    __and__ = _FwMeth(_ForwardMethodHandlerSetLikeBinOpWithPyrResult)
    __xor__ = _FwMeth(_ForwardMethodHandlerSetLikeBinOpWithPyrResult)
    __sub__ = _FwMeth(_ForwardMethodHandlerSetLikeBinOpWithPyrResult)
    union = _FwMeth(_ForwardMethodHandlerSetLikeBinOpWithPyrResult)
    intersection = _FwMeth(_ForwardMethodHandlerSetLikeBinOpWithPyrResult)
    difference = _FwMeth(_ForwardMethodHandlerSetLikeBinOpWithPyrResult)
    symmetric_difference = _FwMeth(_ForwardMethodHandlerSetLikeBinOpWithPyrResult)


class List(_PyrEqBoolHash, _PyrCollection, _ReprMixinListLike, _Common, ty.Generic[V], cabc.Sequence, ty.Hashable):
    _abstract_type = cabc.Sequence
    _pyr_type = pyrsistent.PList

    @staticmethod
    def _pyr_make(*args):
        return pyrsistent.plist(*args)

    def drop_first(self):
        if self.is_empty:
            raise IndexError("empty list")
        return self.rest

    def push_front(self, value):
        return self._from_pyr(self.pyr_data.cons(value))

    def __reversed__(self):
        return self._from_pyr(self.pyr_data.reverse())

    @property
    def first(self):
        try:
            return self.pyr_data.first
        except AttributeError:
            raise IndexError("empty list")

    @property
    def rest(self):
        return self._from_pyr(self.pyr_data.rest)

    __getitem__ = _FwAttr()
    index = _FwAttr()


class Queue(_PyrEqBoolHash, _PyrCollection, _Common, ty.Generic[V], cabc.Sequence, ty.Hashable):
    _pyr_type = pyrsistent.PDeque
    _abstract_type = cabc.Sequence

    @staticmethod
    def _pyr_make(*args):
        return pyrsistent.pdeque(*args)

    def enqueue(self, value):
        return self._from_pyr(self.pyr_data.append(value))

    def dequeue(self):
        if self.is_empty:
            raise IndexError("empty queue")
        return self._from_pyr(self.pyr_data.popleft())

    @property
    def peek(self):
        if self.is_empty:
            raise IndexError("empty queue")
        return self.pyr_data.left

    __getitem__ = _FwAttr()
    index = _FwAttr()

    def _repr_iter(self):
        yield type(self).__name__
        yield "(["
        comma = ""
        for v in self:
            yield comma
            yield repr(v)
            comma = ", "
        yield "])"
