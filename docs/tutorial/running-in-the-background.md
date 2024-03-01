If you are running `beastiary` for a long time you may want to run it in the background. There are several options for running a task in the background.

## beastiary &

Putting a `&` at the end of the `beastiary` will run beackground, but output will still be log to the console. If you close the terminal then the job will also stop. The processes can also be stopped with the `ps` and `kill` commands. Running ps will show all the running commands and their PIDs. Find the PID of the `beastiary` command and used the command `kill <PID>` (where `<PID>` is the beastiary PID) to stop beastiary. Or you can use the fg % 1 command (where 1 is the job id which can be found with `$ jobs`) to bring beastiary back to the foreground and kill it with `ctrl+c`

<div class="termy">

```console
$ beastiary &
[1] 46918

🐙🐁 <span style="color: #3498db;">STARTING BEASTIARY</span> 🐁🐙

Adding log files:
✅ - data/hcv_coal.log

Go to: <span style="color: green;">http://127.0.0.1:5000/login?token=8e02d06b-d30e-4a89-8476-fb22712a31b3</span>
If prompted enter token: 8e02d06b-d30e-4a89-8476-fb22712a31b3

$ jobs 
[1]  + running    beastiary

$ fg % 1 
[1]  + 46918 running    beastiary
^Cfg: job not found: 1
```

</div>


## nohup beastiary &

The `nohup` and `&` at the end of the beast command tells bash to run the command in the background and to not stop if you close the terminal. The processes must be stopped with the `ps` and `kill` commands.

## beastiary; ctrl+z; jobs; fg %1

Jobs can also be pushed to the background using the job control command `ctrl+z`. Start beastiary then press `ctrl+z`. Enter `fg %1` to bring beastiary back to the foreground (where 1 is the job id which can be found with `$ jobs`). 