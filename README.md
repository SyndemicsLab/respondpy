# RESPONDPY

## :warning: NOTICE :warning:

This repository is under active development and not currently in a state for public use.

:snake: Welcome to RESPOND for Python! :snake: This repository acts as a set of python bindings for the Syndemics Lab's RESPOND model. As such, it is simply a set of wrappers for ease of use in various lab projects. Our wheel building procedure consists of simply running the commands:

```bash
git clone git@github.com:SyndemicsLab/respondpy.git
uv sync
uv build
```

This results in a wheel and `tar.gz` being placed in a `dist/` directory. From here, we use `uv` to include it in other projects. Future work would be to allow for building device independent wheels and publishing to PyPI where we could install anywhere.

## RESPOND

We are writing bindings for the RESPOND C++ model. Developed as a model to measure cost effectiveness of various Opioid Use Disorder interventions, we now desire to be able to run the model in different languages and tools.

## Pybind11

This tool makes use of the popular tool [Pybind11](https://pybind11.readthedocs.io/en/stable/index.html). From here, we expose bindings for users to connect to via Python.

## Building

We make use of [Scikit-build-core](https://scikit-build-core.readthedocs.io/en/latest/index.html) along with CMake to build the library.

## ManyLinux Build

We are currently working on supporting a ManyLinux build of the project. This can be tested via the `cibuildwheel` tool.

```bash
uvx cibuildwheel
```
