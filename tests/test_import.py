def test_import_alias():
    from pyrsistent_as_rpds.auto import Queue as Q1

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
    elif Q2 is not None:
        assert Q1 is Q2, "pyrsistent should be used as the fallback"
