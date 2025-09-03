# RESPONDPY

:snake: Welcome to RESPOND for Python! :snake: This repository acts as a set of python bindings for the Syndemics Lab's RESPOND model. As such, it is simply a set of wrappers for ease of use in various lab projects. Our wheel building procedure consists of simply running the commands:

```bash
git clone git@github.com:SyndemicsLab/respondpy.git
uv sync
uv build
```

This results in a wheel and `tar.gz` being placed in a `dist/` directory. From here, we use `uv` to include it in other projects. Future work would be to allow for building device independent wheels and publishing to PyPI where we could install anywhere.
