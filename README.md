# RESPONDPY

:snake: Welcome to RESPOND for Python! :snake: This repository acts as a set of python bindings for the Syndemics Lab's RESPOND model. As such, it is simply a set of wrappers and helper functions for ease of use in various lab projects. Our project can be installed from PyPI or build locally.

## RESPOND

RESPOND is a model developed by the Syndemics Lab at Boston Medical Center to study the various cost-effectiveness impacts of different treatment options for Substance Use Disorders (SUD). While originally built to study Opioid Use Disorder (OUD), RESPOND is a Markov model with the ability to scale to encompass various different treatment options and drug use behaviors. This repository adds bindings and helper functions to easily work with SQLite, both for our own analysts and for our web app to utilize. The original RESPOND model is written in C++ and can be found [on GitHub](https://github.com/SyndemicsLab/respond).

## Pybind11

This tool makes use of the popular tool [Pybind11](https://pybind11.readthedocs.io/en/stable/index.html). From here, we expose bindings for users to connect to via Python.

## Building

We make use of [Scikit-build-core](https://scikit-build-core.readthedocs.io/en/latest/index.html) along with CMake to build the library.

```bash
git clone git@github.com:SyndemicsLab/respondpy.git
uv sync
uv build
```

This results in a wheel and `tar.gz` being placed in a `dist/` directory. From here, we use `uv` to include it in other projects. Future work would be to allow for building device independent wheels and publishing to PyPI where we could install anywhere.

## ManyLinux Build

We are currently working on supporting a ManyLinux build of the project. This can be tested via the `cibuildwheel` tool.

```bash
uvx cibuildwheel
```

## Deployment Notes

Currently, we deploy using the following commands:

```bash
uv build
uvx cibuildwheel
```

After building into a folder called `wheelhouse` we remove the `*.whl` file in the `dist/` directory (only leaving the `.tar.gz`) and run the command:

```bash
uv publish --index testpypi dist/* wheelhouse/*
```

To testpypi we use the username `__token__` and our API key generated from our account.
