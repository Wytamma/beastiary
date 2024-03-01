
One of the main use cases of beastiary is accessing files on a remote server e.g. a high performance computer (HPC). Here we walk though the process of running beastiary on the University of Melbourne's HPC Spartan (although these steps apply to any remote server). This assumes beastiary is already installed on the remote server (e.g. `pip3 --user install beastiary`).

<div class="termy">

```console
$ ssh wytamma@spartan.hpc.unimelb.edu.au

Welcome to Spartan, the general purpose High Performance Computer system.
```
</div>

## Public sharing link

The easiest way to access beastiary on a remote server is to use the `--share` flag when starting beastiary. This will generate a public link that can be accessed from any machine.

<div class="termy">

```console
$ beastiary --share    

🐙🐁 <span style="color: #3498db;">STARTING BEASTIARY</span> 🐁🐙

Go to: <span style="color: green;">http://127.0.0.1:5000/login?token=8e02d06b-d30e-4a89-8476-fb22712a31b3</span>

If prompted enter token: 8e02d06b-d30e-4a89-8476-fb22712a31b3

Creating public shareable link...

Beastiary is now publicly accessible at: <span style="color: green;">https://grave-profits-stories-idaho.trycloudflare.com</span>
```
</div>

When running beastiary with the `--share` it will use [with-cloudflared](https://github.com/wytamma/with-cloudflared) to create a public link that will redirect public traffic to the local beastiary server. The public link will only work while beastiary is running. If you close the beastiary server you will have to generate a new public link.

!!! warning 
    
    We strongly recommend against disabling security when using the `--share` flag. We try to make Beastiary as secure as possible, but it is still a public link and there are bad actors.
    
    
If you want to access beastiary on a remote server without creating a public link then you will have to use an SSH tunnel.

## SSH tunnel

To connect to beastiary on the HPC we must first establish an SSH tunnel so that the port beastiary is running on can be connected to our local machine. We will accomplish this using the `-L` ssh flag. Connect to the HPC using your normal `ssh` command, but add `-L 5000:localhost:5000`. The `-L` flag tells ssh to forward requests to port 5000 on your local machine to port 5000 on the HPC. 

<div class="termy">

```console
$ ssh -L 5000:localhost:5000 wytamma@spartan.hpc.unimelb.edu.au

Welcome to Spartan, the general purpose High Performance Computer system.
```

</div>


!!! note
    
    If you wanted to run beastiary on a different port on the HPC (i.e. if 5000 is occupied) you could change the 5000 to your desired port e.g. 5001. 
    ```
    ssh -L 5001:localhost:5001 wytamma@spartan.hpc.unimelb.edu.au
    ```
    Then start beastiary using the desired port.
    ```
    beastiary --port 5001
    ```



## Start beastiary 

Now that you are logged into the HPC start beastiary using the `beastiary` command. Once beastiary has started you can go to [http://127.0.0.1:5000](http://127.0.0.1:5000) on your local machine to access remote log files. 

<div class="termy">

```console
$ beastiary

🐙🐁 <span style="color: #3498db;">STARTING BEASTIARY</span> 🐁🐙

Go to: <span style="color: green;">http://127.0.0.1:5000/login?token=8e02d06b-d30e-4a89-8476-fb22712a31b3</span>

If prompted enter token: 8e02d06b-d30e-4a89-8476-fb22712a31b3
```

</div>


!!! note

    Because beastiary is running on the remote server you will have to specify paths to log files as they are on the server. 


## Reconnecting 

If you are using ssh tunnelling to connect to Beastiary running on the remote server then you should be able to reopen the forwarded port e.g. [http://127.0.0.1:5000](http://127.0.0.1:5000) while Beastiary is running and the ssh connection remains open. Closing the ssh session or stopping Beastiary will prevent you from reconnect, but that’s expected. If you close the window simply go to [http://127.0.0.1:5000](http://127.0.0.1:5000) again and re-enter the login token.
