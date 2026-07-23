# RESPONDPY

[![Coverage](https://codecov.io/gh/SyndemicsLab/respondpy/branch/main/graph/badge.svg)](https://app.codecov.io/gh/SyndemicsLab/respondpy)
[![Smoke Testing, Unit Testing, and Code Coverage](https://github.com/SyndemicsLab/respondpy/actions/workflows/testing.yml/badge.svg)](https://github.com/SyndemicsLab/respondpy/actions/workflows/testing.yml)
[![Nox Pylint](https://github.com/SyndemicsLab/respondpy/actions/workflows/nox-pylint.yml/badge.svg)](https://github.com/SyndemicsLab/respondpy/actions/workflows/nox-pylint.yml)
[![Build and Deploy to PyPI](https://github.com/SyndemicsLab/respondpy/actions/workflows/deploy.yml/badge.svg)](https://github.com/SyndemicsLab/respondpy/actions/workflows/deploy.yml)

:snake: Welcome to RESPOND for Python! :snake: This repository acts as a set of python bindings for the Syndemics Lab's RESPOND model. As such, it is simply a set of wrappers and helper functions for ease of use in various lab projects. Our project can be installed from PyPI or built locally.

## RESPOND

RESPOND is a simulation model developed by the Syndemics Lab at Boston Medical Center to study the various cost-effectiveness impacts of different treatment options for substance use disorders (SUD). While originally built to study opioid use disorder (OUD), RESPOND is a Markov model with the ability to scale to encompass various drug use behaviors and treatment approaches or venues. This repository adds bindings and helper functions to easily work with SQLite. The original RESPOND model is written in R and C++ and can be found [on GitHub](https://github.com/SyndemicsLab/respondv1).

## Pybind11

This tool makes use of the popular tool [Pybind11](https://pybind11.readthedocs.io/en/stable/index.html). From here, we expose bindings for users to connect to via Python.

## Building and Installing

The bindings are available on PyPI! They can be installed via `pip install respondpy`.

If you want to build the project locally, we make use of [scikit-build-core](https://scikit-build-core.readthedocs.io/en/latest/index.html) along with CMake to build the library. To build locally, you can clone the repository here.

```bash
git clone git@github.com:SyndemicsLab/respondpy.git
uv sync
uv build
```

This results in a wheel and `tar.gz` being placed in a `dist/` directory. From here, we use `uv` to include it in other projects. Future work would be to allow for building device independent wheels and publishing to PyPI where we could install anywhere.

## Supported OSes

We are currently working on supporting as many OSes as possible. As these are bindings for a C++ project, we are limited in our capacity. For the moment, we are generating many linux builds for python versions >= 3.10. We do not have a Windows or Mac build at the present.

## Binding Parity Checklist

Use this checklist when updating bindings, stubs, or API docs.

- Run smoke tests: `uv run pytest -m smoke`
- [ ] Runtime vs stubs parity:
	- [ ] Confirm pybind runtime signatures and return shapes match `.pyi` annotations.
	- [ ] Confirm enum members and bound method names match stub names exactly.
	- [ ] Confirm overload behavior matches typed expectations.
- [ ] Runtime vs docs parity:
	- [ ] Confirm binding docstrings describe actual runtime return types and side effects.
	- [ ] Confirm parameter defaults in docs match bound defaults.
- [ ] Expected-failure messaging parity:
	- [ ] Confirm incorrect arguments raise errors with stable, informative message patterns.
	- [ ] Prefer regex pattern assertions in tests over exact full-message equality.
- [ ] Smoke coverage scope:
	- [ ] Runtime binding smoke lives in `tests/test_smoke_bindings_runtime.py`.
	- [ ] Stub smoke via `mypy` in pytest lives in `tests/test_smoke_stubs_mypy.py`.
