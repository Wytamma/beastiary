## Single

A path to a log file can be passed to `beastiary` via the command line. The ✅ indicates that the log was successfully added and will be available on start up. 

<div class="termy">

```console
$ beastiary data/hcv_coal.log

🐙🐁 <span style="color: blue;">STARTING BEASTIARY</span> 🐁🐙

Adding log files:
✅ - data/hcv_coal.log

Go to: <span style="color: green;">http://127.0.0.1:5000/login?token=8e02d06b-d30e-4a89-8476-fb22712a31b3</span>
If prompted enter token: 8e02d06b-d30e-4a89-8476-fb22712a31b3
```

</div>

## Multiple

Multiple paths can be passed to `beastiary` via the command line. The ✅ indicates that each log was successfully added and will be available on start up. 


<div class="termy">

```console
$ beastiary data/hcv_coal.log data/prior.ebola.log 

🐙🐁 <span style="color: blue;">STARTING BEASTIARY</span> 🐁🐙

Adding log files:
✅ - data/hcv_coal.log
✅ - data/prior.ebola.log

Go to: <span style="color: green;">http://127.0.0.1:5000/login?token=8e02d06b-d30e-4a89-8476-fb22712a31b3</span>
If prompted enter token: 8e02d06b-d30e-4a89-8476-fb22712a31b3
```

</div>

## Pattern 

Bash style pattern matching can be used as short hand to specify multiple files. All matches will be available at start up.

<div class="termy">

```console
$ beastiary data/*.log 

🐙🐁 <span style="color: blue;">STARTING BEASTIARY</span> 🐁🐙

Adding log files:
✅ - data/hcv_coal.log
✅ - data/prior.ebola.log

Go to: <span style="color: green;">http://127.0.0.1:5000/login?token=8e02d06b-d30e-4a89-8476-fb22712a31b3</span>
If prompted enter token: 8e02d06b-d30e-4a89-8476-fb22712a31b3
```

</div>