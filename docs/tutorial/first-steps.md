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

![](../images/login_screen_shot.png)

Add trace files to beastiary. There are two options for adding trace files to beastiary:

- load a local log file from your browser by dragging it into the dialog or choosing it from your machine. If your are using a Chrome-based browser you can choose local files that will auto-reload when they are updated on your machine. 
- browse for a log file that already exists on the Beastiary server and add it from the `Server files` section. Files added from the server will auto-reload when they are updated on the server.

![](../images/add_screen_shot.png)

Explore the traces of different parameters. 

![](../images/screen_shot.png)
