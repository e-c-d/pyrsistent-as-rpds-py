import os


def test_import_alias():
    from pyrsistent_as_rpds.auto import Queue as Q1
    from pyrsistent_as_rpds.auto import is_pure_pyrsistent_as_rpds as is_pure
    from pyrsistent_as_rpds.auto import auto_backend

    assert type(is_pure) is bool
    assert (auto_backend == "pyrsistent") == is_pure

    try:
        import pyrsistent
    except ImportError:
        Q2 = None
    else:
        from pyrsistent_as_rpds.pure import Queue as Q2

    try:
        from rpds import Queue as Q3
    except ImportError:
        Q3 = None

    if Q3 is not None:
        assert Q1 is Q3, "rpds-py should always be used if available"
        if v := os.environ.get("PYR_RPDS_TESTS_HAS_FAKE", None):
            assert is_pure == bool(int(v))
    elif Q2 is not None:
        assert Q1 is Q2, "pyrsistent should be used as the fallback"
        assert is_pure
