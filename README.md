# pyrsistent-as-rpds-py

[![Run tests](https://github.com/e-c-d/pyrsistent-as-rpds-py/actions/workflows/test.yml/badge.svg)](https://github.com/e-c-d/pyrsistent-as-rpds-py/actions/workflows/test.yml)

## what is this?

This is a thin adapter library which implements a subset of [rpds-py](https://pypi.org/project/rpds-py/) using [pyrsistent](https://pypi.org/project/pyrsistent/). The provided functionality is sufficient to run the [jsonschema](https://pypi.org/project/jsonschema/) test cases successfully.

## why is this?

In 2023, the [jsonschema](https://pypi.org/project/jsonschema/) devs [replaced](https://github.com/python-jsonschema/jsonschema/commit/eb004479645a4e1f0d842e4434b909f476569dcc) the pure-Python [pyrsistent](https://pypi.org/project/pyrsistent/) library dependency with a binary dependency called [rpds-py](https://pypi.org/project/rpds-py/). This replacement was done in order to improve performance (as CPython is quite slow). However, [PyPy](https://pypy.org/) users may still prefer the pure-Python version both for speed reasons and also to avoid the hassle of building binary packages.

(The `rpds-py` API also just feels better than the `pyrsistent` one, in my humble opinion. If I wanted to build something with persistent data structures, I would probably either use this module or `rpds-py`.)

## how to use

### use case 1: I can't use rpds-py for whatever reason, some other package requires it, and I need a drop-in replacement

Pip doesn't seem to have a way to override or substitute dependencies (at least [without disabling dependency resolution entirely](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-no-deps)). Therefore, I suggest running something like this:

```sh
# install package "pyrsistent-as-rpds-py"
pip install --no-index --no-build-isolation .

# install fake "rpds" package to make pip happy
cd extra/fake_rpds
pip install --no-index --no-build-isolation .
```

Now you can install `jsonschema` or other packages that depend on `rpds-py` normally.

### use case 2: I am developing a new project and I need a persistent data structures library

Just add `pyrsistent-as-rpds-py` to your requirements.txt / pyproject.toml dependencies like you would any other dependency. Then you can write:

```python
from pyrsistent_as_rpds.auto import List

lst = List(1, 2, 3)
print(lst.rest)
```

This will try to import the original `rpds-py` module first. If it fails (because `rpds-py` is not installed), then it use the pure Python version instead.

This library needs at least one of `rpds-py` or `pyrsistent` to be installed. If you are an end-user application packager / system integrator, you **must** choose to install either `pyrsistent-as-rpds-py[pyrsistent]` or `pyrsistent-as-rpds-py[rpds-py]`. This is unfortunately necessary because pip [does not support](https://discuss.python.org/t/require-any-of-several-alternative-package-dependencies/26293/8) alternative dependencies (e.g., require either X or Y to be installed).
