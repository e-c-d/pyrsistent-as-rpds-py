try:
    from rpds import *  # noqa

    auto_backend = "rpds-py"
except ImportError:
    from .pure import *  # noqa

    auto_backend = "pyrsistent"
