# pyrsistent-as-rpds-py

[![Run tests](https://github.com/e-c-d/pyrsistent-as-rpds-py/actions/workflows/test.yml/badge.svg)](https://github.com/e-c-d/pyrsistent-as-rpds-py/actions/workflows/test.yml)

## what is this?

This is a thin adapter library which implements a subset of `rpds-py` using `pyrsistent`. The provided functionality is sufficient to run the `jsonschema` test cases successfully.

## why is this?

In 2023, the [jsonschema](https://pypi.org/project/jsonschema/) devs [replaced](https://github.com/python-jsonschema/jsonschema/commit/eb004479645a4e1f0d842e4434b909f476569dcc) the pure-Python [pyrsistent](https://pypi.org/project/pyrsistent/) library dependency with a binary dependency called [rpds-py](https://pypi.org/project/rpds-py/). This replacement was done for very reasonable speed reasons. However, [PyPy](https://pypy.org/) users may still prefer the pure-Python version both for speed reasons and also to avoid the hassle of building binary packages.

(The `rpds-py` API also just feels better than the `pyrsistent` one, in my humble opinion. If I wanted to build something with persistent data structures, I would probably either use this module or `rpds-py`.)

## how to use

Pip doesn't seem to have a way to override or substitute dependencies (at least [without disabling dependency resolution entirely](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-no-deps)). Therefore, I suggest running something like this:

```sh
pip install --no-index --no-build-isolation .  # install package "pyrsistent-as-rpds-py"
cd extra/fake_rpds
pip install --no-index --no-build-isolation .  # install fake and empty "rpds" package to make pip happy
```

Now you can install `jsonschema` or other packages that depend on `rpds-py` normally.
