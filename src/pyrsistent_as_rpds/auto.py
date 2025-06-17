_rpds = None
try:
    import rpds as _rpds

    if getattr(_rpds, "is_pure_pyrsistent_as_rpds", False):
        raise ImportError("fake_rpds")
except ImportError:
    from .pure import *  # noqa

    auto_backend = "pyrsistent"
else:
    from rpds import *  # noqa

    auto_backend = "rpds-py"
    is_pure_pyrsistent_as_rpds = False
del _rpds
