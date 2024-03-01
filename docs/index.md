![beastiary logo](images/logo.png)


[![PyPi](https://img.shields.io/pypi/v/beastiary.svg)](https://pypi.org/project/beastiary/)
[![tests](https://github.com/Wytamma/beastiary/actions/workflows/test.yml/badge.svg)](https://github.com/Wytamma/beastiary/actions/workflows/test.yml)
[![cov](https://codecov.io/gh/Wytamma/beastiary/branch/master/graph/badge.svg)](https://codecov.io/gh/Wytamma/beastiary)
[![docs](https://github.com/Wytamma/beastiary/actions/workflows/docs.yml/badge.svg)](https://beastiary.wytamma.com/)

Beastiary is designed for visualising and analysing MCMC trace files generated from Bayesian phylogenetic analyses. Beastiary works in real-time and on remote servers (e.g. a HPC). Its goal is to be a beautiful and simple, yet powerful tool for Bayesian phylogenetic inference.

## Installation

<div class="termy">

```console
$ pip install beastiary

---> 100%
```

</div>

## Example
To start beastiary use the `beastiary` command. This will start the beastiary server. 

<div class="termy">

```console
$ beastiary

🐙🐁 <span style="color: #3498db;">STARTING BEASTIARY</span> 🐁🐙

Go to: <span style="color: green;">http://127.0.0.1:5000/login?token=8e02d06b-d30e-4a89-8476-fb22712a31b3</span>
If prompted enter token: 8e02d06b-d30e-4a89-8476-fb22712a31b3
```

</div>

The server will start on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) by default. Every time the server starts it will generate a unique token that can be used to log into the webapp. 

Go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) and log in with the token. 

![](images/login_screen_shot.png)

Add a log file using the `ADD` button. 

![](images/add_screen_shot.png)

Explore the traces of different parameters. 

![](images/screen_shot.png)
