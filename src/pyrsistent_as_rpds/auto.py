try:
    import rpds

    if getattr(rpds, "is_pure_pyrsistent_as_rpds", None):
        rpds = None
except ImportError:
    rpds = None

if rpds is None:
    try:
        import pyrsistent  # noqa

        del pyrsistent
    except ImportError:
        raise AssertionError(
            "You must install this package as either `pyrsistent-as-rpds-py[pyrsistent]` or "
            "`pyrsistent-as-rpds-py[rpds-py]`.\n\nThis is necessary because pip does not support "
            "alternative dependencies (e.g., require either X or Y to be installed)."
        )
    from .pure import *  # noqa
    auto_backend = "pyrsistent"
else:
    from rpds import *  # noqa
    auto_backend = "rpds-py"

del rpds
