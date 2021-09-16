![beastiary logo](https://beastiary.wytamma.com/images/logo.png)


[![PyPi](https://img.shields.io/pypi/v/beastiary.svg)](https://pypi.org/project/beastiary/)
[![tests](https://github.com/Wytamma/beastiary/actions/workflows/test.yml/badge.svg)](https://github.com/Wytamma/beastiary/actions/workflows/test.yml)
[![cov](https://codecov.io/gh/Wytamma/beastiary/branch/master/graph/badge.svg)](https://codecov.io/gh/Wytamma/beastiary)
[![docs](https://github.com/Wytamma/beastiary/actions/workflows/docs.yml/badge.svg)](https://beastiary.wytamma.com/)

This is a real time version of tracer that can be run on remote servers (e.g. a HPC). Its goal is to be a beautiful and simple, yet power tool for Bayesian phylogenetic inference.

---

**Documentation**: <a href="https://beastiary.wytamma.com" target="_blank">https://beastiary.wytamma.com</a>

**Source Code**: <a href="https://github.com/Wytamma/beastiaryi" target="_blank">https://github.com/Wytamma/beastiary</a>

---

## Installation
```bash
pip install beastiary
```

## Use
To start beastiary use the `beastiary` command. This will start the beastiary server. 

```bash
beastiary
```

The server will start on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) by default. Every time the server starts it will generate a unique id that can be used to log into the webapp. 

![](https://beastiary.wytamma.com/images/screen_shot_dark.png)

For more information read the [docs](https://beastiary.wytamma.com/).
