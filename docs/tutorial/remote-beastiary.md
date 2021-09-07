
One of the main use cases of beastiary is accessing files on a remote server e.g. a high performance computer (HPC). Here we walk though the process of running beastiary on the University of Melbourne's HPC Spartan (although these steps apply to any remote server). This assumes beastiary is already installed on the remote server (e.g. `pip3 --user install beastiary`). 

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


## Start beastiary 

Now that you are logged into the HPC start beastiary using the `beastiary` command. Once beastiary has started you can go to http://127.0.0.1:5000 on your local machine to access remote log files. 

<div class="termy">

```console
$ beastiary

🐙🐁 <span style="color: blue;">STARTING BEASTIARY</span> 🐁🐙

Go to: <span style="color: green;">http://127.0.0.1:5000/login?token=8e02d06b-d30e-4a89-8476-fb22712a31b3</span>
If prompted enter token: 8e02d06b-d30e-4a89-8476-fb22712a31b3
```

</div>


!!! note

    Because beastiary is running on the remote server you will have to specify paths to log files as they are on the server. 

