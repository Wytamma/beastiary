By default beastiary will generate a unique token used to log in to the webapp. This can be disabled using the `--no-security` option. At the login page press login without entering the token.

<div class="termy">

```console
$ beastiary --no-security

🐙🐁 <span style="color: blue;">STARTING BEASTIARY</span> 🐁🐙

Go to: <span style="color: green;">http://127.0.0.1:5000/login?token=8e02d06b-d30e-4a89-8476-fb22712a31b3</span>

<span style="color: yellow;">WARNING</span>: Security disabled!
```

</div>

!!! note
    
    If using beastiary on a shared computer (e.g. a HPC) disabling security will enable other users to log into your beastiary session and thus access files in your account.


## User defined token

Use the `--token` option to define your own token e.g. so it's the same every time you start beastiary. 

<div class="termy">

```console
$ beastiary --token weakPassword

🐙🐁 <span style="color: blue;">STARTING BEASTIARY</span> 🐁🐙

Go to: <span style="color: green;">http://127.0.0.1:5000/login?token=weakPassword</span>

If prompted enter token: weakPassword

```

</div>