# pyrsistent-as-rpds-py

[![Run tests](https://github.com/e-c-d/pyrsistent-as-rpds-py/actions/workflows/test.yml/badge.svg)](https://github.com/e-c-d/pyrsistent-as-rpds-py/actions/workflows/test.yml)

## why

In 2023, the [jsonschema](https://pypi.org/project/jsonschema/) devs [replaced](https://github.com/python-jsonschema/jsonschema/commit/eb004479645a4e1f0d842e4434b909f476569dcc) the pure-Python [pyrsistent](https://pypi.org/project/pyrsistent/) library dependency with a binary dependency called [rpds-py](https://pypi.org/project/rpds-py/). This replacement was done for very reasonable speed reasons. However, [PyPy](https://pypy.org/) users may still prefer the pure-Python version both for speed reasons and to avoid the hassle of binary packages.

## what

This is a thin adapter library which implements a minimal subset of `rpds-py` using `pyrsistent`. The provided functionality is sufficient to run the `jsonschema` test cases successfully.

## how to use

Pip doesn't seem to have a way to override or substitute dependencies [without disabling dependency resolution entirely](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-no-deps). Therefore, I suggest running something like this:

```sh
pip install --no-index --no-build-isolation .  # install package "pyrsistent-as-rpds-py"
cd extra/fake_rpds
pip install --no-index --no-build-isolation .  # install fake and empty "rpds" package to make pip happy
```

Now you can install `jsonschema` or other packages that depend on `rpds-py` normally.
