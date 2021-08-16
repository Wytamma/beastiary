![beastiary logo](docs/images/logo.png)


[![PyPi](https://img.shields.io/pypi/v/beastiary.svg)](https://pypi.org/project/beastiary/)
[![tests](https://github.com/Wytamma/beastiary/actions/workflows/test.yml/badge.svg)](https://github.com/Wytamma/beastiary/actions/workflows/test.yml)
[![cov](https://codecov.io/gh/Wytamma/beastiary/branch/master/graph/badge.svg)](https://codecov.io/gh/Wytamma/beastiary)
[![docs](https://github.com/Wytamma/beastiary/actions/workflows/docs.yml/badge.svg)](https://beastiary.wytamma.com/)

This is a real time version of tracer that can be run on remote servers (e.g. a HPC). Its goal is to be a beautiful and simple, yet power tool for Bayesian phylogenetic inference.

## Installation
```bash
pip install beastiary
```

## Use
To start beastiary use the `beastiary` command. This will start the beastiary webapp on http://127.0.0.1:5000/ by default. 
```bash
beastiary
```

Log files can be added at start up by passing them as command line arguments.
```bash
beastiary path/to/BEAST.log
```

By default beastiary will generate a unique uuid used to log in to the webapp. This can be disabled using the `--no-security` option. 
```bash
beastiary --no-security
```
